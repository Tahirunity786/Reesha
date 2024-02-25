from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
from core.models import ListApp
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers import ListSerailizer
User = get_user_model()
# Create your views here.

def Register(request):
    try:
        if request.method == "POST":
            full_name = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            re_password = request.POST.get('confirm_password')

            if full_name and email and password and re_password:
                if password == re_password:
                    # Create a new user object
                    user = User.objects.create(email=email, full_name=full_name)
                    user.set_password(password)
                    user.save()
                    # Redirect to the / page
                    return redirect("Login")
                else:
                    # Password does not match
                    return redirect("Register")
            else:
                # Fill in every field
                return redirect("Register")
        else:
            # If not a POST request, return the sign-up page
            return render(request, "core/register.html")
    except Exception as e:
        # Catch and handle any exceptions
        print(e)
        return render(request, "core/oops.html", {"Error": e})
    

def Login(request):
    """
    View function to handle user login.

    Args:
        request: HttpRequest object representing the request made to the server.

    Returns:
        HttpResponse: Response to the request.
    """
    if request.method == "POST":
        # Extract data from POST request
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email/username and password are provided
        if email and password:
            # Authenticate user
            user = authenticate(request, email=email, password=password)

            # Check if authentication using username fails, then try with email
            if user is None:
                # Try to find user by email
                try:
                    user = User.objects.get(email=email)
                    user = authenticate(request, email=user.email, password=user.password)
                except User.DoesNotExist:
                    return HttpResponse("User not found")

            if user is not None:
                # If authentication successful, log in the user
                login(request, user)
                # Redirect to a success page or any desired page
                return redirect("/")
            else:
                # If authentication fails, return an error message
                return HttpResponse("Invalid email/username or password. Please try again.")
        else:
            # If email/username or password is missing, return an error message
            return HttpResponse("Please provide both email/username and password.")
    else:
        # If not a POST request, return the login page
        return render(request, "core/login.html")



@login_required(login_url='/core/public/u/login')
def Logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/core/public/u/login')
def create_list(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve data from POST request
            title = request.POST.get("title")
            description = request.POST.get("description")
            image_a = request.FILES.get("imagea")
            image_b = request.FILES.get("imageb")

            # Check if all required fields are present
            if title is not None and description is not None and image_a is not None and image_b is not None:
                # Create and save a new List/ object
                ListApp.objects.create(user=request.user, title=title, description=description, image_a=image_a, image_b=image_b)
                # Redirect to home page upon successful creation
                return redirect("/")
            else:
                # If any required field is missing, redirect to home page
                return redirect("/")
        else:
            # If user is not authenticated, redirect to home page
            return redirect("/")
    else: 
        # If request method is not POST, redirect to home page
        return redirect("/")


@login_required(login_url='/core/public/u/login')
def update_list(request, id):
    """
    Retrieve or update a list item.

    Parameters:
    - request: HTTP request object
    - id: ID of the list item to retrieve or update

    Returns:
    - JsonResponse containing serialized list item data or error message
    - Redirect response after updating the list item
    """
    try:
        if request.method == "GET":
            # Retrieve the list item
            try:
                post_data = ListApp.objects.get(id=id)
            except ObjectDoesNotExist as e:
                return JsonResponse(data={'error': f"List not exist with ID {id}"}, status=404)
            
            # Serialize the list item data
            response = {
                "id": post_data.id,
                "title": post_data.title,
                "description": post_data.description,
            }

            return JsonResponse(data=response, status=200)
        elif request.method == "POST":
            # Update the list item
            try:
                post_data = ListApp.objects.get(id=id)
            except ObjectDoesNotExist as e:
                return JsonResponse(data={'error': f"List not exist with ID {id}"}, status=404)
            title = request.POST.get('title')
            description = request.POST.get('description')
            
            # Handle file uploads
            image_a = request.FILES.get('imagea')
            image_b = request.FILES.get('imageb')
            
            post_data.title = title
            post_data.description = description 
            
            # Update images only if provided in the request
            if image_a:
                post_data.image_a = image_a
            if image_b:
                post_data.image_b = image_b
            
            post_data.save()
            return redirect("/")
    except Exception as e:
        # Return a generic error message
      
        return JsonResponse(data={"error": "An unexpected error occurred"}, status=500)

def list_del(request, id):
    """
    Delete a specific list item.

    Parameters:
    - request: HTTP request object
    - id: ID of the list item to delete

    Returns:
    - Redirect response
    """
    try:
        product_fetch = ListApp.objects.get(id=id)
        if product_fetch:
            product_fetch.delete()
            return redirect("/")
        else:
            messages.error(request, "list not found")
            return redirect('/')
    except Exception as e:
        messages.error(request, f"Error occurred {e}")
        return redirect('/')

def list_marked(request, id):
    try:
        product_fetch = ListApp.objects.get(id=id)
        if product_fetch:
            product_fetch.mark_as_completed = True
            product_fetch.save()
            return redirect("m-completed")
        else:
            messages.error(request, "list not found")
            return redirect('/')
    except Exception as e:
        messages.error(request, f"Error occurred {e}")
        return redirect('/')
    
def list_unmarked(request, id):
    try:
        product_fetch = ListApp.objects.get(id=id)
        if product_fetch:
            product_fetch.mark_as_completed = False
            product_fetch.save()
            return redirect("/")
        else:
            messages.error(request, "list not found")
            return redirect('/')
    except Exception as e:
        messages.error(request, f"Error occurred {e}")
        return redirect('/')

@login_required(login_url='/core/public/u/login')
def marked_as_completed(request):
    try:
        user = request.user
        user_account = User.objects.get(email=user)
        if user_account is not None:
            prod = ListApp.objects.filter(user=user_account)
            return render(request, "core/marked_as_completed.html", {"Lists":prod})
        else:
            render(request, "core/marked_as_completed.html", {"Error":"Not list found!"})
    except Exception as e:
        return render(request, "oops.html", {"Error":e})


def search_list(request):
    query = request.GET.get('q')
    if query:
        # Perform search using case-insensitive contains lookup on title and description fields
        search_results = ListApp.objects.filter(title__icontains=query) | \
                         ListApp.objects.filter(description__icontains=query)
    else:
        search_results = None

    return render(request, 'core/search.html', {'search_results': search_results, 'query': query})

def social_data(request):

    return render(request, 'core/social.html')

def account(request):

    return render(request, 'core/account.html')