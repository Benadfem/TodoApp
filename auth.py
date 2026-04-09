from fastapi import FastAPI

app = FastAPI()

@app.get("/auth")
async def get_auth():
    return {"username": "admin", "password": ""}