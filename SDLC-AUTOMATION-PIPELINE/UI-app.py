import requests
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# --- Streamlit Integration: Only input() replaced, UI in tabs, dark theme, header ---
try:
    import streamlit as st
    if "state" not in st.session_state:
        st.session_state.state = {}

    st.set_page_config(page_title="Agentic AI based SDLC automation", layout="wide")
    st.markdown("""
        <style>
            body, .main, .stApp {
                background-color: #181a1b !important;
                color: #fff !important;
            }
            .stTabs [data-baseweb="tab-list"] {gap: 2rem;}
            .stTabs [data-baseweb="tab"] {
                font-size: 1.1rem; font-weight: bold; color: #fff !important;
            }
            .stTabs [aria-selected="true"] {
                color: #ff4747 !important;
                border-bottom: 2px solid #ff4747 !important;
            }
            .section-header {font-size:2.6rem; margin-top:2rem; margin-bottom:1rem; font-weight:700;}
            .section-sub {color:#aaa; margin-bottom:1rem;}
            .stButton>button, .stDownloadButton>button {
                font-size:1.1rem; padding:0.5em 2em; background:#232324; color:#fff; border-radius:8px;
                border: 1px solid #34363a;
            }
            .stButton>button:hover, .stDownloadButton>button:hover {background-color:#ff4747; color:#fff;}
            .ai-output {background:#232324; border-radius:8px; padding:1.4em; font-family:monospace;}
            .stTextInput>div>div>input, .stTextArea textarea, .stSelectbox div[role="combobox"] {
                background-color: #232324 !important; color: #fff !important;
                border: 1px solid #34363a !important; border-radius: 7px !important;
            }
            hr {border-top: 1px solid #34363a;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown(
        '<h1 style="color:#fff; font-size:2.3rem; font-weight:800; text-align:center; margin-bottom:1.5rem;">Agentic AI based SDLC automation</h1>',
        unsafe_allow_html=True
    )
    tabs = [
        "Info", "Requirements", "User Story", "System Design",
        "Code Generation", "Code Explanation", "Test Cases",
        "Requirements.txt", "README"
    ]
    tab_objs = st.tabs(tabs)
except ImportError:
    st = None
    tab_objs = [None]*9

def info_node(state: dict):
    # Ask the user for the topic to search
    if st and st.session_state.get("use_streamlit_info_node", False):
        topic = st.session_state.get("topic_input", "").strip()
    else:
        topic = input("Enter the topic you want to search information about: ").strip()
    state["topic"] = topic

    source = state.get("info_source", "duckduckgo")  # Default is duckduckgo

    if source == "wikipedia":
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        summary = wikipedia.run(topic)
    else:  # Default to duckduckgo
        url = f"https://api.duckduckgo.com/?q={topic}&format=json"
        response = requests.get(url)
        data = response.json()
        summary = data.get("AbstractText", "No summary found.")

    state["info_summary"] = summary
    state["info_source"] = source
    return state

import requests
import json

def requirements_node(state):
    if st and st.session_state.get("use_streamlit_requirements_node", False):
        topic = st.session_state.get("requirements_topic_input", "").strip()
    else:
        topic = input("Enter the project topic").strip()
    requirements = (
    f"You are a senior technical strategist. I am planning to build a project on the topic: '{topic}'. "
    f"Give me 3 different high-level approaches for how this project can be developed. "
    f"Each approach must be unique and include:\n"
    f"1. The goal or problem being solved\n"
    f"2. A creative and practical solution idea\n"
    f"3. The suggested tech stack or tools that would fit best\n"
    f"Focus on clarity and variety — I want distinctly different ways to build this project. "
    f"Do not include any code. These ideas will be shared with the Technical Design team for evaluation, Also User will be Choosing One of the Stories or Approaches and Then They will be sent to the technical Design Team"
)
    state["requirements"] = requirements

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": requirements
    }
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break
    print()
    state["ollama_response"] = full_response
    return state

def manual_story_node(state):
    if st and st.session_state.get("use_streamlit_manual_story_node", False):
        story = st.session_state.get("manual_story_input", "")
    else:
        story = input("Please enter your story: ")
    state["chosen_story"] = story
    return state

import requests
import json

def system_design_node(state):
    story = state["chosen_story"]
    if st and st.session_state.get("use_streamlit_system_design_node", False):
        user_prompt = st.session_state.get("system_design_input", "")
    else:
        user_prompt = input("Enter your system design request (e.g., focus on scalability, security, etc.): ")
    final_prompt = (
        f"Given the following story, design a software system based on this additional request.\n\n"
        f"Story:\n{story}\n\n"
        f"User Request:\n{user_prompt}\n\n"
        f"Please provide details on system components, data flow, and user interactions, How this can be made, how much time will it take to test the code and stuff. Be Clear and Precise "
    )
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": final_prompt
    }
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break
    print()
    state["system_design"] = full_response
    return state

def code_generation_node(state):
    print("The SystemDesign for the Requiremnent are as follows ")
    print(state["system_design"])
    if st and st.session_state.get("use_streamlit_code_generation_node", False):
        approval = st.session_state.get("code_generation_approval", "yes")
    else:
        approval = input("Do You want to go ahead with the current System Design = yes" "\n" " if You Want to Go back to to the System Design Node = no")
    if approval == "yes":
        prompt = (
        "You are a senior software engineer.\n"
        "Given the system design below, generate the complete and functional code for the core modules and components required.\n\n"
        "Instructions:\n"
        "- Output all code necessary for a working prototype in a single response.\n"
        "- If the system contains multiple files or modules, output them sequentially with clear file names as comments at the top (e.g., # filename.py).\n"
        "- Do not leave any functions, classes, or main logic as placeholders; implement all key logic so that a beginner can run and understand the code.\n"
        "- Add comments explaining complex sections, but keep the output focused on code only (no explanations outside comments).\n"
        "- Include all necessary import statements and initialization code.\n"
        "- If configuration or environment setup is needed, include it at the top as code comments.\n"
        "- Make sure the output does not stop mid-function or mid-class. Finish all code blocks.\n"
        "- Do not generate test cases or documentation here, But CREATE THE CODE FULLY AND DONOT LEAVE ANY FUNCTIONS EMPTY\n\n"
        f"System Design:\n{state['system_design']}\n"
)
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "gemma:2b",
            "prompt": prompt
        }
        response = requests.post(url, json=payload, stream=True)
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if "response" in data:
                    print(data["response"], end='', flush=True)
                    full_response += data["response"]
                if data.get("done", False):
                    break
        print()
        state["generated_code"] = full_response
        print("\n--- Generated Code ---")
        print(full_response)
        return state
    elif approval == "no":
        print("Regenerating system design as per your request...")
        state = system_design_node(state)
    state = next_node_after_generation(state)
    return state

def next_node_after_generation(state):
    generated_code = state.get("generated_code", "")
    print("\nWhat would you like to do next?")
    print("1. Regenerate the code, if The Code is not Up to The mark")
    print("2. Get an explanation of the Generated code")
    print("3. Go to the next node in sequence, That is ")
    if st and st.session_state.get("use_streamlit_next_node_after_generation", False):
        user_choice = st.session_state.get("next_node_after_generation_choice", "").strip()
    else:
        user_choice = input("Enter the number of your choice (one/two/three): ").strip()
    if user_choice == "one":
        print("Taking back to the Code generation Node" "\n")
        state = code_generation_node(state)
    elif user_choice == "two":
        state = code_explainer_node(state)
        print("Explaining The code provided -->" "\n")
        print(state.get("code_explanation"))
    elif user_choice == "three":
        print("nothing Yet , tbc")

def code_explainer_node(state):
    generated_code = state.get("generated_code", "")
    if not generated_code:
        print("No code found.")
        return state
    prompt = (
        "You are a beginner-friendly coding tutor.\n"
        "Explain the following code step by step, in very simple language.\n"
        "Describe what each function does, how the code works, and the main ideas.\n"
        "Do NOT repeat the code, just explain in plain English and The Code should be explained Line by line .\n\n"
        f"Code:\n{generated_code}\n"
    )
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": prompt
    }
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if "response" in data:
                    print(data["response"], end='', flush=True)
                    full_response += data["response"]
                if data.get("done", False):
                    break
    print()
    state["code_explanation"] = full_response
    if st and st.session_state.get("use_streamlit_code_explainer_node", False):
        proper_code = st.session_state.get("code_explainer_proper_code", "one")
    else:
        proper_code = input("was The Code Explanation Proper as per Your Requiremnt? (zero:imProper) , (one:✅)")
    if proper_code =="zero":
        print("Regenerating the Code Explanation Again,Provide the Approval Again")
        state = next_node_after_generation(state)
        return next_node_after_generation(state)
    elif proper_code == "one":
        print("Lets Get to the Next State , Where You Can Generate The Test Cases For Your Chosen Code:")
        state = test_case_node(state)
    return state

def test_case_node(state):
    print("Lets Generate The Test Cases For The Above Code, Provide Your Prompt Along With your Code:")
    generated_code = state.get("generated_code","")
    if not generated_code:
        print("*Code Not Found")
        return state
    if st and st.session_state.get("use_streamlit_test_case_node", False):
        user_prompt = st.session_state.get("test_case_input", "").strip()
    else:
        user_prompt = input("Any specific Requirements? : \n if Not Press Enter").strip()
    prompt = (
        "You are a senior QA engineer.\n"
        "Given the following code, generate all necessary unit tests to ensure its correctness.\n"
        "Include:\n"
        "- Tests for all core functions and classes\n"
        "- Tests for edge cases\n"
        "- Use Python's unittest or pytest (choose based on user request)\n"
        "- Do NOT include code explanations, donot Provide full code too , just mention Where what test thngs are required and Whatwill be the Test statement , only to test the code itself\n")
    prompt += f"There Are some Additional User Requirements : {user_prompt}" 
    prompt += f"Code To test = {generated_code}" "\n"
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": prompt
    }
    response = requests.post(url,json=payload,stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break 
    print()
    state["test_cases"] = full_response
    print("the Generated Test Cases are As Follows")
    print(full_response)
    print("Test cases Provided")
    return state

def requirements_generation_node(state):
    generated_code = state.get("generated_code", "")
    if not generated_code:
        print("Code not found")
    print("analyzing Your Code to Generate The Requirements")
    prompt = (
        "Given the following Python code, list all the external Python packages (pip) "
        "that need to be installed for it to work. Output only the package names, "
        "one per line, as they should appear in a requirements.txt file. "
        "Do not include standard library modules.\n\n"
        f"{generated_code}\n"
    )
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": prompt
    }
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break
    print("\n")
    with open("requirements.txt", "w") as f:
        f.write(full_response.strip())
    print("Requirements saved to requirements.txt")
    state["requirements_txt"] = full_response.strip()
    return state

def documentation_node(state):
    info_summary = state.get("info_summary", "")
    system_design = state.get("system_design", "")
    requirements_txt = state.get("requirements_txt", "")
    generated_code = state.get("generated_code", "")
    prompt = (
        "You are an expert technical writer. Given the following project details, generate a clear, beginner-friendly README.md file.\n"
        f"Project Info Summary:\n{info_summary}\n\n"
        f"System Design:\n{system_design}\n\n"
        f"Requirements.txt:\n{requirements_txt}\n\n"
        "Code:\n"
        f"{generated_code}\n\n"
        "README should include:\n"
        "- Project title and summary (from info summary)\n"
        "- Setup instructions (including dependencies from requirements.txt)\n"
        "- How to run the code\n"
        "- Usage examples if possible\n"
        "- Keep everything simple and clear for a beginner."
    )
    url = "http://localhost:11434/api/generate"
    payload = {
        "model":"gemma:2b",
        "prompt":prompt
    }
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break
    print("Downloading the Readme.md in your Working Directory")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(full_response.strip())
    print("README.md saved.")
    state["readme"] = full_response.strip()
    return state

import networkx as nx
import matplotlib.pyplot as plt

steps = [
    "info_node",
    "requirements_node",
    "manual_story_node",
    "system_design_node",
    "code_generation_node",
    "next_node_after_generation",
    "code_explainer_node",
    "test_case_node",
    "requirements_generation_node",
    "documentation_node"
]

edges = [
    ("info_node", "requirements_node"),
    ("requirements_node", "manual_story_node"),
    ("manual_story_node", "system_design_node"),
    ("system_design_node", "code_generation_node"),
    ("code_generation_node", "next_node_after_generation"),
    ("next_node_after_generation", "code_generation_node"),
    ("next_node_after_generation", "code_explainer_node"),
    ("next_node_after_generation", "test_case_node"),
    ("code_explainer_node", "test_case_node"),
    ("test_case_node", "requirements_generation_node"),
    ("requirements_generation_node", "documentation_node"),
]

if st:
    with tab_objs[0]:
        st.session_state["use_streamlit_info_node"] = True
        st.markdown('<div class="section-header">Project Info</div>', unsafe_allow_html=True)
        topic_input = st.text_input("Enter the topic you want to search information about:", key="topic_input")
        info_source = st.selectbox("Choose information source:", ["duckduckgo", "wikipedia"])
        st.session_state.state["info_source"] = info_source
        if st.button("Fetch Info"):
            st.session_state.state = info_node(st.session_state.state)
        if st.session_state.state.get("info_summary"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["info_summary"]}</div>', unsafe_allow_html=True)

    with tab_objs[1]:
        st.session_state["use_streamlit_requirements_node"] = True
        st.markdown('<div class="section-header">Requirements</div>', unsafe_allow_html=True)
        requirements_topic_input = st.text_input("Enter the project topic for requirements_node:", key="requirements_topic_input")
        if st.button("Submit Requirements"):
            st.session_state.state = requirements_node(st.session_state.state)
        if st.session_state.state.get("ollama_response"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["ollama_response"]}</div>', unsafe_allow_html=True)

    with tab_objs[2]:
        st.session_state["use_streamlit_manual_story_node"] = True
        st.markdown('<div class="section-header">User Story</div>', unsafe_allow_html=True)
        manual_story_input = st.text_area("Please enter your story:", key="manual_story_input")
        if st.button("Submit Story"):
            st.session_state.state = manual_story_node(st.session_state.state)
        if st.session_state.state.get("chosen_story"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["chosen_story"]}</div>', unsafe_allow_html=True)

    with tab_objs[3]:
        st.session_state["use_streamlit_system_design_node"] = True
        st.markdown('<div class="section-header">System Design</div>', unsafe_allow_html=True)
        system_design_input = st.text_input("Enter your system design request (e.g., focus on scalability, security, etc.):", key="system_design_input")
        if st.button("Generate Design"):
            st.session_state.state = system_design_node(st.session_state.state)
        if st.session_state.state.get("system_design"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["system_design"]}</div>', unsafe_allow_html=True)

    with tab_objs[4]:
        st.session_state["use_streamlit_code_generation_node"] = True
        st.markdown('<div class="section-header">Code Generation</div>', unsafe_allow_html=True)
        code_generation_approval = st.radio("Do You want to go ahead with the current System Design?", ["yes", "no"])
        st.session_state["code_generation_approval"] = code_generation_approval
        if st.button("Generate Code"):
            st.session_state.state = code_generation_node(st.session_state.state)
        if st.session_state.state.get("generated_code"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["generated_code"]}</div>', unsafe_allow_html=True)

    with tab_objs[5]:
        st.session_state["use_streamlit_next_node_after_generation"] = True
        st.markdown('<div class="section-header">Next Step</div>', unsafe_allow_html=True)
        next_node_after_generation_choice = st.radio("What would you like to do next?", ["one", "two", "three"])
        st.session_state["next_node_after_generation_choice"] = next_node_after_generation_choice
        if st.button("Continue"):
            st.session_state.state = next_node_after_generation(st.session_state.state)

    with tab_objs[6]:
        st.session_state["use_streamlit_code_explainer_node"] = True
        st.markdown('<div class="section-header">Code Explanation</div>', unsafe_allow_html=True)
        code_explainer_proper_code = st.radio("Was The Code Explanation Proper as per Your Requiremnt?", ["zero", "one"])
        st.session_state["code_explainer_proper_code"] = code_explainer_proper_code
        if st.button("Explain Code"):
            st.session_state.state = code_explainer_node(st.session_state.state)
        if st.session_state.state.get("code_explanation"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["code_explanation"]}</div>', unsafe_allow_html=True)

    with tab_objs[7]:
        st.session_state["use_streamlit_test_case_node"] = True
        st.markdown('<div class="section-header">Test Cases</div>', unsafe_allow_html=True)
        test_case_input = st.text_input("Any specific Requirements? : \n if Not Press Enter", key="test_case_input")
        if st.button("Generate Test Cases"):
            st.session_state.state = test_case_node(st.session_state.state)
        if st.session_state.state.get("test_cases"):
            st.markdown(f'<div class="ai-output">{st.session_state.state["test_cases"]}</div>', unsafe_allow_html=True)

    with tab_objs[8]:
        st.markdown('<div class="section-header">Requirements.txt</div>', unsafe_allow_html=True)
        if st.button("Generate requirements.txt"):
            st.session_state.state = requirements_generation_node(st.session_state.state)
        if st.session_state.state.get("requirements_txt"):
            st.code(st.session_state.state["requirements_txt"])
            st.download_button("Download requirements.txt", st.session_state.state["requirements_txt"], "requirements.txt")
        st.markdown('<div class="section-header">README.md</div>', unsafe_allow_html=True)
        if st.button("Generate README.md"):
            st.session_state.state = documentation_node(st.session_state.state)
        if st.session_state.state.get("readme"):
            st.markdown(st.session_state.state["readme"])
            st.download_button("Download README.md", st.session_state.state["readme"], "README.md")

    st.markdown("""
        <hr>
        <center><small>Designed by IshaanNarayanTyagi | Agentic-AI and Generative-AI</small></center>
    """, unsafe_allow_html=True)