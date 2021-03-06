"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.authorization.views import AuthViewSet
from app.candidates.views import CandidateViewSet
from app.elections.views import PoolViewSet, VoteViewSet, TimeViewSet

from config.settings import DEBUG
from config.components.static import MEDIA_ROOT, MEDIA_URL
from config.components.common import SHOW_DOCS

from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from . import docs


route = routers.SimpleRouter()
route.trailing_slash = ''
route.register('auth', AuthViewSet, 'auth')
route.register('candidates', CandidateViewSet)
route.register('vote-pools', PoolViewSet)
route.register('votes', VoteViewSet)
route.register('time', TimeViewSet)

admin.site.site_title = '北商投票系統管理'
admin.site.site_header = '北商投票系統後台'
admin.site.index_title = '系統管理'

urlpatterns = [
    path('api/', include(route.urls)),
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if SHOW_DOCS:
    urlpatterns += [path('docs/', include_docs_urls(**docs.config))]
