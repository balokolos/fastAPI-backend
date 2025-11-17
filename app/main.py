from fastapi import FastAPI
import oracledb
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# DO NOT CALL init_oracle_client() → Thin mode automatically enabled

ORACLE_USER = os.getenv("ORACLE_USER", "hr")
ORACLE_PASS = os.getenv("ORACLE_PASS", "testpass")
ORACLE_DSN  = os.getenv("ORACLE_DSN", "localhost:1521/freepdb1")

# Create a connection pool (works in Thin mode)
pool = oracledb.create_pool(
    user=ORACLE_USER,
    password=ORACLE_PASS,
    dsn=ORACLE_DSN,
    min=1,
    max=5,
    increment=1
)

@app.get("/employee")
def get_employee(emp_id: int):
    with pool.acquire() as conn:
        cursor = conn.cursor()
        sql = """
            SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID
            FROM EMPLOYEES
            WHERE EMPLOYEE_ID = :id
        """
        cursor.execute(sql, {"id": emp_id})
        row = cursor.fetchone()

        if not row:
            return {"message": "Employee not found"}

        return {
            "employee_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "department_id": row[3]
        }
