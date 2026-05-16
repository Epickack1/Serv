from fastapi import FastAPI

from routers import auth_v1, auth_v2, auth_v3, headers, products, users

app = FastAPI(title="Контрольная работа №2")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth_v1.router)
app.include_router(auth_v2.router)
app.include_router(auth_v3.router)
app.include_router(headers.router)


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "КР2 — FastAPI. Документация: /docs",
        "tasks": {
            "3.1": "POST /create_user",
            "3.2": "GET /product/{id}, GET /products/search",
            "5.1": "POST /v1/login, GET /v1/user",
            "5.2": "POST /v2/login, GET /v2/profile",
            "5.3": "POST /v3/login, GET /v3/profile",
            "5.4": "GET /headers-simple",
            "5.5": "GET /headers, GET /info",
        },
    }
