from django import forms
from django.forms import widgets
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, label="نام کاربری")
    password = forms.CharField(
        max_length=120, widget=forms.PasswordInput, label="رمز عبور"
        )
    # save_information = forms.ChoiceField(
    #     label=" ر",
    #     choices=((True, "ذخیره کن"), (False, "ذخیره نکن")),
    # )
    # users = forms.ModelChoicefireld(label="", queyset=User.objects.all())

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password', 'email']

        labels = {
            'username':_("*نام کاربری"),
            'password':_("*رمز عبور"),
            'email':_("آدرس ایمیل"),
        }  

        help_texts = {
            'username': ("")
        } 

        widgets={
           'password':(forms.PasswordInput)
        }

        error_messages ={
            'username':{
            'required':_("فیلد نام کاربری ضروری است"),
            },

            'password':{
            'required':_("فیلد رمز عبور ضروری است "),
         
            },    
        }

class ResetPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,label=_("رمز عبور"),error_messages={'required': 'رمز عبور خود را وارد کنید'})
    new_password = forms.CharField(widget=forms.PasswordInput,label=_("رمز جدید"),error_messages={'required': 'رمز عبور جدید خود را وارد کنید'})
    repeat_password = forms.CharField(widget=forms.PasswordInput,label=_("تکرار رمز جدید"),error_messages={'required': ' لطفا رمز عبور جدید را تکرار کنید'})

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data['repeat_password']
        new_password = self.cleaned_data['new_password']
        if new_password != repeat_password:
            raise ValidationError("رمز عبور جدید و تکرار آن باید یکی باشند")
        return repeat_password

        

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["title"]

        labels = {
            'title':_("*نام تگ"),
           
        } 

        error_messages ={
            'title':{
            'required':_("فیلد نام تگ باید پر شود"),
            }}

    def create(self):
        print(self.cleaned_data)
        Tag.objects.create(title=self.cleaned_data["title"])

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["parent","title","description"]

        labels = {
            'parent':_("دسته بندی مادر"),
            'title':_("نام"),
            'description':_("توضیحات"),
        } 

        error_messages ={
            'title':{
            'required':_("فیلد نام دسته بندی باید پر شود"),
            },
            'description':{
            'required':_("فیلد توضیحات باید پر شود"),
            },
            
            }

    def create(self):
        print(self.cleaned_data)
        Category.objects.create(parent=self.cleaned_data["parent"],title=self.cleaned_data["title"],description=self.cleaned_data["description"])      


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["category","title","short_description","description","tag","image","is_published"]

        labels = {
            'category':_("دسته بندی "),
            'title':_("نام"),
            'short_description':_("توضیحات کوتاه"),
            'description':_("توضیحات"),
            'tag':_("تگ"),
            'image':_("تصویر"),
            'is_published':_("منتشر شود؟ "),
        } 

        error_messages ={
            'title':{
            'required':_("فیلد نام دسته بندی باید پر شود"),
            },
            'description':{
            'required':_("فیلد توضیحات باید پر شود"),
            },
            'short_description':{
            'required':_("فیلد توضیحات کوتاه باید پر شود"),
            },
            'category':{
            'required':_("فیلد دسته بندی باید پر شود"),
            },
            
            }


class DeleteTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = []

class DeleteCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []    

class DeletePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []             


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['title','description']   
        labels = {
            'title':_("عنوان"),
            'description':_("متن"),
        }     

        error_messages ={
            'title':{
            'required':_("فیلد های ضروری را وارد کنید"),
            'max_length':_("تعداد کاراکتر باید کمتر از 120 باشد"),
            },
        }


class EmailForm(forms.Form):
    title = forms.CharField(max_length=100,label="عنوان",error_messages={'required': 'وارد کردن عنوان ضروری است'})
    message = forms.CharField(widget=forms.Textarea,label="متن پیام",error_messages={'required': ' این فیلد نباید خالی باشد  '})




