import requests
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def info_node(state: dict):
    # Ask the user for the topic to search
    topic = input("Enter the topic you want to search information about: ").strip()
    state["topic"] = topic

    source = state.get("info_source", "duckduckgo")  # Default is duckduckgo

    if source == "wikipedia":
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        summary = wikipedia.run(topic)
    else:  # Default to duckduckgo
        url = f"https://api.duckduckgo.com/?q={topic}&format=json"
        response = requests.get(url) #get and post methods of Http
        data = response.json() # summary is saved as data
        summary = data.get("AbstractText", "No summary found.") # get method saved the Summary as Abstract Text. and if Summary is Not Found then The text , no Summary found will be Printed.

    state["info_summary"] = summary #state is dictionary and Summary is stores here 
    state["info_source"] = source # Source of the Summary is Stored here 
    return state #State Is the Dictionary 

##############################################################################################################################################################



import requests
import json

def requirements_node(state):
    # Ask only for the topic from the user
    topic = input("Enter the project topic").strip() #Strip will remove all the unnecessary spaces From here 
    
    #This is The default Prompt That will be given to the LLM model along with the topic taken as input above
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
    state["requirements"] = requirements #requirements are the promopt That will be Given to the LLm to generate the Stories/Approaches this will be COunted as User Requiremnts 

    url = "http://localhost:11434/api/generate" #ollama Localhost Server url to send the LLM Request 
    payload = {
        "model": "gemma:2b", #gemma is the Google's LLM group of Models
        "prompt": requirements #Prompt to the LLM will be defined by requiremnts and topic will be asked by the user
    }
    response = requests.post(url, json=payload, stream=True) #sends a post request to ollama , payload=json means that data needs to be in json format

    # Ollama streams responses as JSON Lines (one JSON object per line)
    
    
    full_response = "" #here the response will be appened and Stored
    
    for line in response.iter_lines():  #Loop Starts To append the result to the "Full_response"
        if line:
            data = json.loads(line.decode('utf-8')) #the the fetched file is present in the form of bytes now we will be convrted to String Format
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break
    print()  # for a clean new line at the end
    state["ollama_response"] = full_response #prininting the ollama Response (Whole)
    return state

##############################################################################################################################################################



def manual_story_node(state): #Simple Human intervention node to Choose the story , according to This Story The Tech Detail will be Genrated by the Model
    story = input("Please enter your story: ")
    state["chosen_story"] = story
    return state

import requests
import json


##############################################################################################################################################################

def system_design_node(state):
    story = state["chosen_story"]
    user_prompt = input("Enter your system design request (e.g., focus on scalability, security, etc.): ") #user now will be choosing the story and the 

    # Combine story and user prompt into one prompt for the LLM model gemma 
    final_prompt = (
        f"Given the following story, design a software system based on this additional request.\n\n"
        f"Story:\n{story}\n\n"
        f"User Request:\n{user_prompt}\n\n"
        f"Please provide details on system components, data flow, and user interactions, How this can be made, how much time will it take to test the code and stuff. Be Clear and Precise "
    ) #story along with the new promopt Will be shared with the LLM.

    url = "http://localhost:11434/api/generate" #Url to transfer the calls on the Local host Url where Ollama Model is running 
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
                break   # updatin the full response again 
            
    print()  # for output formatting
    state["system_design"] = full_response
    return state

##############################################################################################################################################################



def code_generation_node(state):
    print("The SystemDesign for the Requiremnent are as follows ")
    print(state["system_design"])
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
)       #the prompt will Serve as a text that will be passed to the LLM Via tha api call and the prompt will be Generating the output as a code.
        
        
        
    # elif approval == "no":
    #     print("-Regenerating the System Design-")
    #     state = system_design_node(state)
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "gemma:2b",
            "prompt": prompt
        } #this is used to call the Ollama APi running on the Local host.
        
        
        response = requests.post(url, json=payload, stream=True) #Fetch the response in the form of json
        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                if "response" in data:
                    print(data["response"], end='', flush=True)
                    full_response += data["response"]
                if data.get("done", False):
                    break
        print()  # for output formatting
        state["generated_code"] = full_response
        print("\n--- Generated Code ---")
        print(full_response)
        return state
    elif approval == "no":
        print("Regenerating system design as per your request...")
        # Optionally allow the user to revise the design request
        state = system_design_node(state)
    state = next_node_after_generation(state)
    return state
    
