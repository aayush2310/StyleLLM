from flask import Flask, render_template, jsonify, request
import config
import bamapi
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteriaList, StoppingCriteria

def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
app.config.from_object(config.config['development'])

app.register_error_handler(404, page_not_found)

device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
HF_MODEL_PATH = "tiiuae/falcon-7b-instruct"
print("Loading HF Tokenizer")
HF_TOKENIZER = AutoTokenizer.from_pretrained(HF_MODEL_PATH)
print("Loading HF Model")
HF_MODEL = AutoModelForCausalLM.from_pretrained(HF_MODEL_PATH, trust_remote_code=True)
HF_MODEL.to(device)
print("HF Model Loaded!")

@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':
        prompt = request.form['prompt']

        sarcasm_prompt = f"Rewrite the sentence in a sarcastic tone : {prompt}"

        res = {}
        # res['answer'] = aiapi.generateChatResponse(prompt)
        res['answer'] = bamapi.generateStyleBAMResponse(prompt)
        return jsonify(res), 200

    return render_template('index.html', **locals())


@app.route('/hfmodels', methods = ['POST', 'GET'])
def indexhfmodel():

    if request.method == 'POST':
        prompt = request.form['prompt']

        res = {}
        # res['answer'] = aiapi.generateChatResponse(prompt)
        res['answer'] = bamapi.generateHFModelResponse(prompt, 
                                                       HF_MODEL, 
                                                       HF_TOKENIZER,
                                                       device)
        return jsonify(res), 200

    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=False)
