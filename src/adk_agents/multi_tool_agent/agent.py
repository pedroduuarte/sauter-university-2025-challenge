from dotenv import load_dotenv
import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
import google.auth
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
  credentials=application_default_credentials
)

load_dotenv()

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
DATASET = os.getenv("BIGQUERY_DATASET")

# configurção do BigQueryToolset
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

# Agente para responder perguntas sobre o site Sauter Digital
sauter_agent = Agent(
    name="sauter_info_agent",
    model="gemini-2.5-flash",
    description=(
        "Agente para responder perguntas sobre o site Sauter Digital."
    ),
    instruction=(
        """
        Você é um agente prestativo que responde perguntas sobre a empresa Sauter Digital.
        Use a ferramenta google_search para encontrar informações no site da empresa, garantindo que toda pesquisa inclua o filtro 'site:https://sauter.digital/' para que os resultados sejam apenas desse domínio."
        """
    ),
    tools=[google_search],
)

# Agente para consultar dados no BigQuery
bigquery_agent = Agent(
    name="bigquery_agent",
    model="gemini-2.5-flash",
    description=(
        "Agente para buscar e responder perguntas usando dados do Google BigQuery."
    ),
    instruction=(
        f"""
        Você é um analista de dados especializado em consultar dados do Google BigQuery.
        Ao receber uma solicitação, identifique a necessidade do usuário, formule e execute queries SQL no BigQuery usando a ferramenta disponível.
        Utilizeo projeto onde o ID é '{PROJECT}' o dataset '{DATASET}' para todas as consultas.
        A tabela que será utilizada é a 'trusted_data'.
        Retorne os resultados de forma clara e objetiva, explicando os dados quando necessário.
        Se a consulta for complexa, explique os passos e forneça insights relevantes com base nos dados retornados.
        Caso não tenha informações suficientes para responder, peça detalhes adicionais ao usuário.
        """
    ),
    tools=[bigquery_toolset],
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