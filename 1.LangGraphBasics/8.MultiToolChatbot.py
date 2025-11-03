# arxiv, wikipedia ,custom functions <-- TOOLS

from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from pprint import pprint 
from typing_extensions import TypedDict,Annotated   
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
from langchain_community.tools import tavily_search
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from dotenv import load_dotenv
from langchain_tavily import TavilySearch 
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_core.messages import HumanMessage,AIMessage,AnyMessage
load_dotenv()
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

api_wrapper_arxiv=ArxivAPIWrapper(top_k_results=2,doc_content_chars_max=500)
arxiv=ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
# result=arxiv.invoke("Attention is all you need.")
# print(result)
print("-------------------------------------------------------------------")
api_wrapper_wiki=WikipediaAPIWrapper(k=2,doc_content_chars_max=500)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)
# result2=wiki.invoke("Christopher Nolan")
# print(result2)

print("-------------------------------------------------------------------")
# a search tool which has access to internet
tavily=TavilySearch()
# result3=tavily.invoke("who won the women's odi cricket worldcup?")
# print(result3)
tools=[arxiv,wiki,tavily]

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools=llm.bind_tools(tools)
# res=llm_with_tools.invoke([HumanMessage(content=f"Tell me about Operation  White Sea.")])
# print(res.tool_calls)
# print(res)

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

def tool_calling_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

builder=StateGraph(State)

builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm",tools_condition,)
builder.add_edge("tools",END)

graph_builder=builder.compile()
y=graph_builder.invoke({"messages":HumanMessage(content="Operation White Sea")})
for x in y["messages"]:
    print(x.pretty_print())


