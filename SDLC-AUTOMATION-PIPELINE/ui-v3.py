#All The use of Nodes Are Explained in the Workflow.py 
# Workflow.py is the main File , Instead Of Importing the Nodes The Nodes are pasted again here to manage The Calls 
# 


import requests
import json
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os

try:
    import streamlit as st

    PROJECT_NAME = "Agentic AI based SDLC Automation"
    TABS = [
        "Info", "Requirements", "User Story", "System Design",
        "Code Generation", "Next Step", "Code Explanation", "Test Cases",
        "Requirements.txt", "README"
    ]

    st.set_page_config(page_title=PROJECT_NAME, layout="wide") #Sets the Screen Wide.

  # The top Most Project Name - Agentic Ai Based SDLC Automation
    st.markdown(
        f'<div style="color:#fff; font-size:2.1rem; font-weight:800; text-align:center; margin-bottom:0.7rem; margin-top:1.2rem;">{PROJECT_NAME}</div>',
        unsafe_allow_html=True
    ) #Custom Styling of Fonts , Font Boldness , and Allignment


#Here all the Fonts and Stuff Are Present 
    st.markdown(f"""
        <style>
        body, .main, .stApp {{
            background-color: #16171b !important;
            color: #f7f7f7 !important;                  
            font-size: 1.17rem !important;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }} 
        .stTabs [data-baseweb="tab-list"] {{gap: 2rem;}}
        .stTabs [data-baseweb="tab"] {{
            font-size: 1.18rem; font-weight: 700; color: #fff !important;
        }}
        .stTabs [aria-selected="true"] {{
            color: #ff4747 !important;
            border-bottom: 3px solid #ff4747 !important;
        }}
        .section-header {{
            font-size:2.3rem; margin-top:2rem; margin-bottom:1.3rem; font-weight:800;
            letter-spacing:0.01em; color:#fff;
        }}
        .ai-output, .markdown-preview {{
            background: #17181d;
            border-radius: 12px;
            padding: 2.1em 2.1em 2.1em 2.1em;
            margin-top: 18px;
            margin-bottom: 28px;
            font-size: 1.15rem;
            color: #f8f8f2;
            box-shadow: 0 2px 24px 0 #15161b45;
            line-height: 1.7;
        }}
        .best-code-preview {{
            background: #14171b !important;
            border-radius: 14px;
            padding: 2em 2em 2em 2em;
            margin-top: 30px;
            margin-bottom: 36px;
            font-size: 1.13rem !important;
            font-family: 'JetBrains Mono', 'Fira Mono', 'Menlo', 'Consolas', 'monospace' !important;
            
            overflow-x: auto;
            color: #f7f7f7 !important;
            border: 2px solid #232324;
            line-height: 1.67;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        .stTextInput>div>div>input, .stTextArea textarea, .stSelectbox div[role="combobox"] {{
            background-color: #232324 !important; color: #fff !important;
            border: 1.4px solid #34363a !important; border-radius: 7px !important;
            font-size: 1.18rem !important;
        }}
        .stButton>button, .stDownloadButton>button {{
            font-size:1.13rem; padding:0.5em 1.8em; margin: 0.2em 0.5em 0.2em 0;
            background:#232324; color:#fff; border-radius:7px;
            border: 2px solid #34363a;
            font-weight: 700;
            transition: background 0.2s;
        }}
        .stButton>button:active, .stDownloadButton>button:active {{
            background-color:#ff4747 !important; color:#fff !important;
        }}
        .stButton>button:hover, .stDownloadButton>button:hover {{
            background-color:#ff4747; color:#fff;
        }}
        .tab-progress-box {{
            margin-top: .7em; margin-bottom: .9em; padding: 0.45em 1.0em;
            border-radius: 8px;
            background: #1a9c3a;
            display: flex;
            align-items: center;
            font-size: 1.04rem;
            color: #fff;
            border: 1.5px solid #1a9c3a;
            font-weight: 700;
            box-shadow: 0 1px 7px 0 #1a9c3a20;
            max-width: 340px;
        }}
        .tab-progress-light {{
            display: inline-block;
            width: 10px; height: 10px;
            border-radius: 50%;
            margin-right: 10px;
            background: #29e74a;
            box-shadow: 0 0 5px 0 #41ec41;
            border: 1.5px solid #b6f7b7;
        }}
        hr {{border-top: 1.5px solid #34363a;}}
        </style>
    """, unsafe_allow_html=True)
   # here The background color was set to black , Hover effects tored on buttons , Output Boxes , Progress Bar Fonts and Extra CSS for Modern Dark look with Fonts matching with the Dark Look 
    
    
    

    if "state" not in st.session_state:
        st.session_state["state"] = {} #Similar to the state in our WorkFlow , st.session_state is the way of Keeping that in memory 
