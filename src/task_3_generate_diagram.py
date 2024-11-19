import os

from collections import defaultdict
from task_1 import analysis_results


# Sample analysis_results input for demonstration
# analysis_results = {
#     './src/api.py': {
#         'context': ['SemanticSearch'],
#         'relationships': ['SemanticSearch.__init__', 'SemanticSearch.fit', 'SemanticSearch.__call__', 'SemanticSearch.get_text_embedding', 'preprocess', 'pdf_to_text', 'download_pdf', 'load_recommender', 'ask_url', 'text_to_chunks', 'generate_text', 'load_openai_key', 'generate_answer'],
#         'imports': ['os', 're', 'shutil', 'urllib.request', 'pathlib.Path', 'tempfile.NamedTemporaryFile', 'litellm.completion', 'fitz', 'numpy', 'openai', 'tensorflow_hub', 'fastapi.UploadFile', 'lcserve.serving', 'sklearn.neighbors.NearestNeighbors']
#     },
#     './src/app.py': {
#         'context': [],
#         'relationships': ['ask_api'],
#         'imports': ['json', 'tempfile._TemporaryFileWrapper', 'gradio', 'requests']
#     }
# }

def generate_mermaid_class_diagram(analysis_results):
    """
    Generates a Mermaid class diagram from the analysis results of a Python codebase.

    This function constructs a Mermaid class diagram by iterating through the `analysis_results`
    dictionary, creating class representations with their methods, and indicating standalone
    functions and import relationships. The generated diagram can be visualized using Mermaid
    diagram tools.

    Args:
        analysis_results (dict): A dictionary where each key is a file path, and the value
                                 is a dictionary containing analysis details, including:
                                 - 'context': List of class names in the file.
                                 - 'relationships': Set of function and method names.
                                 - 'imports': List of modules imported in the file.

    Returns:
        str: A formatted Mermaid class diagram string representing the structure of the analyzed
             Python codebase.

    Raises:
        None explicitly, but the function assumes that `analysis_results` is well-formed.
    """
    diagram = "classDiagram\n"
    
    for filepath, details in analysis_results.items():
        filename = os.path.splitext(os.path.basename(filepath))[0]

        # Add classes and their methods
        if details['context']:
            for cls in details['context']:
                diagram += f"    class {cls} {{\n"
                # Add only methods that belong to this class
                for func in details['relationships']:
                    if func.startswith(f"{cls}."):
                        method_name = func.split('.')[-1]
                        diagram += f"        +{method_name}()\n"
                diagram += "    }\n"

            # Add a relationship from the file class to the class it contains
            diagram += f"    {filename} -- {details['context'][0]} : contains\n"

        # Represent standalone functions that are not part of any class
        standalone_functions = [
            func for func in details['relationships']
            if '.' not in func
        ]
        if standalone_functions:
            diagram += f"    class {filename} {{\n"
            for func in standalone_functions:
                diagram += f"        +{func}()\n"
            diagram += "    }\n"
        
        # Add import relationships
        for imp in details['imports']:
            imp_clean = imp.split('.')[-1]  # Get the module name only
            diagram += f"    {filename} ..> {imp_clean} : imports\n"

    return diagram

# Generate the Mermaid class diagram from analysis_results
mermaid_diagram = generate_mermaid_class_diagram(analysis_results)
print(mermaid_diagram)

# Save the diagram to a .mmd file for visualization
with open('mermaid_class_diagram_manual.mmd', 'w', encoding='utf-8') as file:
    file.write(mermaid_diagram)

print("Mermaid diagram has been saved to 'mermaid_class_diagram_manual.mmd'.")
