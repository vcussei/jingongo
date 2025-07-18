# examples/01_generate_api_key.py
import os
import sys
import logging

# Add the src directory to the Python path so we can import the jingongo module
# This is necessary for running examples locally without installing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jingongo import Jingongo

# --- Configuration ---
# Your backend API's public URL
JINGONGO_API_BASE_URL = "https://jingongo-backend-api-723715926581.us-central1.run.app"

def main():
    """
    Demonstrates how to generate a long-lived API key.
    
    Prerequisite:
    You must set the TEMPORARY_USER_TOKEN environment variable. You can get
    this token by logging into the Jingongo web portal.
    """
    print("--- Example: Generating a long-lived API key ---")
    
    # Enable logging to see detailed output from the SDK
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the short-lived token from an environment variable
    id_token = os.environ.get("TEMPORARY_USER_TOKEN")
    if not id_token:
        print("\n❌ Error: Please set the TEMPORARY_USER_TOKEN environment variable.")
        print("   You can get this token after logging into the Jingongo web portal.")
        return

    try:
        # This method is static, so we don't need to initialize the class
        new_key = Jingongo.generate_api_key_from_token(JINGONGO_API_BASE_URL, id_token)
        
        print("\n" + "=" * 60)
        print("🔑 Your new long-lived API key has been generated successfully:\n")
        print(new_key)
        print("\n" + "=" * 60)
        print("\n💡 For all other examples, set this key as the JINGONGO_API_KEY")
        print("   environment variable before running them.")

    except Exception as e:
        print(f"\n❌ Failed to generate API key: {e}")

if __name__ == "__main__":
    main()