#This Line checks if the State is already There 

    # --- ADDED FOR PROGRESS LIGHT COLOR DYNAMIC CHANGE ---
    if "is_running" not in st.session_state:
        st.session_state["is_running"] = False
    if "code_generation_ready" not in st.session_state:
        st.session_state["code_generation_ready"] = False
    # For regenerate logic after code generation "no"
    if "code_regenerate_needed" not in st.session_state:
        st.session_state["code_regenerate_needed"] = False

    def tab_progress(tab_name):
        color = "#ec4141" if st.session_state.get("is_running", False) else "#1a9c3a"
        light_color = color
        return f"""<div class="tab-progress-box" style="background:{color};border-color:{light_color};">
        <span class="tab-progress-light" style="background:{light_color};border-color:{light_color};"></span>                 
        <span>Active step: <b>{tab_name}</b></span>
        </div>"""

    tab_objs = st.tabs(TABS) #tab init.

except ImportError:
    st = None
    tab_objs = [None]*10   # If The St is missing then 
    
#------------------------------------------------------------------- 


def info_node(state: dict):
    if st and st.session_state.get("use_streamlit_info_node", False): #if the node is active ,
        topic = st.session_state.get("topic_input", "").strip()
    else:
        topic = input("Enter the topic you want to search information about: ").strip() 
    state["topic"] = topic
    
    source = state.get("info_source", "duckduckgo")
    
    if source == "wikipedia":
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        summary = wikipedia.run(topic)
    else:
        url = f"https://api.duckduckgo.com/?q={topic}&format=json"
        response = requests.get(url)
        data = response.json()
        summary = data.get("AbstractText", "No summary found.")
    state["info_summary"] = summary
    state["info_source"] = source
    return state


#-------------------------------------------------------------------


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
                full_response += data["response"]
            if data.get("done", False):
                break
    state["ollama_response"] = full_response
    return state


#-------------------------------------------------------------------



def manual_story_node(state):
    if st and st.session_state.get("use_streamlit_manual_story_node", False):
        story = st.session_state.get("manual_story_input", "")
    else:
        story = input("Please State your Preferred Approach: ")
    state["chosen_story"] = story
    return state


#-------------------------------------------------------------------


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
    payload = {"model": "gemma:2b", "prompt": final_prompt}
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                full_response += data["response"]
            if data.get("done", False):
                break
    state["system_design"] = full_response
    return state


#-------------------------------------------------------------------


