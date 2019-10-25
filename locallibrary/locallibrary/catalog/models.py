import uuid
from django.db import models
from django.urls import reverse

# Create your models here.

class Genre(models.Model):
    """model representing a book genre"""
    name = models.CharField(max_length=200, help_text='Enter book genre')


    def __str__(self):
        """string representation of model object"""
        return self.name
        
class Book(models.Model):
    """Model representing a book(not a specific copy  of a book)"""
    title = models.CharField(max_length=200)

    #foreign key used because book can only have one author, but authors can have many books
    #Author as a string rather than object because it hasn't been declared yet in the file

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN',max_length=13, help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN  number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField('Genre', help_text='select a genre for this book.')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """string for representing the model object"""
        return self.title

    def get_absolute_url(self):
        """returns the url to accesss a detail record for this book"""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Create a stringfor genre to be used in Admin """
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """model representing a specific copy of a book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS= (
        ('r', 'Reserved'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('m','Maintenance'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='book availability' )


    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """string for representing model object"""
        return f'{self.id}, ({self.book.title})'

class Author(models.Model):
    """model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """returns url to a particular author instance"""
        return reverse('author-detail', args=[str(self.id)])
        
    def __str__(self):
        """string representation the model"""
        return f'{self.last_name},{self.first_name}'

class Language(models.Model):
    """model  representing a language"""
    name = models.CharField(max_length=100, help_text="Enter the book's natural language")

    def __str__(self):
        """string representing the language model"""
        return self.name

