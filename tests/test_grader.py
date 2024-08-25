import lambdagrader
import nbformat
from nbclient import NotebookClient
import os
from pathlib import Path
import shutil
import json
import hashlib
import sys
import platform

graded_results = []
file_index = 0

TEST_NOTEBOOKS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test-notebooks',
)

notebook_path = os.path.join(TEST_NOTEBOOKS_DIR, 'test-file.ipynb')

print('=============================')
nb = nbformat.read(notebook_path, as_version=4)

test_cases_hash = lambdagrader.get_test_cases_hash(nb)

lambdagrader.preprocess_test_case_cells(nb)
lambdagrader.add_grader_scripts(nb)

p = Path(notebook_path)
filestem = p.name

print(f'Grading {notebook_path}')

client = NotebookClient(
    nb,
    timeout=600,
    kernel_name='python3',
    allow_errors=True
)
client.execute()

# save graded notebook
converted_notebook_path = notebook_path.replace('.ipynb', '-graded.ipynb')
with open(converted_notebook_path, mode='w', encoding='utf-8') as f:
    nbformat.write(nb, f)

# running the notebook will store the graded result to a JSON file
# rename graded result JSON file
graded_result_json_path = notebook_path.replace('.ipynb', '-result.json')
shutil.move('lambdagrader-result.json', graded_result_json_path)

# read graded result to generate a summary
with open(graded_result_json_path, mode='r') as f:
    graded_result = json.load(f)

# add filename
# we add it here instead of trying to add it within the Jupyter notebook
# because it is tricky to grab the current file name inside a Jupyter kernel
graded_result['filename'] = Path(notebook_path).name

# MD5 hash of the submitted Jupyter notebook file
# this can be used to detect duplicate submission to prevent unnecessary re-grading
with open(notebook_path, 'rb') as f:
    graded_result['submission_notebook_hash'] = hashlib.md5(f.read()).hexdigest()

# MD5 hash of test cases code
# this helps us to identify any potential cases
# where a learner has modified or deleted the test cases code cell
graded_result['test_cases_hash'] = test_cases_hash

# store Python version and platform used to run the notebook
graded_result['grader_python_version'] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
graded_result['grader_platform'] = platform.platform()

# save updated JSON to file
with open(graded_result_json_path, 'w') as f:
    json.dump(graded_result, f, indent=2)
    
# clean up notebook
lambdagrader.remove_grader_scripts(nb)
lambdagrader.add_graded_result(nb, graded_result)
    
# extract user code to a Python file
extracted_user_code = lambdagrader.extract_user_code_from_notebook(nb)
extracted_code_path = notebook_path.replace('.ipynb', '_user_code.py')

with open(extracted_code_path, "w", encoding="utf-8") as f:
    f.write(extracted_user_code)

# store graded result to HTML
filestem = Path(notebook_path).name
graded_html_path = notebook_path.replace('.ipynb', '-graded.html')
lambdagrader.save_graded_notebook_to_html(
    nb,
    html_title=filestem,
    output_path=graded_html_path,
    graded_result=graded_result
)

# LOCAL ENVIRONMENT ONLY
# the Lambda handler only processes one file instead of
# running a batch
# the code below generates a CSV to show results for multiple files
# get text summary of user's graded result
text_summary = lambdagrader.generate_text_summary(graded_result)

result_summary = graded_result.copy()
result_summary['text_summary'] = text_summary
del result_summary['results']
graded_results.append(result_summary)

print(f'Finished grading {filestem}')