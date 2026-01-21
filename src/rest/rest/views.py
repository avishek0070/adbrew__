from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from pymongo import MongoClient
from bson import ObjectId

mongo_uri = f'mongodb://{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}'
client = MongoClient(mongo_uri)
db = client["test_db"]
todos_collection = db["todos"]


class TodoListView(APIView):

    def get(self, request):
        try:
            todos = [
                {"id": str(todo["_id"]), "text": todo.get("text", "")}
                for todo in todos_collection.find()
            ]
            return Response(todos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to fetch todos"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        data = request.data

        if "text" not in data or not data["text"].strip():
            return Response(
                {"error": "Todo text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        todo = {
            "text": data["text"]
        }

        result = todos_collection.insert_one(todo)

        return Response(
            {
                "id": str(result.inserted_id),
                "text": data["text"]
            },
            status=status.HTTP_201_CREATED
        )
