# CodeGen

* **app_streaming.py** - Streamlit app that has options to generate R and Python code from English and convert SAS code to R
* **examples.md** - Contains a few prompts that you can use as input in the code generation/conversion app
* **code_generation.ipynb** - Notebook that loads the code generation/conversion model and generates output
* **ct2_converter.ipynb** - Helper utility to quantize the model and make inference faster in the API and app
* **model.py** - Code used to expose the code LLM as an API. This API only generates R code from an English prompt
  
