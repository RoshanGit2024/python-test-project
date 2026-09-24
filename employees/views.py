from django.shortcuts import render
from config.mongodb import db
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from .utils import convert_salary
# Create your views here.


@api_view(['GET'])
def employee_list(request):
    employees = list(db.users.find())
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def employee_create(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        data = convert_salary(serializer.validated_data)
        result = db.users.insert_one(data)
        return Response({
            "message":"Employee created successfully",
            "id": str(result.inserted_id),
        }, status=201)
    return Response(serializer.errors, status=400)