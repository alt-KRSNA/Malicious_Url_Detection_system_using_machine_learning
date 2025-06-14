import pickle
from flask import Flask, request, render_template

# Load the trained model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Initialize Flask app
app = Flask(__name__)

# Initialize counts for predictions
prediction_counts = {'Benign': 0, 'Defacement': 0, 'Phishing': 0, 'Malware': 0}

@app.route('/')
def home():
    return render_template('index.html', prediction_counts=prediction_counts)

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    if not url:  # Validate if URL is empty
        return render_template('index.html', prediction_text="Please enter a valid URL.", prediction_color=None, prediction_counts=prediction_counts)

    url_vec = vectorizer.transform([url])  # Convert input URL into vector using the vectorizer
    prediction = model.predict(url_vec)[0]  # Predict the class

    label_map = {0: 'Benign', 1: 'Defacement', 2: 'Phishing', 3: 'Malware'}  # Map prediction to label
    result = label_map[prediction]  # Get the corresponding label

    # Update prediction counts
    prediction_counts[result] += 1

    # Return the result with a color signal based on prediction type
    if result == 'Benign':
        prediction_color = 'safe'  # Green for benign
    else:
        prediction_color = 'danger'  # Red for malicious types (Defacement, Phishing, Malware)

    return render_template('index.html', prediction_text=f'{result}', prediction_color=prediction_color, prediction_counts=prediction_counts)

if __name__ == '__main__':
    app.run(debug=True)
