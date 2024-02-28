import spacy


from config import LLM_API_KEY

from user_proxy_agent import UserProxyAgent

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_sm") 

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
