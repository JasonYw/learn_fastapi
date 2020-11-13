from sqlalchemy.orm import Session
import models,schemas

class Operation_User():
    database =models.User

    @classmethod
    def get_user(cls,db:Session,user_id:int):
        return db.query(cls.database).filter(cls.database.id ==user_id)
    
    @classmethod
    def get_user_by_email(cls,db:Session,email:str):
        return db.query(cls.database).filter(cls.database.email ==email)
    
    @classmethod
    def get_users(cls,db:Session,skip:int=0,limit:int=100):
        return db.query(cls.database).offset(skip).limit(limit).all()

    @classmethod
    def create_user(cls,db:Session,user:schemas.UserCreate):
        fake_hashed_password =user.password + 'notreallyhashed'
        db_user =cls.database(email=user.email,hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh()
        return db_user
    

class Operation_Item():
    database =models.Item

    @classmethod
    def get_items(cls,db:Session,skip:int=0,limit:int=100):
        return db.query(cls.database).offset(skip).limit(limit).all()

    @classmethod
    def create_user_item(cls,db:Session,item:schemas.ItemCreate,user_id:int):
        db_item =cls.database(**item.dict(),owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    
