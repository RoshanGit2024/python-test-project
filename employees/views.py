from django.shortcuts import render
from config.mongodb import db
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from .utils import convert_salary
from bson.errors import InvalidId
from bson import ObjectId
from .utils import uniqueId_generate
# Create your views here.


@api_view(['GET'])
def employee_list(request):
    employees = list(db.users.find())
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def employee_detail(request,pk):
    try:
        employee = db.users.find_one({
            '_id':ObjectId(pk)
        })

        if employee is None:
            return Response({
                "message":"No employee found with given id"
            },status=404)
        employee['_id'] = str(employee.pop('_id'))

        serializer = EmployeeSerializer(employee)
        return Response({"message":"Employee found","data":serializer.data},status=200)

    except InvalidId:
        return Response({
            "message":"Invalid employee id"
        },status=400)



@api_view(['POST'])
def employee_create(request):
    serializer = EmployeeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.is_valid():
        employee_id = uniqueId_generate()
        data = convert_salary(serializer.validated_data)
        result = db.users.insert_one({
            "employee_id": employee_id,
            **data
        })
        return Response({
            "message":"Employee created successfully",
            "id": str(result.inserted_id),
        }, status=201)
    return Response(serializer.errors, status=400)