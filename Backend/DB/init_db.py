from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, AIModels
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def populate_initial_data():
    user = User(uname='JohnDoe', uemail='john@example.com')
    session.add(user)
    session.commit()
    
    models = [
        AIModels(
            model_id='1',
            model_name='yolov8n',
            model_description='The YOLOv8n (You Only Look Once version 8 nano) model is a lightweight, real-time object detection model designed for high-speed and efficiency',
            model_version='1.0',
            model_summary='The smallest version of the Yolov8 models.',
            model_profileimg='https://placekitten.com/200/200',
            model_img='https://placekitten.com/200/200'
        ),
        AIModels(
            model_id='2',
            model_name='yolov8s',
            model_description='The YOLOv8n (You Only Look Once version 8 nano) model is a lightweight, real-time object detection model designed for high-speed and efficiency',
            model_version='1.0',
            model_summary='The small version of the Yolov8 models.',
            model_profileimg='https://placekitten.com/200/200',
            model_img='https://placekitten.com/200/200'
        ),
        AIModels(
            model_id='3',
            model_name='HV1',
            model_description='Work in progress',
            model_version='1.0',
            model_summary='Under construction',
            model_profileimg='https://placekitten.com/200/201',
            model_img='https://placekitten.com/200/201'
        )
    ]

    session.add_all(models)
    session.commit()

populate_initial_data()
session.close()