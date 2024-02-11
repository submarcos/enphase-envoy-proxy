FROM python:3.11-alpine
LABEL authors="jec"

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "enphase_proxy.wsgi:application"]
