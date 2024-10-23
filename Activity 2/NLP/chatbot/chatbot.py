import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response, session, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from transformers import pipeline
from wordcloud import WordCloud
import io
import base64
import math
import torch
import transformers
from transformers import LlamaTokenizer, pipeline, AutoTokenizer, AutoModelForCausalLM
from hftoken import huggingface_token

# Load LLaMA model
model_id = "meta-llama/Llama-3.2-1B-Instruct"  # Adjust with the correct model name
tokenizer = AutoTokenizer.from_pretrained(model_id, token=huggingface_token)
model = AutoModelForCausalLM.from_pretrained(model_id, token=huggingface_token)

# Initialize text generation pipeline
chat_pipeline = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

@app.route('/chat')
def chat():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chatbot():
    user_input = request.json['message']

    # Add system prompt to behave like a good teacher
    messages = [
        {"role": "system", "content": "You are a helpful, patient, and knowledgeable teacher. You explain things clearly, provide encouragement, and help users learn step-by-step."},
        {"role": "user", "content": user_input}
    ]
    #bot_response = chat_pipeline(messages, max_length=150)
    #response_text = bot_response[0]['generated_text'][2]['content']
    #return jsonify({'response': response_text})

     # Generate the teacher-like response
    bot_response = chat_pipeline(messages, max_new_tokens=150)

    # Extract the assistant's response from the bot_response
    assistant_response = ""
    if isinstance(bot_response, list) and len(bot_response) > 0:
        assistant_response = bot_response[0]['generated_text'][-1]['content']  # Extract the last generated text

    if not assistant_response:
        assistant_response = "I'm sorry, I couldn't generate a response."

    return jsonify({'response': assistant_response})