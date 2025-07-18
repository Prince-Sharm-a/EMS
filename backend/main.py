from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import settings, create_table
from routers.all_routers import emp

create_table()

app=FastAPI(
    title="Employee Management System",
    description='api to manage Employee Management System',
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(emp,prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)