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
    approval = input("Do You want to go ahead with the current System Design Or Should I ReGenerate The System Design")

    if approval ["y", "yes"]:
        prompt = (
            "You are a senior software engineer. Using the following system design, write the core code modules and main functions needed to implement the system. \n\n"
            "Requirements:\n"
            "- Follow best coding practices for organization, readability, and maintainability.\n"
            "- Use modular code structure (split logic into appropriate classes or functions).\n"
            "- Add comments above classes/functions and within complex code sections to explain logic in simple terms.\n"
            "- Include only the code (no explanations outside comments).\n"
            "- Implement realistic function signatures and sample data handling where needed.\n"
            "- If any external dependencies/libraries are needed, show the import statements.\n"
            "- Focus on the essential parts: initialization, data flow, major interactions, and how components connect.\n"
            "- If the system requires configuration or environment setup, include a section of code for that.\n"
            "- Do not generate test cases, documentation, or deployment scripts in this output.\n"
            "- Assume the code will be reviewed by a beginner; prioritize clarity.\n\n"
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
    else:
        print("Regenerating system design as per your request...")
        # Optionally allow the user to revise the design request
        state = system_design_node(state)
        return code_generation_node(state)
        
























# if __name__ == "__main__":
#     # User can specify 'info_source' as 'wikipedia' or leave it out for DuckDuckGo
#     state = {"topic": "SDLC"}  # Try adding "info_source": "wikipedia" to use Wikipedia
#     state = info_node(state)
#     print(f"Summary from {state['info_source'].capitalize()}:")
#     print(state["info_summary"])



# if __name__ == "__main__":
#     state = {}
#     state = requirements_node(state)       # 1. Get requirements from LLM
#     state = manual_story_node(state)       # 2. User enters a story (manual input)
#     state = system_design_node(state)      # 3. Get system design from LLM

#     print("\n--- Final System Design ---")
#     print(state["system_design"])
