from gc import get_objects
from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView,
)

# from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.http import (
    HttpResponseRedirect,
)

from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from .models import User, Article, UserProfile, Follow
from .forms import ArticleForm, CommentForm, UserForm, UserProfileForm, RegisterForm
from taggit.models import Tag


class HomeView(ListView):
    model = Article
    paginate_by = 5

    def get_context_data(self, object_list=None, *args, **kwargs):
        queryset = Article.objects.filter().order_by("-timestamp")
        common_tags = Article.tag.most_common()[:5]

        return super().get_context_data(
            object_list=queryset, common_tags=common_tags, **kwargs
        )


class Tagged(ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return super().get_queryset().filter(tag=tag)


class OurStory(View):
    def get(self, request):
        return render(request, "web/our_story.html")


class ArticleCreateView(CreateView):
    form_class = ArticleForm

    def form_valid(self, form):
        try:
            save_post = form.save(commit=False)
            save_post.article_author = self.request.user
            save_post.slug = slugify(save_post.headline)
            save_post.save()
            form.save_m2m()
            messages.success(self.request, ("Your article was successfully updated!"))
            return HttpResponseRedirect(reverse_lazy("home"))
        except IntegrityError as err:
            messages.error(self.request, f"Something went wrong!")
            return HttpResponseRedirect(reverse_lazy("home"))


class EditArticle(UpdateView):
    queryset = Article.objects.all()
    form_class = ArticleForm
    slug_url_kwarg = "pk"

    def form_valid(self, form):
        try:
            save_post = form.save(commit=False)
            save_post.article_author = self.request.user
            save_post.slug = slugify(save_post.headline)
            save_post.save()
            form.save_m2m()
            messages.success(self.request, ("Your article was successfully updated!"))
            return HttpResponseRedirect(reverse_lazy("home"))
        except IntegrityError as err:
            messages.error(self.request, f"Something went wrong!")
            # To bylo return HttpResponseRedirect(reverse_lazy('edit_article'))
            return HttpResponseRedirect(reverse("edit_article", args=[str(self.pk)]))


class ArticleDetail(DetailView):
    model = Article
    #form_class = CommentForm

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        view_article = Article.objects.get(pk=pk)
        return view_article

    def get_context_data(self, **kwargs):
        # queryset = Article.objects.filter(article_author=self.request.user).order_by(
        #     "-timestamp"
        # )
        # all_users = UserProfile.objects.all()
        # common_tags = Article.tag.most_common()[:5]

        # return super().get_context_data(
        #     object_list=queryset, all_users=all_users, common_tags=common_tags, **kwargs
        # )
        article = self.get_object()
        comments = article.comment.filter()
        likes = article.likes.filter()
        comment_form = CommentForm(instance=self.request.user)

        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        #New logic needed to this checker!!!!
        follow_checker = [
            True
            if int(article.article_author.id)
            in [i.follow_writter_id for i in Follow.objects.filter(user=self.request.user)]
            else False
        ][0]
        #########
        return super().get_context_data(
            article = article,
            comments = comments,
            likes = likes,
            liked = liked,
            follow_checker = follow_checker,
            comment_form = comment_form,
        )


    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.article = self.get_object()
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
    # def form_valid(self, form):
    #         new_comment = form.save(commit=False)
    #         new_comment.post = self.get_object()
    #         return super(ArticleDetail, self).form_valid(form)

    # def form_valid(self, form):
    #     new_comment = form.save(commit=False)
    #     new_comment.user = self.request.user
    #     new_comment.article = self.article
    #     new_comment.save()



# @login_required
# def article_detail(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     comments = article.comment.filter()
#     likes = article.likes.filter()
#     all_users = UserProfile.objects.all()
#     #created_by = Article.objects.get(pk=pk)
#     new_comment = None
#     liked = False
#     if article.likes.filter(id=request.user.id).exists():
#         liked = True

#     follow_checker = [
#         True
#         if int(article.article_author.id)
#         in [i.follow_writter_id for i in Follow.objects.filter(user=request.user)]
#         else False
#     ][0]

#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.user = request.user
#             new_comment.article = article
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     context = {
#         "article": article,
#         "comments": comments,
#         "new_comment": new_comment,
#         "comment_form": comment_form,
#         "likes": likes,
#         "liked": liked,
#         "follow_checker": follow_checker,
#         "all_users": all_users,
#         #"created_by":created_by,
#     }

#     return render(request, "web/article_detail_view.html", context)

#MESSAGE DOES NOT WORK HERE TO FIX!!!!
class DeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    #success_message = "Your article was successfully deleted!"

    def delete(self, request, *args, **kwargs):
        response = super(DeleteView, self).delete(request, *args, **kwargs)
        messages.success(request, ("Your article was successfully deleted!"))
        return response

# def delete(request):
#     article_to_delete = get_object_or_404(Article, id=request.POST.get("article_id"))
#     if request.method == "POST" and request.user.is_authenticated:
#         article_to_delete.delete()
#         messages.success(request, ("Your article was successfully deleted!"))
#     else:
#         messages.warning(request, ("Something went wrong!"))
#     return HttpResponseRedirect(reverse_lazy("home"))


def like(request, pk):

    article = get_object_or_404(Article, id=request.POST.get("article_id"))

    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("article_detail", args=[int(pk)]))


def follow(request, pk):

    get_user_to_follow = request.POST.get("article_writer_id")
    follow = Follow(user=request.user, follow_writter_id=int(get_user_to_follow))
    checker = [
        follow.follow_writter_id for follow in Follow.objects.filter(user=request.user)
    ]

    if request.method == "POST":

        if int(get_user_to_follow) == request.user.id:
            Follow.objects.filter(follow_writter_id=int(get_user_to_follow)).delete()
            message = messages.warning(request, "You cannot follow your self!")

        elif int(get_user_to_follow) in checker:
            Follow.objects.filter(follow_writter_id=int(get_user_to_follow)).delete()

        else:
            follow.save()

    return HttpResponseRedirect(reverse("article_detail", args=[int(pk)]))


@login_required
def profile(request):
    user_info = UserProfile.objects.filter(profile=request.user)
    user_followers = [
        str(all_users.follow_writter_id) for all_users in Follow.objects.all()
    ].count(str(request.user.id))
    user_follow = [
        i.follow_writter_id for i in Follow.objects.filter(user=request.user.id)
    ]
    print(user_follow)

    context = {
        "user_followers": user_followers,
        "user_info": user_info,
        "user_follow": user_follow,
    }
    return render(request, "web/profile.html", context)


@login_required
def create_user_info(request):
    form = UserProfileForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            save_user_info = form.save(commit=False)
            save_user_info.profile = request.user
            save_user_info.save()
            messages.success(request, ("Your User info was successfully added!"))
            return redirect(to="profile")
        else:
            messages.error(request, f"Something went wrong!")
            return redirect(to="profile")

    context = {
        "form": form,
    }
    return render(request, "web/create_user_info.html", context)


@login_required
def edit_user_info(request):
    user = get_object_or_404(User, id=request.user.id)
    user_profile = get_object_or_404(UserProfile, profile=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="profile")
    else:

        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "web/update_user_info.html", context)


class WrittenStories(ListView):
    model = Article
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = Article.objects.filter(article_author=self.request.user).order_by(
            "-timestamp"
        )
        all_users = UserProfile.objects.all()
        common_tags = Article.tag.most_common()[:5]

        return super().get_context_data(
            object_list=queryset, all_users=all_users, common_tags=common_tags, **kwargs
        )


class RegisterView(CreateView):
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("home")


class Login(LoginView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        # user = form.save()
        # login(self.request, self.user)
        login(self.request, form.get_user())
        return redirect("home")


class Logout(LogoutView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home"))
