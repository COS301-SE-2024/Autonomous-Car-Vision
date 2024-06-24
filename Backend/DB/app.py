from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AIModels
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Construct the database URL
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

# Create an engine and bind the base
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/ai_models', methods=['GET'])
def get_ai_models():
    models = session.query(AIModels).all()
    return jsonify([model.to_dict() for model in models])

if __name__ == "__main__":
    app.run(debug=True)