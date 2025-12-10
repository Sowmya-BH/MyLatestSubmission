from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool

# from tools.docling_tool import DoclingTool
# from tools.json_parse_tool import Find_Next_Text_Node
from tools.custom_tool import DoclingTool,Find_Next_Text_Node
from crewai_tools import FileWriterTool

from pydantic import BaseModel
from fastapi import FastAPI

from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI

# ---------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# ---------------------------------------------------------------------------
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
# ---------------------------------------------------------------------------
# LLM CONFIG
# ---------------------------------------------------------------------------
# llm = LLM(
#     model="gemini/gemini-2.5-flash",
#     api_key=gemini_api_key,
#     temperature=0.7
# )
# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = BASE_DIR.parent.parent / "knowledge"
DOCUMENT_PATH = DOCUMENT_DIR / "TSLA-Q2-2025-Update.pdf"
JSON_OUTPUT_PATH = BASE_DIR.parent / "TSLA-Q2-2025-Update.json"


# # ---------------------------------------------------------------------------
# # CREW DEFINITION
# # ---------------------------------------------------------------------------
# crew.py

import os
from pathlib import Path
from dotenv import load_dotenv

from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, task, crew

from crewai_tools import MongoDBVectorSearchTool
from tools.process_pdf_tool import ProcessPDFTool  # your combined tool

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = BASE_DIR / "knowledge"
DOCUMENT_PATH = DOCUMENT_DIR / "TSLA-Q2-2025-Update.pdf"

# LLM configuration (uses env variable from YAML)
from crewai import LLM
llm = LLM(
    model=os.getenv("MODEL"),
    api_key= gemini_api_key,
    temperature=0.0
)


# # ---------------------------------------------------------------------------
# # CREW DEFINITION
# # ---------------------------------------------------------------------------
#
# @CrewBase
# class FullFinancialRAGCrew():
#     """
#     RAG Crew: PDF ingestion → embedding → vector DB storage → querying.
#     """
#
#     agents_config = "config/full_rag_pipeline.yaml"
#     tasks_config = "config/full_rag_pipeline.yaml"
#
#     # --------------------------
#     # 1. PDF PROCESSOR AGENT
#     # --------------------------
#
#     @agent
#     def pdf_processor_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["pdf_processor_agent"],
#             llm=llm,
#             verbose=True,
#             tools=[
#                 ProcessPDFTool()
#             ]
#         )
#
#     # --------------------------
#     # 2. RAG SEARCH AGENT
#     # --------------------------
#
#     @agent
#     def rag_search_agent(self) -> Agent:
#         rag_tool = MongoDBVectorSearchTool(
#             connection_string=os.getenv("MONGO_URI"),
#             database_name="financial_docs",
#             collection_name="financial_chunks",
#             text_field="content",
#             embedding_field="embedding",
#             k=4
#         )
#
#         return Agent(
#             config=self.agents_config["rag_search_agent"],
#             llm=llm,
#             verbose=True,
#             tools=[rag_tool]
#         )
#
#     # --------------------------
#     # TASKS
#     # --------------------------
#
#     @task
#     def process_pdf_task(self):
#         return {
#             "config": self.tasks_config["process_pdf_task"],
#             "input": {
#                 "DOCUMENT_PATH": str(DOCUMENT_PATH)
#             }
#         }
#
#     @task
#     def rag_search_task(self):
#         return {
#             "config": self.tasks_config["rag_search_task"]
#             # Input "query" will be provided in kickoff(inputs={})
#         }
#
#     # --------------------------
#     # CREW
#     # --------------------------
#
#     @crew
#     def crew(self):
#         return Crew(
#             agents=self.agents,
#             tasks=self.tasks,
#             process=Process.sequential,
#             verbose=True
#         )

##################################################################################################
#################################################################################################
@CrewBase
class CkdV3():
    """CkdV3 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def docling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['docling_agent'],
            verbose=True,
            tools=[DoclingTool(),
                   FileWriterTool()],
            llm=llm,
        )

    # @agent
    # def file_writer_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['file_writer_agent'],
    #         verbose=True,
    #         tools=[FileWriterTool()],
    #         output_file="parsed_financial_document.json",
    #         llm=llm,
    #     )


    @agent
    def JSON_data_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['JSON_data_extractor'],
            verbose=True,
            tools=[DoclingTool(),
                   Find_Next_Text_Node()],
            llm=llm,
        )

    @agent
    def financial_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst_agent'],
            verbose=True,
            tools=[],
            llm=llm,
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def parse_pdf(self) -> Task:
        return Task(
            config=self.tasks_config['parse_pdf'],
        )

    @task
    def parse_json(self) -> Task:
        return Task(
            config=self.tasks_config['parse_json'],
            context=[self.parse_pdf()], #  Use output of 'parse_pdf' (the JSON path) as context for this task.
            output_file = 'output.md',
        )

    @task
    def answer_query(self) -> Task:
        return Task(
            config=self.tasks_config['answer_query'],
            context=[self.parse_pdf()],#  Use output of 'parse_pdf' (the JSON path) as context for this task.
            output_file='summary.md',
        )
    # @task
    # def parse_pdf(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['parse_pdf'],
    #         input={
    #             "pdf_path": str(DOCUMENT_PATH),
    #         },
    #         output_file='output.md',
    #     )
    #
    # @task
    # def parse_json(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['parse_json'],
    #         context=[self.parse_pdf()],
    #         # NEW: Explicitly providing both required paths to the task
    #         # input={"json_file_path": str(JSON_OUTPUT_PATH)},
    #         output_file="financial_health_report.md",
    #
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the CkdV3 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            output_log_file='logs/logging.log'
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
