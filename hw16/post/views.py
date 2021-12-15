from django.http import request
from django.shortcuts import redirect,render,get_list_or_404, get_object_or_404,HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, Post, Comment, Tag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q



User = get_user_model() 


class PostList(ListView):
    model = Post
    template_name = "post/index.html"
    queryset = Post.objects.all()[:4]


class AllPosts(ListView):
    model = Post
    template_name = "post/all_post.html"


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post__slug=f"{slug}")
    categories = post.category.all()
    tags = post.tag.all()
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect(reverse("post_detail", kwargs={"slug": slug}))
    return render(
        request,
        "post/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "categories": categories,
            "tags": tags,
            "form": form,
        },
    )


class CateegoryList(ListView):
    model = Category
    template_name = "post/category_list.html"


def category_post(request, slug):
    posts = Post.objects.filter(category__slug=f"{slug}")
    return render(
        request, "post/category_post.html", {"posts": posts, "category_name": slug}
    )

def dashboard(request):
    user = request.user
    user_posts = Post.objects.filter(writer=user)
    print (user)
    return render(request, "post/dashboard.html",{"user_posts":user_posts})


class TagList(ListView):
    model = Tag
    template_name = "post/tag_list.html"


def tag_post(request, slug):
    posts = Post.objects.filter(tag__slug=f"{slug}")
    return render(request, "post/tag_post.html", {"posts": posts, "tag_name": slug})

class SearchView(ListView):
    template_name = "post/search.html"
    context_object_name ='posts'    

    def  get_queryset(self):
        queryset = Post.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__contains=q) | Q(description__contains=q))
        return queryset


class TemplateView(TemplateView):
    template_name = "main.html"


class PostView(TemplateView):
    template_name = "post.html"


"""                Forms                       """


def login_form(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        #   print(form.cleaned_data)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                messages.success(request, 'با موفقیت وارد شدید')
                login(request, user)
                next = request.GET.get('next')
                if next:
                        return redirect(next)
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, 'یوزرنیم و پسورد اشتباه است',extra_tags='danger')
    return render(request, "form/login_form.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse("home"))

def register_form(request):
    form = UserRegisterForm(None or request.POST)
    if form.is_valid():
        user = User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password"],
        )
        user.save()
        messages.success(request, 'با موفقیت عضو شدید')
        return redirect(reverse("home"))
    return render(request, "form/register_form.html", {"form": form})
    

@login_required(login_url="/login") 
def set_new_password(request):
    form = ResetPassword(None or request.POST) 
    if form.is_valid():
        user = request.user
        print(user)
        if user.check_password(form.cleaned_data.get('password')):
            user.set_password(form.cleaned_data.get('new_password'))
            messages.success(request, 'رمز شما با موفقیت تغییر کرد')
            user.save()
            return redirect(reverse("login"))
    return render(request, "form/reset_password_form.html",{"form":form})    

@login_required(login_url="/login")
def add_tag_form(request):
    form = TagForm(None or request.POST)
    print(request.user.id)  ###!!!
    if form.is_valid():
        form.create()
        messages.success(request, ' تگ جدید با موفقیت اضافه شد')
        return redirect(reverse("tags"))
    return render(request, "form/add_tag_form.html", {"form": form})

@login_required(login_url="/login")
def add_category_form(request):
    form = CategoryForm(None or request.POST)
    print(request.user.id)  ###!!!
    if form.is_valid():
        form.create()
        messages.success(request, 'دسته بندی جدید با موفقیت اضافه شد')
        return redirect(reverse("categories"))
    return render(request, "form/add_category_form.html", {"form": form})    

@login_required(login_url="/login")
def add_post_form(request):
    form = PostForm(None or request.POST)
    print(request.user.id)  ###!!!
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.writer = request.user
        new_post.save()
        form.save_m2m()
        messages.success(request, ' پست جدید با موفقیت اضافه شد')
        return redirect(reverse("dashboard"))
    return render(request, "form/add_post_form.html", {"form": form}) 

