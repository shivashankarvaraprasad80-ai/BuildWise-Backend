from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import project, upload, analysis

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BuildWise Backend")

app.include_router(project.router)
app.include_router(upload.router)
app.include_router(analysis.router)

@app.get("/")
def root():
    return {"message": "BuildWise backend is running 🚀"}
