"""linux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers, serializers, viewsets
from django.conf.urls import url
# from myapp.views import ScrummyUserViewSet, ScrummyGoalsViewSet, GoalStatusViewSet
from myapp import views
from django.conf import settings
router = routers.DefaultRouter()
# router.register(r'user', ScrummyUserViewSet)
# router.register(r'goals', ScrummyGoalsViewSet)
# router.register(r'status', GoalStatusViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/user/', views.signup_profile, name='user_signup'),
    path('accounts/signup/admin/', views.signup, name='admin_signup'),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url('api/', include(router.urls)),

    # path('api/scrummyusers/', views.scrummy_list, name="scrummy_list"),
    # path('api/scrummyusers/<int:pk>/', views.scrummy_detail, name="scrummy_detail"),

]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    # urlpatterns += static(settings.MEDIA_URL,
    #                       document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL,
    #                       document_root=settings.STATIC_ROOT)
