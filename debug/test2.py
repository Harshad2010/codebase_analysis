import ast

# Function to traverse and print the type of each node in the AST
def simple_traverse_node(node, level=0):
    """
    Recursively traverses the AST and prints the type of each node with indentation
    for better visualization.
    
    Args:
        node: The current node to traverse.
        level: The level of indentation for the node (used for nested structures).
    """
    # Print the type of the current node with indentation
    print("  " * level + f"Node type: {type(node).__name__}")

    # Recursively process all child nodes
    for child in ast.iter_child_nodes(node):
        simple_traverse_node(child, level + 1)

# Sample Python code to parse
sample_code = """
class SampleClass:
    def method_one(self):
        print("Hello, World!")
        
    def method_two(self, x):
        return x * 2

def standalone_function(y):
    return y + 10
"""

# Parse the sample code into an AST
tree = ast.parse(sample_code)

# Traverse the AST starting from the root
print("Starting AST traversal:")
simple_traverse_node(tree)
