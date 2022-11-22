from dotenv import load_dotenv
from fastapi import APIRouter

from src.data_functions.school_class_functions import SchoolClassFunction

load_dotenv()

router = APIRouter(
    tags=["school_classes"]
)
school_class = SchoolClassFunction()


@router.get('')
async def get_school_classes():
    """ Fetch all school classes """
    return school_class.get_all()
