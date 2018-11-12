from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.VideosView, name = 'videos'),
    path('upload/',views.UploadView,name='upload'),
    path('<int:video_id>', views.VideoDetailView, name='detail'),
    path('like_comment/<int:comment_id>/<int:video_id>', views.LikeComment,name='like_comment'),
    path('dislike_comment/<int:comment_id>/<int:video_id>', views.DislikeComment,name='dislike_comment'),
    path('like_video/<int:video_id>', views.LikeVideo, name='like_video'),
    path('dislike_video/<int:video_id>', views.DislikeVideo, name = 'dislike_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
