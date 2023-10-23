from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the saved model
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load the dataset
data = pd.read_csv("Mobile_phones_data.csv")

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction route
@app.route('/recommend', methods=['POST'])
def predict():
    # Get user input from the form
    ram = int(request.form['ram'])
    rom = int(request.form['rom'])
    rating = float(request.form['rating'])
    battery = request.form['battery']
    budget = int(request.form['budget'])

    # Create a new input instance based on user preferences
    input_instance = pd.DataFrame({
        'RAM Gb': [ram],
        'ROM Gb': [rom],
        'Rating': [rating],
        'Battery Mah': [battery],
        'Price Rs': [budget]
    })

    # Make a prediction using the loaded model
    prediction = model.predict(input_instance)

    # Get the recommended phone based on the prediction

    recommended_phone =  data[data['Name'] != prediction[0]].sample(5)
    print(recommended_phone)

    # Pass the recommended phone details to the template
    return render_template('rec.html', recommended=recommended_phone)

if __name__ == '__main__':
    app.run(debug=True)
