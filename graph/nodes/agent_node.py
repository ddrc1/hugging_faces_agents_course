from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage

from graph.tools import tavily_search_tool, youtube_video_analyzer, text_file_parser, multimedia_file_analyser, thinking_tool#, calculator, 
from graph.llms import get_llm

from graph.graph_state import GraphState
from graph.prompts.agent_prompt_basic import PROMPT


react_agent = create_react_agent(
    model=get_llm(model="gemini-2.5-pro", temperature=0.0),
    # prompt=PROMPT,
    tools=[tavily_search_tool, youtube_video_analyzer, text_file_parser, multimedia_file_analyser]#thinking_tool
)
    
def agent_node(state: GraphState) -> GraphState:
    question: str = state.get("question")
    file_name: str = state.get("file_name")
    
    prompt_template = ChatPromptTemplate([
        SystemMessagePromptTemplate.from_template(template=PROMPT),
        HumanMessage(content=question)
    ])
    
    formated_messages = prompt_template.format_messages(attachment=file_name)
    
    for step_response in react_agent.stream(input={"messages": formated_messages}, stream_mode="values"):
        step_response["messages"][-1].pretty_print()
    
    graph_response: str = step_response["messages"][-1].content
    return {"answer": graph_response}

# def agent_node(state: GraphState) -> GraphState:
#     cache = None
#     if state["file_name"]:
#         client = genai.Client()
#         uploading_file = client.files.upload(file="./GAIA/2023/validation/" + state["file_name"])
#         while uploading_file.state.name == 'PROCESSING':
#             time.sleep(2)
#             file = client.files.get(name=uploading_file.name)
    
#         cache = client.caches.create(
#                 model="gemini-2.5-pro",
#                 config=types.CreateCachedContentConfig(
#                     display_name='Cached Content',
#                     system_instruction=(
#                         'You are an expert content analyzer, and your job is to answer '
#                         'the user\'s query based on the file you have access to.'
#                     ),
#                     contents=[file],
#                     ttl="300s",
#                 )
#             )
    
#     response: dict = react_agent_chain(
#         question=state['question'],
#         content=cache,
#         prompt=PROMPT)

#     return {"thinking_output": response["messages"][-1].content, "final_answer": response["structured_response"].output}