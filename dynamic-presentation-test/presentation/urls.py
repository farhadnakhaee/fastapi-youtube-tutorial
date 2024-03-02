from django.urls import path

from . import views

urlpatterns = [
    path("api/presentations/", views.PresentationList.as_view(), name="presentation_create_list"),
    path("api/presentations/<str:slug>/", views.PresentationDetail.as_view(), name="presentation_detail"),
    path("api/presentations/<str:slug>/<int:order>/", views.SlideDetailView.as_view(), name="slide_detail"),
    # user path
    path("index", views.index, name="index"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create', views.create, name='create'),
    path('delete/<str:slug>', views.delete, name='delete'),
    path('update/<str:slug>', views.update, name='update'),
]
