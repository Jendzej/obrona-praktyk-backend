from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth import router as authentication_router
from src.routers.items import router as item_router
from src.routers.transactions import router as transaction_router
from src.routers.users import router as user_router
from src.routers.school_classes import router as school_class_router

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=os.getenv('FRONTEND_ORIGIN'),
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)

app.include_router(authentication_router, prefix='/auth')
app.include_router(transaction_router, prefix='/transaction')
app.include_router(user_router, prefix='/user')
app.include_router(item_router, prefix='/item')
app.include_router(school_class_router, prefix='/school_class')
