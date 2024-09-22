from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import mimetypes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the BFHL API. Use /bfhl endpoint for operations."}), 200

@app.route('/bfhl', methods=['POST', 'GET'])
def bfhl():
    if request.method == 'POST':
        try:
            data = request.json.get('data', [])
            file_b64 = request.json.get('file_b64', '')
            numbers = [item for item in data if item.isdigit()]
            alphabets = [item for item in data if item.isalpha()]
            highest_lowercase = max([item for item in alphabets if item.islower()], default='')
            file_valid = False
            file_mime_type = None
            file_size_kb = None
            if file_b64:
                try:
                    file_data = base64.b64decode(file_b64)
                    file_valid = True
                    file_mime_type = mimetypes.guess_type('file')[0]
                    file_size_kb = len(file_data) / 1024
                except:
                    pass
            response = {
                "is_success": True,
                "user_id": "your_full_name_ddmmyyyy",  # Replace with your details
                "email": "your.email@example.com",     # Replace with your details
                "roll_number": "your_roll_number",     # Replace with your details
                "numbers": numbers,
                "alphabets": alphabets,
                "highest_lowercase_alphabet": [highest_lowercase] if highest_lowercase else [],
                "file_valid": file_valid,
                "file_mime_type": file_mime_type,
                "file_size_kb": file_size_kb
            }
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"is_success": False, "error": str(e)}), 400
    elif request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)