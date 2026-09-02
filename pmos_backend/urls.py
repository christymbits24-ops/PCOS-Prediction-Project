from django.contrib import admin
from django.urls import path, include
from prediction.views import home, result_page, recommendation_page

urlpatterns = [

    path("", home, name="home"),

    path("admin/", admin.site.urls),

    path("api/", include("prediction.urls")),

    path("result/", result_page, name="result"),

    path(
        "recommendation/",
        recommendation_page,
        name="recommendation"
    ),

]