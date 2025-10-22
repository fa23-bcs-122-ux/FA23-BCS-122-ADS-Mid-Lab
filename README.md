# E-commerce API - Q2 Mini-Project

This project is a FastAPI backend for an e-commerce marketplace, fulfilling the requirements for Q2. It uses MongoDB as the database.

## Project Structure

- `main.py`: The main FastAPI application, containing all API endpoints.
- `seed.py`: A Python script to seed the MongoDB database with data and create indexes.
- `requirements.txt`: All Python dependencies.
- `dataset/`: Contains sample JSON data files.

## How to Run

### 1. Prerequisites

- Python 3.10+
- MongoDB running on `mongodb://localhost:27017/`

### 2. Setup

1.  Clone this repository.
2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
3.  Activate the environment:
    ```bash
    # On Windows
    .\.venv\Scripts\activate
    ```
4.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Seed the Database

Before running the API, you must populate the database and create the search indexes.

```bash
python seed.py