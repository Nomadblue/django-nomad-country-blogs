from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.validators import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ObjectDoesNotExist


class BlogHub(models.Model):
    name = models.CharField(_('blog hub'), max_length=100)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = _('blog hub')
        verbose_name_plural = _('blog hubs')


class Blog(models.Model):
    """
    Ref for ``country_code`` field:
    http://www.iso.org/iso/home/standards/country_codes/country_names_and_code_elements_txt.htm
    """
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=50)
    description = models.TextField(_('description'))
    country_code = models.CharField(_('iso country code'), max_length=2)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogUser', verbose_name=_('users'))
    hubs = models.ManyToManyField(BlogHub, verbose_name=_('hubs'))
    seo_title = models.CharField(_('seo title'), max_length=70, blank=True)
    seo_desc = models.CharField(_('seo meta description'), max_length=160, blank=True)

    class Meta:
        unique_together = ('country_code', 'slug')
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def __unicode__(self):
        return u"%s - %s" % (self.title, self.country_code)

    def get_absolute_url(self):
        return reverse('list_posts', kwargs={'country_code': self.country_code, 'blog_slug': self.slug})


class BlogUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    slug = models.SlugField(_('slug'), max_length=50)
    blog = models.ForeignKey(Blog, verbose_name=_('blog'))
    bio = models.CharField(_('bio'), max_length=255, blank=True)
    seo_title = models.CharField(_('seo title'), max_length=70, blank=True)
    seo_desc = models.CharField(_('seo meta description'), max_length=160, blank=True)

    def __unicode__(self):
        return u"%s - %s" % (self.user.username, self.blog)

    class Meta:
        verbose_name = _('blog user')
        verbose_name_plural = _('blog users')

    def validate_unique(self, *args, **kwargs):
        super(BlogUser, self).validate_unique(*args, **kwargs)
        try:
            obj = self.__class__._default_manager.get(blog__country_code=self.blog.country_code, blog__slug=self.blog.slug, slug=self.slug)
        except ObjectDoesNotExist:
            return
        else:
            if not obj.id == self.id:
                raise ValidationError({NON_FIELD_ERRORS: ('BlogUser with slug "%s" already exists for blog "%s"' % (self.slug, self.blog), )})


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=50, unique=True)
    description = models.CharField(_('description'), max_length=500)
    seo_title = models.CharField(_('seo title'), max_length=70, blank=True)
    seo_desc = models.CharField(_('seo meta description'), max_length=160, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


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
    title = models.CharField(_('title'), max_length=300)
    slug = models.SlugField(_('slug'), max_length=50)
    pub_date = models.DateTimeField(_('publication date'), auto_now_add=True)
    status = models.IntegerField(_('status'), choices=POST_STATUS_CHOICES, default=0)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name=_('category'))
    content = models.TextField(_('content'))
    seo_title = models.CharField(_('seo title'), max_length=70, blank=True)
    seo_desc = models.CharField(_('seo meta description'), max_length=160, blank=True)

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'country_code': self.bloguser.blog.country_code, 'blog_slug': self.bloguser.blog.slug, 'slug': self.slug})

    def __unicode__(self):
        return u"%s - %s" % (self.bloguser, self.title)

    class Meta:
        abstract = True

    def validate_unique(self, *args, **kwargs):
        super(Post, self).validate_unique(*args, **kwargs)
        try:
            obj = self.__class__._default_manager.get(bloguser__blog__country_code=self.bloguser.blog.country_code, bloguser__blog__slug=self.bloguser.blog.slug, slug=self.slug)
        except ObjectDoesNotExist:
            return
        else:
            if not obj.id == self.id:
                raise ValidationError({NON_FIELD_ERRORS: ('Post with slug "%s" already exists for blog "%s"' % (self.slug, self.bloguser.blog), )})
