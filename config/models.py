from django.db import models


class BaseModel(models.Model):
  class Meta:
    abstract = True

  created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
  modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
  deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)

