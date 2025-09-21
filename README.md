# Hate Speech Analyzer Web Application

A modern web interface for detecting hate speech and offensive content using a fine-tuned BERT model.

## Features

- **Modern UI**: Beautiful, responsive web interface with gradient design
- **Real-time Analysis**: Instant hate speech detection with visual feedback
- **Example Texts**: Pre-loaded examples to test the model
- **Mobile Friendly**: Responsive design that works on all devices
- **Error Handling**: Graceful error handling and user feedback

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Model Files**: Make sure your `model_save` directory contains:
   - `config.json`
   - `model.safetensors`
   - `special_tokens_map.json`
   - `tokenizer_config.json`
   - `vocab.txt`

## Running the Application

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```

2. **Open Your Browser**: Navigate to `http://localhost:5000`

3. **Use the Interface**:
   - Enter text in the text area
   - Click "Analyze Text" or press Enter
   - View the results with visual indicators

## API Endpoints

- `GET /` - Serves the web interface
- `POST /predict` - Analyzes text for hate speech
  - Request body: `{"text": "your text here"}`
  - Response: `{"sentiment": "Neither" | "Hate/Offensive"}`

## Model Information

- **Architecture**: BERT (Bidirectional Encoder Representations from Transformers)
- **Task**: Binary classification (Hate/Offensive vs Neither)
- **Input**: Text strings up to 128 tokens
- **Output**: Classification label

## File Structure

```
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface template
└── model_save/           # Trained model files
    ├── config.json
    ├── model.safetensors
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    └── vocab.txt
```

## Usage Examples

The web interface includes example texts you can try:

- **Clean Content**: "I love this beautiful sunny day!"
- **Hate Speech**: "You are such an idiot and should go die!"
- **Neutral**: "Thank you for your help with the project."
- **Offensive**: "I hate all people from that country!"

## Technical Details

- **Backend**: Flask with PyTorch and Transformers
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Custom CSS with gradients and animations
- **Icons**: Font Awesome icons
- **Fonts**: Inter font family for modern typography

## Troubleshooting

- **Model Loading Issues**: Ensure all model files are present in `model_save/`
- **CUDA Errors**: The app automatically falls back to CPU if CUDA is unavailable
- **Port Conflicts**: Change the port in `app.py` if 5000 is already in use
- **Memory Issues**: Large models may require significant RAM/VRAM

## Customization

You can customize the web interface by modifying:
- **Colors**: Update CSS gradient values in `templates/index.html`
- **Styling**: Modify CSS classes and animations
- **Examples**: Add/remove example texts in the HTML
- **Model**: Replace the model files to use a different trained model
