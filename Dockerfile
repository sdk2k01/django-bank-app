FROM python:3.12.4-slim-bullseye

WORKDIR /app

COPY requirements/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

COPY . /app
WORKDIR /app/src

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py" ]
CMD ["runserver", "0.0.0.0:8000"]
