import os
import joblib
import numpy as np

from django.shortcuts import render , redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Prediction

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




def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check username and password
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Login the user
            login(request, user)

            # Go to prediction page
            return redirect("/prediction/")

        else:

            # Invalid username or password
            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password"
                }
            )

    return render(request, "login.html")






def register_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect("/login/")

    return render(request, "register.html")


def prediction_page(request):
    return render(request, "index.html")
    


def about_page(request):
    return render(request, "about.html")



# =========================
# Home page
# =========================

def home(request):
    return render(request, "home.html")


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

        # Check if user is logged in
        if not request.user.is_authenticated:
            return Response(
                {"error": "Please login first."},
                status=401
            )

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
        probability = model.predict_proba(
            features_scaled
        )[0][1] * 100

        if prediction == 1:
            result = "PCOS Positive"
        else:
            result = "PCOS Negative"

        # =========================
        # SAVE PREDICTION TO DATABASE
        # =========================

        Prediction.objects.create(
            user=request.user,
            age=int(age),
            weight=weight,
            height=height,
            bmi=bmi,
            cycle=int(cycle),
            cycle_length=int(cycle_length),
            weight_gain=int(weight_gain),
            hair_growth=int(hair_growth),
            pimples=int(pimples),
            prediction=int(prediction),
            probability=round(float(probability), 2)
        )

        # =========================
        # SEND RESULT TO FRONTEND
        # =========================

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

