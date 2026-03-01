import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load dataset (project root -> dataset)
data = pd.read_csv('dataset/loan_data.csv')

X = data.drop('Loan_Status', axis=1)
y = data['Loan_Status']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Ensure ml directory exists
os.makedirs('predictor/ml', exist_ok=True)

# Save model
with open('predictor/ml/loan_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved successfully!")
