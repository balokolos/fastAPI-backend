from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import mysql.connector
from app.database import pool

router = APIRouter(
    tags=["Healthz"]
)

# GET 
@router.get(
        "/healthz",
        status_code=status.HTTP_200_OK,
        summary="healthz check")
def get_healthz():
    return {"status": "ok"}


@router.get(
    "/readiness",
    status_code=status.HTTP_200_OK,
    summary="readiness check"
)
def readiness():
    conn = pool.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        _ = cursor.fetchone() # just to ensure the query runs
        return JSONResponse(
            status_code=200, content={"status": "ready"}
        )
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()
