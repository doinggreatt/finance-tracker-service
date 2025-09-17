from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError
import uvicorn

from src.routers import api_router

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.include_router(api_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title="AuthX API", version="1.0", description="API with JWT auth", routes=app.routes)
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi


@app.exception_handler(MissingTokenError)
async def missing_token_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=404 ,
        content={"detail": "Not Found"}
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8089, reload=True)

