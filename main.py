from fastapi import FastAPI, Request
from app.core.api import api_router
from starlette.middleware.cors import CORSMiddleware
import uvicorn


description = """
# Welcome to the API documentation for the **Code-Assessment** application.
"""


app = FastAPI(
    title="code-assessment", openapi_url=f"/api/v1/openapi.json",
    redoc_url="/documentation",
    description=description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
