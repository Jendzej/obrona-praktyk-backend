from dotenv import load_dotenv
from fastapi import APIRouter
from src.data_functions.data_fetch import fetch_all
from main import engine, other_models

load_dotenv()

router = APIRouter(
    tags=["school_classes"]
)
school_class_model = other_models[0]


@router.post('/get_classes')
async def get_classes():
    return fetch_all(engine, school_class_model)
