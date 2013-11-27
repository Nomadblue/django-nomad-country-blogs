from django.contrib import admin

from nomadblog.models import BlogHub, Blog, Category, BlogUser


class BlogHubAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'country_code', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    list_filter = ('country_code', )


class BlogUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'bio')
    search_fields = ('user__username', 'user__email', 'blog__title', 'blog__country_code', 'bio')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.register(BlogHub, BlogHubAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogUser, BlogUserAdmin)
