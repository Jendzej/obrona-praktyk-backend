from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth import router as authentication_router
from src.routers.items import router as item_router
from src.routers.transactions import router as transaction_router
from src.routers.users import router as user_router

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

app.include_router(authentication_router)
app.include_router(transaction_router)
app.include_router(user_router)
app.include_router(item_router)

"""
SAMPLE BODIES

USER:
{
"username":"user",
"email":"email",
"first_name":"First",
"last_name":"Last",
"password":"password",
"school_class":"4TIP"
}

ITEM:
{
"item_name":"item1",
"item_price": 4.5,
"item_description": "Description of item 1",
"item_image_url": "url1"
}

"""
