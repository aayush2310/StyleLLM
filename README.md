# StyleLLM
Style Transfer using LLM(s) for Interactive Agents- A demo for Sarcasm and code-Mixing : A demo where we will use LLM(s) to demonstrate control for how a sarcastic a sentence is , or how code-mixed a sentence is , 
with Hindi being the target language.We propose the following steps:-
(i)use BAM and prompts to get response
(ii)Depending on resources, finetune an LLM and add it to demo
(iii)and have a simple website to demo the kit .

Skills that would be nice to have : familiarity with LLM(s), BAM, and building a simple frontend to demo the work.


# My Contribution
My role in the team was to make the app.py file and search for some cool logos to use in the UI.Apart from that, I was assigned the task
to test prompts on the Promt Lab of the BAM portal for the sarcastic mode.



# Explanation of app.py file

# from flask import Flask, render_template, jsonify, request
->We import the necessary modules: Flask for creating the application, render_template for rendering HTML templates, jsonify for converting Python objects to JSON responses, and 
  request for accessing incoming request data.

# import config
->importing a module named config in my Flask application. The config module is typically used to store configuration settings and variables for my application.
->Configuration settings and variables are used in applications to store values that can be modified without changing the code. This allows for greater flexibility and 
  adaptability of the application across different environments or deployments.

# import bamapi
->importing a module named bamapi in my Python script

# import torch 
The statement import torch is used to import the PyTorch library into your Python script or interactive session. PyTorch is a popular open-source machine learning framework primarily used for deep learning tasks. It provides a set of powerful tools and abstractions for building and training neural networks.

# from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteriaList, StoppingCriteria
Let's break down the meanings of the different imports you mentioned:

from transformers import AutoModelForCausalLM: This import statement is used to import the AutoModelForCausalLM class from the transformers library. The AutoModelForCausalLM class is a specific implementation of a pre-trained model for causal language modeling (LM) provided by the Hugging Face Transformers library. It allows you to load and use pre-trained models, such as GPT (Generative Pre-trained Transformer) models, for tasks like text generation.

from transformers import AutoTokenizer: This import statement imports the AutoTokenizer class from the transformers library. The AutoTokenizer class is used for automatic tokenization of text, which is a crucial step in natural language processing (NLP) tasks. It enables you to tokenize input text into subword or word-level tokens that can be processed by transformer models.

from transformers import StoppingCriteriaList: This import statement imports the StoppingCriteriaList class from the transformers library. The StoppingCriteriaList class is part of the early stopping functionality provided by the Hugging Face Transformers library. It allows you to define a list of stopping criteria that can be used during training to determine when to stop the training process based on certain conditions, such as validation loss not improving.

from transformers import StoppingCriteria: It seems that there might be a typo in the import statement you provided. There is no StoppingCriteria class in the transformers library. It's possible that this import statement should have been from transformers import EarlyStoppingCallback. The EarlyStoppingCallback class is used to implement early stopping during training. It allows you to monitor a specific metric, such as validation loss, and stop the training process if the metric does not improve over a certain number of epochs.

# def page_not_found(e):
#  return render_template('404.html'), 404


The code snippet you provided appears to be a Flask route handler for handling a 404 Not Found error. In Flask, you can define custom error handlers to handle specific HTTP error codes.

In this case, the page_not_found function is defined to handle the 404 error. The function takes an argument e, which represents the exception associated with the error (although it is not used in the provided code).

Inside the page_not_found function, it returns a call to render_template('404.html'). This line indicates that when a 404 error occurs, Flask should render the 404.html template, which is expected to be present in the templates directory of your Flask application.

The , 404 at the end of the line is used to specify the HTTP status code to be returned with the response. In this case, it sets the status code to 404 Not Found.

So, when a 404 error occurs, Flask will invoke this page_not_found function, render the 404.html template, and return the response with a 404 status code.

# app = Flask(__name__)
# app.config.from_object(config.config['development'])

The code snippet you provided demonstrates the initialization of a Flask application and configuring it using an external configuration file.

app = Flask(__name__): This line creates a Flask application instance. The __name__ argument is a special Python variable that represents the name of the current module. It is typically used to configure Flask's paths and resources correctly.

app.config.from_object(config.config['development']): This line loads the application configuration from an external configuration object or file. It assumes that there is a config module or package that contains a dictionary named config. Within that dictionary, there is an entry with the key 'development', which holds the configuration settings for the development environment.

The from_object method loads the configuration from the specified object or module. In this case, it loads the configuration from config.config['development']. The configuration object should define the necessary configuration variables, such as database connection details, secret keys, and other application-specific settings.

By setting the configuration, you can access these settings throughout your Flask application using the app.config object. For example, if you have a configuration variable named DATABASE_URL, you can access its value using app.config['DATABASE_URL'] in your application code.

# app.register_error_handler(404, page_not_found)


The code snippet app.register_error_handler(404, page_not_found) is used to register a custom error handler for the 404 Not Found error in a Flask application.

