import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel
import yaml
from dotenv import load_dotenv

# This connects your code to the .env file where API is stored
#
# # Initialize environment variables
load_dotenv()

researcher_llm = LLM(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    # model="ollama/gemma2:9b",
    # base_url="http://localhost:11434",
    # temperature=0.1,
)

#define file paths for YALM configuration

configs ={}
files={
    'agents':'config/agents.yaml',
    'tasks':'config/tasks.yaml'
}

for config_type, file_path in files.items():
    with open(file_path,'r') as file:
        configs[config_type]= yaml.safe_load(file)
    print(f"\nLoaded {config_type} from {file_path}")
    
#assign configuration to specific variables
agents_config=configs["agents"]
tasks_config=configs["tasks"]

#create the tools instance
serper_search_tool = SerperDevTool(
    search_url="http://owasp.org"
)
website_scrape_tool = ScrapeWebsiteTool()

#create the senior developer agent instance
senior_developer = Agent(
   config=agents_config["senior_developer"]
)

#create the Security Engineer Agent instance
security_engineer= Agent(
   config=agents_config["security_engineer"],
   tools=[serper_search_tool, website_scrape_tool]
)

#create the Tech Leader Agent instance
tech_lead= Agent(
   config=agents_config["tech_lead"]
)

