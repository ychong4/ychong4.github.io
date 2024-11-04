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
from transformers import LlamaTokenizer, pipeline, AutoTokenizer, AutoModelForCausalLM, TrOCRProcessor, VisionEncoderDecoderModel
from hftoken import huggingface_token, secret_name, region_name, host
import psycopg2
import boto3
import json
from PIL import Image, ImageEnhance, ImageFilter
import torchvision.transforms as transforms
from flask_cors import CORS
from paddleocr import PaddleOCR
import easyocr
import numpy as np
import traceback

matplotlib.use('Agg')

# Initialize Flask app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server's filesystem
Session(app)
CORS(app)

# Set a secret key to securely sign the session cookie
app.secret_key = os.urandom(24)  # Generates a random secret key each time


def get_secret():

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    response = get_secret_value_response['SecretString']
    secret = json.loads(response)
    return secret['username'], secret['password']

username, password = get_secret()

# Connection to postgreSQL
def get_db_connection():
    conn = psycopg2.connect(
            host=host,
            user=username,
            password=password,
            port=5432 
    )
    return conn


# Directory for storing uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define available models for sentiment analysis
NLP_MODELS = {
    "distilbert-base-uncased-finetuned-sst-2-english": "DistilBERT",
    "nlptown/bert-base-multilingual-uncased-sentiment": "NLPTown BERT",
    "cardiffnlp/twitter-roberta-base-sentiment": "Twitter RoBERTa"
}

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

# Define the sentiment mappings for the specified models
sentiment_mappings = {
        "distilbert-base-uncased-finetuned-sst-2-english": {
            'NEGATIVE': 'negative',
            'POSITIVE': 'positive',
            'NEUTRAL': 'positive'
        },
        "nlptown/bert-base-multilingual-uncased-sentiment": {
            '1 star': 'negative',
            '2 stars': 'negative',
            '3 stars': 'positive',
            '4 stars': 'positive',
            '5 stars': 'positive'
        },
        "cardiffnlp/twitter-roberta-base-sentiment": {
            'LABEL_0': 'negative',
            'LABEL_1': 'positive',
            'LABEL_2': 'positive'
        },
}

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html', nlp_models=NLP_MODELS)

@app.route('/uploads')
def uploads():
    return render_template('uploads.html', nlp_models=NLP_MODELS)

@app.route('/text_classification')
def text_classification():
    return render_template('text_classification.html', nlp_models=NLP_MODELS)

@app.route('/btc')
def btc():
    return render_template('btc.html')

@app.route('/chat')
def chat():
    return render_template('chatbot.html')

# Limit the conversation history to a reasonable length
MAX_HISTORY_LENGTH = 10

@app.route('/chat', methods=['POST'])
def chatbot():
    user_input = request.json['message']

    # Add system prompt to behave like a good teacher
    messages = [
        {"role": "system", "content": "You are a helpful, patient, and knowledgeable teacher."},
        {"role": "user", "content": user_input}
    ]
    #bot_response = chat_pipeline(messages, max_length=150)
    #response_text = bot_response[0]['generated_text'][2]['content']
    #return jsonify({'response': response_text})

     # Generate the teacher-like response
    bot_response = chat_pipeline(messages, max_new_tokens=60)

    # Extract the assistant's response from the bot_response
    assistant_response = ""
    if isinstance(bot_response, list) and len(bot_response) > 0:
        assistant_response = bot_response[0]['generated_text'][-1]['content']  # Extract the last generated text

    if not assistant_response:
        assistant_response = "I'm sorry, I couldn't generate a response."

    return jsonify({'response': assistant_response})

@app.route('/analyze', methods=['POST'])
def analyze():
    sentence = request.form['sentence']
    selected_model = request.form['model']

    # Initialize sentiment analysis model
    sentiment_pipeline = pipeline("sentiment-analysis", model=selected_model)

    result = sentiment_pipeline(sentence)[0]

    # Get the mapping for the selected model
    model_mapping = sentiment_mappings.get(selected_model, {})
    
    sentiment = model_mapping.get(result['label'], 'unknown')
    confidence = round(result['score'], 4)
    model_name = NLP_MODELS.get(selected_model, selected_model)
    return render_template('text_classification.html', sentence=sentence, sentiment=sentiment, confidence=confidence, model_name=model_name, nlp_models=NLP_MODELS)

