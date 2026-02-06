from fastapi import FastAPI
from app.routes import project  # or whatever routers you have

app = FastAPI(
    title="BuildWise Backend",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
def root():
    return {"message": "BuildWise backend is running 🚀"}

# include routers
app.include_router(project.router)
