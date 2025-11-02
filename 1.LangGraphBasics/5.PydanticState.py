#THIS IS USING PYDANTIC
#Enforced.
from multiprocessing.reduction import steal_handle
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel

class PydanticState(BaseModel):
    name:str

def Output(state:PydanticState):
    return {"name":state.name+ " ! What's Up !!"}

graph=StateGraph(PydanticState)
graph.add_node("output",Output)
graph.add_edge(START,"output")
graph.add_edge("output",END)
builder=graph.compile()
# result=builder.invoke({"name": input("🐦 Who are u ??")})
result=builder.invoke({"name":123}) #error here cause of pydantic validation
print(result)