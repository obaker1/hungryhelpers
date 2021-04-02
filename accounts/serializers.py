from .models import Student
from django.core import serializers


data = serializers.serialize("json", Student.objects.all())

with open("studentInfo.json", "w") as out:
    json_serializer.serialize(Student.objects.all(), stream=out)

class StudentSerializer(serializers.ModelSerializer):
    id_student = serializers.RelatedField(many=True)
    class Meta:
        model = Student
        fields = ['name', 'age', 'address', 'city', 'state', 'zip', 'school', 'grade']

class StudentInfoSerializer(serializers.ModelSerializer):
    student_info = serializers.RelatedField(source='student', read_only=True)
    class Meta:
        model = Student
        fields = ['student_id']