################################################################################################################################################################   
    
def next_node_after_generation(state):  #This node will be asking the user if the User wants to Regenerate The code or Go ahead with the Current Code
    generated_code = state.get("generated_code", "")
    print("\nWhat would you like to do next?")
    print("1. Regenerate the code, if The Code is not Up to The mark")
    print("2. Get an explanation of the Generated code")                      # These Will serve as the choices for the User to choose fROM
    print("3. Go to the next node in sequence, That is ")
    user_choice = input("Enter the number of your choice (one/two/three): ").strip()
     
    if user_choice == "one":
        print("Taking back to the Code generation Node" "\n")
        state = code_generation_node(state)
         
    elif user_choice == "two":
        state = code_explainer_node(state)                  # THESE ARE THE ACTIONS ASSOCIATED WITH THE CHOICES PRESENT WITH THE USERS
        print("Explaining The code provided -->" "\n")
        print(state.get("code_explanation"))
        
    elif user_choice == "three":
        print("nothing Yet , tbc")      
    return state

##############################################################################################################################################################

                
def code_explainer_node(state):
    generated_code = state.get("generated_code", "")
    if not generated_code:
        print("No code found.")
        return state 
    
    prompt = (
        "You are a beginner-friendly coding tutor.\n"                             #THIS IS THE PROMPT THAT WILL BE PROVIDED TO THE MODEL ALONG WITH THE GENERATED CODE THAT WAS GENERATED BY THE LLM EARLIER 
        "Explain the following code step by step, in very simple language.\n"
        "Describe what each function does, how the code works, and the main ideas.\n"
        "Do NOT repeat the code, just explain in plain English and The Code should be explained Line by line .\n\n"
        f"Code:\n{generated_code}\n"  #THIS IS THE GENERATED CODE VAR
    )
      
      
    url = "http://localhost:11434/api/generate"   # SAME AGAIN THE LOCAL HOST API CALL to Let Gemma Do the task
    payload = {
        "model": "gemma:2b",        # SMALL MODEL WITH 2 BILLION PARAMATERS
        "prompt": prompt
    }
    
    response = requests.post(url, json=payload, stream=True)      #RESPONSE WILL BE FETCHED BY THE REQUENTS , AND IN THE FORM OF JSON 
    full_response = ""   #HERE ALL WILL BE ADDED TO VIA THA FOR LOOP PRESENT DOWNSIDE 
    
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
    
    proper_code = input("was The Code Explanation Proper as per Your Requiremnt? (zero:imProper) , (one:✅)")
    if proper_code =="zero":
        print("Regenerating the Code Explanation Again,Provide the Approval Again")
        state = next_node_after_generation(state)
        return next_node_after_generation(state)
        
    elif proper_code == "one":
        print("Lets Get to the Next State , Where You Can Generate The Test Cases For Your Chosen Code:")
        state = test_case_node(state)
    return state


##############################################################################################################################################################


def test_case_node(state):
    print("Lets Generate The Test Cases For The Above Code, Provide Your Prompt Along With your Code:")
    generated_code = state.get("generated_code","")
    if not generated_code:
        print("*Code Not Found")
        return state
    
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
    print("the Generated Test Cases are:")
    print(full_response)
    print("Test cases Done")
    return state

##############################################################################################################################################################



