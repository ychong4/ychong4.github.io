import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response, session
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

matplotlib.use('Agg')

# Initialize Flask app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server's filesystem
Session(app)

# Set a secret key to securely sign the session cookie
app.secret_key = os.urandom(24)  # Generates a random secret key each time

# Directory for storing uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploads.html')
def uploads():
    return render_template('uploads.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    sentence = request.form['sentence']
    result = sentiment_pipeline(sentence)[0]
    sentiment = result['label']
    confidence = round(result['score'], 4)
    return render_template('home.html', sentence=sentence, sentiment=sentiment, confidence=confidence)

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

        # Clean the 'text' column by stripping whitespace
        df['text'] = df['text'].str.strip()

        # Assuming the CSV has a column "text" with the sentences
        df['sentiment'] = df['text'].apply(lambda sentence: sentiment_pipeline(sentence)[0]['label'])
        df['confidence'] = df['text'].apply(lambda sentence: round(sentiment_pipeline(sentence)[0]['score'], 4))

        # Plot sentiment distribution
        plt.figure(figsize=(8,6))
        sns.countplot(x='sentiment', data=df)
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')

        # Save the plot to a PNG image in memory
        img_sentiment = io.BytesIO()
        plt.savefig(img_sentiment, format='png')
        img_sentiment.seek(0)
        plot_url_sentiment = base64.b64encode(img_sentiment.getvalue()).decode()

        # Generate word cloud from text
        text_data = " ".join(df['text'].astype(str).tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

        # Save word cloud to PNG image in memory
        img_wordcloud = io.BytesIO()
        plt.figure(figsize=(8,6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img_wordcloud, format='png')
        img_wordcloud.seek(0)
        plot_url_wordcloud = base64.b64encode(img_wordcloud.getvalue()).decode()

        # Store data in session
        session['data'] = df.to_dict()
        session['plot_url_sentiment'] = plot_url_sentiment
        session['plot_url_wordcloud'] = plot_url_wordcloud

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
                           plot_url_wordcloud=session.get('plot_url_wordcloud'))

# Route to download the results CSV
@app.route('/download')
def download_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
