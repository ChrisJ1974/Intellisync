# Corrected and Optimized Main.py Script

import openai
import spacy
from user_proxy_agent import UserProxyAgent
import config

# Load configuration variables
openai_api_key = config.OPENAI_API_KEY
openai.api_key = openai_api_key  # Set the API key for the OpenAI library

# Connection string should be securely managed, consider using environment variables
AZURE_SQL_CONNECTIONSTRING = config.AZURE_SQL_CONNECTIONSTRING

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Initialize the UserProxyAgent
user_proxy_agent = UserProxyAgent("User Proxy", {"read": True, "write": False})

# Define a dictionary to maintain context for each user
user_contexts = {}

# Function Definitions

def ask_openai(prompt, model="text-davinci-003", temperature=0.7):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=2000
    )
    return response.choices[0].text.strip()

def handle_user_query(user_id, user_query):
    # Check for existing user context, else create a new one
    context = user_contexts.get(user_id, {})

    # Pass the user's query and context to the UserProxyAgent
    try:
        response, updated_context = user_proxy_agent.route_query(user_query, context)
        # Update the user's context
        user_contexts[user_id] = updated_context
    except Exception as e:
        response = f"An error occurred: {e}"
        # Log the error here if necessary

    print(response)

# Main interaction loop
if __name__ == "__main__":
    while True:
        user_id = input("Enter your user ID (type 'exit' to quit): ").strip()
        if user_id.lower() == 'exit':
            break

        user_input = input(f"[{user_id}] Enter your query: ").strip()
        if user_input.lower() == 'exit':
            break

        handle_user_query(user_id, user_input)

    # Optional: Implement feedback mechanism here
