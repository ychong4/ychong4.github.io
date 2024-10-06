from flask import Flask, request, render_template
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)

# Initialize sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    sentence = request.form['sentence']
    result = sentiment_pipeline(sentence)[0]
    sentiment = result['label']
    confidence = round(result['score'], 4)
    return render_template('index.html', sentence=sentence, sentiment=sentiment, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)