def code_generation_node(state):
    if st and st.session_state.get("use_streamlit_code_generation_node", False):
        approval = st.session_state.get("code_generation_approval", "yes")
    else:
        approval = input("Do You want to go ahead with the current System Design = yes\nIf You Want to Go back to the System Design Node = no")
    if approval == "yes":
        prompt = (
            "You are a senior software engineer.\n"
            "Given the system design below, generate the complete and functional code for the core modules and components required.\n\n"
            "Instructions:\n"
            "- Output all code necessary for a working prototype in a single response.\n"
            "- THE CODE SHOULD BE AS BIG AS POSSIBLE ,If the system contains multiple files or modules, output them sequentially with clear file names as comments at the top (e.g., # filename.py).\n"
            "- Do not leave any functions, classes, or main logic as placeholders; implement all key logic so that a beginner can run and understand the code.\n"
            "- Add comments explaining complex sections, but keep the output focused on code only (no explanations outside comments).\n"
            "- Include all necessary import statements and initialization code.\n"
            "- If configuration or environment setup is needed, include it at the top as code comments.\n"
            "- Make sure the output does not stop mid-function or mid-class. Finish all code blocks.\n"
            "- Do not generate test cases or documentation here, But CREATE THE CODE FULLY AND DONOT LEAVE ANY FUNCTIONS EMPTY, I WANT THE CODE TO BE AS BIG AS POSSIBLE Also Keep The Following System Design in Memory.\n\n"
            f"System Design:\n{state['system_design']}\n"
        )
        url = "http://localhost:11434/api/generate"
        payload = {"model": "gemma:2b", "prompt": prompt}
        response = requests.post(url, json=payload, stream=True)
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if "response" in data:
                    full_response += data["response"]
                if data.get("done", False):
                    break
        state["generated_code"] = full_response
        # Reset the regenerate flag
        if st:
            st.session_state["code_regenerate_needed"] = False
        return state
    elif approval == "no":
        if st:
            st.session_state["code_regenerate_needed"] = True
        # Do not call system_design_node(state) directly here; let UI handle it.
        return state
    return state



#-------------------------------------------------------------------



def next_node_after_generation(state):
    if st and st.session_state.get("use_streamlit_next_node_after_generation", False):
        user_choice = st.session_state.get("next_node_after_generation_choice", "")
        if isinstance(user_choice, str):
            user_choice = user_choice.strip()
    else:
        user_choice = input("Enter the number of your choice (one/two/three): ").strip()
    next_node = None
    if user_choice == "one" or user_choice.startswith("Regenerate"):
        next_node = "Code Generation"
    elif user_choice == "two" or user_choice.startswith("Get an explanation"):
        next_node = "Code Explanation"
    elif user_choice == "three" or user_choice.startswith("Go to test"):
        next_node = "Test Cases"
    st.session_state["next_node_after_generation_result"] = next_node
    return state


#-------------------------------------------------------------------


