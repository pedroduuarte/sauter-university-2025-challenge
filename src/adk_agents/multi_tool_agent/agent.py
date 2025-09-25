from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import bigquery
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

sauter_agent = Agent(
    name="sauter_info_agent",
    model="gemini-2.0-flash",
    description=(
        "Agente para responder perguntas sobre o site Sauter Digital."
    ),
    instruction=(
        """
        Você é um agente prestativo que responde perguntas sobre a empresa Sauter Digital.
        Use a ferramenta google_search para encontrar informações no site da empresa, garantindo que toda pesquisa inclua o filtro 'site:sauter.digital' para que os resultados sejam apenas desse domínio."
        """
    ),
    tools=[google_search],
)

# Agente para consultar dados no BigQuery
bigquery_agent = Agent(
    name="bigquery_agent",
    model="gemini-2.0-flash",
    description=(
        "Agente para buscar e responder perguntas usando dados do Google BigQuery."
    ),
    instruction=(
        """
        Você é um agente especializado em consultar dados do BigQuery.
        No momento você é apenas um prototipo e não tem acesso a dados reais.
        Caso seja feito alguma pergunta, responda com dados ficticios.
        
        """
    ),
    tools=[],
)

# Agente orquestrador
coordinator = LlmAgent(
    name="HelpDeskCoordinator",
    model="gemini-2.5-flash",
    instruction= 
    """
        Você é o agente orquestrador principal do Help Desk.
        Analise cuidadosamente cada solicitação do usuário e encaminhe para o agente mais adequado:
        - Use o agente 'sauter_info_agent' para perguntas sobre a empresa Sauter Digital ou informações do site sauter.digital.
        - Use o agente 'bigquery_agent' para solicitações que envolvam dados, relatórios ou consultas ao BigQuery.
        Se não tiver certeza de qual agente usar, peça esclarecimentos ao usuário antes de encaminhar.
        Sempre busque oferecer a melhor experiência, direcionando a solicitação ao agente mais especializado.
        """,
    description="Main help desk router.",
    tools=[agent_tool.AgentTool(agent=sauter_agent),
           agent_tool.AgentTool(agent=bigquery_agent)],
)

root_agent = coordinator