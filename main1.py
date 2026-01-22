from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Depends

#just auto open 
import webbrowser
from threading import Timer


#auto opening part
def open_browser():
    webbrowser.open("http://127.0.0.1:8000/docs")

Timer(1, open_browser).start()

# -----------------------
# DATABASE SETUP
# -----------------------

DATABASE_URL = "mysql+mysqlconnector://root:Ayush%4017@localhost/fastapi_db"

print("DATABASE_URL USED:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------
# DATABASE MODEL
# -----------------------

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    age = Column(Integer)

# Create tables
#Base.metadata.create_all(bind=engine)

# -----------------------
# FASTAPI APP
# -----------------------

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.get("/")
def health():
    return {"status": "ok"}


class UserCreate(BaseModel):
    name: str
    age: int

#db create
@app.post("/users/db", tags=["Users"])
def create_user_db(user: UserCreate,db: Session = Depends(get_db)):
    new_user = UserDB(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "id": new_user.id,
        "name" : new_user.name,
        "age": new_user.age
    }

#get db
@app.get("/users/db/", tags=["Users"])
def get_user_db(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    return {
        "id": user.id,
        "name": user.name,
        "age" : user.age
    }        
         
#read all users
@app.get("/users/db/", tags=["Users"])
def get_users_db(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

#update User (put)
@app.put("/users/db/{user_id}", tags=["Users"])
def update_user_db(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not db_user:
        return {"error": "User not found"}
    
    db_user.name = user.name
    db_user.age = user.age
    
    db.commit()
    db.refresh(db_user)

    return {"message": "User updated",
            "id": db_user.id,
            "name" : db_user.name,
            "age" : db_user.age
        }

#delete user
@app.delete("/users/db/{user_id}", tags=["Users"])
def delete_user_db(
    user_id: int,
    db: Session = Depends(get_db)
):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not db_user:
        return {"error": "User not found"}
    
    db.delete(db_user)
    db.commit()

    return {"message": "User deleted"}
    

# -----------------------
# ITEMS IN-MEMORY CRUD
# -----------------------

class Item(BaseModel):
    name : str
    price: float
    in_stock: bool

items = []

@app.post("/items", tags=["Items"])
def create_item(item: Item):
    items.append(item.dict())
    return {"message": "Item added", "data": item}

@app.get("/items/{item_id}", tags=["Items"])
def get_item(item_id: int):
    if item_id < len(items):
        return items[item_id]
    return {"error": "Item not found"}

@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, updated_item: Item):
    if item_id < len(items):
        items[item_id] = updated_item.dict()
        return {"message": "Item updated" , "data": updated_item}
    return {"error": "Item not found"}

@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    if item_id < len(items):
        removed = items.pop(item_id)
        return {"message": "Item deleted", "data": removed}
    return {"error": "Item not found"}
