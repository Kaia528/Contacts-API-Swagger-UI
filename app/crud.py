from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from . import models, schemas





def create_contact(db: Session, data: schemas.ContactCreate) -> models.Contact:
    contact = models.Contact(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contact(db: Session, contact_id: int) -> models.Contact | None:
    return db.get(models.Contact, contact_id)


def list_contacts(db: Session, q: str | None, skip: int, limit: int) -> list[models.Contact]:
    stmt = select(models.Contact)
    if q:
        ilike = f"%{q.lower()}%"
        stmt = stmt.where(
            or_(
                func.lower(models.Contact.first_name).like(ilike),
                func.lower(models.Contact.last_name).like(ilike),
                func.lower(models.Contact.email).like(ilike),
            )
        )
    stmt = stmt.order_by(models.Contact.id).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def update_contact(db: Session, contact: models.Contact, data: schemas.ContactUpdate) -> models.Contact:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact: models.Contact) -> None:
    db.delete(contact)
    db.commit()


# --- Extra: birthdays in next N days ---


def contacts_with_birthdays_in_next_days(db: Session, days: int = 7) -> list[models.Contact]:
    """
    Повертає контакти, у яких день народження впродовж найближчих `days` днів.
    Коректно працює навіть при переході через кінець року.
    """
    today = date.today()
    end = today + timedelta(days=days)

    # Порівняння за місяцем і днем без року
    month_day = func.to_char(models.Contact.birthday, 'MMDD')
    today_md = f"{today.month:02d}{today.day:02d}"
    end_md = f"{end.month:02d}{end.day:02d}"

    if end >= today and end.year == today.year and end.month >= today.month:
        # звичайний випадок без переходу через 31/12
        stmt = select(models.Contact).where(
            models.Contact.birthday.is_not(None),
            month_day >= today_md,
            month_day <= end_md,
        ).order_by(month_day)
        return list(db.execute(stmt).scalars())
    else:
        # перехід через кінець року
        stmt = select(models.Contact).where(
            models.Contact.birthday.is_not(None),
            or_(month_day >= today_md, month_day <= end_md),
        ).order_by(month_day)
        return list(db.execute(stmt).scalars())