In this case, the register_error_handler method is called on the Flask application app. It takes two arguments: the HTTP error code (404) and the function to handle the error (page_not_found).

By registering the error handler using app.register_error_handler(404, page_not_found), you are instructing Flask to invoke the page_not_found function whenever a 404 error occurs in your application.

The page_not_found function should be defined earlier in your code and contain the logic for rendering an appropriate error page or handling the 404 error in some other way, such as redirecting to a different page or returning a custom response.

It's important to note that error handlers should be registered after the Flask application is created (app = Flask(__name__)), but before running the application using app.run().

# device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
# HF_MODEL_PATH = "tiiuae/falcon-7b-instruct"
# print("Loading HF Tokenizer")
# HF_TOKENIZER = AutoTokenizer.from_pretrained(HF_MODEL_PATH)
# print("Loading HF Model")
# HF_MODEL = AutoModelForCausalLM.from_pretrained(HF_MODEL_PATH, trust_remote_code=True)
# HF_MODEL.to(device)
# print("HF Model Loaded!")

The code snippet you provided sets up the device, loads a Hugging Face tokenizer and model, and moves the model to the specified device (CPU or CUDA).

Let's break down the code step by step:

"device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))"
This line checks if a CUDA-enabled GPU is available. If it is, the device variable is set to "cuda", indicating that the code will utilize the GPU for computations. Otherwise, it sets the device to "cpu", meaning that computations will be performed on the CPU.

" HF_MODEL_PATH = "tiiuae/falcon-7b-instruct" "
This line defines the path or identifier of the Hugging Face model you want to load. In this case, it is set to "tiiuae/falcon-7b-instruct", representing the Falcon-7B Instruct model.

" print("Loading HF Tokenizer")
  HF_TOKENIZER = AutoTokenizer.from_pretrained(HF_MODEL_PATH)  "
These lines load the tokenizer from the Hugging Face model specified by HF_MODEL_PATH. The AutoTokenizer.from_pretrained() method is used to automatically load the tokenizer associated with the model. The tokenizer is stored in the HF_TOKENIZER variable for later use.

" print("Loading HF Model")
  HF_MODEL = AutoModelForCausalLM.from_pretrained(HF_MODEL_PATH, trust_remote_code=True) "
These lines load the pre-trained model from the Hugging Face model specified by HF_MODEL_PATH. The AutoModelForCausalLM.from_pretrained() method is used to automatically load the model for causal language modeling. The trust_remote_code=True parameter is set to allow loading of the model from a remote source. The loaded model is stored in the HF_MODEL variable.

" HF_MODEL.to(device) "
This line moves the loaded model to the specified device ("cuda" or "cpu") using the .to() method. If the device is "cuda", the model will be moved to the GPU for computations. If the device is "cpu", the model remains on the CPU.

" print("HF Model Loaded!") "
Finally, this line prints a message indicating that the Hugging Face model and tokenizer have been successfully loaded.

Please note that the code assumes that you have already imported the necessary modules and classes from PyTorch and the Hugging Face Transformers library.

# @app.route('/', methods = ['POST', 'GET'])


The code snippet @app.route('/', methods=['POST', 'GET']) is a decorator in Flask that defines a route for the root URL ("/") of your Flask application. It specifies that the route should handle both POST and GET requests.

Let's break down the code:

@app.route('/', methods=['POST', 'GET'])


The @app.route() decorator is used to associate a function with a specific URL or route in your Flask application. In this case, the route is '/', which represents the root URL or homepage of your application.

The methods parameter is set to ['POST', 'GET'], indicating that the route handler function should be invoked for both POST and GET requests to the root URL.

Here's an example of how you can use the @app.route() decorator to define a function that handles the root URL:

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # Handle POST request
        return "This is a POST request to the homepage."
    else:
        # Handle GET request
        return "This is the homepage."

In the example above, the home() function is associated with the root URL ("/") using the @app.route() decorator. If a POST request is made to the root URL, it returns the message "This is a POST request to the homepage." If a GET request is made, it returns the message "This is the homepage."

You can customize the implementation of the function according to your application's requirements. Remember to import the necessary Flask modules (Flask, request) before using them in your code.

# def index():

#    if request.method == 'POST':
#        prompt = request.form['prompt']

#        sarcasm_prompt = f"Rewrite the sentence in a sarcastic tone : {prompt}"

#        res = {}
#        # res['answer'] = aiapi.generateChatResponse(prompt)
#        res['answer'] = bamapi.generateStyleBAMResponse(prompt)
#        return jsonify(res), 200

#    return render_template('index.html', **locals())


The code snippet you provided defines a Flask route handler for the /index URL. Let's break it down step by step:

" def index(): "

This is the definition of the index function, which will be associated with the /index URL. This function handles both GET and POST requests.

