import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

# Load dataset
df = pd.read_csv('Agriculture_commodities_dataset.csv')

# Convert month names to numbers
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}
df['Month'] = df['Month'].map(month_mapping)

# Drop rows with missing values
df = df.dropna()

# ✅ Use only necessary features
X = df[['Year', 'Month', 'arrivals_in_qtl', 'Commodity']]
y = df['modal_price']

# One-hot encode Commodity
X = pd.get_dummies(X, columns=['Commodity'], drop_first=True)
feature_names = X.columns.tolist()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model & features
with open('commodity_price_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model_features.pkl', 'wb') as f:
    pickle.dump(feature_names, f)

print("✅ Model trained and saved successfully!")

