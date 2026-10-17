from rest_framework import serializers
from config.mongodb import db

class EmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    position = serializers.CharField(max_length=100)
    salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def validate_email(self,value):
        if db.users.find_one({"email":value}):
            raise serializers.ValidationError("This email already exist")
        return value