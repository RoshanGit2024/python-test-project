from rest_framework import serializers

class EmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    position = serializers.CharField(max_length=100)
    salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )