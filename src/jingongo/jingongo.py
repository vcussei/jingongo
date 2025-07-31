# src/jingongo_framework/jingongo.py

import os
import json
import requests
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
import shutil
import tempfile
from tqdm import tqdm

# Set up a logger for the library.
# Users of the SDK can configure this logger to control output.
_logger = logging.getLogger(__name__)

# --- Custom Exceptions for Clearer Error Handling ---

class JingongoAuthError(Exception):
    """Raised for authentication failures (e.g., invalid API key)."""
    pass

class JingongoAPIError(Exception):
    """Raised for general API errors (e.g., bad requests, server errors)."""
    pass

class JingongoConversionError(Exception):
    """Raised when an FMU conversion job fails on the backend."""
    pass


class Jingongo:
    """The Jingongo Digital Twin Framework SDK."""

    def __init__(self, api_base_url: str, api_key: str, verbose: bool = False):
        """
        Initializes the Jingongo SDK client.

        Args:
            api_base_url (str): The base URL of your Jingongo cloud API.
            api_key (str): The long-lived API key for programmatic access.
            verbose (bool): If True, enables detailed logging to the console.
        """
        if not api_base_url or not api_key:
            raise ValueError("API base URL and API key must be provided.")

        if verbose:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.api_base_url = api_base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        })
        self.user_id = None

        _logger.info("Initializing Jingongo client and verifying API key...")
        self._verify_api_key()
        _logger.info("--- Jingongo Client Initialized Successfully ---")

    def _verify_api_key(self):
        """Validates the API key against the /auth/me endpoint."""
        try:
            whoami_response = self._make_request("GET", "/auth/me")
            self.user_id = whoami_response.get("user_id")
            if not self.user_id:
                raise JingongoAPIError("API key is valid, but the backend did not return a user ID.")
            _logger.info(f"API Key successfully validated for user: {self.user_id}")
        except JingongoAuthError:
            _logger.error("API Key authentication failed.")
            raise

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Helper method to make authenticated API requests."""
        url = f"{self.api_base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise JingongoAuthError("Authentication failed: The provided API key is invalid or has been revoked.") from e
            _logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise JingongoAPIError(f"API request to {url} failed: {e.response.status_code} - {e.response.text}") from e
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            _logger.error(f"Error during request to {url}: {str(e)}")
            raise JingongoAPIError(f"Failed to communicate with the Jingongo API at {url}.") from e

    def list_models(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieves a list of the most recent FMU conversion jobs for the user.
        
        Returns:
            A list of dictionaries, each representing a conversion job.
        
        Raises:
            JingongoAPIError: If the API request fails.
        """
        _logger.info(f"Fetching the latest {limit} models from the cloud...")
        return self._make_request("GET", f"/models?limit={limit}")

    @staticmethod
    def generate_api_key_from_token(api_base_url: str, id_token: str) -> str:
        """
        Uses a short-lived user ID token to generate a new long-lived API key.
        """
        if not api_base_url or not id_token:
            raise ValueError("api_base_url and id_token must be provided.")
        
        api_key_url = f"{api_base_url.rstrip('/')}/auth/api-key"
        headers = {"Authorization": f"Bearer {id_token}", "Content-Type": "application/json"}
        
        _logger.info("Requesting a new long-lived API key from the backend...")
        try:
            response = requests.post(api_key_url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            new_api_key = response_data.get("api_key")
            if not new_api_key:
                raise JingongoAPIError(f"Backend did not return an API key. Response: {response_data}")
            _logger.info("SUCCESS! New API Key generated.")
            return new_api_key
        except requests.exceptions.HTTPError as e:
            _logger.error(f"API key generation failed. Status: {e.response.status_code}, Response: {e.response.text}")
            raise JingongoAPIError(f"API key generation failed: {e.response.status_code}") from e

    # --- Helper methods refactored from convert_to_fmu ---

    def _prepare_and_upload_source(self, project_path: Path, model_name: str, version: str) -> str:
        """Zips a project directory and uploads it to a signed URL."""
        _logger.info(f"Zipping project at: {project_path}...")
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_name = f"{project_path.name}_{time.time_ns()}"
            zip_path_base = Path(temp_dir) / archive_name
            zip_path = Path(shutil.make_archive(str(zip_path_base), 'zip', project_path))
            
            file_size_bytes = zip_path.stat().st_size
            _logger.info(f"Project zipped to: {zip_path} (Size: {file_size_bytes} bytes)")

            init_payload = {"model_name": model_name, "version": version, "file_size_bytes": file_size_bytes}
            upload_init_response = self._make_request("POST", "/models/upload-init", json=init_payload)
            
            upload_url = upload_init_response.get("upload_url")
            upload_id = upload_init_response.get("upload_id")
            if not upload_url or not upload_id:
                raise JingongoAPIError("Failed to get upload URL or upload ID from server.")

            _logger.info("Uploading zipped project to signed URL...")
            with open(zip_path, 'rb') as f:
                upload_response = requests.put(upload_url, data=f, headers={'Content-Type': 'application/zip'})
                upload_response.raise_for_status()
            _logger.info("Upload complete.")
            return upload_id

    def _poll_for_completion(self, job_id: str, poll_interval: int, model_name: str) -> Dict[str, Any]:
        """Polls the conversion status endpoint until the job is complete or failed."""
        _logger.info("Waiting for cloud conversion to complete...")
        while True:
            status_response = self.get_conversion_status(job_id)
            status = status_response.get("status")
            _logger.info(f"Cloud Conversion status for '{model_name}': {status}")
            if status in ["COMPLETED", "FAILED"]:
                if status == "COMPLETED":
                    _logger.info(f"FMU conversion for '{model_name}' completed successfully!")
                else:
                    error_message = status_response.get('error_message', 'N/A')
                    _logger.error(f"FMU conversion for '{model_name}' FAILED. Details: {error_message}")
                    raise JingongoConversionError(f"FMU cloud conversion failed: {error_message}")
                return status_response
            time.sleep(poll_interval)

    # --- Main Public Methods ---

    def convert_to_fmu(self, project_path: Union[str, Path], wait_for_completion: bool = True, poll_interval: int = 5, **kwargs) -> Dict[str, Any]:
        """
        Converts a local digital twin project into an FMU via the Jingongo cloud service.
        Configuration can be passed as keyword arguments or loaded from a `.jingongo.yml` file in the project path.
        """
        project_path = Path(project_path)
        if not project_path.is_dir():
            raise ValueError(f"Project path '{project_path}' is not a valid directory.")

        config = kwargs.copy()
        config_path = project_path / ".jingongo.yml"
        if config_path.exists():
            _logger.info(f"Found '{config_path.name}', loading configuration from file.")
            import yaml
            with open(config_path, 'r') as f:
                yaml_data = yaml.safe_load(f).get('model', {})
            config.update(yaml_data)

        input_variables = {
            v["name"]: v.get("type", "Real")
            for v in config.get("inputs", [])
        }
        output_variables = {
            v["name"]: v.get("type", "Real")
            for v in config.get("outputs", [])
        }
        parameters = {
            p["name"]: p.get("default", 0.0)
            for p in config.get("parameters", [])
        }

        # Build the final payload for the API
        payload = {
            "model_name": config.get("model_name", "UntitledModel"),
            "version": config.get("version", "1.0.0"),
            "description": config.get("description", ""),
            "language": config.get("language", "python"),
            "component_type": config.get("component_type", "unknown"),
            "fmi_type": config.get("fmi_type", "CoSimulation"),
            # Add the correctly formatted variables
            "input_variables": input_variables,
            "output_variables": output_variables,
            "parameters": parameters
        }
        _logger.info(f"Final configuration for conversion: Language = '{payload['language']}', Model = '{payload['model_name']}'")

        upload_id = self._prepare_and_upload_source(project_path, payload['model_name'], payload['version'])
        payload["upload_id"] = upload_id

        _logger.info(f"Requesting FMU conversion for '{payload['model_name']}' via cloud API...")
        conversion_response = self._make_request("POST", "/models/convert-fmu", json=payload)
        job_id = conversion_response.get("job_id")
        if not job_id:
            raise JingongoAPIError("API did not return a job ID for the conversion request.")
        _logger.info(f"Conversion job started with ID: {job_id}")

        if wait_for_completion:
            return self._poll_for_completion(job_id, poll_interval, payload['model_name'])
        
        return conversion_response

    def get_conversion_status(self, job_id: str) -> Dict[str, Any]:
        """Retrieves the status of a specific FMU conversion job."""
        _logger.info(f"Fetching status for job ID: {job_id}...")
        return self._make_request("GET", f"/models/conversion-status/{job_id}")

    def download_fmu(self, job_id: str, download_dir: Union[str, Path] = ".") -> Path:
        """Downloads a completed FMU from the cloud to a local directory."""
        _logger.info(f"Requesting download for FMU from job: {job_id}...")
        
        response_data = self._make_request("GET", f"/models/download/{job_id}")
        download_url = response_data.get("download_url")
        fmu_filename = response_data.get("fmu_filename")
        if not download_url or not fmu_filename:
            raise JingongoAPIError("Backend did not provide a valid download URL or filename.")
            
        destination_path = Path(download_dir)
        destination_path.mkdir(parents=True, exist_ok=True)
        local_fmu_path = destination_path / fmu_filename
        
        _logger.info(f"Downloading '{fmu_filename}' to '{local_fmu_path}'...")
        try:
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                with open(local_fmu_path, 'wb') as f, tqdm(total=total_size, unit='iB', unit_scale=True, desc=fmu_filename) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        size = f.write(chunk)
                        bar.update(size)
            return local_fmu_path
        except Exception as e:
            _logger.error(f"An error occurred during download: {e}")
            if local_fmu_path.exists():
                os.remove(local_fmu_path)
            raise JingongoAPIError(f"Download of {fmu_filename} failed.") from e
    def health_check(self) -> Dict[str, Any]:
        """
        Performs a health check on the Jingongo API.
        
        Returns:
            A dictionary with the health status of the API.
        
        Raises:
            JingongoAPIError: If the health check fails.
        """
        _logger.info("Performing health check on the Jingongo API...")
        return self._make_request("GET", "/health")
    
    @staticmethod
    def get_login_url(portal_url: str = "http://www.jingongo.com") -> str:
        """
        Provides the URL to the web portal for users to sign in.

        Args:
            portal_url (str): The base URL of the Jingongo web portal.

        Returns:
            str: The full URL to the login page.
        """
        login_url = f"{portal_url}/login"
        print(f"\nPlease open the following URL in your web browser to sign in:")
        print(f"  {login_url}")
        print("\nAfter signing in, copy your TEMPORY (Up to an Hour) User Token from the dashboard and use it to generate_api_key_from_token an API KEY that Lives Longer. Or Copy your API KEY if you generate already.")
        return login_url
        

    @staticmethod
    def get_signup_url(portal_url: str = "http://www.jingongo.com") -> str:
        """
        Provides the URL to the web portal for users to sign up.

        Args:
            portal_url (str): The base URL of the Jingongo web portal.

        Returns:
            str: The full URL to the signup page.
        """
        signup_url = f"{portal_url}/signup"
        print(f"\nPlease open the following URL in your web browser to create an account:")
        print(f"  {signup_url}")
        print("\nAfter signing up, you will be taken to your dashboard where you can find your user Token.")
        return signup_url