def code_explainer_node(state):
    generated_code = state.get("generated_code", "")
    if not generated_code:
        return state
    prompt = (
        "You are a beginner-friendly coding tutor.\n"
        "Explain the following code step by step, in very simple language.\n"
        "Describe what each function does, how the code works, and the main ideas.\n"
        "Do NOT repeat the code, just explain in plain English and The Code should be explained Line by line .\n\n"
        f"Code:\n{generated_code}\n"
    )
    url = "http://localhost:11434/api/generate"
    payload = {"model": "gemma:2b", "prompt": prompt}
    response = requests.post(url, json=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                full_response += data["response"]
            if data.get("done", False):
                break
    state["code_explanation"] = full_response
    return state


#-------------------------------------------------------------------


def test_case_node(state):
    generated_code = state.get("generated_code","")
    if not generated_code:
        return state
    
    if st and st.session_state.get("use_streamlit_test_case_node", False):
        user_prompt = st.session_state.get("test_case_input", "").strip()
    else:
        user_prompt = input("Any specific Requirements? : \n if Not Continue:").strip()
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
                full_response += data["response"]
            if data.get("done", False):
                break 
    state["test_cases"] = full_response
    return state


#-------------------------------------------------------------------


def requirements_generation_node(state):
    generated_code = state.get("generated_code", "")
    if not generated_code:
        return state
    
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
                full_response += data["response"]
            if data.get("done", False):
                break
    with open("requirements.txt", "w") as f:
        f.write(full_response.strip())
    state["requirements_txt"] = full_response.strip()
    return state


#-------------------------------------------------------------------

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
                full_response += data["response"]
            if data.get("done", False):
                break
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(full_response.strip())
    state["readme"] = full_response.strip()
    return state

# All the nodes same as , WorkFlow

#Now The Tabs Are stated

if st:
    for idx, tab in enumerate(tab_objs):
        with tab:
            st.markdown(tab_progress(TABS[idx]), unsafe_allow_html=True)
            
    
     # Generalised Information For all The tabs:
        #st.tabs() --> Into clear Tabs for all Nodes
        # The * st.session_state preserves the data for users as they move ahead triggering actions 
        # It is a Special Dictionary That helps Retaining and Bringing the Out put to the next State in Sequence If that requires Data from the previous Node/Action
          
        #There are st.buttons to trigger actions
        #st.text_input() --> to take user Input in the form of Text So that,    
        #there are if else statements that triggers when the button is pressed but if the data was not fetched From the Node , it will return error  

        #There are markdownTabs to print the Output After The Defined Buttons state and Results are used for the same logic
        #There are Download Buttons That helps us Download Them in our own directory. or it Automatically Gets Saved in your Working Directory.
        
        
        
    #-----------The Information Tab--------------
    
    with tab_objs[0]: #0th Tab thats info.
        st.session_state["use_streamlit_info_node"] = True
        st.markdown('<div class="section-header">Project Info</div>', unsafe_allow_html=True)
        topic_input = st.text_input("Enter the topic you want to search information about:", key="topic_input")
        info_source = st.selectbox("Choose information source:", ["duckduckgo", "wikipedia"])
        st.session_state["state"]["info_source"] = info_source
        if st.button("Fetch Info", key="fetch_info_btn"):
            with st.spinner("Fetching info..."):
                st.session_state["state"] = info_node(st.session_state["state"])
        if st.session_state["state"].get("info_summary"):
            st.markdown(f'<div class="ai-output">{st.session_state["state"]["info_summary"]}</div>', unsafe_allow_html=True)
            
    
            

    with tab_objs[1]: #next Node's Tab.
        st.session_state["use_streamlit_requirements_node"] = True 
        st.markdown('<div class="section-header">Requirements</div>', unsafe_allow_html=True)
        requirements_topic_input = st.text_input("Enter the project topic for requirements_node, It will be providing you the Approaches ", key="requirements_topic_input")
        if st.button("Submit Requirements", key="submit_reqs_btn"):
            with st.spinner("Generating requirements..."):
                st.session_state["state"] = requirements_node(st.session_state["state"])
        if st.session_state["state"].get("ollama_response"):
            st.markdown(f'<div class="ai-output">{st.session_state["state"]["ollama_response"]}</div>', unsafe_allow_html=True)
            
       
    with tab_objs[2]:
        st.session_state["use_streamlit_manual_story_node"] = True
        st.markdown('<div class="section-header">User Story</div>', unsafe_allow_html=True)
        manual_story_input = st.text_area("Please enter Your Selected Approach:", key="manual_story_input")
        if st.button("Submit Story", key="submit_story_btn"):
            st.session_state["state"] = manual_story_node(st.session_state["state"])
        if st.session_state["state"].get("chosen_story"):
            st.markdown(f'<div class="ai-output">{st.session_state["state"]["chosen_story"]}</div>', unsafe_allow_html=True)
            
            
            

    with tab_objs[3]:
        st.session_state["use_streamlit_system_design_node"] = True
        st.markdown('<div class="section-header">System Design</div>', unsafe_allow_html=True)
        system_design_input = st.text_input("Enter your system design request (e.g., focus on scalability, security, etc.):", key="system_design_input")
        if st.button("Generate Design", key="generate_design_btn"):
            with st.spinner("Generating system design..."):
                st.session_state["state"] = system_design_node(st.session_state["state"])
                st.session_state["code_regenerate_needed"] = False
        # Only show "Regenerate" button if previous code generation was cancelled ("no")
        if st.session_state.get("code_regenerate_needed", False):
            if st.button("Regenerate", key="regenerate_design_btn"):
                with st.spinner("Regenerating system design..."):
                    st.session_state["state"] = system_design_node(st.session_state["state"])
                    st.session_state["code_regenerate_needed"] = False
        if st.session_state["state"].get("system_design"):
            st.markdown(f'<div class="ai-output">{st.session_state["state"]["system_design"]}</div>', unsafe_allow_html=True)
            
            

    with tab_objs[4]:
        st.session_state["use_streamlit_code_generation_node"] = True
        st.markdown('<div class="section-header">Code Generation</div>', unsafe_allow_html=True)
        code_generation_approval = st.radio("Do You want to go ahead with the current System Design?", ["yes", "no"])
        st.session_state["code_generation_approval"] = code_generation_approval
        if st.button("Generate Code", key="generate_code_btn"):
            with st.spinner("Generating code via Ollama Pls Wait..."):
                st.session_state["state"] = code_generation_node(st.session_state["state"])
        code = st.session_state["state"].get("generated_code")
        if code:
            st.code(code, language="python")
            # Display full code in a large, scrollable text area for big outputs
            st.text_area("Full Generated Code (for copy/paste)", value=code, height=800)
            st.download_button("Download generated_code.py", code, "generated_code.py")
            
            

    with tab_objs[5]:
        st.session_state["use_streamlit_next_node_after_generation"] = True
        st.markdown('<div class="section-header">Next Step</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:1.12rem; margin-bottom:1.0em;">What would you like to do next? Choose an action to proceed:</div>',
            unsafe_allow_html=True
        )
        next_options = ["Regenerate the code", "Get an explanation of the generated code", "Go to test cases"]
        next_node_after_generation_choice = st.radio("Next action", next_options, key="next_node_after_generation_choice")
        if st.button("Continue to Next Step", key="continue_nextstep_btn"):
            st.session_state["state"] = next_node_after_generation(st.session_state["state"])
            st.rerun()
    
    
    
    with tab_objs[6]:
        st.session_state["use_streamlit_code_explainer_node"] = True
        st.markdown('<div class="section-header">Code Explanation</div>', unsafe_allow_html=True)
        if st.button("Explain Code", key="explain_code_btn"):
            with st.spinner("Explaining code..."):
                st.session_state["state"] = code_explainer_node(st.session_state["state"])
        code_exp = st.session_state["state"].get("code_explanation")
        if code_exp:
            st.markdown(f'<div class="ai-output">{code_exp}</div>', unsafe_allow_html=True)
            



    with tab_objs[7]:
        st.session_state["use_streamlit_test_case_node"] = True
        st.markdown('<div class="section-header">Test Cases</div>', unsafe_allow_html=True)
        test_case_input = st.text_input("Any specific Requirements? : \n if Not Press Enter", key="test_case_input")
        if st.button("Generate Test Cases", key="generate_testcases_btn"):
            with st.spinner("Generating test cases..."):
                st.session_state["state"] = test_case_node(st.session_state["state"])
        tests = st.session_state["state"].get("test_cases")
        if tests:
            st.markdown(f'<div class="ai-output">{tests}</div>', unsafe_allow_html=True)
            
            
            

    with tab_objs[8]:
        st.markdown('<div class="section-header">Requirements.txt</div>', unsafe_allow_html=True)
        if st.button("Generate requirements.txt", key="generate_reqs_btn"):
            with st.spinner("Generating requirements.txt..."):
                st.session_state["state"] = requirements_generation_node(st.session_state["state"])
        reqs = st.session_state["state"].get("requirements_txt")
        if reqs:
            st.code(reqs, language="text")
            st.download_button("Download requirements.txt", reqs, "requirements.txt")
            
            
            

    with tab_objs[9]:
        st.markdown('<div class="section-header">README.md</div>', unsafe_allow_html=True)
        if st.button("Generate README.md", key="generate_readme_btn"):
            with st.spinner("Generating README.md..."):
                st.session_state["state"] = documentation_node(st.session_state["state"])
        readme = st.session_state["state"].get("readme")
        if readme:
            st.markdown(f'<div class="markdown-preview">{readme}</div>', unsafe_allow_html=True)
            st.download_button("Download README.md", readme, "README.md")
            
            

    st.markdown(f"""
        <hr>
        <center><small>Designed by IshaanNarayanTyagi | {PROJECT_NAME}</small></center>
    """, unsafe_allow_html=True)