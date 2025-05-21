from flask import Flask, request, jsonify
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Enable logging for better error tracking
logging.basicConfig(level=logging.DEBUG)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        # Step 1: Log that we received the request
        app.logger.debug("Received a request to /receive_data")

        # Step 2: Try to access and parse the JSON data
        received_data = request.get_json()

        # Step 3: Check if JSON data was parsed correctly
        if received_data is None:
            raise ValueError("No JSON data provided or invalid format")

        # Step 4: Log the received data
        app.logger.debug(f"Received data: {received_data}")

        # Step 5: Return a success message with the received data
        return jsonify({
            "message": "Data received successfully",
            "received_data": received_data
        }), 200

    except Exception as e:
        # Log the error details and return a 500 status code
        app.logger.error(f"Error in /receive_data: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5002)