@login_required(login_url="/login") 
def edit_tag_form(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    form = TagForm(instance=tag)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, ' تگ موردنظر با موفقیت ویرایش شد')
        return redirect(reverse("tags"))
    return render(request, "form/edit_tag_form.html", {"form": form, "slug": slug})
   
@login_required(login_url="/login") 
def edit_category_form(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, ' دسته بندی موردنظر با موفقیت ویرایش شد')
        return redirect(reverse("categories"))
    return render(request, "form/edit_category_form.html", {"form": form, "slug": slug}) 

@login_required(login_url="/login") 
def edit_post_form(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.id == post.writer.id:
     form = PostForm(instance=post)
     if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, ' پست موردنظر با موفقیت ویرایش شد')
        return redirect(reverse("dashboard"))
     return render(request, "form/edit_post_form.html", {"form": form, "slug": slug})
    else:
        messages.warning(request, ' تنها پست های خودتان را می توانید ویرایش کنید')
        return redirect(reverse("home"))         

@login_required(login_url="/login") 
def delete_tag_form(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    form = DeleteTagForm(instance=tag)
    if request.method == "POST":
        tag.delete()
        messages.success(request, ' تگ موردنظر با موفقیت حذف شد')
        return redirect(reverse("tags"))
    return render(request, "form/delete_tag_form.html", {"form": form, "slug": slug})

@login_required(login_url="/login") 
def delete_category_form(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = DeleteCategoryForm(instance=category)
    if request.method == "POST":
        category.delete()
        messages.success(request, ' دسته بندی موردنظر با موفقیت حذف شد')
        return redirect(reverse("categories"))
    return render(request, "form/delete_category_form.html", {"form": form, "slug": slug}) 


@login_required(login_url="/login") 
def delete_post_form(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.id == post.writer.id:
     form = DeletePostForm(instance=post)
     if request.method == "POST":
        post.delete()
        messages.success(request, ' پست موردنظر با موفقیت حذف شد')
        return redirect(reverse("dashboard"))
     return render(request, "form/delete_post_form.html", {"form": form, "slug": slug})
    else:
        messages.warning(request, ' تنها پست های خودتان را می توانید حذف کنید')
        return redirect(reverse("home"))     

def contact_us_form(request):
    messageSent = False
    form = EmailForm(None or request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        message = form.cleaned_data["message"] 

        send_mail(title, message,
                      settings.DEFAULT_FROM_EMAIL, ['alidtaha@gmail.com']) 
        messages.success(request, 'نامه شما ارسال شد ')
    return render(request, "form/contactus.html",{"form":form,"messageSent":messageSent})         


"""                API                         """


@api_view(["GET", "POST"])
def post_list_api(request):
    if request.method == "GET":

        posts = Post.objects.filter(is_published=True)
        serializer = PostListSerializer(posts, many=True)

        return Response(data=serializer.data, status=200)
    elif request.method == "POST":
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            resp_serializer = PostSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def post_api(request, id):

    post = get_object_or_404(Post, id=id)
    serializer = PostSerializer(post)

    return Response(data=serializer.data, status=200)


@api_view(["GET"])
def category_list_api(request):

    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)

    return Response(data=serializer.data, status=200)


@api_view(["GET"])
def category_api(request, id):

    category = get_object_or_404(Category, id=id)
    serializer = CategorySerializer(category)

    return Response(data=serializer.data, status=200)


@api_view(["GET"])
def comment_list_api(request):

    comments = Comment.objects.all()
    serializer = CommentListSerializer(comments, many=True)

    return Response(data=serializer.data, status=200)


@api_view(["GET"])
def comment_api(request, id):

    comment = get_object_or_404(Comment, id=id)
    serializer = CommentSerializer(comment)

    return Response(data=serializer.data, status=200)
