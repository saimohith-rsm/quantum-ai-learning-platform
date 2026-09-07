from fastapi import APIRouter, HTTPException
from app.curriculum.lessons import get_all_modules, get_lesson_by_id

router = APIRouter(prefix="/api/curriculum", tags=["Curriculum & Lessons"])

@router.get("/modules")
def list_curriculum_modules():
    """Returns the full curriculum of quantum modules and lessons."""
    return get_all_modules()

@router.get("/lessons/{lesson_id}")
def get_curriculum_lesson(lesson_id: str):
    """Returns the details, interactive starter circuit, and quiz for a specific lesson."""
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")
    return lesson
