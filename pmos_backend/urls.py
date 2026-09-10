
from django.contrib import admin
from django.urls import path, include

from prediction.views import (
    home,
    prediction_page,
    result_page,
    recommendation_page,
    about_page,
    register_page,
    login_page
)

urlpatterns = [

    path("", home, name="home"),

    path("prediction/", prediction_page, name="prediction"),

    path("admin/", admin.site.urls),

    path("api/", include("prediction.urls")),

    path("result/", result_page, name="result"),

    path(
        "recommendation/",
        recommendation_page,
        name="recommendation"
    ),

    path("about/", about_page, name="about"),

    path("register/", register_page, name="register"),

    path("login/", login_page, name="login"),
]

