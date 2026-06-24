import joblib

model = joblib.load("health_model.pkl")
encoder = joblib.load("label_encoder.pkl")

def predict_health(
    glucose,
    haemoglobin,
    cholesterol
):

    prediction = model.predict([[
        glucose,
        haemoglobin,
        cholesterol
    ]])

    result = encoder.inverse_transform(
        prediction
    )

    return result[0]