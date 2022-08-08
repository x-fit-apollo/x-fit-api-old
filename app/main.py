from typing import List
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from model import ExerciseRecord
from fastapi.middleware.cors import CORSMiddleware
from db.main import get_db
from db import schemas, crud

from sqlalchemy.orm import Session

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "Hello World!"

    # @app.get("/records", response_model=List[ExerciseRecord])
    # def read_records(user_id: int, exercise_name: str) -> list:

    record_1 = {
        "date": datetime(2022, 6, 1),
        "exercise_name": "DeadLift",
        "weight": 185,
        "weight_unit": "lb",
    }
    record_2 = {
        "date": datetime(2022, 6, 2),
        "exercise_name": "DeadLift",
        "weight": 195,
        "weight_unit": "lb",
    }

    return [record_1, record_2]


@app.post("/record/", response_model=schemas.Record)
def create_record_for_user(
    user_id: int, record: schemas.RecordCreate, db: Session = Depends(get_db)
):

    return crud.create_user_records(db=db, record=record, user_id=user_id)


@app.get("/records", response_model=list[schemas.Record])
def read_records_for_user(
    user_id: int, exercise_name: str, db: Session = Depends(get_db)
) -> list[schemas.Record]:

    records = crud.get_records_for_user(db, user_id, exercise_name, skip=0, limit=100)

    return records
