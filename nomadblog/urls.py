from django.conf.urls import patterns, url
from nomadblog.views import PostList, PostDetail, PostsByCategoryList, CategoriesList


urlpatterns = patterns(
    '',
    url(r'^$', PostList.as_view(), name='list_posts'),
    url(r'^categories/$', CategoriesList.as_view(), name='list_categories'),
    url(r'^categories/(?P<category_slug>[-\w]+)/$', PostsByCategoryList.as_view(), name='list_posts_by_category'),
    url('^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='show_post'),
)
