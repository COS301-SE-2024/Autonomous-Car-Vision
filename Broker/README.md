# Create the virtual enviroment

python -m venv brokerVenv

## Activate venv

brokerVenv\Scripts\activate

## Deactivate venv

deactivate

## Install Dependencies:

pip install -r Broker\requirements.txt
pip list (To verify)

## Run ASGI SERVER
cd Broker/API
uvicorn broker:app --reload --port 8006


## To test via postman

http://127.0.0.1:8001

main refers to the Python file (without the .py extension).
app refers to the FastAPI instance inside that file.
--reload enables auto-reload on code changes, useful for development.

## Documentation

Swagger UI: http://127.0.0.1:8001/docs
ReDoc: http://127.0.0.1:8001/redoc

## Prod server:
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

-w 4 specifies the number of worker processes.
-k uvicorn.workers.UvicornWorker specifies the worker class.

# Tips for FastAPI Development
Use Pydantic models for data validation.
Take advantage of FastAPI's dependency injection system.
Use background tasks for time-consuming operations.
Secure your API with authentication and authorization.

## include dependencies in requirments file

pip freeze > Broker/requirements.txt