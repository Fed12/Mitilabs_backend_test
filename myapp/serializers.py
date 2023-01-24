from rest_framework import serializers
from .models import FileModel


# class FileSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = FileModel
# 		fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True, required=False)