FROM python:3-slim

ARG SECRET_KEY
ARG PAYMENT_URL
ARG PAYMENTS_PORT
ARG DEBUG

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install python-dotenv
COPY ./server.py .
EXPOSE 5000
CMD [ "python", "./server.py" ]