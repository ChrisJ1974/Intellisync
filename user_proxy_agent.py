

import spacy
from ai_agent_base import AIAgentBase
from ceo_agent import CEOAgent
from cfo_agent import CFOAgent
from hr_agent import HRAgent
from cmo_agent import CMOAgent

from sales_agent import SalesAgent
from customer_insights_agent import CustomerInsightsAgent  # Ensure this is the correct import path

nlp = spacy.load("en_core_web_sm")  # Load the spaCy NLP model

class UserProxyAgent(AIAgentBase):
    def __init__(self, name, permissions):
        super().__init__(name, 'UserProxy', permissions)
        # Map roles to their corresponding agent classes
        self.agent_classes = {
            'CEO': CEOAgent,
            'CFO': CFOAgent,
            'HR': HRAgent,
            'CMO': CMOAgent,
            'Sales': SalesAgent,
            'CustomerInsights': CustomerInsightsAgent
        }

    def invoke_specialized_agent(self, query):
        doc = nlp(query)  # Process the query using NLP
        identified_role = None
        # Determine which agent to invoke based on the analysis
        for token in doc:
            if token.text in self.agent_classes:
                identified_role = token.text
                break

        if identified_role:
            agent_instance = self.agent_classes[identified_role]("AI " + identified_role, {"read": True, "write": True})
            agent_instance.receive_input(query)
            agent_instance.analyze_data({'placeholder': 'data'})  # Replace with actual data handling logic
            return agent_instance.send_response()
        else:
            return "Query does not match any specialized agent."
