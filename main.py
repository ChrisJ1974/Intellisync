import openai
import azure

import spacy as spaCy

import calc as calc
from user_proxy_agent import UserProxyAgent

import config

openai_api_key = config.OPENAI_API_KEY

def ask_openai(prompt, model="text-davinci-003", temperature=0.7):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=2000 
    )
    return response.choices[0].text.strip()

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=[
        {"role": "system", "content": "You are Noesis, a conversational AI assistant. You re here to answer questions about Intellisync. How may I help you?\n\n"},
        {"role": "user", "content": "What is our Gross profit margin trending over the last 3 years?"},
        {"role": "assistant", "content": "Your Gross Profit Margin trending up by 5% in the last 3 years."},
        {"role": "user", "content": " What is our Net Profit Margin trending over the last 3 years?"},
    ],
    temperature=.6 #The lower the value, the more predictable the output is. The higher the value, the more random the output is.
)

print(response.choices[0].message.content)

#Connection to server string
AZURE_SQL_CONNECTIONSTRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:ivorsql.database.windows.net,1433;Database=IntellisyncData;Uid=Intellisync;Pwd=TheRaptors!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"




# Load the spaCy model for NLP
nlp = spaCy.load("en_core_web_sm") 

# Initialize the UserProxyAgent
user_proxy_agent = UserProxyAgent("User Proxy", {"read": True, "write": True})

# Define a dictionary to maintain context for each user
user_contexts = {}

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
        # Log error here if necessary

    print(response)  

# Main interaction loop
if __name__ == "__main__":
    while True:
        user_id = 'default_user'  # This could be dynamically set for different users
        user_input = input(f"[{user_id}] Enter your query (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        handle_user_query(user_id, user_input)

    # Optional: Implement feedback mechanism here
    # Ask the user for feedback on the provided responses
    # Use this feedback to improve the UserProxyAgent and underlying agents
