from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Comment, UserProfile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth
#from moviepy.editor import *

# Create your views here.

@login_required
def UploadView(request):
    #Used When Query Search Used in Video Detail View to redirect to the search view.
    if request.GET.get('query'):
        return redirect('/videos/?query=' + request.GET.get('query') )
    if request.FILES.get('video'):
        print("AT LEAST VIDEO IS WORKING")
        if request.POST.get('title') and request.FILES.get('thumbnail') and request.FILES.get('video') and request.POST.get('description'):
            video = Video()
            video.title = request.POST.get('title')
            video.description = request.POST.get('description')
            video.thumbnail = request.FILES.get('thumbnail')
            video.video = request.FILES.get('video')
            video.user = request.user
            video.save()
            return redirect('/videos/' + str(video.id))

    return render(request, 'videos/upload.html', {})


def VideosView(request):

    queryset_list = Video.objects.all()
    query = request.GET.get('query')
    if query:
        queryset_list = queryset_list.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)|
        Q(user__username__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5) # Show 25 comments per page
    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    likes_percent = {}
    for i in range(0,len(queryset)):
        tempquery = queryset.object_list.all()[i]
        if tempquery.dislikes == 0 and tempquery.likes == 0:
            likes_percent[tempquery.id] = 0
        elif tempquery.dislikes == 0 and tempquery.likes !=0:
            likes_percent[tempquery.id] = 100
        else:
            likes_percent[tempquery.id] = 100*(tempquery.likes/(tempquery.likes+tempquery.dislikes))

    print(likes_percent)
    return render(request, 'videos/videos.html', {'queryset': queryset,'likes_percent':likes_percent})


@login_required
def LikeComment(request, comment_id, video_id):

    comment = get_object_or_404(Comment, pk = comment_id)

    hasRated = False
    for rateduser in comment.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        comment.likes = comment.likes + 1
        comment.ratedUsers.add(request.user)
        comment.save()
    else:
        print("HAS ALREADY RATED THIS COMMENT!")


    return redirect('/videos/'+str(video_id))
@login_required
def DislikeComment(request, comment_id, video_id):

    comment = get_object_or_404(Comment, pk = comment_id)

    hasRated = False
    for rateduser in comment.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        comment.dislikes = comment.dislikes + 1
        comment.ratedUsers.add(request.user)
        comment.save()
    else:
        print("HAS ALREADY RATED THIS COMMENT!")


    return redirect('/videos/'+str(video_id))

@login_required
def LikeVideo(request,video_id):
    video = get_object_or_404(Video, pk = video_id)
    hasRated = False
    for rateduser in video.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        video.likes = video.likes + 1
        video.ratedUsers.add(request.user)
        video.save()
    else:
        print("HAS ALREADY VOTED!")

    return redirect('/videos/'+str(video_id))

@login_required
def DislikeVideo(request,video_id):
    video = get_object_or_404(Video, pk = video_id)
    hasRated = False
    for rateduser in video.ratedUsers.all():
        if rateduser.username == request.user.username:
            hasRated = True
            break
    if hasRated == False:
        video.dislikes = video.dislikes + 1
        video.ratedUsers.add(request.user)
        video.save()
    else:
        print("HAS ALREADY VOTED!")

    return redirect('/videos/'+str(video_id))

def VideoDetailView(request,video_id):


    video = get_object_or_404(Video, pk = video_id)
    videoUserName = video.user.username
    userprofile = get_object_or_404(UserProfile, username=videoUserName)


    recentvideos =Video.objects.all()
    tempvideos= []
    count = 0
    #adding first 4 new videos, not including the playing one, to the recommendations
    for recentvideo in recentvideos:
        if recentvideo.id != video_id:
            tempvideos.append(recentvideo)
            count= count +1
            if count >= 4:
                break


    recentvideos = tempvideos


    queryset_list = video.comments.all()
    paginator = Paginator(queryset_list, 3) # Show 25 comments per page
    #paginator = Paginator(comment_list, 1) # Show 25 comments per page
    page = request.GET.get('page')
    queryset = paginator.get_page(page)


    #Used When Query Search Used in Video Detail View to redirect to the search view.
    if request.GET.get('query'):

        return redirect('/videos/?query=' + request.GET.get('query') )


    if request.method == 'POST' and 'submitComment' in request.POST and request.POST.get('textareaComment') and request.user.is_authenticated:

        comment = Comment()
        comment.comment = request.POST.get('textareaComment')
        comment.user = request.user
        commentUserName = request.user.username
        commentUserProfile = get_object_or_404(UserProfile, username=commentUserName)
        comment.picture = commentUserProfile.picture
        comment.save()
        video.comments.add(comment)

    videoUserName = video.user.username
    userprofile = get_object_or_404(UserProfile, username=videoUserName)
    #adding a view with every video detail GET request
    video.views = video.views + 1
    video.save()





    return render(request,'videos/videodetail.html',{'video':video,'queryset':queryset,'recentvideos':recentvideos, 'userprofile':userprofile})
