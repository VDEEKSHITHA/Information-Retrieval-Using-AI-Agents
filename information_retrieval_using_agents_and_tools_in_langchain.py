# -*- coding: utf-8 -*-
"""Information Retrieval Using Agents and Tools in LangChain.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y9JebHqyGmBFhR7IT5mBoMBTpkm804G-

**Information Retrieval Using Agents and Tools in LangChain**
"""

#Get all the tools that are installed with Langchain
import pprint as p
from langchain.agents import get_all_tool_names

pp = p.PrettyPrinter(indent = 4)
pp.pprint(get_all_tool_names())

#Ex 1 Using Action agent
#from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.agents import load_tools, initialize_agent

prompt = "When was the 3rd President of United States born? What is that year raised to the power 3?"

llm  = OpenAI(temperature = 0)
tools = load_tools(['wikipedia', 'llm-math'],
                   llm=llm)
agent = initialize_agent(tools,
                         llm,
                         agent = 'zero-shot-react-description',
                         verbose = True)
agent.run(prompt)

#Ex2 Plan and Execute Agent
#They plan  series of steps and then execute

prompt = """Where is the next summer Olympics to be conducted?
What is the population of that country raised to 0.4 power?"""

#1. Search for the location
#2. Identify the country
#3. Search for the population of this country
#4. Raise it to the power 0.4

# we may need to use the tools like Google Search, wikipedia, calculator - llm-math
# get the API key of Google Search

#from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute,load_chat_planner,load_agent_executor

from langchain import SerpAPIWrapper, WikipediaAPIWrapper,LLMMathChain

from langchain.agents.tools import Tool


llm = OpenAI(temperature = 0)
llm_mathchain = LLMMathChain.from_llm(llm = llm, verbose = True)

search = SerpAPIWrapper()
wikipedia = WikipediaAPIWrapper()


#create Tools

tools = [
     Tool(
         name = "Search",
         func = search.run,
         description= "Useful when you have to answer questions about current events"
         ),

    Tool(
        name = "Wikipedia",
        func = wikipedia.run,
        description= "Useful when you have to look up facts and statistics"
        ),

    Tool(
        name = "Calculator",
        func = llm_mathchain.run,
        description= "Useful when you have to calculate"
        ),


    ]

# For planner and executor model we need a model with the context information.
# The default OpenAI model text-davinci-003 has no memory and context.
# Hence for Plan and Execute models( use ChatOpenAI to leverage previous information

model = ChatOpenAI(temperature = 0)

planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose = True)

agent = PlanAndExecute(planner = planner, executor = executor, verbose = True)

agent.run(prompt)