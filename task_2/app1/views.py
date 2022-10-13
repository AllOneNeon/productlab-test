import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.parser import task_run, task_one_run
from app1.serializers import InputFileSerializer, InputArticleSerializer
from app1.utils import make_article

logger = logging.getLogger(__name__)

class App1FileView(APIView):
    def post(self, request):
        file_serializer = InputFileSerializer(data=request.FILES)
        file_serializer.is_valid(raise_exception=True)
        articles = make_article(request.FILES.get("article_file"))
        if not articles:
            return Response({"detail": "Articles in file not found"}, status=status.HTTP_404_NOT_FOUND)
        result = task_run(articles)
        return Response(result, status=status.HTTP_200_OK)


class App1ArticleView(APIView):
    def post(self, request):
        article_serializer = InputArticleSerializer(data=request.data)
        article_serializer.is_valid(raise_exception=True)
        article = article_serializer.data["article"]
        result = task_one_run(article)
        if not result:
            return Response({"detail": f"Article {article} not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)