" if request.method == 'POST':
    prompt = request.form['prompt']
    sarcasm_prompt = f"Rewrite the sentence in a sarcastic tone : {prompt}"
    res = {}
    res['answer'] = bamapi.generateStyleBAMResponse(prompt)
    return jsonify(res), 200  "

This block of code is executed when a POST request is made to the /index URL. It first retrieves the value of the prompt field from the form data submitted with the request using request.form['prompt']. Then, it constructs a sarcastic prompt by appending the original prompt to a string.

Next, it initializes an empty dictionary res. The key 'answer' in res is assigned the response generated by calling the generateStyleBAMResponse function of the bamapi object with the prompt as an argument. The exact implementation and definition of bamapi are not provided in the code snippet.

Finally, it returns the response as JSON using jsonify(res), along with an HTTP status code of 200 (indicating success).

" return render_template('index.html', **locals()) "

This line is executed when a GET request is made to the /index URL. It renders the index.html template and passes the local variables to the template. The local variables in this case include prompt and sarcasm_prompt.

Please note that in order to use the request and jsonify objects, you need to import them from the Flask module. Also, make sure you have the appropriate HTML template (index.html) defined in your Flask application templates directory.

You might need to provide additional details or context regarding the bamapi object and other related code for a more complete understanding of the functionality.

# @app.route('/hfmodels', methods = ['POST', 'GET'])

The code snippet @app.route('/hfmodels', methods=['POST', 'GET']) is a Flask decorator that defines a route for the "/hfmodels" URL in your Flask application. It specifies that the route should handle both POST and GET requests.
The @app.route() decorator is used to associate a function with a specific URL or route in your Flask application. In this case, the route is "/hfmodels".

The methods parameter is set to ['POST', 'GET'], indicating that the route handler function should be invoked for both POST and GET requests to the "/hfmodels" URL.

# def indexhfmodel():

#    if request.method == 'POST':
#        prompt = request.form['prompt']

#        res = {}
#        # res['answer'] = aiapi.generateChatResponse(prompt)
#        res['answer'] = bamapi.generateHFModelResponse(prompt, 
#                                                      HF_MODEL, 
#                                                       HF_TOKENIZER,
#                                                       device)
#        return jsonify(res), 200

#    return render_template('index.html', **locals())

The code snippet you provided defines a Flask route handler for the /indexhfmodel URL. Let's break it down step by step:

" def indexhfmodel(): "
This is the definition of the indexhfmodel function, which will be associated with the /indexhfmodel URL. This function handles both GET and POST requests.

" if request.method == 'POST':
    prompt = request.form['prompt']
    res = {}
    res['answer'] = bamapi.generateHFModelResponse(prompt, HF_MODEL, HF_TOKENIZER, device)
    return jsonify(res), 200 "

This block of code is executed when a POST request is made to the /indexhfmodel URL. It first retrieves the value of the prompt field from the form data submitted with the request using request.form['prompt'].

Next, it initializes an empty dictionary res. The key 'answer' in res is assigned the response generated by calling the generateHFModelResponse function of the bamapi object. It takes the prompt, HF_MODEL, HF_TOKENIZER, and device as arguments. The exact implementation and definition of bamapi, HF_MODEL, HF_TOKENIZER, and device are not provided in the code snippet.

Finally, it returns the response as JSON using jsonify(res), along with an HTTP status code of 200 (indicating success).

" return render_template('index.html', **locals()) "

This line is executed when a GET request is made to the /indexhfmodel URL. It renders the index.html template and passes the local variables to the template.

Please note that in order to use the request, jsonify, and render_template objects, you need to import them from the Flask module. Also, make sure you have the appropriate HTML template (index.html) defined in your Flask application templates directory.

You might need to provide additional details or context regarding the bamapi, HF_MODEL, HF_TOKENIZER, and device objects for a more complete understanding of the functionality.


# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port='8888', debug=False)

The code snippet if __name__ == '__main__': app.run(host='0.0.0.0', port='8888', debug=False) is used to start the Flask application when the Python script is executed directly.

Let's break down the code:

" if __name__ == '__main__': "

This condition checks whether the script is being executed directly as the main entry point. The __name__ variable contains the name of the current module. If the value of __name__ is '__main__', it means the script is being run directly.

" app.run(host='0.0.0.0', port='8888', debug=False) "

Inside the if block, the app.run() method is called to start the Flask application. It takes several optional parameters:

host='0.0.0.0': This specifies the hostname or IP address on which the application will be accessible. '0.0.0.0' means the application will be available on all network interfaces.
port='8888': This sets the port number on which the application will listen for incoming requests. In this case, it is set to 8888.
debug=False: This parameter determines whether debug mode is enabled. When set to True, the application will run in debug mode, providing detailed error messages and auto-reloading the code when changes are detected. In this case, it is set to False.
When the script is executed directly, the if __name__ == '__main__': condition is satisfied, and the app.run() method is called to start the Flask application with the specified configuration.

Make sure you have imported the necessary modules and defined the Flask application (app) before running the script.






 


