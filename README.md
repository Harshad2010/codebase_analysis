# CodeBase-Analysis

Following are the python file structure for the task given:

1. src - folder contains all the four tasks file.
2. env contains openai API secret key - enter your secrets.
3. codebase file are the input files given by you.
3. output folder contains all the json file of QA as asked.
4. Mermaid diagrams codefiles present in .mmd format.
5. Mermaid diagrrams HTML document and reference image from visualizer.
5. please folow the below steps for executing the code.

### STEP 01- Navigate to codebase and Create a conda environment after opening the repository

```bash
cd codebase
```

```bash
conda create -n llmapp python=3.10 -y
```

```bash
conda activate llmapp
```

### STEP 02- install the requirements

```bash
pip install -r requirement.txt
```

### STEP 03- Start running the python files in this order.

#### TASK-1
```bash
python src/task_1.py 
```

#### TASK-2
```bash
python src/task_2.py
```

#### TASK-3
```bash
python src/task_3_generate_diagram.py
```
#### TASK-4
```bash
python src/task_4_generate_using_llm.py
```