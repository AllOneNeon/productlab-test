from django.urls import path
from app1.views import App1FileView, App1ArticleView

urlpatterns = [
    path("app1-file/", App1FileView.as_view()),
    path("app1-article/", App1ArticleView.as_view())
]
