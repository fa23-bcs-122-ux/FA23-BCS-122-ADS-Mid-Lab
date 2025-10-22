import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import sys

# --- Configuration ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecom_marketplace"

# --- Data Definitions ---

# We'll pre-define ObjectIDs so we can link documents
user_sufyan_id = ObjectId()
user_jane_id = ObjectId()

prod_laptop_id = ObjectId()
prod_mouse_id = ObjectId()
prod_book_id = ObjectId()


def get_data():
    """Defines the expanded seed data."""

    # --- ObjectIDs for linking ---
    # Users
    user_sufyan_id = ObjectId()
    user_jane_id = ObjectId()
    user_ali_id = ObjectId()

    # Products
    prod_laptop_hp_id = ObjectId()
    prod_mouse_logi_id = ObjectId()
    prod_book_pragmatic_id = ObjectId()
    prod_keyboard_keychron_id = ObjectId()
    prod_monitor_dell_id = ObjectId()
    prod_book_design_id = ObjectId()
    prod_coffee_maker_id = ObjectId()
    prod_headphones_sony_id = ObjectId()

    # Orders
    order_1_id = ObjectId()
    order_2_id = ObjectId()
    order_3_id = ObjectId()
    order_4_id = ObjectId()

    # --- Collections ---

    users = [
        {
            "_id": user_sufyan_id,
            "name": "Sufyan Ahmed",
            "email": "sufyan@example.com",
            "hashed_password": "bcrypt_hash_string_1",
            "location": {"address": "123 Main St", "city": "Lahore", "country": "Pakistan"},
            "purchase_history": [order_1_id],  # Will be updated
            "created_at": datetime(2025, 1, 15)
        },
        {
            "_id": user_jane_id,
            "name": "Jane Doe",
            "email": "jane@example.com",
            "hashed_password": "bcrypt_hash_string_2",
            "location": {"address": "456 Oak Ave", "city": "New York", "country": "USA"},
            "purchase_history": [order_2_id, order_4_id],
            "created_at": datetime(2025, 2, 20)
        },
        {
            "_id": user_ali_id,
            "name": "Ali Raza",
            "email": "ali@example.com",
            "hashed_password": "bcrypt_hash_string_3",
            "location": {"address": "789 Pine Ln", "city": "Karachi", "country": "Pakistan"},
            "purchase_history": [order_3_id],
            "created_at": datetime(2025, 5, 10)
        }
    ]

    products = [
        {
            "_id": prod_laptop_hp_id,
            "name": "HP Spectre x360 14",
            "description": "Premium 2-in-1 laptop with 14-inch display.",
            "category": "Electronics",
            "brand": "HP",
            "price": 1499.99,
            "stock": 150,
            "specs": {"ram_gb": 16, "storage_ssd_gb": 512, "processor": "Intel Core i7"},
            "review_summary": {"average_rating": 4.7, "review_count": 2},  # Updated count
            "purchase_count": 120,
            "created_at": datetime(2025, 3, 1)
        },
        {
            "_id": prod_mouse_logi_id,
            "name": "Logitech MX Master 3",
            "description": "Advanced wireless mouse for productivity.",
            "category": "Electronics",
            "brand": "Logitech",
            "price": 99.99,
            "stock": 300,
            "specs": {"connectivity": "Bluetooth/USB", "dpi": 4000},
            "review_summary": {"average_rating": 4.8, "review_count": 1},  # Updated count
            "purchase_count": 450,
            "created_at": datetime(2025, 3, 5)
        },
        {
            "_id": prod_book_pragmatic_id,
            "name": "The Pragmatic Programmer",
            "description": "A classic book on software engineering and coding.",
            "category": "Books",
            "brand": "Addison-Wesley",
            "price": 45.50,
            "stock": 100,
            "specs": {"format": "Paperback", "pages": 352},
            "review_summary": {"average_rating": 4.6, "review_count": 1},  # Updated count
            "purchase_count": 75,
            "created_at": datetime(2025, 1, 10)
        },
        {
            "_id": prod_keyboard_keychron_id,
            "name": "Keychron Q2 Mechanical Keyboard",
            "description": "A fully customizable 65% layout mechanical keyboard.",
            "category": "Electronics",
            "brand": "Keychron",
            "price": 189.99,
            "stock": 75,
            "specs": {"layout": "65%", "switch": "Gateron Brown"},
            "review_summary": {"average_rating": 4.9, "review_count": 1},  # Updated count
            "purchase_count": 210,
            "created_at": datetime(2025, 4, 15)
        },
        {
            "_id": prod_monitor_dell_id,
            "name": "Dell UltraSharp 27\" 4K Monitor",
            "description": "A 4K UHD monitor with stunning color accuracy.",
            "category": "Electronics",
            "brand": "Dell",
            "price": 549.99,
            "stock": 50,
            "specs": {"resolution": "3840x2160", "panel_type": "IPS"},
            "review_summary": {"average_rating": 4.5, "review_count": 0},
            "purchase_count": 35,
            "created_at": datetime(2025, 2, 28)
        },
        {
            "_id": prod_book_design_id,
            "name": "Designing Data-Intensive Applications",
            "description": "The big book on data systems design.",
            "category": "Books",
            "brand": "O'Reilly",
            "price": 59.99,
            "stock": 120,
            "specs": {"format": "Paperback", "pages": 616},
            "review_summary": {"average_rating": 4.9, "review_count": 1},  # Updated count
            "purchase_count": 180,
            "created_at": datetime(2025, 1, 5)
        },
        {
            "_id": prod_coffee_maker_id,
            "name": "Breville Barista Express",
            "description": "All-in-one espresso machine with integrated grinder.",
            "category": "Home Appliances",
            "brand": "Breville",
            "price": 749.95,
            "stock": 30,
            "specs": {"type": "Espresso Machine", "water_tank_l": 2},
            "review_summary": {"average_rating": 4.7, "review_count": 0},
            "purchase_count": 40,
            "created_at": datetime(2025, 3, 20)
        },
        {
            "_id": prod_headphones_sony_id,
            "name": "Sony WH-1000XM5",
            "description": "Industry-leading noise-canceling wireless headphones.",
            "category": "Electronics",
            "brand": "Sony",
            "price": 399.99,
            "stock": 90,
            "specs": {"connectivity": "Bluetooth", "noise_canceling": "Active"},
            "review_summary": {"average_rating": 0, "review_count": 0},
            "purchase_count": 0,  # New product
            "created_at": datetime(2025, 10, 20)  # Very recent
        }
    ]

    orders = [
        {
            "_id": order_1_id,
            "user_id": user_sufyan_id,
            "products": [
                {
                    "product_id": prod_laptop_hp_id,
                    "name": "HP Spectre x360 14",
                    "price_at_purchase": 1499.99,
                    "quantity": 1
                },
                {
                    "product_id": prod_mouse_logi_id,
                    "name": "Logitech MX Master 3",
                    "price_at_purchase": 99.99,
                    "quantity": 1
                }
            ],
            "total_cost": 1599.98,
            "status": "shipped",
            "shipping_address": {"address": "123 Main St", "city": "Lahore", "country": "Pakistan"},
            "timestamp": datetime(2025, 10, 15)  # Last month
        },
        {
            "_id": order_2_id,
            "user_id": user_jane_id,
            "products": [
                {
                    "product_id": prod_book_pragmatic_id,
                    "name": "The Pragmatic Programmer",
                    "price_at_purchase": 45.50,
                    "quantity": 2
                }
            ],
            "total_cost": 91.00,
            "status": "delivered",
            "shipping_address": {"address": "456 Oak Ave", "city": "New York", "country": "USA"},
            "timestamp": datetime(2025, 9, 10)
        },
        {
            "_id": order_3_id,
            "user_id": user_ali_id,
            "products": [
                {
                    "product_id": prod_keyboard_keychron_id,
                    "name": "Keychron Q2 Mechanical Keyboard",
                    "price_at_purchase": 189.99,
                    "quantity": 1
                },
                {
                    "product_id": prod_monitor_dell_id,
                    "name": "Dell UltraSharp 27\" 4K Monitor",
                    "price_at_purchase": 549.99,
                    "quantity": 1
                }
            ],
            "total_cost": 739.98,
            "status": "pending",
            "shipping_address": {"address": "789 Pine Ln", "city": "Karachi", "country": "Pakistan"},
            "timestamp": datetime(2025, 10, 21)  # Very recent
        },
        {
            "_id": order_4_id,
            "user_id": user_jane_id,
            "products": [
                {
                    "product_id": prod_book_design_id,
                    "name": "Designing Data-Intensive Applications",
                    "price_at_purchase": 59.99,
                    "quantity": 1
                },
                {
                    "product_id": prod_coffee_maker_id,
                    "name": "Breville Barista Express",
                    "price_at_purchase": 749.95,
                    "quantity": 1
                }
            ],
            "total_cost": 809.94,
            "status": "delivered",
            "shipping_address": {"address": "456 Oak Ave", "city": "New York", "country": "USA"},
            "timestamp": datetime(2025, 8, 5)
        }
    ]

    reviews = [
        # Reviews for HP Laptop
        {
            "_id": ObjectId(),
            "product_id": prod_laptop_hp_id,
            "user_id": user_sufyan_id,
            "rating": 5,
            "review_text": "Amazing laptop, battery life is fantastic!",
            "timestamp": datetime(2025, 10, 20)
        },
        {
            "_id": ObjectId(),
            "product_id": prod_laptop_hp_id,
            "user_id": user_jane_id,
            "rating": 4,
            "review_text": "A bit expensive, but build quality is top-notch.",
            "timestamp": datetime(2025, 10, 21)
        },
        # Review for Mouse
        {
            "_id": ObjectId(),
            "product_id": prod_mouse_logi_id,
            "user_id": user_sufyan_id,
            "rating": 5,
            "review_text": "Best mouse I have ever used.",
            "timestamp": datetime(2025, 10, 20)
        },
        # Review for Pragmatic Programmer book
        {
            "_id": ObjectId(),
            "product_id": prod_book_pragmatic_id,
            "user_id": user_jane_id,
            "rating": 5,
            "review_text": "A must-read for every developer.",
            "timestamp": datetime(2025, 9, 15)
        },
        # Review for Keychron Keyboard
        {
            "_id": ObjectId(),
            "product_id": prod_keyboard_keychron_id,
            "user_id": user_ali_id,
            "rating": 5,
            "review_text": "Love the typing feel. The build is solid aluminum.",
            "timestamp": datetime(2025, 10, 22)
        },
        # Review for Data-Intensive book
        {
            "_id": ObjectId(),
            "product_id": prod_book_design_id,
            "user_id": user_jane_id,
            "rating": 5,
            "review_text": "The bible of system design. Incredibly dense but rewarding.",
            "timestamp": datetime(2025, 8, 10)
        }
    ]

    return users, products, orders, reviews

