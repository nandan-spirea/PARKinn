from flask import Flask, request, jsonify
import requests
from sklearn.metrics import accuracy_score
import os
import logging

app = Flask(__name__)

regions = ["mx", "us-ca"]
api_token = 'f8c913773f798cf9ee11736c34e8135d18f1ca8f'
desired_score_threshold = 0.9
max_attempts = 2
api_2_url = "http://127.0.0.1:5002/receive_data" #can change the receiving API based on the requirement

def get_plate_recognition_score(image_data):
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        data=dict(regions=regions),
        files=dict(upload=image_data),
        headers={'Authorization': f'Token {api_token}'}
    )
    return response.json()

@app.route('/extract_plate', methods=['POST'])
def extract_plate():
    # Check if the request contains a file
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    
    attempts = 0
    best_score = 0.0
    best_plate = None
    predicted_plates = []

    while attempts < max_attempts:
        attempts += 1
        # Use the uploaded file directly instead of saving it
        response_data = get_plate_recognition_score(image_file)

        if 'results' in response_data and len(response_data['results']) > 0:
            plate = response_data['results'][0].get('plate', 'Unknown').upper()
            current_score = response_data['results'][0].get('score', 0)
            
            predicted_plates.append(plate)

            if current_score > best_score:
                best_score = current_score
                best_plate = plate

            if current_score >= desired_score_threshold:
                break
        else:
            print(response_data)


    if best_plate:
        plate_data = {
            "license_plate": best_plate,
            "confidence_score": best_score
        }

        # Sending the plate data to the second API
        try:
            response_to_api_2 = requests.post(api_2_url, json=plate_data)
            if response_to_api_2.status_code == 200:
                return jsonify({
                    "message": "License plate detected and sent to the second API successfully!",
                    "license_plate": best_plate
                }), 200
            else:
                return jsonify({
                    "message": "License plate detected but failed to send to the second API.",
                    "license_plate": best_plate,
                    "error": response_to_api_2.text
                }), response_to_api_2.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending data to API 2: {e}")
            return jsonify({
                "message": "License plate detected but failed to send to the second API due to a connection issue.",
                "license_plate": best_plate,
                "error": str(e)
            }), 500
    else:
        return jsonify({"error": "No plate detected with a valid score."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



