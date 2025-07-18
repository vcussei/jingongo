# examples/04_list_models.py
import os
import sys
import logging

# Add the src directory to the Python path to allow importing the library locally
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jingongo import Jingongo
from jingongo.jingongo import JingongoAPIError # Import custom exceptions

# --- Configuration ---
JINGONGO_API_BASE_URL = os.environ.get("JINGONGO_API_BASE_URL", "https://jingongo-backend-api-723715926581.us-central1.run.app")
JINGONGO_API_KEY = os.environ.get("JINGONGO_API_KEY")

def main():
    """
    Demonstrates how to list all recent model conversion jobs for your account.

    Prerequisite:
    You must set the JINGONGO_API_KEY environment variable.
    """
    print("--- Example: Listing Your Recent Models ---")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if not JINGONGO_API_KEY:
        print("\n❌ Error: JINGONGO_API_KEY environment variable not set.")
        return

    try:
        # We don't need verbose logging for this example, the table is the focus.
        client = Jingongo(JINGONGO_API_BASE_URL, JINGONGO_API_KEY)

        print("\n🔎 Fetching your recent models from the cloud...")
        models = client.list_models(limit=25)

        if not models:
            print("\nNo models found. You can create some by running the conversion examples.")
            return

        print("\n--- Your Recent Models ---")
        print(f"{'Job ID':<40} | {'Model Name':<30} | {'Version':<10} | {'Status':<12}")
        print("-" * 100)

        for model in models:
            print(
                f"{model.get('job_id', 'N/A'):<40} | "
                f"{model.get('model_name', 'N/A'):<30} | "
                f"{model.get('version', 'N/A'):<10} | "
                f"{model.get('status', 'N/A'):<12}"
            )
        
        print("\n💡 Tip: Copy the 'Job ID' of a 'COMPLETED' model to use in the download example.")

    except JingongoAPIError as e:
        print(f"\n❌ An error occurred while fetching models: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()