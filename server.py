#! /usr/bin/env python3.6
# docker run -p 5000:5000 damonwong2022148/server:2.0
# docker build --build-arg SECRET_KEY="sk_test_Ou1w6LVt3zmVipDVJsvMeQsc" --build-arg PAYMENT_URL="http://localhost:5000" --build-arg PAYMENTS_PORT="5000" --build-arg DEBUG="True" -t damonwong2022148/server:2.0 .
# https://docs.stripe.com/checkout/quickstart?client=html
"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import stripe

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PAYMENTS_PORT")
DEBUG = os.getenv("DEBUG")
stripe.api_key = SECRET_KEY

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

DOMAIN = os.environ.get("PAYMENT_URL")
PROCESS_BOOKING_URL = os.environ.get("PROCESS_BOOKING_URL")
FRONTEND_URL= os.environ.get("FRONTEND_URL")

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    name = request.form.get('name')
    pricePerNight = int(request.form.get('pricePerNight'))*100  # Convert to cents!
    currency = request.form.get('currency')
    duration = int(request.form.get('duration'))
    email = request.form.get('email')
    guestId = request.form.get('guestId')
    listingId = request.form.get('listingId')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    hostId = request.form.get('hostId')


    try:
        metadata = {
            'email': email,
            'guestId': guestId,
            'listingId': listingId,
            'hostId': hostId,
            'startDate': startDate,
            'endDate': endDate,
            'totalPrice': pricePerNight * duration
        }

        print('metadata', pricePerNight,  duration)
        print('metadata', metadata)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': currency,
                        'unit_amount': pricePerNight,
                        'product_data': {
                            'name': name
                        }
                    },
                    'quantity': duration,
                },
            ],
            mode='payment',
            success_url=FRONTEND_URL + '/listings',
            cancel_url=FRONTEND_URL + '/reservations',
            metadata=metadata
        )
        print(checkout_session.id)

        return jsonify({"checkout_url": checkout_session.url, 
                        "session_id": checkout_session.id,
                        "status": 303})

    except Exception as e:
        return str(e), 500
    


@app.route('/success')
def success():
    return jsonify({"status": "success", "message": "Payment Successful"})


@app.route('/canceled')
def canceled():
    return jsonify({"status": "canceled", "message": "Payment Canceled"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=(DEBUG or False))