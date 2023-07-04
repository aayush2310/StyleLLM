# StyleLLM
Style Transfer using LLM(s) for Interactive Agents- A demo for Sarcasm and code-Mixing : A demo where we will use LLM(s) to demonstrate control for how a sarcastic a sentence is , or how code-mixed a sentence is , 
with Hindi being the target language.We propose the following steps:-
(i)use BAM and prompts to get response
(ii)Depending on resources, finetune an LLM and add it to demo
(iii)and have a simple website to demo the kit .

Skills that would be nice to have : familiarity with LLM(s), BAM, and building a simple frontend to demo the work.



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

#
