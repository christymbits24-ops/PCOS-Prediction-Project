from django.urls import path
from .views import home, predict, result_page, recommendation_page


urlpatterns = [

    path("", home, name="home"),

    path("predict/", predict, name="predict"),

    path("result/", result_page, name="result"),

    path(
        "recommendation/",
        recommendation_page,
        name="recommendation"
    ),

]