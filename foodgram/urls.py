from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views as flatpages_views
from django.urls import include, path

from recipes import views as recipe_views

urlpatterns = [
    path("404", recipe_views.page_not_found),
    path("500", recipe_views.server_error),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('', include('recipes.urls')),
]

urlpatterns += [
    path(
        "about/author/",
        flatpages_views.flatpage,
        {"url": "/author/"},
        name="about_author",
    ),
    path(
        "about/spec/",
        flatpages_views.flatpage,
        {"url": "/spec/"},
        name="about_spec",
    ),
]

handler404 = "recipes.views.page_not_found"  # noqa
handler500 = "recipes.views.server_error"  # noqa

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
