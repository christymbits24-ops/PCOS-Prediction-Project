import os
import joblib
import numpy as np

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# =========================
# Load ML model
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(
    os.path.join(BASE_DIR, "pmos_logistic_model.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "pmos_scaler.pkl")
)


# =========================
# Home page
# =========================

def home(request):
    return render(request, "index.html")


# =========================
# Result page
# =========================

def result_page(request):
    return render(request, "result.html")


# =========================
# Recommendation page
# =========================

def recommendation_page(request):
    return render(request, "recommendation.html")


# =========================
# PCOS Prediction API
# =========================

@api_view(["POST"])
def predict(request):

    try:

        age = float(request.data.get("age"))
        weight = float(request.data.get("weight"))
        height = float(request.data.get("height"))
        bmi = float(request.data.get("bmi"))
        cycle = float(request.data.get("cycle"))
        cycle_length = float(request.data.get("cycle_length"))
        weight_gain = float(request.data.get("weight_gain"))
        hair_growth = float(request.data.get("hair_growth"))
        pimples = float(request.data.get("pimples"))


        # Same order as your trained model
        features = np.array([[
            age,
            weight,
            height,
            bmi,
            cycle,
            cycle_length,
            weight_gain,
            hair_growth,
            pimples
        ]])


        # Scale input
        features_scaled = scaler.transform(features)


        # Prediction
        prediction = model.predict(features_scaled)[0]


        # Probability
        probability = model.predict_proba(features_scaled)[0][1] * 100


        if prediction == 1:

            result = "PCOS Positive"

        else:

            result = "PCOS Negative"


        return Response({
            "prediction": int(prediction),
            "probability": round(float(probability), 2),
            "result": result
        })


    except Exception as e:

        return Response(
            {
                "error": str(e)
            },
            status=400
        )