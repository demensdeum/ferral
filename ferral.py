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
    output: str
    comment: str

model = os.getenv("MODEL_NAME", "qwen2.5-coder:3b")
verbose = os.getenv("VERBOSE", "False").lower() == "true"

input_filepath = argv[1]
target_language = argv[2]
output_filepath = argv[3]

ferral_instruction_prefix = "# Ferral: "

with open(input_filepath, 'r', encoding='utf-8') as file:
    with open(output_filepath, "w", encoding='utf-8') as output_file:
        for line in file:
            print(line.strip())

            if line.startswith(ferral_instruction_prefix):
                ferral_instruction=line[len(ferral_instruction_prefix):]
                prompt=f"Target programming language: {target_language}; {ferral_instruction}; Give code only."
                response_str = ollama_call(
                    prompt,
                    format=FerralCodegeneratorResponse.model_json_schema(),
                    verbose=verbose,
                    model=model
                )

                try:
                    result=FerralCodegeneratorResponse.model_validate_json(response_str)
                    output_file.write(result.output)
                    print(result.output)
                    print(result.comment)

                except Exception as e:
                    print(f"Validation Error: {e}")

            else:
                output_file.write(line)
