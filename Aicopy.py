import streamlit as st
import requests

# Set the Etherscan API key
etherscan_api_key = "A6UYXAXW6Q4IMF451XU6J3JAG8WB41AWWZ"

# Set the base URL for the Etherscan API
base_url = "https://api.etherscan.io/api?"

# Initialize the Streamlit app
st.title("Smart Contract Source Code")

# Get the smart contract address from the user
contract_address = st.text_input("Enter the smart contract address:")

# Define a function to get the source code of a smart contract from Etherscan
def get_source_code(address):
  # Build the API URL for getting the contract source code
  url = base_url + "module=contract&action=getsourcecode&address=" + address + "&apikey=" + etherscan_api_key
  
  # Send the API request and get the response
  response = requests.get(url)
  
  # Return the contract source code
  return response.json()["result"][0]["SourceCode"]

# If the user has entered a contract address, show the source code
if contract_address:
  # Get the source code of the contract
  source_code = get_source_code(contract_address)

  # Display the source code
  st.write("Source code:")
  st.code("Audit this source code for any issues, use bullet points for your findings. Rewrite the code in solidity once with solutions to these issues if they are found: "+ source_code)
