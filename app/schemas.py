from datetime import date
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
      first_name: str = Field(min_length=1, max_length=100)
      last_name: str = Field(min_length=1, max_length=100)
      email: EmailStr
      phone: str = Field(min_length=3, max_length=50)
      birthday: date | None = None
      notes: str | None = Field(default=None, max_length=1000)


class ContactCreate(ContactBase):
 pass


class ContactUpdate(BaseModel):
      first_name: str | None = Field(default=None, min_length=1, max_length=100)
      last_name: str | None = Field(default=None, min_length=1, max_length=100)
      email: EmailStr | None = None
      phone: str | None = Field(default=None, min_length=3, max_length=50)
      birthday: date | None = None
      notes: str | None = Field(default=None, max_length=1000)


class ContactOut(ContactBase):
 id: int


class Config:
      from_attributes = True