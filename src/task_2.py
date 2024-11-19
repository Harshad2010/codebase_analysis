import os
import json
import openai

from dotenv import load_dotenv
from prompts import prompt_template
from task_1 import analysis_results, common_functions

load_dotenv()

# Set up OpenAI API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is not set in the environment.")
    exit(1)

openai.api_key = OPENAI_API_KEY

def create_prompt(file_key, question, analysis_results):
    """
    Creates a formatted prompt using data from a specific Python file's analysis results.

    This function extracts context (classes), relationships (functions/methods), and imports
    for a given Python file from the `analysis_results` dictionary. It formats these details
    along with a given question into a prompt using a predefined template.

    Args:
        file_key (str): The key representing the file path in the `analysis_results` dictionary.
        question (str): The question or instruction to include in the prompt.
        analysis_results (dict): A dictionary where each key is a file path, and the value
                                 is a dictionary containing analysis details such as 'context',
                                 'relationships', and 'imports'.

    Returns:
        str or None: A formatted prompt string containing the file name, context, relationships,
                     imports, and question. If a `KeyError` occurs, prints an error message and
                     returns `None`.

    Raises:
        KeyError: Prints an error message if the `file_key` does not exist in `analysis_results`.
    """
    try:
        file_name = os.path.basename(file_key)  # Extract just the file name for display
        # Extract relevant data for the specific .py file mentioned
        analysis_data = {
            "context": ", ".join(analysis_results[file_key]["context"]),
            "relationships": ", ".join(analysis_results[file_key]["relationships"]),
            "imports": ", ".join(analysis_results[file_key]["imports"])  # Join imports into a single string
        }
        # Format the prompt with the extracted data and the question
        return prompt_template.format(
            file_name=file_name,
            context=analysis_data["context"] if analysis_data["context"] else "No classes",
            relationships=analysis_data["relationships"] if analysis_data["relationships"] else "No functions/methods",
            imports=analysis_data["imports"] if analysis_data["imports"] else "No imports",
            common_functions = common_functions,
            question=question
        )
    except KeyError as e:
        print(f"Key error: {e} - Check the structure of the analysis results or file_key.")
        return None

def ask_question_and_save(question):
    """
    Sends a question to the OpenAI GPT-4 model and saves the response to a JSON file.

    This function interacts with the OpenAI API to get a response for a given question.
    It increments a global question counter, sends the question to the model, and saves
    both the question and the response to a JSON file in an 'output' directory.

    Args:
        question (str): The question or prompt to send to the OpenAI GPT-4 model.

    Returns:
        None. The function prints a success message when the response is saved and an error
        message if there is a failure.

    Raises:
        Exception: Prints an error message if the request to OpenAI API fails or if there is
                   an issue with file operations (e.g., writing to a file).
    """

    global question_number
    question_number += 1  # Increment the counter for each new question
    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            temperature=0  
        )
        answer = response['choices'][0]['message']['content']
        # answer = "manually written"
        

        # Ensure the output folder exists
        os.makedirs('output', exist_ok=True)

        # Construct the filename using the incremented counter
        output_filename = f'output/question_{question_number}.json'

        # Save the response in a JSON file
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump({"question": user_input, "answer": answer}, f, ensure_ascii=False, indent=4)

        print(f"Response has been saved in '{output_filename}'.")
    except Exception as e:
        print(f"Failed to save or retrieve response: {e}")

def process_user_question(user_question):
    """
    Processes a user question to find the relevant Python file and generates a prompt for OpenAI.

    This function searches through the `analysis_results` dictionary to find a matching Python file
    based on the filename mentioned in the `user_question`. If a matching file is found, it calls
    `create_prompt` to generate a prompt with analysis details and then sends it to OpenAI using
    `ask_question_and_save`.

    Args:
        user_question (str): The question or input provided by the user that should refer to a
                             specific Python file (e.g., 'api.py' or 'app.py').

    Returns:
        None. The function prints an error message if no matching file is found or if the question
        is not associated with a specific file.

    Raises:
        None explicitly, but prints an error if the `file_key` is not found or if `create_prompt`
        returns `None`.
    """
    file_key = None
    for file_path in analysis_results.keys():
        file_name = os.path.basename(file_path).lower()
        if file_name in user_question.lower():
            file_key = file_path
            break

    if not file_key:
        print("Error: The question must refer to a specific .py file (e.g., 'api.py' or 'app.py').")


    prompt = create_prompt(file_key, user_question, analysis_results)
    if prompt:
        ask_question_and_save(prompt)

# Initialize a static counter
question_number = 0
try:
    user_input = input("Please enter your question: ")
    process_user_question(user_input)
except Exception as e:
    print(f"An error occurred while processing the question: {e}")
