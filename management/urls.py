"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from management.views import UploadImageView, CloseView, ReportView, InvoiceView, OnItemView


app_name = 'management'

urlpatterns = [
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),
    path('close/', CloseView.as_view(), name='close_list'),
    path('onitem/', OnItemView.as_view(), name='on_item'),
    path('report/<int:unixtime>', ReportView.as_view(), name='report'),
    path('invoice/<int:unixtime>/<int:custom_user_pk>/', InvoiceView.as_view(), name='invoice'),
]