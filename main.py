from fastapi import FastAPI

app=FastAPI()


# Path Operation

@app.get("/")
async def root():
    return ["message","Hello World"]