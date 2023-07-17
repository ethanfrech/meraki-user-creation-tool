import os
import sys
import time
import logging
import string
import secrets
import meraki
import datetime
import shutil
from meraki.exceptions import APIError
from requests.exceptions import RequestException

# Author: Ethan Frech
# Date: July 14, 2023
# Description: See README.md file.

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
API_KEY_ENV_VAR = 'MERAKI_API_KEY'
NETWORK_ID_ENV_VAR = 'NETWORK_ID'
GROUP_POLICY_ID_ENV_VAR = 'GROUP_POLICY_ID'
PASSWORD_LENGTH = 8
APARTMENT_FILE = 'apartments.txt'
OUTPUT_FILE = 'output.txt'

# Default values
DEFAULT_MAX_RETRIES = 3

# Obtain environment variables
def get_env_vars():
    env_vars = [API_KEY_ENV_VAR, NETWORK_ID_ENV_VAR, GROUP_POLICY_ID_ENV_VAR]
    missing_vars = []

    for var in env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logging.error(f"The environment variables {', '.join(missing_vars)} must be set.")
        sys.exit(1)

def generate_secure_password(length=PASSWORD_LENGTH):
    """Generate a secure password."""
    if length < 4:
        raise ValueError("Password length must be at least 4 to accommodate all character types.")

    # Exclude the comma from the character sets
    alphabet = string.ascii_letters
    digits = string.digits
    punctuation_without_comma = string.punctuation.replace(',', '')

    # Generate one character of each type
    lower = secrets.choice(string.ascii_lowercase)
    upper = secrets.choice(string.ascii_uppercase)
    digit = secrets.choice(digits)
    punctuation = secrets.choice(punctuation_without_comma)

    # Generate the remaining characters randomly from the alphabet
    remaining_length = length - 4
    remaining = ''.join(secrets.choice(alphabet) for _ in range(remaining_length))

    # Combine all parts
    password = lower + upper + digit + punctuation + remaining

    # Convert the password into a list and shuffle it to ensure randomness
    password = list(password)
    secrets.SystemRandom().shuffle(password)

    # Convert the list back into a string
    password = ''.join(password)

    return password

def create_meraki_identity_psk(api, network_id, name, passphrase):
    """Create a Meraki Identity PSK."""
    max_retries = os.getenv('MAX_RETRIES', DEFAULT_MAX_RETRIES)
    group_policy_id = os.getenv(GROUP_POLICY_ID_ENV_VAR)

    for attempt in range(max_retries):
        try:
            response = api.wireless.createNetworkWirelessSsidIdentityPsk(
                network_id,
                0,  # Keep the number at 0
                name,
                group_policy_id,  # now using environment variable for group policy ID
                passphrase=passphrase
            )

            if 'errors' not in response:
                logging.info("Created Meraki Identity PSK")
                return True

            logging.error(f"Attempt {attempt + 1} of {max_retries}: Failed to create Meraki Identity PSK: {response.get('errors', [])}")
            time.sleep(2 ** attempt)  # exponential backoff

        except (APIError, RequestException) as e:
            logging.error(f"Attempt {attempt + 1} of {max_retries}: Failed to create Meraki Identity PSK: {e}")
            time.sleep(2 ** attempt)  # exponential backoff

    logging.error(f"Failed to create Meraki Identity PSK after {max_retries} attempts.")
    return False

def generate_and_write_users():
    """Generate users based on apartment numbers from a file and secure passwords."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    network_id = os.getenv(NETWORK_ID_ENV_VAR)
    group_policy_id = os.getenv(GROUP_POLICY_ID_ENV_VAR)

    dashboard_api = meraki.DashboardAPI(api_key=api_key)

    with open(os.getenv('APARTMENT_FILE', APARTMENT_FILE), 'r') as f, open(os.getenv('OUTPUT_FILE', OUTPUT_FILE), 'w') as out_f:
        for line in f:
            apartment_number = line.strip()  # Remove any trailing newline
            passphrase = generate_secure_password()

            success = create_meraki_identity_psk(
                dashboard_api, network_id, apartment_number, passphrase
            )
            success_str = "success" if success else "failure"

            out_f.write(f"{apartment_number},{passphrase},{group_policy_id},{success_str}\n")
            out_f.flush()  # Ensure all data is written to disk

        os.fsync(out_f.fileno())  # Explicitly close file descriptor

def rename_output_file():
    """Rename the output file with a timestamp."""
    # Generate the current date
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate the new file name
    new_file_name = f"subnet_{os.getenv(GROUP_POLICY_ID_ENV_VAR)}_{date_str}.txt"

    # Copy the file
    shutil.copy(os.getenv('OUTPUT_FILE', OUTPUT_FILE), new_file_name)

def main():
    """Main function."""
    get_env_vars()  # Ensure all required environment variables are set
    generate_and_write_users()  # Generate users and write to file
    rename_output_file()  # Rename the output file with a timestamp

if __name__ == '__main__':
    message = "Started Meraki User Creation Script..."
    total_width = 60
    padding = (total_width - len(message)) // 2

    print("\n\n" + "=" * total_width)
    print(" " * padding + message + " " * padding)
    print("=" * total_width + "\n\n")

    main()

    message = "...Finished Meraki User Creation Script"
    padding = (total_width - len(message)) // 2

    print("\n\n" + "=" * total_width)
    print(" " * padding + message + " " * padding)
    print("=" * total_width + "\n\n")