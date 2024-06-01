# Dev (cmd)

## To create a Virtual enviroment

- python -m venv <Name>

## To activate it:

- <name>\Scripts\activate

## To deactivate:

- deactivate

## Install Dependencies:

- pip install -r Backend\requirements.txt
- pip list (To verify)

## run dev server:

- cd Backend\hvserve
- python manage.py runserver

# Deployment:

- docker-compose up -d --build
- docker-compose exec web alembic revision --autogenerate -m "Initial migration"
- docker-compose exec web alembic upgrade head
- docker-compose down