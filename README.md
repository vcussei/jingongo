# jingongo

Jingongo: The Open Platform for Digital Twin Co-simulation
🚀 Welcome to Jingongo!
Jingongo is an innovative open-source platform designed to democratize the creation, simulation, and deployment of digital twins for complex industrial systems, with a particular focus on power substations. We empower engineers and model developers to build, test, and integrate their component models (relays, transformers, circuit breakers, etc.) using familiar programming languages (C, Python) and leverage the power of cloud-native co-simulation.

Our mission is to provide a seamless experience for developing high-fidelity digital twins, enabling real-time monitoring, predictive analysis, and system validation against live or static data.

✨ Key Features
FMU-Centric Design: Leverage the Functional Mock-up Interface (FMI) standard for model exchange, ensuring interoperability with a wide range of simulation tools.

"Bring Your Own Model": Develop your digital twin components in C or Python using the intuitive Jingongo framework.

Automated FMU Conversion: Push your code to GitHub, and our cloud backend automatically converts it into a standardized FMU, ready for simulation.

Cloud-Native Co-simulation: Run complex substation simulations by connecting multiple FMUs in a scalable, isolated, and high-performance cloud environment.

Real-time & Static Simulation: Test your digital twins with predefined static data or integrate them with live data streams from physical facilities.

Secure Model Hosting: Deploy and host your validated digital twin setups on our platform for repeated use and sharing.

Developer-Friendly SDK: A local Python SDK (jingongo-framework) to easily interact with the cloud platform for conversion, testing, and simulation initiation.

Open Source Community: Contribute your models, enhance the framework, and collaborate with a growing community of digital twin enthusiasts.

⚡ Getting Started
This guide will help you install the jingongo-framework SDK and convert your first dummy model.

Prerequisites
Python 3.8+

A GitHub account

