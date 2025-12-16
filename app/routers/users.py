from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import mysql.connector
from app.models import User
from app.database import pool

router = APIRouter(
    tags=["Users"]
)

# GET endpoint to retrieve a user by phone number
@router.get(
        "/users",
        status_code=status.HTTP_200_OK,
        summary="Retrieve a user by phone number")
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
            raise HTTPException(status_code=404, detail="User not found")

        return row
    finally:
        cursor.close()
        conn.close()

@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
def create_user(user: User):
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
    except mysql.connector.IntegrityError as err:
        if err.errno == 1062:  # Duplicate entry error code
            raise HTTPException(status_code=400, detail="User with this phone number already exists")
    except mysql.connector.Error as err:
        conn.rollback()  # rollback in case of error
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
