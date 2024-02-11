FROM python:3.11-alpine
LABEL authors="jec"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["gunicorn", "-b", "0.0.0.0:8000", "enphase_proxy.wsgi:application"]
