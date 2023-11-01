# Import all the dependencies
import ctranslate2
import nvidia
import os
import time
import torch
import transformers
     
from random import randint
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import GenerationConfig 
     
cuda_install_dir = '/'.join(nvidia.__file__.split('/')[:-1]) + '/cuda_runtime/lib/'
os.environ['LD_LIBRARY_PATH'] =  cuda_install_dir
     
# Load the ctranslate model
model_device = 'cuda' if torch.cuda.is_available() else 'cpu'


model_path = '/mnt/artifacts/codellama-ct'
model_device = 'cuda' if torch.cuda.is_available() else 'cpu'

# load the ctranslate model
generator = ctranslate2.Generator(model_path, device=model_device)
tokenizer = transformers.AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-Instruct-hf')


prompt_template= f"You are a helpful polite code assistant.Please write R code using statistics libraries for example stats and plotting libraries for example ggplot for the task that follows. Output the result in markdown \n Task : {{dialogue}} \n ```r"
     
#Generate the output from the LLM
def generate(prompt: str = None, pct_new_tokens: float = 1.2):
    if prompt is None:
        return 'Please provide a prompt.'
            
    # Construct the prompt for the model
    user_input = prompt_template.format(dialogue=prompt)
    
    tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(user_input))
    input_length = len(tokens)
    # new_tokens = round(pct_new_tokens*input_length)
    new_tokens = 750
    results = generator.generate_batch([tokens], sampling_topk=10, max_length=new_tokens, include_prompt_in_result=False)
    output_text = tokenizer.decode(results[0].sequences_ids[0])
    
    return {'text_from_llm': output_text}
    
