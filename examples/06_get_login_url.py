# examples/05_get_login_url.py
import os
import sys

# Add the src directory to the Python path so we can import the jingongo module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# The get_login_url method is static, so we can call it directly from the class
from jingongo import Jingongo

def main():
    """
    Demonstrates how to retrieve the URL for the Jingongo web portal login page.
    """
    print("--- Example: Getting the Jingongo Login URL ---")

    # This is a static method, so you don't need an API key or an
    # initialized client to call it.

    # You can optionally specify a different portal URL if it's not the default
    # portal_url = "https://my-custom-portal.com"
    # login_url = Jingongo.get_login_url(portal_url=portal_url)

    login_url = Jingongo.get_login_url()

    print("\n✅ The method has printed the instructions to the console.")
    print(f"   The generated URL was: {login_url}")


if __name__ == "__main__":
    main()