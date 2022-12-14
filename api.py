"""API endpoints, routers, hosts, paths, methods, etc. configuration"""
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main import startup_class, startup_roles, startup_status
from src.data_functions.school_class import SchoolClassFunction
from src.data_functions.status_and_roles import StatusRoleFunctions
from src.log import logger
from src.routers.auth import router as authentication_router
from src.routers.items import router as item_router
from src.routers.school_classes import router as school_class_router
from src.routers.transactions import router as transaction_router
from src.routers.users import router as user_router

load_dotenv()

school_class = SchoolClassFunction()
status_role_function = StatusRoleFunctions()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=os.getenv('FRONTEND_ORIGIN'),
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    """Inserting some data to database on API startup"""
    for single_school_class in startup_class:
        if school_class.insert(single_school_class, True):
            logger.info("Successfully added '%s' to school classes!", single_school_class)
    for single_role in startup_roles:
        if status_role_function.insert_role(single_role):
            logger.info("Successfully adedd `%s` to roles!", single_role)
    for single_status in startup_status:
        if status_role_function.insert_status(single_status):
            logger.info("Successfully added '%s' to payment statuses!", single_status)


app.include_router(authentication_router, prefix='/auth')
app.include_router(transaction_router, prefix='/transaction')
app.include_router(user_router, prefix='/user')
app.include_router(item_router, prefix='/item')
app.include_router(school_class_router, prefix='/school_class')
