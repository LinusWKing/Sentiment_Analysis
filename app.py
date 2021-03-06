# Contributed by Linus Wahome
from flask import Flask, render_template, request
import pickle
from keras_preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K

with open('models/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)  # Load tokenizer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    model = load_model('models/model.h5')  # Load model

    if request.method == 'POST':
        namequery = request.form['text']
        data = [namequery]

        x_seq = tokenizer.texts_to_sequences(data)  # Vectorize input data
        # Pad the vectorized data
        encoded = pad_sequences(x_seq, maxlen=1000, padding='post')

        prediction = model.predict(encoded)  # Predict

        if prediction[0] >= 0.0:
            sentiment = 'Positive'
        else:
            sentiment = 'Negative'

        K.clear_session()
    return render_template('index.html', prediction_text=sentiment)


if __name__ == '__main__':
    app.run(debug=True)
