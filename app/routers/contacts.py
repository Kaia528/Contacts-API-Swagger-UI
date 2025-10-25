from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Annotated
from .. import schemas, crud
from ..deps import get_db_dep, contact_by_id


router = APIRouter(prefix="/contacts", tags=["contacts"])

Db = Annotated[Session, Depends(get_db_dep)]


@router.post("/", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(data: schemas.ContactCreate, db: Db):
    return crud.create_contact(db, data)


@router.get("/", response_model=list[schemas.ContactOut])
def list_contacts(
    db: Db,
    q: str | None = Query(default=None, description="Пошук за ім'ям/прізвищем/емейлом"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    return crud.list_contacts(db, q=q, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact: Annotated[schemas.ContactOut, Depends(contact_by_id)]):
    return contact


@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, data: schemas.ContactUpdate, db: Db):
    contact = contact_by_id.__wrapped__(contact_id, db)  # синхронний виклик залежності
    return crud.update_contact(db, contact, data)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Db):
    contact = contact_by_id.__wrapped__(contact_id, db)
    crud.delete_contact(db, contact)
    return None


@router.get("/birthdays/upcoming", response_model=list[schemas.ContactOut])
def upcoming_birthdays(db: Db, days: int = Query(7, ge=1, le=30)):
    return crud.contacts_with_birthdays_in_next_days(db, days=days)
