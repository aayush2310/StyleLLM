import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
import requests
from bamapi import predict_text_greedy

import os
from dotenv import load_dotenv
from genai.model import Credentials, Model
from genai.schemas import GenerateParams, ModelType


import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteriaList, StoppingCriteria

from prompt_wrappers import *

#************* Functions for making BAM and Huggingface Model inference query **************

def generateHFModelResponse(user_input, HF_MODEL, HF_TOKENIZER, device):
    answer = predict_text_greedy(st.session_state.HF_MODEL, 
                                st.session_state.HF_TOKENIZER,
                                user_input, 
                                st.session_state.device, 
                                use_cache=True)[0]    

    print(f"answer : {answer}")
    answer = answer.replace(user_input, '')
    print(f"answer after strip: {answer}")

    return answer

MODEL_NAMES = ['bigscience/bloom', 'mosaicml/mpt-30b', 'tiiuae/falcon-40b', 'google/flan-t5-xxl', 'google/flan-ul2', 'togethercomputer/gpt-neoxt-chat-base-20b', 'mosaicml/mpt-7b', 'openassistant/oasst-sft-4-pythia-12b', 'togethercomputer/redpajama-incite-instruct-7b-v01']

def generateStyleBAMResponse(prompt, model_name):

    # make sure you have a .env file under bampy root with
    # BAM_KEY=<your-bam-key>
    load_dotenv()
    api_key = os.getenv("BAM_KEY", None)
    
    creds = Credentials(api_key, api_endpoint="https://bam-api.res.ibm.com/v1")

    # Instantiate parameters for text generation
    params = GenerateParams(decoding_method="sample", max_new_tokens=50, temperature=0.95, top_p=0.95)

    # Instantiate a model proxy object to send your requests
    model = Model(model_name, params=params, credentials=creds)

    try:
        answer = model.generate([prompt])[0].generated_text
    except: 
        answer = 'Oops you beat the AI, try a different question, if the problem persists, come back later.'

    answer = answer.replace(prompt, '')

    return answer



#************* Functions for making BAM and Huggingface Model inference query **************


# Collect text from the text input box
def get_text():
    input_text = st.text_input("You: ","Large language models will take over the world.", key="input")
    return input_text 


#*************** Initialising Streamlit Session_state keys for stateful behaviour**********
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'device' not in st.session_state:
    device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
    st.session_state['device'] = device
    print(f"Device in session_state initialised to : {st.session_state['device']}")

if 'HF_MODEL_PATH' not in st.session_state: #change it to pick from drop down
    HF_MODEL_PATH = "tiiuae/falcon-7b-instruct"
    st.session_state['HF_MODEL_PATH'] = HF_MODEL_PATH
    print(f"HF_MODEL_PATH in session_state initialised to : {st.session_state['HF_MODEL_PATH']}")


if 'HF_TOKENIZER' not in st.session_state: #change it to pick from drop down model name if its a HF model
    print("Loading HF Tokenizer")
    HF_TOKENIZER = AutoTokenizer.from_pretrained(HF_MODEL_PATH)
    st.session_state['HF_TOKENIZER'] = HF_TOKENIZER
    print(f"HF_TOKENIZER in session_state initialised to : AutoTokenizer {st.session_state['HF_MODEL_PATH']}")


if 'HF_MODEL' not in st.session_state:
    print("Loading HF Model")
    HF_MODEL = AutoModelForCausalLM.from_pretrained(HF_MODEL_PATH, 
                                                    trust_remote_code=True,
                                                    torch_dtype=torch.float16)
    HF_MODEL.to(device)
    print("HF Model Loaded!")
    st.session_state['HF_MODEL'] = HF_MODEL

    print(f"HF_MODEL in session_state initialised to : AutoModelForCausalLM {st.session_state['HF_MODEL_PATH']}")



if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": 'Hello Friend! How may I help you?'})

if 'select_llm' not in st.session_state:
    st.session_state.select_llm = 'tiiuae/falcon-40b'

if 'role' not in st.session_state:
    st.session_state.role = 'Chandler-Mode'

st.title("StyleLLM")

