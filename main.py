from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.users.api import router as router_user

app = FastAPI()
app.include_router(router_user)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"status": "Pagina pricipal"}
