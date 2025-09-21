import torch
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from transformers import BertForSequenceClassification, BertTokenizer
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Analysis history storage
analysis_history = []

# --- Load the saved model and tokenizer ---
model_path = "./model_save"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
model.eval() # Set model to evaluation mode

# Define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Define a prediction function
def predict_sentiment(text):
    # Tokenize the input text
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits

    # Get the predicted class and confidence scores
    probabilities = torch.softmax(logits, dim=1)
    confidence, prediction = torch.max(probabilities, dim=1)
    
    # Map the prediction to a human-readable label
    if prediction.item() == 0:
        return "Neither", confidence.item()
    else:
        return "Hate/Offensive", confidence.item()

# --- Define the API endpoint ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json(force=True)
    text_to_predict = data['text']

    # Get the prediction and confidence
    prediction, confidence = predict_sentiment(text_to_predict)

    # Store analysis in history
    analysis_entry = {
        'timestamp': datetime.now().isoformat(),
        'text': text_to_predict[:100] + '...' if len(text_to_predict) > 100 else text_to_predict,
        'sentiment': prediction,
        'confidence': round(confidence * 100, 2)
    }
    analysis_history.append(analysis_entry)
    
    # Keep only last 50 analyses
    if len(analysis_history) > 50:
        analysis_history.pop(0)

    # Return the prediction as JSON
    return jsonify({
        'sentiment': prediction,
        'confidence': round(confidence * 100, 2)
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read file content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean up file
            os.remove(filepath)
            
            # Analyze content
            prediction, confidence = predict_sentiment(content)
            
            return jsonify({
                'sentiment': prediction,
                'confidence': round(confidence * 100, 2),
                'content': content[:500] + '...' if len(content) > 500 else content
            })
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
    else:
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'md'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({'history': analysis_history[-20:]})  # Return last 20 analyses

@app.route('/batch', methods=['POST'])
def batch_analyze():
    data = request.get_json(force=True)
    texts = data.get('texts', [])
    
    if not texts:
        return jsonify({'error': 'No texts provided'}), 400
    
    results = []
    for text in texts:
        prediction, confidence = predict_sentiment(text)
        results.append({
            'text': text[:100] + '...' if len(text) > 100 else text,
            'sentiment': prediction,
            'confidence': round(confidence * 100, 2)
        })
    
    return jsonify({'results': results})

# Run the Flask app
if __name__ == '__main__':
    # To make it accessible from outside, use host='0.0.0.0'
    app.run(host='0.0.0.0', port=5000)