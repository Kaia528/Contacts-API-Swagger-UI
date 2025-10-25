from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .crud import get_contact
from . import models


DbDep = Session


async def get_db_dep(db: Session = Depends(get_db)) -> Session:
    return db


async def contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db_dep),
) -> models.Contact:
    contact = get_contact(db, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact
