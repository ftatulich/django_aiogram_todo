FROM python:3.11

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000