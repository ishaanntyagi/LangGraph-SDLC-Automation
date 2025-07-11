import requests
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

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
        "model": "gemma:2b", #gemma is the Googles LLM group
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
    state["ollama_response"] = full_response #prininting the ollama Response (Whole )
    return state


def manual_story_node(state): #Simple Human intervention node to Choose the story , according to This Story The Tech Detail will be Genrated by the Model
    story = input("Please enter your story: ")
    state["chosen_story"] = story
    return state


import requests
import json

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
        "- Do not generate test cases or documentation here.\n\n"
        f"System Design:\n{state['system_design']}\n"
)       #the prompt will Serve as a text that will be passed to the LLM Via tha api call and the prompt will be Generating the output as a code.
        
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
        print()  # for output formatting
        state["generated_code"] = full_response
        print("\n--- Generated Code ---")
        print(full_response)
        return state
    elif approval == "no":
        print("Regenerating system design as per your request...")
        # Optionally allow the user to revise the design request
        state = system_design_node(state)
        return code_generation_node(state) #✅
    
    
    
def next_node_after_generation(state):
    generated_code = state.get("generated_code", "")
    print("\nWhat would you like to do next?")
    print("1. Regenerate the code, if The Code is not Up to The mark")
    print("2. Get an explanation of the Generated code")
    print("3. Go to the next node in sequence, That is ")
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
        "Do NOT repeat the code, just explain in plain English.\n\n"
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
    return state 

    
    
if __name__ == "__main__":
    state = {}
    # DuckDuckGo/Wikipedia info node
    info_choice = input("Do you want to fetch info from Wikipedia or DuckDuckGo? (Type 'wikipedia' or 'duckduckgo'): ").strip().lower()
    if info_choice in ["wikipedia", "duckduckgo"]:
        state["info_source"] = info_choice
    state = info_node(state)
    print(f"Summary from {state['info_source'].capitalize()}:")
    print(state["info_summary"])

    state = requirements_node(state)       
    state = manual_story_node(state)       
    state = system_design_node(state)      

    print("\n--- Final System Design ---")
    print(state["system_design"])

    # 4. Generate code from approved system design
    state = code_generation_node(state)    # 4. Generate code with approval

    print("\n--- Generated Code ---")
    print(state.get("generated_code", "No code generated."))

    #This Node will be Providing The Option if user Wants to choose b 1/2/3 so that the Node can Work Accordingly 
    state = next_node_after_generation(state)
