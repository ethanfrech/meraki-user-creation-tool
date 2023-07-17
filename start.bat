@echo off

echo. 
echo ==============================================================================
echo Welcome to the Meraki User Creation Tool!
echo This tool automates the process of creating users in a Meraki network.
echo It prompts you for your Meraki API Key, Network ID, and
echo Group Policy ID, and finally runs a Python script to create the users.
echo Let's get started!
echo ==============================================================================
echo.

set /p MERAKI_API_KEY="Please enter your Meraki API Key: "
set MERAKI_API_KEY=%MERAKI_API_KEY%

echo.

set /p NETWORK_ID="Please enter your Network ID: "
set NETWORK_ID=%NETWORK_ID%

echo.

set /p GROUP_POLICY_ID="Please enter your Group Policy ID: "
set GROUP_POLICY_ID=%GROUP_POLICY_ID%

echo.

python meraki_user_creation.py

