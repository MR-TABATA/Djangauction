from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
import hashlib
from config.models import BaseModel



class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		if not email:
			raise ValueError('Emailを入力して下さい')
		email = self.normalize_email(email)
		username = self.model.normalize_username(username)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('is_staff=Trueである必要があります。')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('is_superuser=Trueである必要があります。')
		return self._create_user(username, email, password, **extra_fields)


def avater_file_path(instance, filename):
  hash = hashlib.sha256(str(instance.id).encode()).hexdigest()
  return f'images/icons/{hash}/{filename}'

class CustomUser(AbstractBaseUser, PermissionsMixin):
	username_validator = UnicodeUsernameValidator()
	license_number = models.CharField(verbose_name='古物許可証番号', max_length=100, blank=True, null=True)
	representative_name = models.CharField(verbose_name='代表者', max_length=100, blank=True, null=True)
	company_name = models.CharField(verbose_name='会社名または屋号', max_length=100, blank=True, null=True)
	zip = models.CharField(verbose_name='郵便番号', max_length=10, blank=True, null=True)
	prefecture = models.CharField(verbose_name='都道府県', max_length=10, blank=True, null=True)
	address = models.CharField(verbose_name='市区町村', max_length=100, blank=True, null=True)
	block = models.CharField(verbose_name='番地', max_length=100, blank=True, null=True)
	building = models.CharField(verbose_name='建物等', max_length=100, blank=True, null=True)
	phone = models.CharField(verbose_name='連絡先', max_length=15, blank=True, null=True)
	mobile_phone = models.CharField(verbose_name='モバイル', max_length=15, blank=True, null=True)
	email = models.EmailField(verbose_name='メール', max_length=200, blank=True, null=True)

	username = models.CharField(_("username"), max_length=50, validators=[username_validator], unique=True)

	is_staff = models.BooleanField(_("staff status"), default=False)
	is_active = models.BooleanField(_("active"), default=True)
	created = models.DateTimeField(verbose_name='生成日時', auto_now_add=True)
	modified = models.DateTimeField(verbose_name='更新日時', auto_now=True)
	deleted = models.DateTimeField(verbose_name='削除日時', blank=True, null=True)
	delete_memo = models.TextField(verbose_name='削除理由', blank=True, null=True)

	objects = UserManager()
	USERNAME_FIELD = "username"
	EMAIL_FIELD = "email"
	#REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = _("会員")
		verbose_name_plural = _("会員")

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)
