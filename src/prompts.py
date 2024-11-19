

# Template for a prompt that guides the LLM to use only relevant .py file data

prompt_template = """
Given the analysis results from the file '{file_name}', please answer the question based only on the provided data.

Details from file '{file_name}':
- Classes: {context}
- Functions and Methods: {relationships}
- Imports: {imports}
- CommonFunctions : {common_functions}

Question: {question}

Please use only the details provided above to formulate your response.
"""


