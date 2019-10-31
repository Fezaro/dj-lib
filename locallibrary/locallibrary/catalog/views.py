from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
def index(request):
    """view function for the home page site"""

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_books +1

    #Available Books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The all() is implied by default
    num_authors = Author.objects.count()
    
    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_visits' : num_visits,
    }
    
    #Render the HTML template index.html with data from the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
   
    '''context_object_name = 'my_book_list'   # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location'''

    #add model to view
    model = Book
    paginate_by = 2

    #best way to represent queryset

    def get_queryset(self):
        #gets 5 titles containing 'war in the title
        return Book.objects.all()[:5]
    
    """We can override get_context_data() in order to pass additional context variables to the template
            when doing this it is important to follow this pattern:
                1. First get the existing context from our superclass.
                2. Add your new context information.
                3. Return the new (updated) context.

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context        
    """
    
class BookDetailView(generic.DetailView):
    """detail view for the books"""
    model = Book

class AuthorListView(generic.ListView):
    """Author list """
    model = Author
    paginate_by = 2
   
class AuthorDetailView(generic.DetailView):
    """details about aauthor"""
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """class-based view listing books on loan to current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):

    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_all_borrowed_books.html"
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
