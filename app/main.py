from fastapi import FastAPI

from app.models import ValidationRequest
from app.validator import validate


app = FastAPI(
    title="AI Policy Validation Platform",
    description="API for validating resources against security policies",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/validate")
def validate_resource(request: ValidationRequest):

    result = validate(request)

    return result