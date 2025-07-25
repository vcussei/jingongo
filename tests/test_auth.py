import pytest
import os
import sys

# Add the src directory to the path to allow importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import your custom exceptions and the main class
from jingongo.jingongo import Jingongo, JingongoAuthError

# A dummy URL for testing purposes
JINGONGO_API_BASE_URL = os.environ.get('JINGONGO_API_BASE_URL')

def test_initialization_with_invalid_key():
    """
    Tests that initializing the Jingongo client with an obviously invalid
    API key correctly raises a JingongoAuthError.
    
    This test uses a special feature of pytest called "mocking" to simulate
    the API's response without actually making a network call.
    """
    print("Running test: test_initialization_with_invalid_key")
    
    # We use pytest.raises to assert that the code inside this 'with'
    # block MUST raise the specified exception. If it doesn't, the
    # test will fail.
    with pytest.raises(JingongoAuthError):
        # We need to "mock" the _verify_api_key method so it doesn't
        # actually make an HTTP request during our test.
        # Here, we'll temporarily replace it with a function that just
        # raises the error we expect.
        
        original_verifier = Jingongo._verify_api_key
        
        def mock_verify_failure(self):
            # This is our fake verification function
            raise JingongoAuthError("Mocked authentication failure.")

        # Monkeypatch: Replace the real method with our fake one for this test
        Jingongo._verify_api_key = mock_verify_failure
        
        try:
            # Now, when we create the client, it will call our fake method
            # instead of the real one, triggering the expected error.
            Jingongo(api_base_url=JINGONGO_API_BASE_URL, api_key="this-key-is-bad")
        finally:
            # Important: Always restore the original method after the test!
            Jingongo._verify_api_key = original_verifier


def test_initialization_requires_api_key():
    """
    Tests that attempting to initialize without an API key raises a ValueError.
    """
    print("Running test: test_initialization_requires_api_key")
    with pytest.raises(ValueError):
        Jingongo(api_base_url=JINGONGO_API_BASE_URL, api_key=None)