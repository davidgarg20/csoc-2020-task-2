from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
        'rating': '-1',
    }
    template_name = 'store/book_detail.html'
    context['book'] = Book.objects.get(id=bid)
    context['num_available']=BookCopy.objects.filter(book_id=bid).filter(status=False).count()
    if request.user.is_authenticated :
        userid=request.user.id
        if Rating.objects.filter(user_id=userid).filter(book_id=bid).count() == 1:
            context['rating'] = Rating.objects.filter(user_id=userid).filter(book_id=bid).first().rating
    # START YOUR CODE HERE
    print(context['rating'])
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    title=get_data.get('title')
    author=get_data.get('author')
    genre=get_data.get('genre')
    if title == "" :
        title=None
    if author == "" :
        author=None
    if genre == "" :
        genre=None

    filter_data = {'title__icontains': title, 'author__icontains': author, 'genre__icontains': genre }
    book=Book.objects.all()
    for key , value in filter_data.items():
        if value is not None :
            book = book.filter(**{key: value})
    context['books']=book
    # START YOUR CODE HERE
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    userid = request.user.id
    context['books']=BookCopy.objects.filter(status=True).filter(borrower_id=userid)
    # START YOUR CODE HERE
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = None # get the book id from post data
    data=request.POST
    book_id=data.get('bid')
    count=BookCopy.objects.filter(book_id=book_id).filter(status=False).count()
    if count > 0:
        book = BookCopy.objects.filter(book_id=book_id).filter(status=False).first()
        book.status = True
        userid = request.user.id
        book.borrow_date = datetime.datetime.now().strftime('%Y-%m-%d')
        book.borrower_id = userid
        book.save()
        response_data['message']="success"
    else:
        response_data['message']="failure"
    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    response_data = {
        'message': "failure"
    }
    data = request.POST
    copybook_id = data.get('bid')
    if copybook_id is not None:
        copybook = BookCopy.objects.get(id=copybook_id)
        copybook.borrow_date = None
        copybook.borrower_id = None
        copybook.status = False
        copybook.save()
        response_data['message']="success"
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    response_data = {
        'message': "failure"
    }
    prating = '-1'
    userid=request.user.id
    data = request.POST
    rating =data.get('rating')
    bookid = data.get('bid')
    print(rating)
    if Rating.objects.filter(user_id=userid).filter(book_id=bookid).count() == 1:
        prating = Rating.objects.filter(user_id=userid).filter(book_id=bookid).first().rating
        print('rating')
    if prating == '-1':
        rate = Rating.objects.create(book_id=bookid,user_id=userid,rating=rating)
        response_data['message'] = "success"
    else :
        rate=Rating.objects.filter(user_id=userid).filter(book_id=bookid).first()
        rate.rating = rating
        rate.save()
        response_data['message'] = "success"
    book=Book.objects.get(id=bookid)
    sum=0
    l=Rating.objects.filter(book_id=bookid).count()
    for i in range(l):
        rate=Rating.objects.filter(book_id=bookid)[i]
        sum = sum + int(rate.rating)
    arate=float(sum)/float(l)
    book.rating = round(arate,2)
    book.save()

    return JsonResponse(response_data)

