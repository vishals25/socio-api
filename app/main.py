from fastapi import FastAPI
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins=["*"] # domain of front end application change it in deployment

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return "Hello World"