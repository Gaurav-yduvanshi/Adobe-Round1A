# train_model.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the labeled data
df = pd.read_csv('data.csv')

# Encode the labels
label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['label'])

# Features and target
X = df[['font_size', 'bold', 'x', 'y', 'page']]
y = df['label_encoded']

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model and label encoder
joblib.dump(model, 'heading_classifier.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
print("✅ Model saved as heading_classifier.pkl")
    