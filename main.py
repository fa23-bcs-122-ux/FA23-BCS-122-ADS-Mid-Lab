import pymongo
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
import uvicorn
from typing import List, Optional
from datetime import datetime


# --- Pydantic Models (Data Validation) ---

# --- Pydantic v1 Class for ObjectId ---
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# --- Models using Pydantic v1 'class Config' ---

# Model for displaying a single product in an order
class OrderProduct(BaseModel):
    product_id: PyObjectId = Field(..., alias="_id")
    name: str
    price_at_purchase: float
    quantity: int

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


# Model for displaying a single order's full details
class Order(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    products: List[OrderProduct]
    total_cost: float
    status: str
    shipping_address: dict
    timestamp: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


# Model for just the order summary (for the user's list)
class OrderSummary(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    total_cost: float
    status: str
    timestamp: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


# Model for displaying a single review
class Review(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    product_id: PyObjectId
    user_id: PyObjectId
    rating: int
    review_text: str
    timestamp: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class ProductSearchResult(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    name: str
    price: float
    category: str
    brand: str
    review_summary: dict

    final_score: float = Field(..., alias="weighted_score")
    similarity_score: float
    popularity_score: float
    price_score: float

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


# --- Application Setup ---
app = FastAPI(
    title="E-commerce API",
    description="Backend for the E-commerce Marketplace (Q2)",
    version="1.0.0"
)

# --- Database Connection ---
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ecom_marketplace"]
    print("Connected to MongoDB successfully!")
except pymongo.errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    db = None


# --- API Endpoints ---

@app.get("/")
def read_root():
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    return {"message": "Welcome to the E-commerce API!", "db_status": "connected"}


# --- API 1: Get Order Details ---
@app.get("/orders/{id}", response_model=Order)
def get_order_by_id(id: str):
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    try:
        order_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Order ID format")
    order = db.orders.find_one({"_id": order_id})
    if order:
        return order
    raise HTTPException(status_code=404, detail=f"Order with id {id} not found")


# --- API 2: Get User's Orders ---
@app.get("/users/{id}/orders", response_model=List[OrderSummary])
def get_user_orders(id: str):
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    try:
        user_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid User ID format")
    user = db.users.find_one({"_id": user_id}, {"purchase_history": 1})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    order_ids = user.get("purchase_history", [])
    if not order_ids:
        return []
    orders_cursor = db.orders.find(
        {"_id": {"$in": order_ids}}
    ).sort("timestamp", pymongo.DESCENDING)
    return list(orders_cursor)


# --- API 3: Get Product Reviews ---
@app.get("/products/{id}/reviews", response_model=List[Review])
def get_product_reviews(id: str):
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")
    try:
        product_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Product ID format")
    product = db.products.find_one({"_id": product_id}, {"_id": 1})
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    reviews_cursor = db.reviews.find(
        {"product_id": product_id}
    ).sort("timestamp", pymongo.DESCENDING)
    return list(reviews_cursor)


# --- API 4: Search ---
@app.get("/products/search", response_model=List[ProductSearchResult])
def search_products(
        query: str,
        budget: Optional[float] = None,
        limit: int = 10
):
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection not available")

    pipeline = []

    # --- Stage 1: Text Search (Keyword Search) ---
    pipeline.append({
        "$match": {
            "$text": {"$search": query}
        }
    })

    # --- Stage 2: Calculate Initial Scores (Hybrid Ranking) ---
    pipeline.append({
        "$addFields": {
            "similarity_score": {"$meta": "textScore"},
            "popularity_score": {"$log10": {"$add": ["$purchase_count", 1]}},
            "price_score": {
                "$cond": {
                    "if": {"$and": [budget, {"$gt": [budget, 0]}]},
                    "then": {
                        # --- THIS IS THE NEW, FIXED CODE ---
            "$max": [
                0,
                {
                    "$subtract": [
                        1,
                        {
                            "$abs": {
                                "$divide": [
                                    { "$subtract": ["$price", budget] },
                                    budget
                                ]
                            }
                        }
                    ]
                }
            ]
# --- END OF FIXED CODE ---
                    },
                    "else": 0
                }
            }
        }
    })

    # --- Stage 3: Normalize Scores ---
    pipeline.append({
        "$group": {
            "_id": None,
            "products": {"$push": "$$ROOT"},
            "max_similarity": {"$max": "$similarity_score"},
            "max_popularity": {"$max": "$popularity_score"}  # <-- Bug fix from earlier is included
        }
    })

    pipeline.append({"$unwind": "$products"})

    pipeline.append({
        "$addFields": {
            "norm_similarity": {
                "$cond": {
                    "if": {"$gt": ["$max_similarity", 0]},
                    "then": {"$divide": ["$products.similarity_score", "$max_similarity"]},
                    "else": 0
                }
            },
            "norm_popularity": {
                "$cond": {
                    "if": {"$gt": ["$max_popularity", 0]},
                    "then": {"$divide": ["$products.popularity_score", "$max_popularity"]},
                    "else": 0
                }
            },
            "price_score": "$products.price_score"
        }
    })

    # --- Stage 4: Calculate Final Weighted Score (The Bonus) ---
    pipeline.append({
        "$addFields": {
            "weighted_score": {
                "$add": [
                    {"$multiply": ["$norm_similarity", 0.4]},
                    {"$multiply": ["$norm_popularity", 0.4]},
                    {"$multiply": ["$price_score", 0.2]}
                ]
            },
            "name": "$products.name",
            "_id": "$products._id",
            "price": "$products.price",
            "category": "$products.category",
            "brand": "$products.brand",
            "review_summary": "$products.review_summary",
            "similarity_score": "$products.similarity_score",
            "popularity_score": "$products.popularity_score"
        }
    })

    # --- Stage 5: Sort by Final Score and Limit ---
    pipeline.append({"$sort": {"weighted_score": -1}})
    pipeline.append({"$limit": limit})

    # --- Stage 6: Clean up final output ---
    pipeline.append({
        "$project": {
            "_id": 1,
            "name": 1,
            "price": 1,
            "category": 1,
            "brand": 1,
            "review_summary": 1,
            "weighted_score": 1,
            "similarity_score": "$norm_similarity",
            "popularity_score": "$norm_popularity",
            "price_score": 1
        }
    })

    # --- Execute the Pipeline ---
    try:
        results = list(db.products.aggregate(pipeline))
        return results
    except Exception as e:
        print(f"Error during search aggregation: {e}")
        raise HTTPException(status_code=500, detail="Search query failed")


# --- Run the App ---
if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )