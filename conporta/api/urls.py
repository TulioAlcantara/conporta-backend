from rest_framework.routers import SimpleRouter
from api import views


router = SimpleRouter()

router.register(r'ordinancecitation', views.OrdinanceCitationViewSet)
router.register(r'directive', views.DirectiveViewSet)
router.register(r'adminunitmember', views.AdminUnitMemberViewSet)
router.register(r'notification', views.NotificationViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'ordinance', views.OrdinanceViewSet)
router.register(r'ordinancemember', views.OrdinanceMemberViewSet)
router.register(r'adminunit', views.AdminUnitViewSet)

urlpatterns = router.urls
