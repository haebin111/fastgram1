from django.contrib import admin

from contents.models import Content, Image, FollowRelation


class ImageInline(admin.TabularInline):
    model = Image

# 위 이미지인라인의 상위개념


class ContentAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    #유저이름, 시간
    list_display = ('user', 'created_at',)


admin.site.register(Content, ContentAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class FollowRelationAdmin(admin.ModelAdmin):
    pass


admin.site.register(FollowRelation, FollowRelationAdmin)
