# Flask Stripe Sample

This is a Flask application for handling payments using Stripe.

## Requirements
- Python 3.6 or newer
- Stripe API secret key
- Docker (if you want to containerize the application)

## Installation
1. Clone the repository: `git clone https://github.com/yourusername/<your_project_name>.git`
2. Navigate to the project directory: `cd <your_project_folder>`
3. Install dependencies: `pip install -r requirements.txt`

## Configuration
1. Create a `.env` file in the project directory.
2. Add the following environment variables to the `.env` file:
```
SECRET_KEY=<your_stripe_secret_key>
PAYMENTS_PORT=<port_number>
DEBUG=<true_or_false>
PAYMENT_URL=<your_payment_url>
PROCESS_BOOKING_URL=<your_process_booking_url>
FRONTEND_URL=<your_frontend_url>
```
Replace `<your_stripe_secret_key>`, `<port_number>`, `<your_payment_url>`, `<your_process_booking_url>`, and `<your_frontend_url>` with your actual values.

## Usage
1. Run the Flask application: `python server.py`
2. The server will be running at `http://localhost:<PORT>` by default.

## Endpoints

### `POST /create-checkout-session`
- **Description:** Endpoint for creating a checkout session.
- **Parameters:**
- `propertyName`: Name of the property.
- `pricePerNight`: Price per night in cents.
- `currency`: Currency of the payment.
- `duration`: Duration of stay.
- `email`: Email of the guest.
- `guestId`: ID of the guest.
- `listingId`: ID of the listing.
- `startDate`: Start date of the booking.
- `endDate`: End date of the booking.
- `hostId`: ID of the host.
- **Response:**
- `checkout_url`: URL for the checkout session.
- `session_id`: ID of the checkout session.
- `status`: HTTP status code (303).

### `GET /success`
- **Description:** Endpoint for indicating successful payment.
- **Response:**
- `status`: Status of the payment (success).
- `message`: Message indicating payment success.

### `GET /canceled`
- **Description:** Endpoint for indicating canceled payment.
- **Response:**
- `status`: Status of the payment (canceled).
- `message`: Message indicating payment cancellation.

## Building and Deploying with Docker

### Building the Docker Image
To build the Docker image, execute the following command in the project directory:
```bash
docker build -t <dockerid>/server:3.0 --build-arg SECRET_KEY=<your_stripe_secret_key> --build-arg PAYMENTS_PORT=<port_number> --build-arg DEBUG=<true_or_false> --build-arg PAYMENT_URL=<your_payment_url> .
```
Replace `<your_stripe_secret_key>`, `<port_number>`, `<your_payment_url>`, and `<true_or_false>` with your actual values.

### Running the Docker Container
After building the Docker image, you can run the container using the following command:
```bash
docker run -p <host_port>:<container_port> <dockerid>/server:3.0
```
Replace `<host_port>` and `<container_port>` with the desired port mappings.

The Flask application will be accessible at `http://localhost:<host_port>`.

