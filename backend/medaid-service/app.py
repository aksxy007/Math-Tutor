from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.chat import router as ChatRouter

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ChatRouter,prefix='/api')

# @app.get("/")
# def home():
#     return {"message":"Home"}