from flask import Flask, request, jsonify  # Flask lets us create the server
from flask_cors import CORS               # CORS allows the website to talk to the server
import re

app = Flask(__name__)  # Create the app
CORS(app)  # Allow frontend to communicate with backend

# Function to check password strength
def check_password_strength(password):
    # Define rules for a good password
    length_error = len(password) < 8  # At least 8 characters
    digit_error = re.search(r"\d", password) is None  # At least one number
    uppercase_error = re.search(r"[A-Z]", password) is None  # At least one uppercase letter
    lowercase_error = re.search(r"[a-z]", password) is None  # At least one lowercase letter
    special_char_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None  # At least one special character

    # Count errors and calculate strength
    errors = [length_error, digit_error, uppercase_error, lowercase_error, special_char_error]
    score = 5 - sum(errors)  # Score ranges from 0 (bad) to 5 (strong)

    # Decide the strength
    if score == 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return {"strength": strength, "score": score}

# Add a simple route for the home page
@app.route('/')
def home():
    return "Welcome to the Password Strength Checker!"

# Add a route to check password strength
@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.get_json()  # Get the password from the request
    password = data.get("password", "")  # If no password, use an empty string

    if not password:
        return jsonify({"error": "Password is required"}), 400

    result = check_password_strength(password)  # Check the password
    return jsonify(result)  # Send back the result

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
