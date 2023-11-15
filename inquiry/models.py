from django.db import models
from config.models import BaseModel

# Create your models here.
class Inquiry(BaseModel):
  name = models.CharField(verbose_name='お名前', max_length=100)
  mail = models.EmailField(verbose_name='メールアドレス', max_length=200)
  subject = models.CharField(verbose_name='件名', max_length=100, default='')
  contents = models.CharField(verbose_name='問い合わせ内容', max_length=1000)


  def __str__(self):
    return self.subject

  class Meta:
    db_table = 'da_inquiry'
    verbose_name = '問い合わせ'
    verbose_name_plural = '問い合わせ'