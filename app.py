from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load model
with open('commodity_price_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load features
with open('model_features.pkl', 'rb') as f:
    model_features = pickle.load(f)

# List of available commodities from features
commodities = sorted([col.replace("Commodity_", "") for col in model_features if col.startswith("Commodity_")])

# Month names
month_names = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

@app.route('/')
def home():
    return render_template('index.html', commodities=commodities, months=month_names)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        year = int(request.form['year'])
        month_name = request.form['month']
        arrivals = float(request.form['arrivals'])
        commodity = request.form['commodity']

        # Validate inputs
        if year < 2024:
            raise ValueError("2024 or greater.")
        if arrivals <= 1:
            raise ValueError("Arrivals must be greater than 1.")

        month_number = month_names.index(month_name) + 1

        input_data = {
            'Year': [year],
            'Month': [month_number],
            'arrivals_in_qtl': [arrivals],
            'Commodity': [commodity]
        }

        df_input = pd.DataFrame(input_data)
        df_input = pd.get_dummies(df_input, columns=['Commodity'], drop_first=True)

        for col in model_features:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[model_features]

        prediction = model.predict(df_input)[0]

        return render_template('index.html',
                               prediction=f"Predicted Modal Price: ₹{prediction:.2f}",
                               commodities=commodities,
                               months=month_names)

    except Exception as e:
        return render_template('index.html',
                               prediction=f"Error: {str(e)}",
                               commodities=commodities,
                               months=month_names)

if __name__ == '__main__':
    app.run(debug=True)

