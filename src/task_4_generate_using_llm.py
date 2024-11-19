import os
import json
import openai

from dotenv import load_dotenv
from task_1 import analysis_results

load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is not set in the environment.")
    exit(1)

openai.api_key = OPENAI_API_KEY

# Convert set objects in analysis_results to lists for JSON serialization
serializable_results = {
    filepath: {
        'context': details['context'],
        'relationships': list(details['relationships']),  # Convert set to list
        'imports': details['imports']
    }
    for filepath, details in analysis_results.items()
}

try:
    # Serialize the updated structure for the prompt
    analysis_summary = json.dumps(serializable_results, indent=2)

    # Refine the prompt for GPT-4
    prompt_generate_diagram = f"""
    Given the following analysis results from a Python codebase, generate a Mermaid class diagram with the following requirements:

    1. Each Python file should be represented as a class only if it contains standalone functions or when no classes are present.
    2. For files containing classes, each class should be represented separately, with its methods listed inside using appropriate visibility symbols (+ for public, # for protected, - for private).
    3. Ensure that methods that are part of a class are not duplicated as standalone functions under the file class.
    4. Standalone functions should be listed under the file class only if they do not belong to any specific class.
    5. Represent imports as relationships using `..>` between the file or class and the imported module, not as members inside the class.

    Use the provided analysis results to format the diagram:

    {analysis_summary}

    Ensure that imports are shown as relationships (e.g., `file ..> module`) and not as members inside the class.
    """

    # Call OpenAI's GPT-4 model to generate the diagram
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_generate_diagram}]
    )

    # Extract and print the Mermaid diagram
    mermaid_diagram = response['choices'][0]['message']['content']
    print(mermaid_diagram)

    # Verify that the diagram matches expectations
    if 'classDiagram' not in mermaid_diagram:
        raise ValueError("The generated output does not contain a valid Mermaid class diagram structure.")

    # Save the generated Mermaid diagram to a file
    with open('mermaid_diagram_from_gpt.mmd', 'w', encoding='utf-8') as file:
        file.write(mermaid_diagram)

    print("Mermaid diagram has been saved to 'mermaid_diagram_from_gpt.mmd'.")

except json.JSONDecodeError as e:
    print(f"JSON serialization error: {e}")
except openai.error.OpenAIError as e:
    print(f"OpenAI API error: {e}")
except IOError as e:
    print(f"File operation error: {e}")
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
