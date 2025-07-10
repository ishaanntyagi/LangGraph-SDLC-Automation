import requests
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def info_node(state: dict):
    topic = state["topic"]
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

# if __name__ == "__main__":
#     # User can specify 'info_source' as 'wikipedia' or leave it out for DuckDuckGo
#     state = {"topic": "LangChain"}  # Try adding "info_source": "wikipedia" to use Wikipedia
#     state = info_node(state)
#     print(f"Summary from {state['info_source'].capitalize()}:")
#     print(state["info_summary"])

import requests
import json

def requirements_node(state):
    # Ask only for the topic from the user
    topic = input("Enter the project topic (e.g., food website): ").strip()
    
    # Set the default prompt using the topic
    requirements = (
    f"You are a senior technical strategist. I am planning to build a project on the topic: '{topic}'. "
    f"Give me 3 different high-level approaches for how this project can be developed. "
    f"Each approach must be unique and include:\n"
    f"1. The goal or problem being solved\n"
    f"2. A creative and practical solution idea\n"
    f"3. The suggested tech stack or tools that would fit best\n"
    f"Focus on clarity and variety — I want distinctly different ways to build this project. "
    f"Do not include any code. These ideas will be shared with the Technical Design team for evaluation."
)   
    state["requirements"] = requirements

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": requirements
    }
    response = requests.post(url, json=payload, stream=True)

    # Ollama streams responses as JSON Lines (one JSON object per line)
    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            # Each 'data' is a partial response; the 'response' key has the generated text so far
            if "response" in data:
                print(data["response"], end='', flush=True)
                full_response += data["response"]
            if data.get("done", False):
                break
    print()  # for a clean new line at the end
    state["ollama_response"] = full_response
    return state


def manual_story_node(state):
    story = input("Please enter your story: ")
    state["chosen_story"] = story
    return state


import requests
import json

def system_design_node(state):
    story = state["chosen_story"]
    user_prompt = input("Enter your system design request (e.g., focus on scalability, security, etc.): ")

    # Combine story and user prompt into one prompt for the LLM
    final_prompt = (
        f"Given the following story, design a software system based on this additional request.\n\n"
        f"Story:\n{story}\n\n"
        f"User Request:\n{user_prompt}\n\n"
        f"Please provide details on system components, data flow, and user interactions."
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
    print()  # for output formatting
    state["system_design"] = full_response
    return state



# if __name__ == "__main__":
#     state = {}
#     state = requirements_node(state)       # 1. Get requirements from LLM
#     state = manual_story_node(state)       # 2. User enters a story (manual input)
#     state = system_design_node(state)      # 3. Get system design from LLM

#     print("\n--- Final System Design ---")
#     print(state["system_design"])