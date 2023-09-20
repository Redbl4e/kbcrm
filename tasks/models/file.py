import os

from django.db import models


class File(models.Model):
    data = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        verbose_name='файл'
    )

    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'

    def __str__(self):
        return self.data.name

    def filename(self):
        return os.path.basename(self.data.name)
