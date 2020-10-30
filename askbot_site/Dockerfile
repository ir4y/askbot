FROM python:3.8
RUN mkdir /app
WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
COPY . .

CMD ["pipenv", "run", "gunicorn", "sovereignty_network.wsgi", "-b", "0.0.0.0:8000"]
EXPOSE 8000
