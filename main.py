from fastapi import FastAPI
from routers.users.api import router as router_user

app = FastAPI()
app.include_router(router_user)


@app.get("/")
async def main():
    return {"status": "Pagina pricipal"}