# Route to handle file upload and sentiment analysis
@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'csvFile' not in request.files:
        return "No file uploaded!", 400
    
    file = request.files['csvFile']
    
    if file.filename == '':
        return redirect(request.url)
    
    # Ensure the file is a CSV
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)

        # Assuming the CSV has a column with the sentences
        if 'text' not in df.columns:
            return "CSV file must have a 'text' column", 400

        # Get the selected model from the form
        selected_model = request.form['model']
        sentiment_pipeline = pipeline("sentiment-analysis", model=selected_model)

        # Clean the 'text' column by stripping whitespace
        df['text'] = df['text'].str.strip()

        if selected_model in sentiment_mappings:
            # Initialize lists to hold sentiment labels and confidence scores
            sentiments = []
            confidences = []

            # Analyze each sentence and store sentiment and confidence
            for sentence in df['text']:
                # Get the sentiment result from the pipeline
                result = sentiment_pipeline(sentence)[0]
                label = result['label']  # Extract the sentiment label
                confidence = round(result['score'], 4)  # Extract and round the confidence score

                # Map sentiment label to the human-readable form
                mapped_sentiment = sentiment_mappings[selected_model].get(label, 'unknown')

                # Append to lists
                sentiments.append(mapped_sentiment)
                confidences.append(confidence)

            # Assign the lists to the DataFrame
            df['sentiment'] = sentiments
            df['confidence'] = confidences  # Ensure 'confidence' is correctly named without trailing spaces

        else:
            return "Invalid model selected!", 400   
        
        # Generate word clouds for positive and negative sentiments
        pos_text = " ".join(df[df['sentiment'] == 'positive']['text'].astype(str).tolist())
        neg_text = " ".join(df[df['sentiment'] == 'negative']['text'].astype(str).tolist())

        # Save the DataFrame as results.csv in the uploads directory
        results_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
        df.to_csv(results_filepath, index=False)

        # Plot sentiment distribution
        plt.figure(figsize=(6,4))
        ax = sns.countplot(x='sentiment', data=df, color='blue')
        sns.countplot(x='sentiment', data=df)
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')

        # Add the count labels on top of the bars
        ax.margins(y=0.1)

        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 5),
                textcoords='offset points')

        # Save the plot to a PNG image in memory
        img_sentiment = io.BytesIO()
        plt.savefig(img_sentiment, format='png')
        img_sentiment.seek(0)
        plot_url_sentiment = base64.b64encode(img_sentiment.getvalue()).decode()

        # Generate word cloud from text
        text_data = " ".join(df['text'].astype(str).tolist())
        if text_data.strip():  # Check if there's any text data
            wordcloud = WordCloud(width=400, height=200, background_color='white').generate(text_data)

            # Save word cloud to PNG image in memory
            img_wordcloud = io.BytesIO()
            plt.figure(figsize=(8, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(img_wordcloud, format='png')
            img_wordcloud.seek(0)
            plot_url_wordcloud = base64.b64encode(img_wordcloud.getvalue()).decode()
        else:
            plot_url_wordcloud = None  # No data for word cloud


        # Generate word cloud for positive sentiment
        if pos_text.strip():  # Check if there's any positive text
            pos_wordcloud = WordCloud(width=400, height=200, background_color='white').generate(pos_text)
            img_pos_wordcloud = io.BytesIO()
            plt.figure(figsize=(8, 6))
            plt.imshow(pos_wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(img_pos_wordcloud, format='png')
            img_pos_wordcloud.seek(0)
            plot_url_pos_wordcloud = base64.b64encode(img_pos_wordcloud.getvalue()).decode()
        else:
            plot_url_pos_wordcloud = None  # No data for positive word cloud

        # Generate word cloud for negative sentiment
        if neg_text.strip():  # Check if there's any negative text
            neg_wordcloud = WordCloud(width=400, height=200, background_color='white').generate(neg_text)
            img_neg_wordcloud = io.BytesIO()
            plt.figure(figsize=(8, 6))
            plt.imshow(neg_wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(img_neg_wordcloud, format='png')
            img_neg_wordcloud.seek(0)
            plot_url_neg_wordcloud = base64.b64encode(img_neg_wordcloud.getvalue()).decode()
        else:
            plot_url_neg_wordcloud = None  # No data for negative word cloud

        # Store data in session
        session['data'] = df.to_dict()
        session['plot_url_sentiment'] = plot_url_sentiment
        session['plot_url_wordcloud'] = plot_url_wordcloud
        session['plot_url_pos_wordcloud'] = plot_url_pos_wordcloud  # Positive word cloud
        session['plot_url_neg_wordcloud'] = plot_url_neg_wordcloud  # Negative word cloud

        # Redirect to pagination route
        return redirect(url_for('paginate'))
    
    return "Invalid file type! Only CSV files are accepted", 400

# Route for paginating and displaying the results
@app.route('/paginate', methods=['GET'])
def paginate():
    data = session.get('data')  # Retrieve data from session
    if data is None:
        return "No data available! Please upload a CSV file first.", 400

    # Convert session data back to a DataFrame
    df = pd.DataFrame.from_dict(data)

    # Pagination logic
    page = request.args.get('page', 1, type=int)  # Get current page from URL
    per_page = 10  # Number of rows per page
    total_pages = math.ceil(len(df) / per_page)

    # Get the rows for the current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = df[start:end]

    # Pass enumerated data to the template
    enumerated_data = list(enumerate(paginated_data.values.tolist(), start=start+1))
    
    return render_template('results_paginated.html', 
                           enumerated_data=enumerated_data, 
                           current_page=page, 
                           total_pages=total_pages,
                           plot_url_sentiment=session.get('plot_url_sentiment'), 
                           plot_url_wordcloud=session.get('plot_url_wordcloud'),
                           plot_url_pos_wordcloud=session.get('plot_url_pos_wordcloud'), 
                           plot_url_neg_wordcloud=session.get('plot_url_neg_wordcloud'),
                           nlp_models = NLP_MODELS)

# Route to download the results CSV
@app.route('/download')
def download_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
    return send_file(filepath, as_attachment=True)

@app.route('/download_sentiment_plot')
def download_sentiment_plot():
    img_sentiment = session.get('plot_url_sentiment')
    if img_sentiment is None:
        return "No sentiment plot available", 400
    
    # Decode the image from base64 and create a response
    img_data = base64.b64decode(img_sentiment)
    response = make_response(img_data)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment; filename=sentiment_plot.png')
    return response

@app.route('/download_wordcloud')
def download_wordcloud():
    img_wordcloud = session.get('plot_url_wordcloud')
    if img_wordcloud is None:
        return "No word cloud available!", 400
    
    # Decode the image from base64 and create a response
    img_data = base64.b64decode(img_wordcloud)
    response = make_response(img_data)
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment; filename=word_cloud.png')
    return response

@app.route('/time_series')
def time_series():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query for historical prices
    cursor.execute("""
    SELECT date AT TIME ZONE 'UTC' AT TIME ZONE 'America/Chicago' AS date, close, ticker 
    FROM stock_historical_price;
    """)

    historical_data = cursor.fetchall()
    historical_df = pd.DataFrame(historical_data, columns=['date', 'close', 'ticker'])
    
    # Query for predicted prices
    cursor.execute("""
    SELECT id, ticker,
           insert_date AT TIME ZONE 'UTC' AT TIME ZONE 'America/Chicago' AS insert_date,
           prediction_date AT TIME ZONE 'UTC' AT TIME ZONE 'America/Chicago' AS prediction_date,
           price, price_upper, price_lower
    FROM stock_prediction_price
    WHERE (ticker, insert_date) IN (
        SELECT ticker, MAX(insert_date)
        FROM stock_prediction_price
        GROUP BY ticker
    );
    """)
    prediction_data = cursor.fetchall()
    prediction_df = pd.DataFrame(prediction_data, columns=['id', 'ticker', 'insert_date', 'prediction_date', 'price', 'price_upper', 'price_lower'])
    
    cursor.close()
    conn.close()

    prediction_df = prediction_df[['ticker', 'prediction_date','price', 'price_upper', 'price_lower']]
    
    return render_template('time_series.html', 
                           historical_data=historical_df.to_dict(orient='records'), 
                           prediction_data=prediction_df.to_dict(orient='records'))




# Load the TrOCR model and processor
vision_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
vision_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

@app.route('/image-to-text', methods=['GET', 'POST'])
def image_to_text():
    extracted_text = None

    def preprocess_image(image):
        transform = transforms.Compose([
            transforms.Resize((384, 384)),  # Resize to a specific size
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize based on your needs
        ])
        image = transform(image)
        return image.unsqueeze(0)  # Add batch dimension

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            return render_template('image-to-text.html', error="No file part"), 400

        file = request.files['image']
        if file.filename == '':
            return render_template('image-to-text.html', error="No selected file"), 400

        # Process the image
        try:
            image = Image.open(file).convert("RGB")
            # Then pass this preprocessed image to the model
            pixel_values = preprocess_image(image)

            # Generate text from the image
            with torch.no_grad():
                generated_ids = vision_model.generate(pixel_values, max_new_tokens=100)
            extracted_text = vision_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        except Exception as e:
            return render_template('image-to-text.html', error=f"Error processing image: {e}"), 500

    return render_template('image-to-text.html', extracted_text=extracted_text)

@app.route('/image-to-text-write', methods=['GET', 'POST'])
def image_to_text_write():

    def preprocess_image(image):
        # Convert to grayscale
        gray = image.convert('L')
    
        # Increase contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)
    
        # Denoise
        denoised = enhanced.filter(ImageFilter.MedianFilter(size=3))

        # Resize image for OCR
        target_size = (640, 480)  # Adjust as needed
        resized = denoised.resize(target_size)
    
        # Binarization
        threshold = 128
        binary = resized.point(lambda x: 255 if x > threshold else 0)
    
        return binary.convert('RGB')
    
    def recognize_text_ensemble(image):
        results = []

        # TrOCR
        try:
            pixel_values = vision_processor(image, return_tensors="pt").pixel_values
            generated_ids = vision_model.generate(pixel_values)
            trocr_text = vision_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            if trocr_text:
                results.append(trocr_text)
        except Exception as e:
            print("TrOCR failed:", e)
        
        # EasyOCR
        try:
            image_np = np.array(image)
            reader = easyocr.Reader(['en'])
            easyocr_result = reader.readtext(image_np)
            easyocr_text = ' '.join([text[1] for text in easyocr_result])
            if easyocr_text:
                results.append(easyocr_text)
        except Exception as e:
            print("EasyOCR failed:", e)
        
        # PaddleOCR
        try:
            paddle_ocr = PaddleOCR(lang='en', use_angle_cls=True)
            paddle_result = paddle_ocr.ocr(image_np)
            if paddle_result:
                paddle_text = ' '.join([line[1][0] for line in paddle_result])
                results.append(paddle_text)
            else:
                print("PaddleOCR found no text.")
        except Exception as e:
            print("PaddleOCR failed:", e)
        
        # Handle empty results
        if not results:
            return "No text found in the image", 400

        # Simple voting system
        return max(set(results), key=results.count)

    if request.method == 'GET':
        return render_template('image-to-text-write.html')
    
    if request.method == 'POST':
        try:
            data = request.json
            if not data or 'image' not in data:
                return jsonify({'error': 'No image data received'}), 400
            
            image_data = data['image'].split(',')[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Process image
            processed_image = preprocess_image(image)

            # Debugging output
            print("Processed image size:", processed_image.size)
            print("Processed image mode:", processed_image.mode)

            # Use ensemble method for text recognition
            recognized_text = recognize_text_ensemble(processed_image)
            
            return jsonify({'text': recognized_text})
        except Exception as e:
            print("Exception occurred:", e)
            print(traceback.format_exc())  # This will show the stack trace in the logs
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)