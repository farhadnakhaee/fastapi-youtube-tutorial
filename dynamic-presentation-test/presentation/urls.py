from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('presentations', views.presentation_list, name='presentation_list'),
    path('presentations/create', views.create_presentation, name='create_presentation'),
    path('presentations/delete/<int:pk>', views.delete_presentation, name='delete_presentation'),
    # path('presentations/view/<int:pk>', views.update_presentation, name='update_presentation'),
    # path('presentations/edit/<int:pk>', views.update_presentation, name='update_presentation'),
    path('<slug:presentation_name>', views.presentation_slides_order, name='presentation_slides_order'),
    path('<slug:presentation_name>/<int:slide_id>', views.slide_detail, name='slide_detail'),
]

