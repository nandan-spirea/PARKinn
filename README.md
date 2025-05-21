# NP_extraction

This Flask-based API uses the Platerecognizer API(https://www.platerecognizer.com/) to detect and recognize license plates from images. It accepts image files via a POST request and returns the best-matching license plate.

## Requirements
- Python 3.6 or higher
- `Flask` for building the web API.
- `requests` for making HTTP requests to the Platerecognizer API.

Install dependencies using:
pip install Flask requests scikit-learn

## Configuration
You can modify the following variables in the script:
- `regions`: List of region codes where the API should look for license plates (e.g., `'mx'` for Mexico, `'us-ca'` for California, USA).
- `api_token`: Your Platerecognizer API token. Obtain this from your account at the Platerecognizer website.
- `desired_score_threshold`: Minimum confidence score (from the API) required for a license plate to be considered valid.
- `max_attempts`: Maximum number of recognition attempts before the API stops trying.

## API Endpoints
 `/extract_plate` (POST)
This endpoint accepts an image file and returns the detected license plate.

Request:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameter:
  - `image` (required): The image file containing the license plate.

Response:
- On success (`200 OK`):
  json
  {
      "license_plate": "ABC1234"
  }
  
- On error (`400 Bad Request`):
  json
  {
      "error": "No image file provided"
  }
  
- If no valid plate is found (`404 Not Found`):
  json
  {
      "error": "No plate detected with a valid score."
  }

## Usage
1. Ensure your API token is set in the script.
2. Run the Flask app:
python app.py
The API will start on `http://127.0.0.1:5002` by default.
3. To use the API, send a POST request to `http://127.0.0.1:5002/extract_plate` with an image file. 


