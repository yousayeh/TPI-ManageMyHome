from django.urls import path
from . import views

# URLs for the applications
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),
    path('detailWork/<int:workId>', views.detailWork, name='detailWork'),
    path('deleteWork/<int:workId>', views.deleteWork, name='deleteWork'),
    path('addWorkProject/', views.addWorkProject, name='addWorkProject'),
    path('updateWork/<int:workId>', views.updateWork, name='updateWork'),
    path('updateProject/<int:projectId>', views.updateProject, name='updateProject'),
    path('deleteProject/<int:projectId>', views.deleteProject, name='deleteProject'),
    path('myHouse/<int:userId>', views.myHouse, name='myHouse'),
    path('deleteHouse/<int:houseId>', views.deleteHouse, name='deleteHouse'),
    path('addHouse/', views.addHouse, name='addHouse'),
    path('updateHouse/<int:houseId>', views.updateHouse, name='updateHouse')
]