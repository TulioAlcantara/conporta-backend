from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from api import views
from rest_framework_jwt.views import obtain_jwt_token

from api.views import user_mentioned_ordinances_list

router = routers.DefaultRouter()

router.register(r'ordinancecitation', views.OrdinanceCitationViewSet)
router.register(r'directive', views.DirectiveViewSet)
router.register(r'adminunitmember', views.AdminUnitMemberViewSet)
router.register(r'notification', views.NotificationViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'ordinance', views.OrdinanceViewSet)
router.register(r'ordinancemember', views.OrdinanceMemberViewSet)
router.register(r'adminunit', views.AdminUnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token),
    path('user-mentioned-ordinances-list/', views.user_mentioned_ordinances_list)
]
