from django.urls import path
from .views import *


urlpatterns = [
    path("", PostList.as_view(), name="home"),
    path("post/<slug:slug>", post_details, name="post_detail"),
    path("post/", AllPosts.as_view(), name="posts"),
    path("category/", CateegoryList.as_view(), name="categories"),
    path("category/<slug:slug>", category_post, name="category_post"),
    path("tag/", TagList.as_view(), name="tags"),
    path("tag/<slug:slug>", tag_post, name="tag_post"),
    path("theme-view", TemplateView.as_view()),
    path("post-view", PostView.as_view()),
    
    path("api/post/", post_list_api, name="post_list_api"),
    path("api/post/<int:id>", post_api, name="post_api"),
    path("api/category/", category_list_api, name="category_list_api"),
    path("api/category/<int:id>", category_api, name="category_api"),
    path("api/comment/", comment_list_api, name="comments_list_api"),
    path("api/comment/<int:id>", comment_api, name="comments_api"),
    
    path("login", login_form, name="login_form"),
    path("logout", logout_view, name="logout"),
    path("register", register_form, name="register_form"),
    path("dashboard", dashboard, name="dashboard"),
    path("reset_password", set_new_password, name="reset_password_form"),
    path("add_tag", add_tag_form, name="add_tag_form"),
    path("add_category", add_category_form, name="add_category_form"),
    path("add_post", add_post_form, name="add_post_form"),
    path("edit_tag/<slug:slug>", edit_tag_form, name="edit_tag_form"),
    path("edit_category/<slug:slug>", edit_category_form, name="edit_category_form"),
    path("edit_post/<slug:slug>", edit_post_form, name="edit_post_form"),
    path("delete_tag/<slug:slug>", delete_tag_form, name="delete_tag_form"),
    path("delete_category/<slug:slug>", delete_category_form, name="delete_category_form"),
    path("delete_post/<slug:slug>", delete_post_form, name="delete_post_form"),

    path("contact_us", contact_us_form, name="contact_us_form"),
    path("search", SearchView.as_view(), name="search"),

]
