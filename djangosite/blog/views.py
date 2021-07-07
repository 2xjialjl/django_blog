from django.shortcuts import render, redirect
from .models import _get_articles, _create_articles, _get_articles_by_id, _edit_articles_by_id, _del_articles_by_id
from .create_articles import create_articles_form, edit_article_form
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .form import django_form
# Create your views here.
def index(request):
    articles = _get_articles()
    content = {"articles": articles}
    return render(request, 'index.html', content)


def articles(request,a_num):
    form = django_form()
    if request.user.is_authenticated:
        context = {"form": form, "user": request.user.usernames}
    else:
        context = {"form": form, "user": ""}
    return render(request,"articles.html",context)


def create_article(request):
    if request.method == 'POST':
        _create_articles(request)
        return redirect("index")
    else:
        form = create_articles_form()
        context = {"form": form, "user": ""}
        return render(request, "create_articles.html", context)

def edit_article(request, a_id):
    if request.method == "POST":
        _edit_articles_by_id(request, a_id)
        return redirect("index")
    else:
        form = edit_article_form(a_id)
        context = {"form": form, "id": a_id}
        return render(request, "edit_articles.html", context)

def delete_article(request,a_id):
    _del_articles_by_id(a_id)
    return redirect("index")


def login(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    return redirect("index")


def usr_login(request):
    user = authenticate(request, username= request.POST['username'], password= request.POST['password'])
    if user is not None:
        auth_login(request,user)
        return redirect('index')
    else:
        return redirect('usr_login')

def usr_logout(request):
    auth_logout(request)
    return redirect('index')

def view_article(request,a_id):
    context = {"article":_get_articles_by_id(a_id)}
    return render(request,"show_articles.html",context)