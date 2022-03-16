FROM python:3.9-slim

COPY . /
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

EXPOSE 8080

CMD gunicorn -b 0.0.0.0:8080 main:server