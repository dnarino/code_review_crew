from hooks import read_file_hook
import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel
import yaml
from dotenv import load_dotenv

from guardrails import security_review_output_guardrail, review_decision_guardrail 

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


#TASKS

#define the pydantic model for the code quality analysis output

class CodeQualityJSON(BaseModel):
    critical_issues: list[str]
    minor_issues: list[str]
    reasoning: str

#create the quality analysis task

analyse_code_quality = Task(
    config = tasks_config['analyze_code_quality'],
    output_json=CodeQualityJSON,
    agent=senior_developer
)

#create the Review Security Task

class SecurityVulnerability(BaseModel):
    description: str
    risk_level: str
    evidence: str

#define the pydantic model for the security review output

class ReviewSecurityJSON(BaseModel):
    security_vulnerabilities:list[SecurityVulnerability]
    blocking: bool
    highest_risk:str
    security_recommendations:list[str]

#Create the security Review class

review_security = Task(
    config=tasks_config["review_security"],
    output_json=ReviewSecurityJSON,
    guardrails=[security_review_output_guardrail],
    agent=security_engineer
)

#create the review decision task
make_review_decision= Task(
    config=tasks_config["final_review_task"],
    markdown=True,
    guardrails=[review_decision_guardrail],
    context=[analyse_code_quality, review_security],
    agent=tech_lead
)

#creating CREW

codeReviewPandilla = Crew(
    agents=[senior_developer, security_engineer , tech_lead],
    tasks =[analyse_code_quality,review_security, make_review_decision],
    memory=True,
    before_kickoff_callbacks= [read_file_hook]
)

#kickoff the crew

file_path= 'files/code_changes.txt'

result = codeReviewPandilla.kickoff(
    inputs={
        'file_path':file_path,
        'code_changes':''
        }
)