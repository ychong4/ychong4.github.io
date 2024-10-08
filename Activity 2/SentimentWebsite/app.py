import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Initialize NLTK Sentiment Analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Initialize Flask app
app = Flask(__name__)

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

        # Assuming the CSV has a column "text" with the sentences
        df['sentiment'] = df['text'].apply(analyze_sentiment)
        
        # Optionally, you can save the results back to CSV or perform further analysis
        result_csv = df.to_csv(index=False)
        
        # Return some sort of result to the frontend (this is up to you)
        return result_csv, 200

    return "Invalid file type!", 400


# Function to analyze sentiment from CSV file
def analyze_sentiment(filepath):
    df = pd.read_csv(filepath)
    
    # Assuming the CSV has a 'sentence' column
    df['sentiment'] = df['sentence'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Save the updated CSV
    result_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
    df.to_csv(result_filepath, index=False)
    
    # Visualization: Plot sentiment scores
    fig = plt.figure(figsize=(10, 6))
    sns.boxplot(x='sentiment', data=df)
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment Score')
    fig_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sentiment_distribution.png')
    plt.savefig(fig_path)
    
    # Return the results (CSV and visualization path)
    return df[['sentence', 'sentiment']].to_dict('records'), fig_path

# Route to download the results CSV
@app.route('/download')
def download_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
