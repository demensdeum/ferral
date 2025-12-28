from ollama_call import ollama_call
from pydantic import BaseModel
from sys import argv
from dotenv import load_dotenv
import os

load_dotenv()

target_argv_count = 4

if len(argv) != target_argv_count:
    print(f"{argv} len() != {target_argv_count}")
    exit(1)

class FerralCodegeneratorResponse(BaseModel):
    code: str

model = os.getenv("MODEL_NAME", "qwen2.5-coder:3b")
verbose = os.getenv("VERBOSE", "False").lower() == "true"

input_filepath = argv[1]
target_language = argv[2]
output_filepath = argv[3]

ferral_instruction_prefix = "# Ferral: "
ferral_num_predict_option_prefix = "# Ferral: num_predict "
ferral_model_option_prefix = "# Ferral: model "

num_predict = -1

with open(input_filepath, 'r', encoding='utf-8') as file:
    with open(output_filepath, "w", encoding='utf-8') as output_file:
        for line in file:
            print(line.strip())

            if line.startswith(ferral_num_predict_option_prefix):
                num_predict=int(line[len(ferral_num_predict_option_prefix):].strip())
                if verbose:
                    print(f"set num_predict = {num_predict}")

            elif line.startswith(ferral_model_option_prefix):
                model=line[len(ferral_model_option_prefix):].strip()
                if verbose:
                    print(f"set model = {model}")

            elif line.startswith(ferral_instruction_prefix):
                ferral_instruction=line[len(ferral_instruction_prefix):].strip()
                prompt=f"Target programming language: {target_language}; {ferral_instruction}; Give code only, without quoting. Without code comments."
                response_str = ollama_call(
                    prompt,
                    format=FerralCodegeneratorResponse.model_json_schema(),
                    verbose=verbose,
                    model=model,
                    num_predict=num_predict
                )
                print(response_str)

                try:
                    result=FerralCodegeneratorResponse.model_validate_json(response_str)
                    output_file.write(result.code)
                    print(result.code)

                except Exception as e:
                    print(f"Validation Error: {e}")
                    print("Probably ollama bug with structured output for cloud models: https://github.com/ollama/ollama/issues/12362")
                    print("trying to extract...")
                    code_lines = response_str.split("\n")
                    if code_lines[0].startswith("```"):
                        code_lines.pop(0)
                    if code_lines[len(code_lines) - 1].startswith("```"):
                        code_lines.pop(len(code_lines) - 1)
                    
                    output_file.write("\n".join(code_lines))


            else:
                output_file.write(line)
