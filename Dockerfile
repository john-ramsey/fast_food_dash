FROM python:3.9-slim

COPY . /
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

CMD gunicorn -b 0.0.0.0:80 main:server