from fastapi import FastAPI, Depends, HTTPException, Query 
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List, Optional
from datetime import date, timedelta

app = FastAPI()

# Створюємо таблиці в БД автоматично
models.Base.metadata.create_all(bind=database.engine)

# --- МАРШРУТИ (ENDPOINTS) ---

@app.get("/")
def read_root():
    return {"message": "Welcome to Contacts API. Go to /docs for documentation."}

# Створення нового контакту
@app.post("/contacts/", response_model=schemas.ContactResponse, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Отримання списку всіх контактів
@app.get("/contacts/", response_model=List[schemas.ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Contact).offset(skip).limit(limit).all()

# Пошук контактів за іменем, прізвищем або email
@app.get("/contacts/search/", response_model=List[schemas.ContactResponse])
def search_contacts(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Contact)
    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    return query.all()

# Отримання контактів з днями народження на найближчі 7 днів
@app.get("/contacts/birthdays/", response_model=List[schemas.ContactResponse])
def get_upcoming_birthdays(db: Session = Depends(database.get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    
    all_contacts = db.query(models.Contact).all()
    upcoming = []
    
    for contact in all_contacts:
        if contact.birthday:
            # Перевіряємо день народження в цьому році
            try:
                bday_this_year = contact.birthday.replace(year=today.year)
            except ValueError: # Для тих, хто народився 29 лютого
                bday_this_year = contact.birthday.replace(year=today.year, month=3, day=1)

            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)
            
            if today <= bday_this_year <= next_week:
                upcoming.append(contact)
    return upcoming

# Отримання одного контакту за ID
@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(database.get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Оновлення контакту
@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, body: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in body.model_dump().items():
        setattr(contact, key, value)
    
    db.commit()
    db.refresh(contact)
    return contact

# Видалення контакту
@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return None