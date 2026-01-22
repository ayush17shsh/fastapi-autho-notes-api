from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app import models
from app.schemas.notes import NoteCreate, NoteResponse
from app.deps import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.UserDB).filter(
        models.UserDB.name == current_user
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_note = models.NotesDB(
        title=note.title,
        content=note.content,
        owner_id=user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note



@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    note = db.query(models.NotesDB).filter(
        models.NotesDB.id == note_id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}



@router.get("/", response_model=List[NoteResponse])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.UserDB).filter(
        models.UserDB.name == current_user
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(models.NotesDB).filter(
        models.NotesDB.owner_id == user.id
    ).all()



@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    note = db.query(models.NotesDB).filter(
        models.NotesDB.id == note_id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note



@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated_note: NoteCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    note = db.query(models.NotesDB).filter(
        models.NotesDB.id == note_id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.content = updated_note.content

    db.commit()
    db.refresh(note)

    return note
