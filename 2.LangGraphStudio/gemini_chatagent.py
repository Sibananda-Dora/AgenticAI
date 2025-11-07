#needs some refining
# change the .json as per your settings

#use langgraph dev and then move to your langgraph studio in your Langsmith website.

from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage,AnyMessage
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import StateGraph,START,END

load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def add(a:int,b:int):
    '''
    input:
        a:int
        b:int
    returns:
        a+b
'''
    return a+b
tools=[add]
llm_with_tools=model.bind_tools(tools)

def tool_calling_llm(state:State):
    return {"messages":[(llm_with_tools.invoke(state["messages"]))]}
def make_graph():

    graph_workflow=StateGraph(State)
    graph_workflow.add_node("tool_calling_llm",tool_calling_llm)
    graph_workflow.add_node("tools",ToolNode(tools))
    graph_workflow.add_edge(START,"tool_calling_llm")
    graph_workflow.add_conditional_edges("tool_calling_llm",tools_condition,)

    graph_workflow.add_edge("tools","tool_calling_llm")
    graph_workflow.add_edge("tool_calling_llm",END)

    builder=graph_workflow.compile()
    return builder

agent=make_graph()

