# Models Directory

This directory contains ML model configurations and training scripts.

## Pretrained Models Used

The application uses several pretrained models:

1. **Text Emotion Analysis**
   - Model: `j-hartmann/emotion-english-distilroberta-base`
   - Type: DistilRoBERTa fine-tuned for emotion classification
   - Emotions: anger, disgust, fear, joy, neutral, sadness, surprise

2. **Sentiment Analysis**
   - Model: `cardiffnlp/twitter-roberta-base-sentiment-latest`
   - Type: RoBERTa for sentiment classification
   - Classes: negative, neutral, positive

3. **Speech Emotion Recognition**
   - Model: `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`
   - Type: Wav2Vec2 for audio emotion recognition
   - Emotions: angry, calm, disgust, fearful, happy, sad, surprised, neutral

4. **Facial Expression Analysis**
   - Library: DeepFace
   - Backend: Multiple (VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace)
   - Emotions: angry, disgust, fear, happy, sad, surprise, neutral

## Custom Model Training

If you want to train custom models on your organization's data:

1. **Data Collection**: Collect labeled emotion data from your employees (with consent)
2. **Preprocessing**: Clean and prepare the data
3. **Fine-tuning**: Fine-tune pretrained models on your data
4. **Evaluation**: Validate model performance
5. **Deployment**: Replace the models in the emotion analyzers

## Model Files Structure

```
models/
├── text/
│   └── custom_emotion_model/  # Custom text emotion model (if trained)
├── facial/
│   └── custom_facial_model/   # Custom facial model (if trained)
├── speech/
│   └── custom_speech_model/   # Custom speech model (if trained)
└── fusion/
    └── fusion_weights.json    # Weights for multi-modal fusion
```

## Training Scripts (Examples)

Training scripts would go here for custom model development:
- `train_text_emotion.py`
- `train_facial_emotion.py`
- `train_speech_emotion.py`
- `optimize_fusion_weights.py`

## Model Performance Tracking

Track model performance metrics:
- Accuracy
- Precision/Recall/F1
- Confusion matrices
- Cross-validation scores
- A/B testing results

## Ethical Considerations

- Ensure training data is collected ethically with proper consent
- Audit models for bias regularly
- Maintain transparency in model decisions
- Protect employee privacy
- Follow data protection regulations (GDPR, CCPA, etc.)