def requirements_generation_node(state):
    generated_code = state.get("generated_code", "")
    if not generated_code:
        print("Code Not Found")

        
    print("Gettin Your Code to Generate The Requirements to Execute The Code:")
    
    #The prompt Will be Provided to the ollama LLM
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
        
    response = requests.post(url, json=payload, stream=True) #Similar to all the other Nodes till now , 
    full_response = "" #Will be added to this Variable Then
    
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                print(data["response"], end='', flush=True)    #THIS WILL FETCH THE INFORMATION AND ADD IT TO THE full_response
                full_response += data["response"]
            if data.get("done", False):
                break
    print("\n")
    
    
    with open("requirements.txt", "w") as f:
        f.write(full_response.strip())
    print("Requirements saved to requirements.txt")

    state["requirements_txt"] = full_response.strip()
    return state

##############################################################################################################################################################


def documentation_node(state):
    info_summary = state.get("info_summary", "")
    system_design = state.get("system_design", "")      #These are the Variables That are Required to Generate The documentation/Readme can be made and downloaded as .md format.
    requirements_txt = state.get("requirements_txt", "")
    generated_code = state.get("generated_code", "")
    
    
    
    #This will be The Prompt For The Ollama Api 
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
    

    print("Downloading the Readme.md file in your Current Workflow Folder:")
    
 
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(full_response.strip())
    print("README.md saved.")

    state["readme"] = full_response.strip()
    return state


############################################################################################################################################################## 

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
    "documentation_node",
    "readme.md_node"
]

edges = [
    ("info_node", "requirements_node"),
    ("requirements_node", "manual_story_node"),
    ("manual_story_node", "system_design_node"),
    ("system_design_node", "code_generation_node"),
    ("code_generation_node", "next_node_after_generation"),
    ("next_node_after_generation", "code_generation_node"),      # Regenerate code (loop)
    ("next_node_after_generation", "code_explainer_node"),       # Explanation                 #As these are the Repeative steps that Reqire Going Up and Down via edges
    ("next_node_after_generation", "test_case_node"),            # Proceed to test cases
    ("code_explainer_node", "test_case_node"),
    ("test_case_node", "requirements_generation_node"),
    ("requirements_generation_node", "documentation_node"),
]

# G = nx.DiGraph()
# G.add_nodes_from(steps)
# G.add_edges_from(edges)

# plt.figure(figsize=(13, 8))
# pos = nx.spring_layout(G, seed=42)
# nx.draw(G, pos, with_labels=True, node_color='white', node_size=3000, arrowsize=30, font_size=12)
# plt.title("Generative AI Workflow Graph")
# plt.show()

def main():
    state = {}

    print("\n--- Info Node ---")
    state = info_node(state)
    print("\n--- Info Summary ---")
    print(state.get("info_summary", "No summary found."))

    print("\n--- Requirements Node ---")
    state = requirements_node(state)
    # print("\n--- Requirements Prompt ---")
    # print(state.get("requirements", "No requirements prompt generated."))

    print("\n--- Manual Story Node ---")
    state = manual_story_node(state)
    print("\n--- Chosen Story ---")
    print(state.get("chosen_story", "No story chosen."))

    print("\n--- System Design Node ---")
    state = system_design_node(state)
    print("\n--- System Design ---")
    print(state.get("system_design", "No system design generated."))

    print("\n--- Code Generation Node ---")
    state = code_generation_node(state)
    print("\n--- Generated Code ---")
    print(state.get("generated_code", "No code generated."))

    print("\n--- Next Node After Generation ---")
    state = next_node_after_generation(state)

    print("\n--- oneCode Explainer Node ---")
    state = code_explainer_node(state)
    print("\n--- Code Explanation ---")
    print(state.get("code_explanation", "No explanation generated."))

    print("\n--- Test Case Node ---")
    state = test_case_node(state)
    print("\n--- Test Cases ---")                                                               #THIS IS FOR USING THE APP IN THE TERMINAL 
    print(state.get("test_cases", "No test cases generated."))

    print("\n--- Requirements Generation Node ---")
    state = requirements_generation_node(state)
    print("\n--- Requirements.txt ---")
    print(state.get("requirements_txt", "No requirements generated."))

    print("\n--- Documentation Node ---")
    state = documentation_node(state)
    print("\n--- README.md ---")
    print(state.get("readme", "No documentation generated."))

    print("\n--- Workflow done! ---")

if __name__ == "__main__":
    main()

