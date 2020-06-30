from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from blogs.views import BlogViewSet

router = SimpleRouter(trailing_slash=False)

router.register('blog', BlogViewSet, basename='blog')
urlpatterns = router.urls
