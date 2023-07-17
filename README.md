# README

## Meraki User Creation Tool

This tool automates the process of creating users in a Meraki network. It reads apartment numbers from a file and generates a secure password for each apartment. The tool then creates a Meraki identity PSK for each apartment and saves the results to a file. The tool also retries if an error occurs during the creation of the Meraki identity PSK.

## Requirements

To run this script, you need Python 3.7 or later installed on your machine. 

Additionally, the script relies on the `meraki` Python library. You can install it with pip, Python's package installer. Use the following command:

```
pip install meraki
```

## Environment Variables

Before running the script, you need to set the following environment variables:

- `MERAKI_API_KEY`: Your Meraki API Key
- `NETWORK_ID`: The Network ID of your Meraki network
- `GROUP_POLICY_ID`: The Group Policy ID for the users

You can set these environment variables in your shell, or you can use the provided batch file to prompt for them.

## File Input

The script reads apartment numbers from a file called `apartments.txt`. This file should be located in the same directory as the script. Each apartment number should be on a new line. 

## File Output

The script writes the results to a file called `output.txt`. This file should be located in the same directory as the script and must exist before running the script. If it doesn't exist, create a blank file named `output.txt` in the same directory as the script. 

The format of the output file is as follows:

```
{apartment_number},{password},{number},{group_policy_id},{success|failure}
```

The script also creates a copy of the output file with the current date and the group policy ID in the filename.

## Batch Script

The batch script `start.bat` prompts the user for their Meraki API Key, Network ID, and Group Policy ID, and then runs the Python script. **We recommend always running the tool through the batch script**. This ensures that the environment variables are set correctly each time you run the script.

## Usage

To run the tool, always use the following command:

```
start.bat
```

When prompted, enter your Meraki API Key, Network ID, and Group Policy ID. The Python script will then be started automatically.

## License

This project is licensed under the terms of the MIT license.

## Author

Ethan Frech
