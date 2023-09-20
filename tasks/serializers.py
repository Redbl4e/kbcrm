from abc import ABC

from rest_framework import serializers
from tasks.models import Task, File
from users.models import User


class ChoicesStatusSerializerField(serializers.SerializerMethodField, ABC):
    def to_representation(self, value):
        method_name = f'get_{self.field_name}_display'
        method = getattr(value, method_name)
        return method()


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "patronymic")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "patronymic")


class TaskSerializer(serializers.ModelSerializer):
    status = ChoicesStatusSerializerField()
    guarantor = UserSerializer(read_only=True)
    executor = UserSerializer(many=True, read_only=True)
    file = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'description',
                  'deadline', 'status', 'created_at',
                  'guarantor', 'executor', 'file')
