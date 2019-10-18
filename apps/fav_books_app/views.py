from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
# import pymsgbox
# Create your views here.
def index(request):

    return render(request, 'fav_books_app/index.html')


def register(request):
    print('POST DATA:', request.POST)

    #VALIDATION FOR REGISTRATION FORM
    errors = User.objects.basic_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    else:


    #HASHING PASSWORD
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash)

        #if email does not exist alrady then okay if it exists throw ERROR
        if request.POST['email'] not in User.objects.filter(email=request.POST['email']):
        #CREATING new user WITH pw_hash!!
            new_user = User.objects.create(first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'],
                                        password=pw_hash)

            print("USER CREATED --------",)
            #alert to show user creation success
            # pymsgbox.alert(text='User Created', title='Success!', button='Lit')

            # Setting user EMAIL iN SESSION
            print('-------EMAIL:', new_user.email)
            request.session['email'] = new_user.email
            # request.session['id'] = new_user.id

            return redirect('/books')

        else:
            messages.error(request, 'Email already in use')
            # pymsgbox.alert(text='Email already in use', title='Fail!', button='Ok')



def books(request):
    print("HOME PAGE")
    if 'email' not in request.session:
        messages.error(request, 'Please log in')
        
        return redirect('/')
    
    else: 
        #matching User with the email provided in SESSION and passing the user info in CONTEXT
        user = User.objects.get(email=request.session['email'])

        allUsers = User.objects.all()
        likedBooks = user.liked_books.filter(users_who_liked=user.id)

        #passing db query data in context to front end
        context = {
            'user': user,
            'alUsers': allUsers,
            'allBooks': Book.objects.all(),
            'likedBooks': user.liked_books.filter(users_who_liked=user.id)
        }
        #MANY TO MANY ASSOCIATION FOR LIKED BOOKS AND USERS WHO LIKED --- matching the filtered query set with the complete OBJECT not finding the specific title
        # print('LIKEDBOOKSS-------',user.liked_books.filter(users_who_liked=user.id))
        # print(likedBooks.filter(users_who_liked=user.id).values())
        return render(request, 'fav_books_app/books.html', context)


def login(request):
    #VALIDATION FOR LOGIN FORM
    errors = User.objects.login_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    else:

        #matching user info with queried user list to find USER AND seT SESSION
        matched_user_list = User.objects.filter(email=request.POST['email'])
        # login_pass_hash = bcrypt.hashpw(password_login.encode(), bcrypt.gensalt())

        if len(matched_user_list) > 0 and matched_user_list[0].email == request.POST['email']:
            request.session['email'] = matched_user_list[0].email

            return redirect('/books')

        else:
            # pymsgbox.alert(text='User Not Found', title='Fail!', button='Ok')
            messages.error(request, "No user found!")

            return redirect('/')

    
def add_book(request):
    print('ADDED BOOK DATA', request.POST)

    errors = Book.objects.basic_validator(request.POST)
    print(errors)

    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/books')

    else:
        this_user = User.objects.get(email=request.session['email'])
        print(this_user.first_name)

        #crating book!! with many to many and one to many relationship
        new_book = Book.objects.create(title=request.POST['title'],
                                        desc=request.POST['desc'],
                                        uploaded_by=this_user,
                                        )

        new_book.users_who_liked.add(this_user)


        #BOOK Created 
        print('BOOK CREATED---------:', new_book)

        context = {
            'allBooks': Book.objects.all(),
            'user': this_user,
            'newBook': new_book,
        }
        
        print(this_user.liked_books.values())

        return redirect('/books', context)

def book_session(request, id):
    #filtering by ID to fin the users who liked this specific book AND if USER in SESSION then they have the option of 
    # UPDATING the info, DELETING BOOK or and un-favoriting 
    book = Book.objects.get(id=id)
    liked_by = book.users_who_liked.all()

    user = User.objects.get(email=request.session['email'])

    print(book.uploaded_by.id)
    print(user.id)
    #context and queries needed to display LOGGED IN user updated fields inputs and un-fav
    context = {
        'user': user,
        'book': book,
        'allBooks': Book.objects.all(),
        'liked_by': liked_by,

    }


    return render(request, 'fav_books_app/book_session.html', context)




def update(request, id):
    print('POST DATA FOR UPDATE', request.POST )
    book_to_update = Book.objects.get(id=id)

    book_to_update.title = request.POST['title']
    book_to_update.desc = request.POST['desc']
    book_to_update.save()

    return redirect('/books')



def delete(request, id):
    
    book = Book.objects.get(id=id)

    book.delete()

    
    return redirect('/books')


def logout(request):
    request.session.clear()

    return redirect('/')



def add_book_to_fav(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(email=request.session['email'])
    
    #addtoFAVS
    book.users_who_liked.add(user)

    return redirect('/books')


def unfavorite(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(email=request.session['email'])

    user.liked_books.remove(book)


    return redirect('/books')