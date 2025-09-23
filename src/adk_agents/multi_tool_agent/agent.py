from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="sauter_info_agent",
    model="gemini-2.0-flash",
    description=(
        "Agente para responder perguntas sobre o site Sauter Digital."
    ),
    instruction=(
        "Você é um agente prestativo que responde perguntas sobre a empresa Sauter Digital. Use a ferramenta google_search para encontrar informações no site da empresa, garantindo que toda pesquisa inclua o filtro 'site:sauter.digital' para que os resultados sejam apenas desse domínio."
    ),
    tools=[google_search],
)