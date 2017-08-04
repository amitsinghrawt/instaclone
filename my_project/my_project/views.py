# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect,HttpResponseRedirect,HttpResponse,Http404
from django.utils import timezone
from imgurpython import ImgurClient
from settings import BASE_DIR

from forms import SignUpFrom, LoginFrom, PostFrom, LikeFrom,CommentFrom
from models import UserModel, Seccion_token, LikeModel, PostModel,CommentModel,swachh_bharat
from clarifai.rest import ClarifaiApp

dirty_list=['garbage','waste','polluttion','junk','trash','litter','disposal']
CLARIFY_KEY='be172b9581264b87a0761d85e2a4597e'


def signup_view(request):

    if request.method == "POST":

        form = SignUpFrom(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)

            user.save()

            return render(request, 'success.html') # return redirect('login/')
        else:
            print "worng username"
            return render(request,"index.html")
    elif(request.method=="GET"):
            form = SignUpFrom()
            return render(request, 'index.html', {'form': form})

def Login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = Seccion_token(user=user)
                    token.create_token()
                    token.save()
                    response= redirect("feed/")
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
            else:

                return render(request, 'login.html')

    elif request.method == 'GET':
        form = LoginFrom()
        response_data['form'] = form
        return render(request, 'login.html', response_data)

def feed_view(request):
    user = check_validantion(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')


def post_view(request):
    user = check_validantion(request)
    if user:
        if request.method == 'GET':
            form = PostFrom()
            return render(request, 'post.html', {'form': form, 'user': user})
        elif request.method == 'POST':
            form = PostFrom(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                path = str(BASE_DIR +"/user_images/"+ post.image.url)
                post.save()
                client = ImgurClient("e86df9c6155435d", "b2d3db1d4409ce0edf07cf05d46eda64af25ac08")
                post.image_url = client.upload_from_path(path, anon=True)['link']
                swachh_bharat(post)
                post.save()

                return render(request, 'post.html', {'form': form, 'user': user})
            else:
                return render(request, 'post.html', {'form': form, 'user': user,'error':"Unable to Add Post"})

    else:
        return redirect('/login/')

def like_view(request):
    user = check_validantion(request)
    if user and request.method == 'POST':
        form = LikeFrom(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


def check_validantion(request):
    if request.COOKIES.get('session_token'):
        session = Seccion_token.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
            else:
                print "nothing"
        else:
            print "no way"
    else:
        return None


def comment_view(request):
    user = check_validantion(request)
    if user and request.method=='POST':
        print ' user valid and post called'
        comment_obj = CommentFrom(request.POST)
        if comment_obj.is_valid():
            print ' comment form valid'
            post_id=comment_obj.cleaned_data.get('post').id
            comment_text=comment_obj.cleaned_data.get('comment_text')
            comment=CommentModel.objects.create(username=user , post_id=post_id, comment_text=comment_text)
            comment.save()

        else :
            print ' comment form invalid'
            return redirect('/feed/')

    else :
        print ' not logged in '
        return redirect ('/login/')

    return redirect('/feed/')

def logout_view(request):
    user=check_validantion(request)
    if user is not None:
        latest_sessn = Seccion_token.objects.filter(user=user).last()
        if latest_sessn:
            latest_sessn.delete()
            return redirect("/login/")
        else:
            return redirect('/feeds/')
def swachh_bharat(post):
    app = ClarifaiApp(api_key=CLARIFY_KEY)
    model = app.models.get('general-v1.3')
    response = model.predict_by_url(url=post.image_url)

    if response["status"]["code"] == 10000:
        if response["outputs"]:
            if response["outputs"][0]["data"]:
                if response["outputs"][0]["data"]["concepts"]:
                    for index in range(0, len(response["outputs"][0]["data"]["concepts"])):
                        if response["outputs"][0]["data"]["concepts"][index]["name"] in dirty_list:
                            category = swachh_bharat(post=post,text=response["outputs"][0]["data"]["concepts"][index]["name"])
                            category.save()
                        else:
                            pass
                else:
                    print "No Concepts List Found"
            else:
                print "No Data List Found"
        else:
            print "No Outputs List Found"
    else:
        print "Response Code Error"