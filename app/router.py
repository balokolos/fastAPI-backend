from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel  
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "testpass")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB   = os.getenv("MYSQL_DB", "testdb")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

# Create a connection pool
pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=MYSQL_DB
)

# Pydantic model for the request body
class User(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str

# GET endpoint to retrieve a user by phone number
@app.get("api/v1/users")
def get_users(phone_number: int):
    conn = pool.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT first_name, last_name, phone_number
            FROM users
            WHERE phone_number = %s
        """
        cursor.execute(sql, (phone_number,))
        row = cursor.fetchone()

        if not row:
            return {"message": "User not found"}

        return row
    finally:
        cursor.close()
        conn.close()

# POST endpoint to create a new user
@app.post("/api/v1/users")
def create_users(user: User):
    conn = pool.get_connection()
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO users (first_name, last_name, phone_number, address)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (user.first_name, user.last_name, user.phone_number, user.address))
        conn.commit()  # commit the transaction
        return JSONResponse(
            status_code=201, content={"message": "User created successfully", "user_id": cursor.lastrowid}
            )
    except mysql.connector.Error as err:
        conn.rollback()  # rollback in case of error
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()