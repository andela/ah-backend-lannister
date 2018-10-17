from django.contrib import admin

from .models import Comment,CommentHistory


# Register your models here.
class CommentAdmin(admin.ModelAdmin):

    fields = ('author', 'body', 'parent', 'slug')

    list_display = ('body', 'author', 'created_at',
                    'updated_at', 'parent', 'id', 'slug')


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentHistory)