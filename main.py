from http.client import ResponseNotReady
from urllib import response
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schema
from db_handler import SessionLocal, engine 

models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "Monkey Developers Profiles API",
    version = "0.0.1"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get('/retrieveAllMonkeys', response_model = list[schema.Monkey])
def retrieveAllMonkeys(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    monkeys = crud.getMonkeys(db = db, skip = skip, limit = limit)
    return monkeys

@app.put('/updateMonkey', response_model = schema.Monkey)
def updateMonkey(sl_id:int, update_param:schema.UpdateMonkey, db:Session = Depends(get_db)):
    details = crud.getMonkeyById(db = db, sl_id = sl_id)
    if not details:
        raise HTTPException(status_code=400, detail=f'Nothing was found to update')
    return crud.updateMonkey(db = db, details = update_param, sl_id = sl_id)

@app.delete('/deleteMonkey')
def deleteMonkey(sl_id:int, db:Session = Depends(get_db)):
    details = crud.getMonkeyById(db = db, sl_id = sl_id)
    
    if not details:
        raise HTTPException(status_code = 400, detail=f'Nothing was found to delete')
    
    try:
        crud.delMonkeyById(db = db, sl_id = sl_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail=f'Unable to delete: {e}')
    return {'delete status':'success'}

@app.post('/addNewMonkey', response_model = schema.MonkeyAdd)
def addNewMonkey(monkey:schema.MonkeyAdd, db:Session = Depends(get_db)):
    monkey_id = crud.getMonkeyByMonkeyId(db = db, monkey_id = monkey.monkey_id)
    if monkey_id:
        raise HTTPException(status_code=400, detail=f"Monkey ID: {monkey.monkey_id} is already on db: {monkey_id}")
    return crud.addNewMonkey(db = db, monke=monkey)