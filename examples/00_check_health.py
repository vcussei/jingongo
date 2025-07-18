# examples/00_check_health.py
import os
import sys
import json
import logging

# Add the src directory to the Python path to allow importing the library locally
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jingongo import Jingongo
from jingongo.jingongo import JingongoAuthError, JingongoAPIError # Import custom exceptions

# --- Configuration ---
# It's best practice to load sensitive data from environment variables
# instead of hardcoding them in the script.
JINGONGO_API_BASE_URL = os.environ.get("JINGONGO_API_BASE_URL", "https://jingongo-backend-api-723715926581.us-central1.run.app")
JINGONGO_API_KEY = os.environ.get("JINGONGO_API_KEY")

def main():
    """
    Demonstrates how to check the health and connectivity of the Jingongo API.
    This is a great first step to ensure your credentials and network are set up correctly.

    Prerequisites:
    - You must set the JINGONGO_API_KEY environment variable.
    - The JINGONGO_API_BASE_URL can also be set as an environment variable,
      but a default is provided.
    """
    print("--- Example: Checking Jingongo API Health ---")
    
    # Enable logging to see detailed output from the SDK
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if not JINGONGO_API_KEY:
        print("\n❌ Error: JINGONGO_API_KEY environment variable not set.")
        print("   Please set your API key before running this example.")
        return

    try:
        # Initialize the client. The constructor will automatically verify the API key.
        # We set verbose=True to ensure the SDK's internal log messages are printed.
        client = Jingongo(api_base_url=JINGONGO_API_BASE_URL, api_key=JINGONGO_API_KEY, verbose=True)

        # If initialization was successful, the key is valid. Now check health.
        print("\nAPI Key is valid. Now checking service health...")
        health_status = client.health_check()

        print("\n" + "="*50)
        print("✅ Health Check Successful!")
        print("   The Jingongo API is running and reachable.")
        print("\nAPI Response:")
        print(json.dumps(health_status, indent=2))
        print("="*50)

    except JingongoAuthError as e:
        # This catches errors specifically related to a bad API key
        print(f"\n❌ Authentication Failed: {e}")
        print("   Please ensure your JINGONGO_API_KEY is correct and has not been revoked.")

    except JingongoAPIError as e:
        # This catches other API-related errors, like the service being down
        print(f"\n❌ API Error: {e}")
        print("   The Jingongo API might be temporarily unavailable or there could be a network issue.")

    except Exception as e:
        # A general catch-all for any other unexpected errors
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()