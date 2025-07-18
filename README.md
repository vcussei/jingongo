# Jingongo Framework SDK

[![PyPI version](https://img.shields.io/pypi/v/jingongo-framework.svg)](https://pypi.org/project/jingongo-framework/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Versions](https://img.shields.io/pypi/pyversions/jingongo-framework.svg)](https://pypi.org/project/jingongo-framework)

Welcome to the Jingongo SDK! This Python library is your gateway to the **Jingongo Digital Twin Platform**. It provides the essential tools to programmatically convert your simulation models into industry-standard Functional Mock-up Units (FMUs) and manage them in the cloud.

This SDK handles the complex work of packaging your local code, uploading it securely, and communicating with our powerful cloud-based conversion engine. It is the perfect companion to the user-friendly web platform at **[www.jingongo.com](https://www.jingongo.com)**.

---

## The Jingongo Vision: A Complete Digital Twin Ecosystem

While the current SDK focuses on robust FMU conversion, Jingongo is being built as a comprehensive platform for the entire digital twin lifecycle. Our goal is to empower engineers and scientists with a seamless workflow from concept to real-time operation.

#### ✨ **Current Features (Ready Today)**

*   **Simple Conversion:** Turn local Python or C models into FMUs with a single command.
*   **Cloud-Powered Engine:** Offload the heavy lifting of compilation and packaging to a scalable cloud service.
*   **Model Management:** Programmatically list your cloud models and download completed FMUs.
*   **Flexible Configuration:** Define your model's parameters, inputs, and outputs using a simple `.jingongo.yml` file.
*   **Secure by Design:** All communication is authenticated using secure API keys.

#### 🛠️ **Future Features (Under Active Development)**

*   **Integrated Testing:** Test your models against various scenarios directly within the Jingongo cloud environment.
*   **Advanced Version Control:** Manage versions of any model format (FMU, Simulink, etc.) with a clear history and rollback capabilities.
*   **Live Data Connection:** Easily connect your digital twins to real-time data streams from physical assets for performance monitoring and optimization.
*   **Rapid Prototyping:** Assemble complex digital twins from a library of pre-built "LEGO block" models to accelerate development.
*   **AI-Powered Model Creation:** Use our platform to generate powerful simulation models directly from high-level requirements.

---

## 🚀 Getting Started: Your First FMU in 5 Minutes

This guide will walk you through installing the SDK and converting your first model.

### Step 1: Install the SDK

Open your terminal and install the framework from PyPI.

pip install jingongo-framework

Step 2: Get Your API Key
The SDK requires a secure API Key.
Sign up or log in to the Jingongo web portal at www.jingongo.com.
Navigate to your user dashboard or settings page.
Click the "Generate New API Key" button.
Copy the generated key immediately. Save it somewhere safe, like a password manager. This key is permanent and will not be shown again.
Step 3: Set Up Your Environment
For the SDK to authenticate, you must set your new API key as an environment variable.
In your terminal, run the appropriate command for your system:

# On Windows Command Prompt (CMD)
set JINGONGO_API_KEY="your_permanent_api_key_here"

# On macOS, Linux, or PowerShell
export JINGONGO_API_KEY="your_permanent_api_key_here"

You will need to do this for every new terminal session, or add it to your system's profile script.
Step 4: Run Your First Conversion
Now you are ready to use the SDK!
1. Get the Example Files: To run our pre-made examples, you'll need to clone this repository.

git clone https://github.com/vcussei/jingongo.git
cd jingongo

2. Run the Conversion Script: Navigate to the examples directory and run the Python conversion script.

# From the project root directory:
python -m examples.02_convert_python_model

# Or, if you are inside the examples/ directory:
# python 02_convert_python_model.py

You will see real-time status updates from the cloud engine in your console. Once it's complete, you've successfully used the entire Jingongo pipeline!

📚 SDK Usage and Examples
The examples/ folder in this repository is the best place to learn. Each script is small, focused, and demonstrates a core feature.
00_check_health.py: A simple script to verify your API key and connection to the backend.
01_generate_api_key.py: An alternative, programmatic way to generate an API key.
02_convert_python_model.py: The primary example for converting a Python model.
03_convert_c_model.py: Shows how to convert a C-based model.
04_list_models.py: Demonstrates how to list all your models in the cloud.
05_download_model.py: Shows how to download a specific FMU using its Job ID.
06_get_login_url.py & 07_get_signup_url.py: Simple helpers for getting web portal URLs.
Example Command:

To download a model after finding its ID with the list_models script
python -m examples.05_download_model YOUR_JOB_ID_HERE


---

## 🏗️ Project Structure for Contributors

Interested in contributing? This repository follows standard Python packaging best practices.

*   **`pyproject.toml`**: The heart of the project. Defines all metadata and dependencies.
*   **`src/jingongo/`**: The actual Python package source code. This is what gets installed via `pip`.
*   **`examples/`**: Standalone scripts that demonstrate how to use the library. Not included in the `pip` installation.
*   **`tests/`**: The automated test suite (`pytest`) to ensure code quality and prevent bugs.

### How to Contribute

1.  **Clone the repository:** `git clone https://github.com/vcussei/jingongo.git && cd jingongo`
2.  **Create a virtual environment:** `python -m venv venv && source venv/bin/activate`
3.  **Install in editable mode with test dependencies:** `pip install -e .[test]`
4.  **Run the tests:** `pytest`

If all tests pass, you are ready to start developing!

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.