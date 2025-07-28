# examples/03_convert_c_model.py
import os
import sys
import json
import logging
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from jingongo import Jingongo

# --- Configuration ---
JINGONGO_API_BASE_URL = os.environ.get('JINGONGO_API_BASE_URL')

def main():
    """
    Demonstrates converting a local C-based model into an FMU.
    
    Prerequisite:
    You must set the JINGONGO_API_KEY environment variable.
    """
    print("--- Example: Converting a C model to an FMU ---")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    api_key = os.environ.get("JINGONGO_API_KEY")
    if not api_key:
        print("\n❌ Error: Please set the JINGONGO_API_KEY environment variable.")
        return

    try:
        client = Jingongo(JINGONGO_API_BASE_URL, api_key, verbose=True)

        c_model_path = Path(__file__).parent / "example_models" / "c_identity_block_model"
        
        if not c_model_path.exists():
            raise FileNotFoundError(f"❌ Model directory not found: {c_model_path.resolve()}")

        print(f"\n🚀 Starting conversion for model at: {c_model_path}")
        
        c_job = client.convert_to_fmu(
            project_path=c_model_path,
            model_name="YourCModelName",  # Replace with your model name
            language="c"
        )
        
        print("\n✅ C Conversion Job Finished!")
        print(json.dumps(c_job, indent=2))

    except Exception as e:
        print(f"\n❌ An error occurred during conversion: {e}")

if __name__ == "__main__":
    main()