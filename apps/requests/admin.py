from apps.requests.models import User, Request, Comment, Agency
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    exclude = ("path", "total_css", "total_section_content", )

admin.site.register(User)
admin.site.register(Request)
admin.site.register(Comment)
admin.site.register(Agency)
