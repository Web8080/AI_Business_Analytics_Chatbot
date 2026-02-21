# Victor.I
from django.urls import path
from . import views

urlpatterns = [
    path("upload/csv/", views.upload_csv),
    path("query/", views.query),
    path("datasets/", views.list_datasets),
    path("datasets/<str:dataset_id>/preview/", views.get_preview),
    path("health/", views.health),
]
