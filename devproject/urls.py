from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from . import settings_common
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('devapp.urls')),
    path("accounts/", include("accounts.urls")),
     # LB からのヘルスチェックに答えるためのURLで、アプリが起動していれば常に 200 OK を返す
    path('status/', lambda request: HttpResponse()),
]

# 以下、DEBUG=Trueの時用
urlpatterns += static(settings_common.STATIC_URL, document_root=settings_common.STATIC_ROOT)
urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_common.MEDIA_ROOT)