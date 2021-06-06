from django.contrib import admin
from .models import Category, Tag, Post, ContentImage
# pip install django-summernote
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1

class PostAdmin(SummernoteModelAdmin):
    summeernote_fields = ('content',)
"""     inlines = [
        ContentImageInline,
    ] """

""" class PostAdmin(admin.ModelAdmin):
    
    inlines = [
        ContentImageInline,
    ]  """

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
# admin.site.register(Blog, BlogAdmin)

