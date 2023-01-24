from django.db import models


class FileModel(models.Model):
	file_name = models.TextField(max_length=200)