from Workflow import (
    info_node,
    requirements_node,
    manual_story_node,
    system_design_node,
    code_generation_node,
    next_node_after_generation,
    code_explainer_node,
    test_case_node,
    requirements_generation_node,
    documentation_node
)

def main():
    state = {}

    print("\n--- Step 1: Info Node ---")
    state = info_node(state)
    print("\n--- Info Summary ---")
    print(state.get("info_summary", "No summary found."))

    print("\n--- Step 2: Requirements Node ---")
    state = requirements_node(state)
    print("\n--- Requirements Prompt ---")
    print(state.get("requirements", "No requirements prompt generated."))

    print("\n--- Step 3: Manual Story Node ---")
    state = manual_story_node(state)
    print("\n--- Chosen Story ---")
    print(state.get("chosen_story", "No story chosen."))

    print("\n--- Step 4: System Design Node ---")
    state = system_design_node(state)
    print("\n--- System Design ---")
    print(state.get("system_design", "No system design generated."))

    print("\n--- Step 5: Code Generation Node ---")
    state = code_generation_node(state)
    print("\n--- Generated Code ---")
    print(state.get("generated_code", "No code generated."))

    print("\n--- Step 6: Next Node After Generation ---")
    state = next_node_after_generation(state)

    print("\n--- Step 7: Code Explainer Node ---")
    state = code_explainer_node(state)
    print("\n--- Code Explanation ---")
    print(state.get("code_explanation", "No explanation generated."))

    print("\n--- Step 8: Test Case Node ---")
    state = test_case_node(state)
    print("\n--- Test Cases ---")
    print(state.get("test_cases", "No test cases generated."))

    print("\n--- Step 9: Requirements Generation Node ---")
    state = requirements_generation_node(state)
    print("\n--- Requirements.txt ---")
    print(state.get("requirements_txt", "No requirements generated."))

    print("\n--- Step 10: Documentation Node ---")
    state = documentation_node(state)
    print("\n--- README.md ---")
    print(state.get("readme", "No documentation generated."))

    print("\n--- Workflow Complete! ---")

if __name__ == "__main__":
    main()