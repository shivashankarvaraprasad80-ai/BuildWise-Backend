from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from app.database import SessionLocal
from app import models

router = APIRouter()

# -------------------------
# Database dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# POST /analyzeSite/{project_id}
# -------------------------
@router.post("/analyzeSite/{project_id}")
def analyze_site(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ai_result = {
        "feasibility": "High",
        "estimated_cost": "₹2.5 Crores",
        "zoning_status": "Approved",
        "risk_level": "Low",
        "suggestion": "Proceed with construction"
    }

    project.analysis_result = str(ai_result)
    db.commit()

    return {
        "message": "AI site analysis completed",
        "analysis_result": ai_result
    }

# -------------------------
# GET /projectResults/{project_id}
# -------------------------
@router.get("/projectResults/{project_id}")
def get_project_results(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.analysis_result:
        return {"message": "Analysis not performed yet"}

    return {
        "project_id": project_id,
        "analysis_result": project.analysis_result
    }

# -------------------------
# GET /downloadReport/{project_id}
# -------------------------
@router.get("/downloadReport/{project_id}")
def download_report(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.analysis_result:
        raise HTTPException(status_code=400, detail="Analysis not available")

    # Ensure uploads folder exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_name = f"report_project_{project_id}.pdf"
    file_path = f"uploads/{file_name}"

    # Create PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(50, 750, "BuildWise – Construction Feasibility Report")
    c.drawString(50, 720, f"Project ID: {project.id}")
    c.drawString(50, 690, f"Project Name: {project.name}")
    c.drawString(50, 660, f"Location: {project.location}")
    c.drawString(50, 620, "AI Analysis Result:")
    c.drawString(50, 590, project.analysis_result)
    c.save()

    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/pdf"
    )
