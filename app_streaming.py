import ctranslate2
import streamlit as st
import nvidia
import os
import torch
import transformers

# Configuration and Initialization
cuda_install_dir = os.path.join(os.path.dirname(nvidia.__file__), 'cuda_runtime', 'lib')
os.environ['LD_LIBRARY_PATH'] = cuda_install_dir

MODEL_PATH = '/mnt/data/codellama-ct'
MODEL_DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
PROMPT_TEMPLATE= "You are a helpful polite code assistant.Please write R code using statistics libraries for example stats and plotting libraries for example ggplot for the task that follows. Output the result in markdown \n Task : {dialogue} \n ```r"

# Load the ctranslate model
generator = ctranslate2.Generator(MODEL_PATH, device=MODEL_DEVICE) if 'generator' not in locals() else generator
tokenizer = transformers.AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-Instruct-hf') if 'tokenizer' not in locals() else tokenizer

st.session_state.setdefault("messages", [])

# Sidebar with Clear Conversation button
with st.sidebar:
    st.title("Settings")
    selected_language = st.radio("Choose a language:", ["SAS-R", "English-R"])
    
    # Update the PROMPT_TEMPLATE based on the selected language
    if selected_language == "English-R":
        PROMPT_TEMPLATE= "You are a helpful polite code assistant.Please write R code using statistics libraries for example stats and plotting libraries for example ggplot for the task that follows. Output the result in markdown \n Task : {dialogue} \n ```r"
    else:
        PROMPT_TEMPLATE= "You are a helpful polite code assistant.Please write R code using statistics libraries for example stats and plotting libraries for example ggplot for the SAS code that follows. Output the result in markdown \n SAS Code : {dialogue} \n ```r"
        
    if st.button('Clear Conversation'):
        st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get new user input and generate response
if (user_input := st.chat_input("How can I help?")):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    formatted_input = PROMPT_TEMPLATE.format(dialogue=user_input)
    tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(formatted_input))
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        step_results = generator.generate_tokens(tokens, sampling_temperature=0.8, sampling_topk=20, max_length=1024)
        
        full_response = ""
        output_ids = []
        for step_result in step_results:
            is_new_word = step_result.token.startswith("▁")
            if is_new_word and output_ids:
                word = tokenizer.decode(output_ids) + " "
                full_response += word
                output_ids = []
            output_ids.append(step_result.token_id)
            message_placeholder.markdown(full_response)

        if output_ids:
            word = tokenizer.decode(output_ids)
            full_response += word.replace("</s>", "")
        
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
