from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AIModels
import os
from dotenv import load_dotenv
from pathlib import Path

app = Flask(__name__)

load_dotenv()

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/ai_models', methods=['GET'])
def get_ai_models():
    models = session.query(AIModels).all()
    return jsonify([model.to_dict() for model in models])

if __name__ == "__main__":
    app.run(debug=True)