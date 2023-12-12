# Import necessary modules
import logging  # Module for logging
import os  # Module for interacting with the operating system
import sys  # Module for interacting with the Python interpreter

from dotenv import load_dotenv  # Module for loading environment variables from a file
from fastapi import FastAPI, HTTPException  # FastAPI framework for building APIs
from pydantic import BaseModel  # Base class for data models in Pydantic
import uvicorn  # ASGI server for running FastAPI applications

from fact.lib import factorial  # Import the factorial function from a custom module

# Load environment variables from .env file
load_dotenv()

# Create a FastAPI app instance
app = FastAPI()

# Set up logging to both file and console
log_file = "/tmp/file_search_app.log"
logging.basicConfig(
    handlers=[
        logging.FileHandler(log_file),  # Log handler for writing logs to a file
        logging.StreamHandler(sys.stdout),  # Log handler for displaying logs on the console
    ],
    level=logging.DEBUG,  # Set logging level to DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
)


class FactorialRequest(BaseModel):
    """Pydantic model for validating the request to the /factorial endpoint.

    Attributes:
        number (int): The input number for calculating the factorial.
    """


@app.get("/factorial/{number}")
async def get_factorial(number: int):
    """
    FastAPI endpoint for calculating the factorial of a given number.

    Args:
        number (int): The input number for calculating the factorial.

    Returns:
        dict: Dictionary containing the input number and its factorial.

    Raises:
        HTTPException: If there is an error, such as an invalid input or calculation failure.
    """
    try:
        logging.info(f"Calculating factorial for number: {number}")
        result = factorial(number)
        return {"factorial": result}
    except ValueError as e:
        logging.error(f"Error calculating factorial: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from e  # Address B904


# Entry point when the script is executed directly
if __name__ == "__main__":
    # Get host and port information from environment variables
    host_arg = os.getenv("HOST")
    port_arg = int(os.getenv("PORT"))

    # Configure and run the UVicorn server
    server_config = uvicorn.Config(
        app, host=host_arg, port=port_arg, log_level="debug", reload=True
    )
    server = uvicorn.Server(server_config)

    logging.info(f"UVicorn is starting. Host: {host_arg}, Port: {port_arg}")

    # Run the server and log appropriate messages
    server.run()
    if not server.started:
        logging.fatal("Server failed to start")
        sys.exit(1)
    else:
        logging.info("Server started")
