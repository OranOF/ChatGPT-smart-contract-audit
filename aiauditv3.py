import streamlit as st
import openai
import requests

# Set the OpenAI API key
openai.api_key = "your-api-key"

# Set the Etherscan API key
etherscan_api_key = "your-api-key"

# Set the base URL for the Etherscan API
base_url = "https://api.etherscan.io/api?"

# Initialize the Streamlit app
st.title("Smart Contract AI Audit")

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

# Define a function to audit a smart contract using OpenAI
def audit_smart_contract(source_code):
  # Split the source code into chunks of 4097 tokens or less
  chunks = [source_code[i:i+4097] for i in range(0, len(source_code), 4097)]

  # Initialize a list to store the analysis results for each chunk
  audit_results = []

  # Process each chunk of the source code
  for chunk in chunks:
    # Use the OpenAI API to analyze the chunk of source code
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt="Please review the following smart contract source code and identify any possible issues, list reponse in bullet points:\n\n" + chunk,
      temperature=0.5,
      max_tokens=1200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    # Add the analysis results for the chunk to the list
    audit_results.append(response["choices"][0]["text"])

  # Concatenate the results from all the chunks into a single string
  audit_results = "\n".join(audit_results)

  # Return the combined analysis results
  return audit_results

# If the user has entered a contract address, show the source code and AI audit results
if contract_address:
  # Get the source code of the contract
  source_code = get_source_code(contract_address)

# If the user clicks the "AI Audit" button, show the audit results
if st.button("AI Audit"):
  # Audit the smart contract
  audit_results = audit_smart_contract(source_code)

  # Display the audit results
  st.write("AI Audit Results:")
  st.write(audit_results)