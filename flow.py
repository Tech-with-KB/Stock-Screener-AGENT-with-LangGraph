# 1. Bring in dependencies
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from colorama import Fore, Style

from langgraph.prebuilt import ToolNode
from Tools.tool import simple_screener

# 2. Create an LLM
# llm = ChatOllama(model="gpt-oss:latest")
# llm = ChatOllama(model="deepseek-r1:1.5b")
llm = ChatOllama(model="qwen2.5:1.5b")

# 3. Create tool
tools = [simple_screener]

# 4. Bind tools to graph
llm_with_tools = llm.bind_tools(tools)

# 5. Create Tool Node 
tool_node = ToolNode(tools)

# 6. Create State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 7. Build the graph
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 8. Create Router Node
def router(state: State):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return "END"

# 9. Assemble the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    router,
    {
        "tools": "tools",
        "END": END
    }
)

## 10. Add Memory and Compile Graph
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

  


