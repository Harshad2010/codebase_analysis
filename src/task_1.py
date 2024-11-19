import os
import ast

from collections import Counter, defaultdict

# Dictionary to store context, relationships, imports, and function call references for each file
analysis_results = defaultdict(lambda: {
    'context': [],
    'relationships': set(),
    'imports': [],
    'function_calls': Counter(),  
    'node_type_counts': Counter()
})

# Function to parse a Python file and extract detailed information
def analyze_file(file_path):
    """
    Analyzes a Python file and extracts detailed information about its structure.

    This function reads a Python file, parses it into an Abstract Syntax Tree (AST),
    and traverses the tree to extract information such as class and function definitions,
    import statements, and function call occurrences. The results are stored in a global
    dictionary for later use in analysis or diagram generation.

    Args:
        file_path (str): The path to the Python file to be analyzed.

    Returns:
        None. The function updates the global `analysis_results` dictionary with:
            - 'context': A list of class names found in the file.
            - 'relationships': A set of function relationships (methods and standalone functions).
            - 'imports': A list of modules and elements imported in the file.
            - 'function_calls': A Counter object with the frequency of function calls.
            - 'node_type_counts': A Counter object with the frequency of AST node types.

    Raises:
        Prints error messages if the file cannot be opened or parsed due to I/O errors or
        syntax errors.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
    except IOError as e:
        print(f"Error opening file {file_path}: {e}")
        return

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax error in file {file_path}: {e}")
        return

    relationships = set()
    context = []
    imports = []
    function_calls = Counter()  # Use Counter for frequency analysis
    node_type_counts = Counter()

    def traverse_node(node, current_class=None):
        try:
            # Count the node type
            node_type_counts[type(node).__name__] += 1

            # Extract function definitions with class context
            if isinstance(node, ast.FunctionDef):
                func_name = f"{current_class}.{node.name}" if current_class else node.name
                relationships.add(func_name)

            # Extract class definitions and traverse its body
            if isinstance(node, ast.ClassDef):
                context.append(node.name)
                for child in node.body:
                    traverse_node(child, current_class=node.name)

            # Extract import statements
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append(f"{node.module}.{alias.name}" if node.module else alias.name)

            # Extract function calls and count their occurrences
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    function_calls[node.func.id] += 1
                elif isinstance(node.func, ast.Attribute):
                    function_calls[node.func.attr] += 1

            # Recursively process child nodes
            for child in ast.iter_child_nodes(node):
                traverse_node(child, current_class)
        except Exception as e:
            print(f"Error processing node in file {file_path}: {e}")
    
    traverse_node(tree)
    analysis_results[file_path] = {
        'context': context,
        'relationships': filter_class_methods(relationships),
        'imports': imports,
        'function_calls': function_calls,
        'node_type_counts': node_type_counts
    }
    
def filter_class_methods(relationships):
    """
    Filters out standalone method names from the relationships set if their class-qualified
    counterparts exist.

    This function identifies methods that are both standalone and part of a class and removes
    the standalone version when a class-qualified version exists. This helps maintain clarity
    by ensuring that only the class-specific representation is kept when both forms are present.

    Args:
        relationships (set): A set containing method names, both standalone (e.g., 'method_name')
                             and class-qualified (e.g., 'ClassName.method_name').

    Returns:
        set: A filtered set containing only the class-qualified method names and standalone
             method names that do not have a class-qualified counterpart.
    """
    # Create a set to store standalone method names
    standalone_methods = {method for method in relationships if '.' not in method}
    
    # Create a set to store class-qualified method names
    class_methods = {method.split('.')[-1] for method in relationships if '.' in method}

    # Remove standalone methods that are associated with a class-qualified method
    filtered_relationships = {
        method for method in relationships
        if '.' in method or method not in class_methods
    }
    
    return filtered_relationships

def analyze_codebase(directory_path):
    """
    Analyzes all Python files in a given directory and its subdirectories.

    This function walks through a directory tree, identifies Python files, and calls
    the `analyze_file` function on each one to extract structural information and
    update the global `analysis_results` dictionary with details from each file.

    Args:
        directory_path (str): The path to the directory containing Python files to be analyzed.

    Returns:
        None. The function iterates through the directory and calls `analyze_file` on each
        Python file, storing analysis results globally.
    """
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                analyze_file(os.path.join(root, file))

def compare_and_print_common_functions(analysis_results):
    """
    Compares the relationships (functions) between two Python files and prints the common functions.

    This function takes the analysis results from multiple Python files and checks for
    common functions between the first two files in the results. If there are common
    functions, it prints them; otherwise, it indicates that there are no common functions.

    Args:
        analysis_results (dict): A dictionary where each key is a file path, and the value
                                 is a dictionary containing analysis details, including
                                 'relationships' which is a set of function names.

    Returns:
        str: A message indicating the common functions between the first two files or
             stating that there are no common functions. If there is a KeyError, it returns
             an error message.
    """
    keys = list(analysis_results.keys())
    if len(keys) > 1:
        try:
            common_functions = analysis_results[keys[0]]['relationships'].intersection(analysis_results[keys[1]]['relationships'])
            if common_functions:
                return f"\nCommon functions between '{os.path.basename(keys[0])}' and '{os.path.basename(keys[1])}': {common_functions}"
            else:
                return f"\nThere are no common functions between '{os.path.basename(keys[0])}' and '{os.path.basename(keys[1])}'."
        except KeyError as e:
            return f"Error comparing functions: {e}"
    else:
        return "Not enough files to compare functions."

codebase_path = './codebase_files'
analyze_codebase(codebase_path)

# Print summary of analysis
print("\nSummary of analysis:")
for file, data in analysis_results.items():
    print(f"\nFile: {file}")
    print(f"\nContext (Classes): {data['context']}")
    print(f"\nRelationships (Functions): {data['relationships']}")
    print(f"\nImports: {data['imports']}")
    print(f"\nFunction Calls (with Frequencies): {dict(data['function_calls'])}")
    print(f"\nNode Type Counts: {dict(data['node_type_counts'])}")

common_functions = compare_and_print_common_functions(analysis_results)
print(f"\nCommon functions: {common_functions}")
