# examples/02_convert_python_model.py
import os
import sys
import json
import logging
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jingongo import Jingongo

# --- Configuration ---
JINGONGO_API_BASE_URL = os.environ.get("JINGONGO_API_BASE_URL")
MODEL_NAME = "your_model_name"  # Replace with your desired model name

def main():
    """
    Demonstrates converting a local Python-based model into an FMU.
    
    Prerequisite:
    You must set the JINGONGO_API_KEY environment variable. You can generate one
    by running the 01_generate_api_key.py example.
    """
    print("--- Example: Converting a Python model to an FMU ---")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    api_key = os.environ.get("JINGONGO_API_KEY")
    if not api_key:
        print("\n❌ Error: Please set the JINGONGO_API_KEY environment variable.")
        return

    try:
        # Initialize the client with the verbose flag to see detailed logs
        client = Jingongo(JINGONGO_API_BASE_URL, api_key, verbose=True)

        # Define the path to the sample model, relative to this script
        py_model_path = Path(__file__).parent / "example_models" / "python_identity_block_model"
        
        if not py_model_path.exists():
            raise FileNotFoundError(f"❌ Model directory not found: {py_model_path.resolve()}")

        print(f"\n🚀 Starting conversion for model at: {py_model_path}")
        
        # Call the conversion method.
        # Most parameters will be read from the model's .jingongo.yml file.
        py_job = client.convert_to_fmu(
            project_path=py_model_path,
            model_name=MODEL_NAME,  # Replace with your model name
            language="python"
        )
        
        print("\n✅ Python Conversion Job Finished!")
        print(json.dumps(py_job, indent=2))

    except Exception as e:
        print(f"\n❌ An error occurred during conversion: {e}")

if __name__ == "__main__":
    main()