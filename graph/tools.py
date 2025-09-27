from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import pandas as pd
import math
import numexpr
import yt_dlp
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()

tavily_search_tool = TavilySearch(
        max_results=3,
        topic="general",
        auto_parameters=True,
        include_images=True,
        include_image_descriptions=True,
        # include_answer=False,
        # include_raw_content=False,
        search_depth="advanced", 
        # time_range="day",
        # include_domains=None,
        # exclude_domains=None
    )

@tool
def calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem. Don't use python functions.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}
    print("calculator", expression)
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
    )

@tool
def youtube_video_analyzer(video_url: str, query: str) -> str:
    """
    Retrieves information in a youtube video
    
    Args:
        video_url (str): full video url
        query (str): query about the video
        
    Returns:
        str: answer about the video
    """
    temp_video_path = f"./temp_files/{video_url.split("v=")[-1]}.mp4"
    if not os.path.exists(temp_video_path):
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': temp_video_path,
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

        except Exception as e:
            return "Video download failed: " + str(e)
        
    uploaded_file_ref = genai.upload_file(path=temp_video_path)
    
    while uploaded_file_ref.state.name == "PROCESSING":
        print('Aguardando o processamento do vídeo...')
        time.sleep(5)
        uploaded_file_ref = genai.get_file(uploaded_file_ref.name)
        
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")
    response = model.generate_content(contents=[uploaded_file_ref, query],
                                      generation_config={"temperature": 0})
    
    if uploaded_file_ref:
        genai.delete_file(uploaded_file_ref.name)
    if os.path.exists(temp_video_path):
        os.remove(temp_video_path)
    
    return response.text 
     

@tool
def multimedia_file_analyser(file_name: str, query: str) -> str:
    """
    Retrieves information an multimedia file
    
    Args:
        file_name (str): image file name
        query (str): query about the image
        
    Returns:
        str: answer about the image
    """
    
    path = "./GAIA/2023/validation/" + file_name
    uploaded_file_ref = genai.upload_file(path=path)

    while uploaded_file_ref.state.name == "PROCESSING":
        time.sleep(5)
        uploaded_file_ref = genai.get_file(uploaded_file_ref.name)
    
    model = genai.GenerativeModel(model_name="gemini-2.5-pro")
    response = model.generate_content(contents=[uploaded_file_ref, query],
                                      generation_config={"temperature": 0})
    
    if uploaded_file_ref:
        genai.delete_file(uploaded_file_ref.name)
    
    return response.text


@tool
def text_file_parser(file_name: str) -> str:
    """
    Extrats the content of a text file (.xlsx, .csv, .txt, .py, .json)
    
    Args:
        file_name (str): file name
        
    Returns:
        str: file content
    """
    
    extension: str = file_name.split(".")[-1]
    path = "./GAIA/2023/validation/" + file_name
    if extension == 'xlsx':
        return pd.read_excel(path).to_csv()

    return open(path, "r").read()

@tool
def thinking_tool(reflection: str) -> str:
    """
    Use the tool to help thinking about something. Will help you to get better answers.
    
    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?
    
    Args:
        reflection: Your detailed reflection, findings, gaps, and next steps
        
    Returns:
        str: Confirmation that reflection was recorded for decision-making
    """
    
    return "Reflection recorded:", reflection