from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from recipes import views as recipe_views


urlpatterns = [
    path("404", recipe_views.page_not_found),
    path("500", recipe_views.server_error),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
]


handler404 = "recipes.views.page_not_found"  # noqa
handler500 = "recipes.views.server_error"  # noqa

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    # urlpatterns += static(
    #     settings.STATIC_URL, document_root=settings.STATIC_ROOT
    # )