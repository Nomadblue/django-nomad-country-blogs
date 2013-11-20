from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.conf import settings

from nomadblog.models import Blog, Category
from nomadblog import get_post_model


DEFAULT_STATUS = getattr(settings, 'PUBLIC_STATUS', 0)
POST_MODEL = get_post_model()


class NomadBlogMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(NomadBlogMixin, self).get_context_data(*args, **kwargs)
        context['blog'] = get_object_or_404(Blog, country_code=self.kwargs.get('country_code'), slug=self.kwargs.get('blog_slug'))
        return context


class PostList(NomadBlogMixin, ListView):
    model = POST_MODEL
    template_name = 'nomadblog/list_posts.html'


class PostDetail(NomadBlogMixin, DetailView):
    model = POST_MODEL
    template_name = 'nomadblog/show_post.html'


class PostsByCategoryList(NomadBlogMixin, ListView):
    model = POST_MODEL
    template_name = 'nomadblog/list_posts_by_category.html'

    def get_queryset(self, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('category_slug', ''))
        return self.model.objects.filter(category=self.category)

    def get_context_data(self, *args, **kwargs):
        context = super(PostsByCategoryList, self).get_context_data(*args, **kwargs)
        context['category'] = self.category
        return context


class CategoriesList(NomadBlogMixin, ListView):
    model = Category
    template_name = 'nomadblog/list_categories.html'
