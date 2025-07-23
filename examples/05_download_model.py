# examples/05_download_model.py
import os
import sys
import argparse  # Import the argparse library
import logging
from pathlib import Path

# Add the src directory to the Python path to allow importing the library locally
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jingongo import Jingongo
from jingongo.jingongo import JingongoAPIError

# --- Configuration ---
JINGONGO_API_BASE_URL = os.environ.get("JINGONGO_API_BASE_URL")
JINGONGO_API_KEY = os.environ.get("JINGONGO_API_KEY")


def main(job_id_to_download: str):
    """
    Connects to the Jingongo API and downloads a specific FMU.

    Args:
        job_id_to_download (str): The Job ID of the completed FMU to download.
    """
    print(f"--- Example: Downloading an FMU for Job ID: {job_id_to_download} ---")

    if not JINGONGO_API_KEY:
        print("\n❌ Error: JINGONGO_API_KEY environment variable not set.")
        return

    try:
        # Set verbose=True to see the download progress bar and SDK messages.
        client = Jingongo(JINGONGO_API_BASE_URL, JINGONGO_API_KEY, verbose=True)

        print(f"\n📦 Attempting to download FMU...")
        
        # The download directory will be created if it doesn't exist.
        download_directory = Path("./fmu_downloads")
        
        fmu_path = client.download_fmu(job_id_to_download, download_dir=download_directory)

        print("\n" + "="*50)
        print("✅ FMU downloaded successfully!")
        print(f"   Saved to: {fmu_path.resolve()}")
        print("="*50)

    except JingongoAPIError as e:
        print(f"\n❌ Download failed: {e}")
        print("   Please ensure the Job ID is correct and the job status is 'COMPLETED'.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- This is the new section that handles command-line arguments ---

    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Download a specific, completed FMU from the Jingongo platform.",
        epilog="Example: python 05_download_model.py f4e2abdb-21c8-4279-9a2a-716daeec23c0"
    )

    # 2. Define the required 'job_id' argument
    parser.add_argument(
        "job_id",  # The name of the argument
        type=str,
        help="The Job ID of the completed FMU you want to download."
    )
    
    # 3. Parse the arguments provided by the user
    args = parser.parse_args()

    # 4. Enable logging and call the main function with the parsed argument
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main(job_id_to_download=args.job_id)