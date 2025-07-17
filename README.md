# LangGraph‑SDLC‑Automation 🚀

## 🖼️ Project Snapshots

<table>
  <tr>
    <td><img src="Screenshot 2025-07-14 162738.png" width="350"/></td>
    <td><img src="Screenshot 2025-07-14 163047.png" width="350"/></td>
  </tr>
  <tr>
    <td><img src="Screenshot 2025-07-14 163057.png" width="350"/></td>
    <td><img src="Screenshot 2025-07-16 164837.png" width="350"/></td>
  </tr>
</table>

An intelligent SDLC automation assistant built with `LangGraph` and LLM agents, designed to streamline software development processes — from idea to code. This tool walks the user through requirement gathering, technical system design, and code generation using LLMs and interactive nodes.

---

## 📌 Features Implemented (So Far)

This project automates the early phases of the Software Development Life Cycle (SDLC) using a graph-based workflow. Current flow includes:

1. **Information Gathering (via Wikipedia or DuckDuckGo)**
2. **Requirement Generation with LLM (Ollama + Gemma)**
3. **Manual Story Selection**
4. **System Design Generation using LLM**
5. **Code Generation from Approved System Design**
6. **Optional: Code Explanation in Beginner-Friendly Language**
7. **Test Case Generation**
8. **Requirements.txt Generation**
9. **README.md Generation**
10. **Modular Nodes for Workflow Extension**

---

## 🔁 Current Workflow Stages

Each step in the workflow is executed via a function-based node that modifies and updates a shared `state` dictionary.

### 🧠 1. `info_node()`
- Asks user for a topic.
- Fetches basic summary from:
  - `DuckDuckGo API` (default)
  - `Wikipedia` via `langchain_community`

### 📋 2. `requirements_node()`
- Asks for the project topic.
- Sends a prompt to a local LLM (`gemma:2b` via Ollama).
- Returns **3 high-level approaches** for the project idea.

### ✍️ 3. `manual_story_node()`
- Allows the user to select one of the approaches or write their own.

### 🧩 4. `system_design_node()`
- Uses the selected story and an additional design prompt.
- Generates a **detailed system design** including:
  - Components
  - Architecture
  - Data flow
  - Testing/validation notes

### 💻 5. `code_generation_node()`
- Takes the system design and prompts the LLM to generate **working prototype-level code**.
- Adds options for user approval or revisiting system design.

### 🔄 6. `next_node_after_generation()`
- Offers user options:
  - Regenerate code
  - Explain the code
  - Go to test cases

### 📖 7. `code_explainer_node()`
- Explains the generated code in **very simple English**.
- Designed for beginners and educational use.

### 🧪 8. `test_case_node()`
- Generates test cases for the produced code.
- Focuses on unit tests and edge case coverage.
- User can provide specific requirements for test coverage.

### 📦 9. `requirements_generation_node()`
- Analyzes the generated code and outputs a `requirements.txt` with all needed pip packages.
- Ignores standard library modules.

### 📝 10. `documentation_node()`
- Produces a beginner-friendly `README.md` file.
- Includes project summary, setup steps, how to run, and usage notes.

---

## ⚙️ Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally
- LangChain and LangGraph-related dependencies

Install required Python packages:

```bash
pip install langchain langchain-community requests
