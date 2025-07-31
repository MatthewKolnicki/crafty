from fastapi import FastAPI
from mangum import Mangum
from routers import py_questions, sql_questions
from connectors.database import Database
from app.config import config


app = FastAPI()

app.include_router(py_questions.router)
app.include_router(sql_questions.router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Hello from Crafty CRM API",
        "version": "1.0.0",
        "environment": "production" if config.is_production else "development",
    }


@app.get("/health")
def health_check():
    """Health check endpoint to test database connectivity."""
    try:
        db = Database()
        if db.test_connection():
            return {
                "status": "healthy",
                "database": "connected",
                "message": "API and database are working correctly",
            }
        else:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "message": "Database connection failed",
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "message": f"Health check failed: {str(e)}",
        }


handler = Mangum(app)