def on_llm_select():
    st.info('You have selected the LLM ' + st.session_state.select_llm, icon="ℹ️")

def on_clear_btn_click():
    del st.session_state.messages

def on_role_change(key):
    st.info(f"You have selected the role {st.session_state[key]}")

with st.sidebar:
    with st.container():
        st.session_state.llm = st.selectbox('Please Select the LLM',
                                            ('HF-tiiuae/falcon-7b-instruct', 'bigscience/bloom', 'google/flan-t5-xxl', 'google/flan-ul2',
                                            'mosaicml/mpt-30b', 'mosaicml/mpt-7b', 'openassistant/oasst-sft-4-pythia-12b', 'tiiuae/falcon-40b',  
                                            'togethercomputer/gpt-neoxt-chat-base-20b', 'togethercomputer/redpajama-incite-instruct-7b-v01'), 
                                            index=2, key='select_llm', on_change=on_llm_select)

    with st.container():
        role = option_menu('Role', ["Chandler-Mode", "Direct-Mode", "Formal-Mode", "Indirect-Mode", "Melodramatic-Mode", "Metaphor-Mode",
                                    "Old-English", "Optimistic-Mode", "Sarcasm-Mode", "Self-Deprecating-Mode", "Witty-Mode"],
                                    default_index=0, orientation="vertical", on_change=on_role_change, key='role')

    with st.container():
        st.button("Clear messages", on_click=on_clear_btn_click)

chat_placeholder = st.container()


def get_chat_response(user_query):

    print(f"st.session_state.role = {st.session_state['role']}")

    if st.session_state['role'] == "Chandler-Mode":
        prompt = get_chandler_prompt(user_query)
        prompt = prompt.strip()

    elif st.session_state['role'] == "Sarcasm-Mode":
        prompt = get_sarcasm_prompt(user_query)
        prompt = prompt.strip()

    elif st.session_state['role'] == "Self-Deprecating-Mode":
        prompt = get_self_deprecating_prompt(user_query)
        prompt = prompt.strip()

    elif st.session_state['role'] == "Formal-Mode":
        prompt = get_formal_prompt(user_query)
        prompt = prompt.strip()        
    
    elif st.session_state['role'] == "Optimistic-Mode":
        prompt = get_optimisitc_prompt(user_query)
        prompt = prompt.strip()
        
    elif st.session_state['role'] == "Witty-Mode":
        prompt = get_witty_prompt(user_query)
        prompt = prompt.strip()

    elif st.session_state['role'] == "Melodramatic-Mode":
        prompt = get_melodramatic_prompt(user_query)
        prompt = prompt.strip()

    elif st.session_state['role'] == "Metaphor-Mode":
        prompt = get_metaphor_prompt(user_query)
        prompt = prompt.strip()

    elif st.session_state['role'] == "Direct-Mode":
        prompt = get_direct_prompt(message['content'])
        prompt = prompt.strip()

    elif st.session_state['role'] == "Indirect-Mode":
        prompt = get_indirect_prompt(message['content'])
        prompt = prompt.strip()
    
    elif st.session_state['role'] == "Old-English":
        prompt = get_oldenglish_prompt(message['content'])
        prompt = prompt.strip()


    #Based on the model to query make suitable function call. 
    if st.session_state['select_llm'] == "HF-tiiuae/falcon-7b-instruct": #for HF model
        print("generating using HF-tiiuae/falcon-7b-instruct")
        response = generateHFModelResponse(prompt, 
                                        st.session_state.HF_MODEL, 
                                        st.session_state.HF_TOKENIZER,
                                        st.session_state.device)

    else: #st.session_state['select_llm'] == "BAM-UL2": # for BAM model
        print(f"generating using BAM model - {st.session_state['select_llm']}")
        print(f"prompt : {prompt}")
        response = generateStyleBAMResponse(prompt,
                                            st.session_state['select_llm'])

    return response.split('\n')[0]



# Display chat messages from history on app rerun
with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(""):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            print(f"prompt before calling get_chat_response ; {prompt}")
            response = get_chat_response(prompt)

            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})



