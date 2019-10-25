from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

#create bookinline
class BookInline(admin.TabularInline):
    model = Book
    extra = 0
#Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

#adding associated records by declaring inlines
class BookInstanceInline(admin.TabularInline):
    model = BookInstance 
    extra = 0
#use decorator to register
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
#register admin class for Bookinstance
@admin.register(BookInstance)

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'id', 'status', 'due_back')
    fieldsets = ((None, {
                    'fields': ('book', 'imprint', 'id')
                }),
                ('Availability', {
                    'fields': ('status', 'due_back')})
                )


#Register the admin class of the associated model
admin.site.register(Author, AuthorAdmin)
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)