Access to the Jingongo cloud platform (you'll need an API key/token)

1. Install the Jingongo Framework
pip install jingongo-framework

2. Set Up Your Authentication
You'll need an API base URL and an authentication token from your Jingongo platform account. Set these as environment variables or manage them securely in your application.

export JINGONGO_API_BASE_URL="https://api.jingongo.com/v1" # Replace with your actual API Gateway URL
export JINGONGO_AUTH_TOKEN="your_super_secret_auth_token" # Replace with your actual token

3. Create Your First Dummy Component
Let's create a simple Python-based "Gain Block" model.

mkdir my-first-gain-block
cd my-first-gain-block

Create a file named model.py inside my-first-gain-block/:

# my-first-gain-block/model.py

def initialize(params):
    """Initializes the model with parameters."""
    return {"state": 0.0, "gain": params.get("gain", 1.0)}

def do_step(current_time, inputs, state):
    """Performs one simulation step."""
    input_val = inputs.get("input_val", 0.0)
    gain = state["gain"]
    output_val = input_val * gain
    
    # Update state if necessary, for this simple model, state doesn't change much
    new_state = state 
    
    return {"outputs": {"output_val": output_val}, "new_state": new_state}

def terminate(state):
    """Cleans up resources if any."""
    print(f"Gain block terminated. Final state: {state}")
    return True

Now, create a .jingongo.yml file in the same directory (my-first-gain-block/) to define its FMI interface:

# my-first-gain-block/.jingongo.yml
model:
  name: MyPythonGainBlock
  version: 1.0.0
  description: A simple gain block model implemented in Python.
  component_type: signal_processing
  fmi_type: CoSimulation # Or ModelExchange if supported by your Jingongo backend
  inputs:
    - name: input_val
      type: Real
  outputs:
    - name: output_val
      type: Real
  parameters:
    - name: gain
      type: Real
      default: 1.0

4. Convert to FMU
Now, use the jingongo-framework SDK to convert your model to an FMU on the cloud.

Create a Python script (e.g., convert_model.py) in your parent directory:

# convert_model.py
import os
from jingongo_framework.jingongo import Jingongo # Assuming jingongo_framework is installed

JINGONGO_API_BASE_URL = os.environ.get("JINGONGO_API_BASE_URL")
JINGONGO_AUTH_TOKEN = os.environ.get("JINGONGO_AUTH_TOKEN")

if not JINGONGO_API_BASE_URL or not JINGONGO_AUTH_TOKEN:
    print("Please set JINGONGO_API_BASE_URL and JINGONGO_AUTH_TOKEN environment variables.")
    exit(1)

jingongo_client = Jingongo(JINGONGO_API_BASE_URL, JINGONGO_AUTH_TOKEN)

project_path = "./my-first-gain-block"

try:
    conversion_job = jingongo_client.convert_to_fmu(
        project_path=project_path,
        model_name="MyPythonGainBlock",
        version="1.0.0",
        description="A simple gain block model in Python",
        component_type="signal_processing",
        input_variables={"input_val": "Real"},
        output_variables={"output_val": "Real"},
        parameters={"gain": 2.5},
        wait_for_completion=True # Wait for the cloud conversion to finish
    )
    print("\nFMU Conversion Job Details:")
    print(json.dumps(conversion_job, indent=2))

    if conversion_job.get("status") == "COMPLETED":
        fmu_id = conversion_job.get("fmu_id")
        print(f"\nFMU successfully created with ID: {fmu_id}")
        
        # You can now download it
        downloaded_path = jingongo_client.download_fmu(fmu_id, download_path="./downloads")
        print(f"FMU downloaded to: {downloaded_path}")

        # Or test it
        test_results = jingongo_client.test_fmu(fmu_id, wait_for_completion=True)
        print("\nFMU Test Results:")
        print(json.dumps(test_results, indent=2))

except Exception as e:
    print(f"An error occurred: {e}")


Run the script:

python convert_model.py

This will trigger the cloud conversion process. Once completed, your FMU will be hosted on Jingongo, ready for simulation!

🌐 Core Concepts
Jingongo builds upon the following principles:

Functional Mock-up Interface (FMI): An open standard for exchanging dynamic models between simulation tools. Your C/Python models are converted into FMUs, which are self-contained, executable units.

Co-simulation: Running multiple FMUs simultaneously, exchanging data at discrete communication points to simulate complex, interconnected systems (like a substation with relays, transformers, and circuit breakers).

Cloud-Native Architecture: Leveraging Google Cloud services (Cloud Run, GKE, Pub/Sub, Cloud Storage, Memorystore for Redis) to provide a scalable, resilient, and high-performance platform for model management and simulation execution.

🏗️ Architecture Overview
The Jingongo platform is composed of several decoupled microservices communicating asynchronously:

Frontend (Next.js): User interface for model design, simulation setup, and real-time visualization.

API Gateway: Secure entry point for all client requests.

Model & FMU Management Service: Handles model source code and FMU binary storage, metadata, and versioning.

FMU Conversion Service (Jingongo Backend): Securely converts user-uploaded C/Python code into FMUs within isolated containers.

Simulation Orchestration Service: Receives simulation requests, prepares the co-simulation setup, and dispatches jobs.

FMU Co-simulation Worker Pool: Scalable pool of containers (GKE/Cloud Run) that execute the actual FMU co-simulations.

Real-time Data Ingestion: For live simulations, securely ingests data from user facilities.

Real-time Push Service: Streams simulation results and alarms back to the frontend.

Data Stores: Cloud Storage (FMUs, source code), Cloud SQL/Firestore (metadata), Memorystore for Redis (cache), BigQuery (historical data).

This modular design ensures high availability, scalability, and maintainability.

👋 Contributing
We welcome contributions from the community! Whether you want to:

Develop new component models (e.g., a specific type of relay, a new load model).

Improve the Jingongo framework (add features, enhance performance).

Contribute to the platform's documentation.

Report bugs or suggest features.

Please read our CONTRIBUTING.md for detailed guidelines. We adhere to a CODE_OF_CONDUCT.md to ensure a welcoming and inclusive environment.

Model Submission
You can submit your own digital twin component models by creating a Pull Request to the models/community/ directory in this repository. Our automated CI/CD pipeline will build and test your FMU, and if successful, it will be made available on the Jingongo platform for others to use.

🛡️ Security
Security is paramount. We follow best practices for secure development, data handling, and isolated execution of user-provided code. Please refer to our SECURITY.md for details on how to report vulnerabilities.

📄 License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

💬 Support & Community
Discord: Join our Discord server for real-time discussions and support.

GitHub Issues: For bug reports and feature requests, please use the GitHub Issues section.
