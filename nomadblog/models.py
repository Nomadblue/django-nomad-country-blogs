from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


class BlogHub(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.name


class Blog(models.Model):
    """
    Ref for ``country_code`` field:
    http://www.iso.org/iso/home/standards/country_codes/country_names_and_code_elements_txt.htm
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    country_code = models.CharField(max_length=2)
    slug = models.SlugField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogUser')
    hubs = models.ManyToManyField(BlogHub)

    class Meta:
        unique_together = ('country_code', 'slug')

    def __unicode__(self):
        return u"%s - %s" % (self.title, self.country_code)

    def get_absolute_url(self):
        return reverse('list_posts', kwargs={'country_code': self.country_code, 'blog_slug': self.slug})


class BlogUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    blog = models.ForeignKey(Blog)
    bio = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.blog)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    PUBLIC_STATUS = 0
    DRAFT_STATUS = 1
    PRIVATE_STATUS = 2
    DEFAULT_POST_STATUS_CHOICES = (
        (PUBLIC_STATUS, 'public'),
        (DRAFT_STATUS, 'draft'),
        (PRIVATE_STATUS, 'private'),
    )
    POST_STATUS_CHOICES = getattr(settings,
                                  'POST_STATUS_CHOICES',
                                  DEFAULT_POST_STATUS_CHOICES)

    bloguser = models.ForeignKey(BlogUser)
    pub_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=POST_STATUS_CHOICES, default=0)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'country_code': self.bloguser.blog.country_code, 'blog_slug': self.bloguser.blog.slug, 'slug': self.slug})

    def __unicode__(self):
        return u"%s - %s" % (self.bloguser, self.title)

    class Meta:
        abstract = True
