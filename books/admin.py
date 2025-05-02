from django.contrib import admin

# Register your models here.

from .models import Book, Tag, BookTag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'purchase_type', 'status', 'rating')
    list_filter = ('purchase_type', 'status')
    search_fields = ('title',)

    # Inline for BookTag relationships
    inlines = []

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['tags'].queryset = Tag.objects.all()
        return form

@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    list_display = ('book', 'tag')
    search_fields = ('book__title', 'tag__name')
