from django.urls import path

from . import views

urlpatterns = [
    path("", views.SampleApi.as_view()),
    path("question/", views.QuestionApi.as_view()),
    path("question/<pk>", views.QuestionDetailApi.as_view()),
    path("product/", views.ProductApi.as_view()),
    path("product/<pk>", views.ProductDetailApi.as_view()),
]
