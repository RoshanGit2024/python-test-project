import time
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.hashers import make_password, check_password
from pymongo.errors import DuplicateKeyError
from config.mongodb import db


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data =request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    user = {
        "username":data["username"],
        "email":data["email"].strip().lower(),
        "password":make_password(data["password"])
    }

    try:
        result = db.auth.insert_one(user)
        return Response({
        "message":"User registered successfully",
        "id":str(result.inserted_id)
        },status=201)
    except DuplicateKeyError:
        return Response({
            "message":"Email already exists"
        },status=400)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    if not serializer.is_valid():
        return Response(serializer.errors,status=400)
    if serializer.is_valid():
        data = serializer.validated_data
        user = db.auth.find_one({"email":data["email"].strip().lower()}) 
    if user is None:
        return Response({
            "message":"Invalid email or password"
        },status=401)
    if not check_password(data["password"],user["password"]):
        return Response({
            "message":"Invalid email or password"
        },status=401)

    now = int(time.time())
    payload = {
        "user_id":str(user["_id"]),
        "username":user["username"],
        "exp":now + 3600,
        "iat":now
    }  

    token = jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")

    return Response({
        "message":"Login successful",
        "token":token
    },status=200)
