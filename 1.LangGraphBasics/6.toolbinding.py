
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,AIMessage,AnyMessage
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from IPython.display import display,Image
from langgraph.graph import StateGraph,START,END
from pprint import pprint

load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv("GOOGLE_API_KEY")
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# print(llm.invoke("hey there "))

def subtract(a:int,b:int)->int:
    ''' 
    Subtract a and b
    a(int): first int 
    b(int): second int 

    returns:
    int
    '''
    return a-b

llm_with_tools=llm.bind_tools([subtract])

# x=llm_with_tools.invoke("subtract 5 from 10")
# x=llm_with_tools.invoke("subtract 5 from 10")

# print(x)

class State(TypedDict):
    message: Annotated[list[AnyMessage],add_messages]

initial_msg=[AIMessage(content=f"Hey there!What can I do for you today ?",name="LLMModel")]
initial_msg.append(HumanMessage(content=f"I want to learn GenAI but I am confused, in what language should I start ?",name="Sibananda"))
ai_msg=[AIMessage(content=f"What languages are you familiar with ?",name="LLMModel")]

add_messages(initial_msg,ai_msg)

def llm_tool(state:State):
    return {"message":[llm_with_tools.invoke(state["message"])]}

builder=StateGraph(State)
builder.add_node("llm_tool",llm_tool)
builder.add_edge(START,"llm_tool")
builder.add_edge("llm_tool",END)
graph_builder=builder.compile()
# display(Image(graph_builder.get_graph().draw_mermaid_png()))

y=graph_builder.invoke({"message":"subtract 5 from 10"})

for x in y["message"]:
    print(x.pretty_print())