import os
from dotenv import load_dotenv
from genai.model import Credentials, Model
from genai.schemas import GenerateParams, ModelType
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteriaList, StoppingCriteria
import torch 


class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self, stops=[], encounters=1):
        super().__init__()
        self.stops = [stop.to("cuda") for stop in stops]
        
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        for stop in self.stops:
            if torch.all((stop == input_ids[0][-len(stop):])).item():
                return True
        
        return False


def predict_text_greedy(model, tokenizer, prompt, device, use_cache):
    tokenized_prompt = tokenizer(prompt, return_tensors="pt")
    input_ids = tokenized_prompt.input_ids.to(dtype=torch.long, device=device)
    attention_mask = tokenized_prompt.attention_mask.to(dtype=torch.long, device=device)
    stop_words = ["\n"]
    stop_words_ids = [
        tokenizer(stop_word, return_tensors="pt")["input_ids"][0]
        for stop_word in stop_words
        ]
    stopping_criteria = StoppingCriteriaList(
        [StoppingCriteriaSub(stops=stop_words_ids)]
        )
        
    model.eval()
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=200,
            use_cache=use_cache,
            stopping_criteria=stopping_criteria,
            pad_token_id=tokenizer.eos_token_id,
        )

        # print(f"input_ids : {input_ids}")
        # print(f"generated_ids : {generated_ids}")

        preds = [
            tokenizer.decode(
                g, skip_special_tokens=True, clean_up_tokenization_spaces=True
                )
                for g in generated_ids
                ]
        print(f"preds : {preds}")
    return preds


def generateHFModelResponse(user_input, HF_MODEL, HF_TOKENIZER, device):
    answer = predict_text_greedy(HF_MODEL, 
                        HF_TOKENIZER,
                        user_input, 
                        device, 
                        use_cache=True)[0]    
    answer = answer.replace(user_input, '')
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

    return answer


# def generateStyleBAMResponse(prompt, bammodelname):

#     # make sure you have a .env file under bampy root with
#     # BAM_KEY=<your-bam-key>
#     load_dotenv()
#     api_key = os.getenv("BAM_KEY", None)
#     #creds = Credentials(api_key) # credentials object to access BAM
#     creds = Credentials(api_key, api_endpoint="https://bam-api.res.ibm.com/v1")

#     # Instantiate parameters for text generation
#     params = GenerateParams(decoding_method="sample", max_new_tokens=10)

#     # Instantiate a model proxy object to send your requests
#     if bammodelname == "BAM-UL2":
#         bammodel = Model(ModelType.FLAN_UL2, params=params, credentials=creds)

#     # prompts = ["Hello! How are you?", "How's the weather?"]
#     # for response in flan_ul2.generate(prompts):
#     #     print(response.generated_text)
    
#     try:
#         answer = bammodel.generate([prompt])[0].generated_text
#     except: 
#         answer = 'Oops you beat the AI, try a different question, if the problem persists, come back later.'

#     return answer

# def generateChatResponse(prompt):
    # messages = []
    # messages.append({"role": "system", "content": "Your name is Karabo. You are a helpful assistant."})

    # question = {}
    # question['role'] = 'user'
    # question['content'] = prompt
    # messages.append(question)

    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)

    # try:
    #     answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
    # except:
    #     answer = 'Oops you beat the AI, try a different question, if the problem persists, come back later.'

    # return answer