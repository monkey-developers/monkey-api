from sqlalchemy.orm import Session
import models
import schema

def getMonkeyByMonkeyId(db:Session, monkey_id: str):
    return db.query(models.Monkeys).filter(models.Monkeys.monkey_id == monkey_id).first()

def getMonkeys(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.Monkeys).offset(skip).limit(limit).all()

def getMonkeyById(db:Session, sl_id: int):
    return db.query(models.Monkeys).filter(models.Monkeys.id == sl_id).first()  

def addNewMonkey(db:Session, monke: schema.MonkeyAdd):
    mky_details = models.Monkeys(
        monkey_id = monke.monkey_id,
        monkey_name = monke.monkey_name,
        monkey_age = monke.monkey_age,
        species = monke.species,
        gender = monke.gender,
        vip = monke.vip
    )
    db.add(mky_details)
    db.commit()
    db.refresh(mky_details)
    return models.Monkeys(**monke.dict())

def updateMonkey(db: Session, sl_id: int, details: schema.UpdateMonkey):
    
    # monke_details = db.query(models.Monkeys).filter(models.Monkeys.id == sl_id).first()
    
    # if monke_details is None:
    #     return None
    
    db.query(models.Monkeys).filter(models.Monkeys.id == sl_id).update(vars(details))
    db. commit()
    return db.query(models.Monkeys).filter(models.Monkeys.id == sl_id).first()

def delMonkeyById(db: Session, sl_id: int):
    try:
        db.query(models.Monkeys).filter(models.Monkeys.id == sl_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)