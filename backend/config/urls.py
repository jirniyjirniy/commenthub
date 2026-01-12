from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from strawberry.django.views import GraphQLView
from app.graphql.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/user/", include("app.users.urls")),

    path("api/comments/", include("app.comments.urls")),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)