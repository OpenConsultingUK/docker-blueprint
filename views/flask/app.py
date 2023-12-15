# Import necessary modules
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Construct the base URL for FastAPI from environment variables
fastapi_base_url = f"http://{os.getenv('FASTHOST')}:{os.getenv('FASTPORT')}"


# Define a route for the homepage ("/") that handles both GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles requests to the homepage.

    If the request method is POST, it extracts the number from the form data,
    makes a request to the FastAPI factorial endpoint, and displays the result.

    Returns:
        Rendered template with the result.
    """
    # Initialize result variable to None
    result = None

    # Check if the request method is POST
    if request.method == "POST":
        try:
            # Extract the number from the form data and convert it to an integer
            number = int(request.form.get("number"))

            # Make a request to the FastAPI factorial endpoint
            factorial_response = requests.get(f"{fastapi_base_url}/factorial/{number}")

            # Check the response status code
            if factorial_response.status_code == 200:
                # Parse the JSON response and get the factorial result
                result = factorial_response.json()["factorial"]
            else:
                # Handle error response
                result = f"Error: {factorial_response.text}"
        except ValueError:
            # Handle invalid input (non-integer)
            result = "Please enter a valid number."

    # Render the homepage template with the result
    return render_template("index.html", result=result)


# Entry point to start the Flask app
if __name__ == "__main__":
    # Get host and port information from environment variables
    host_arg = os.getenv("HOST")
    port_arg = int(os.getenv("PORT"))

    # Run the Flask app with debug mode enabled
    app.run(debug=True, host=host_arg, port=port_arg)
