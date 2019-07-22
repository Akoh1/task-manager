from django.urls import path

from . import views
app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('task/',views.add_task, name='add_task'),
    path('user/task/', views.user_add_task, name="user_add_task"),
    path('add/status/', views.add_status, name="add_status"),
    # path('filter/<int:task_id>/', views.filter, name='filter'),
    path('move/<int:ta_id>/',views.move_goal, name='move_goal'),
    path('delete/<int:pk>/',views.user_delete, name='user_delete'),
    # path('adduser/', views.add_user, name='add_user'),
    # path('goals/', views.GoalView.as_view(), name='goal'),
    # path('home/', views.home, name='home'),
    #path('scrummy/', views.ScrummyUserViewSet.as_view('list'), name='scrummy'),
    path('api/users/', views.UserCreateView.as_view(), name="create_users"),
    # path('api/tasks/users', views.UserTaskCreateView.as_view(), name="create_users_tasks"),
    path('api/users/<int:pk>/', views.UserDetailsView.as_view(), name="detail_users"),
    path('api/admin/', views.AdminCreateView.as_view(), name="create_admin"),
    path('api/admin/<int:pk>/', views.AdminDetailsView.as_view(), name="detail_admin"),
    path('api/tasks/', views.ScrummyGoalsCreateView.as_view(), name="create_tasks"),
    path('api/tasks/<int:pk>', views.ScrummyGoalsDetailsView.as_view(), name="detail_tasks"),
    path('api/status/', views.StatusCreateView.as_view(), name="create_status"),
    # path('api/login/', views.apilogin)

]