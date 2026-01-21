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
        todos = []
        for todo in todos_collection.find():
            todos.append({
                "id": str(todo["_id"]),   # IMPORTANT
                "text": todo.get("text", "")
            })

        return Response(todos, status=status.HTTP_200_OK)

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