def create_indexes(db):
    """Creates the indexes we designed in Q1."""

    # 1. On users
    db.users.create_index("email", unique=True)

    # 2. On products (CRITICAL for search)

    db.products.create_index(
        [
            ("name", pymongo.TEXT),
            ("description", pymongo.TEXT),
            ("brand", pymongo.TEXT),
            ("category", pymongo.TEXT)  # <-- ADDED THIS LINE
        ],
        name="product_text_search_index"
    )

    # --- THIS IS THE CORRECTED LINE ---
    db.products.create_index([("purchase_count", pymongo.DESCENDING)])

    db.products.create_index([("category", 1), ("price", 1)])

    # 3. On reviews
    db.reviews.create_index([("product_id", 1), ("timestamp", -1)])

    # 4. On orders
    db.orders.create_index([("user_id", 1), ("timestamp", -1)])

    print("Indexes created successfully.")

def main():
    """Main seeding function."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]

        print(f"Connected to MongoDB. Seeding database: {DB_NAME}")

        # --- 1. Get Data ---
        users, products, orders, reviews = get_data()

        # --- 2. Drop Old Collections ---
        print("Dropping old collections...")
        db.users.drop()
        db.products.drop()
        db.orders.drop()
        db.reviews.drop()

        # --- 3. Insert New Data ---
        print("Inserting new data...")
        db.users.insert_many(users)
        db.products.insert_many(products)
        db.orders.insert_many(orders)
        db.reviews.insert_many(reviews)
        print("Data inserted successfully.")

        # --- 4. Create Indexes ---
        print("Creating indexes...")
        create_indexes(db)

        print("--- Seeding Complete ---")

    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()