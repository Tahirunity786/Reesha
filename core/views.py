from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
from core.models import ListApp, Prefdefinelist, SocialPost
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from core.models import ListApp
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers import ListSerailizer, PostSerializer, PrelistSerializer

User = get_user_model()



def Register(request):
    """
    View function for user registration.

    Handles POST request to create a new user account.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the registration page or login page based on the outcome.

    Raises:
        Exception: Any unhandled exceptions are caught and rendered in the 'oops.html' template.
    """
    try:
        if request.method == "POST":
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            re_password = request.POST.get('confirm_password')
            if first_name and last_name and  email and password and re_password:
                if password == re_password:
                    # Create a new user object
                    user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
                    user.set_password(password)
                    user.save()
                    success_message = 'Account has been created successfully, Please <b><a href="/core/public/u/logout">Login</a></b> to continue!'
                    messages.success(request, mark_safe(success_message))
                    return redirect("/core/public/u/register")
                else:
                    # Password does not match
                    messages.error(request, "Password doesn't matched!")
                    return redirect("/core/public/u/register")
            else:
                # Fill in every field
                messages.error(request, "May be you missed some fields")
                return redirect("/core/public/u/register")
        else:
            # If not a POST request, return the sign-up page
            return render(request, "core/register.html")
    except Exception as e:
        # Catch and handle any exceptions
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
                messages.error(request, "Invalid Credentials")
                return redirect("Login")
        else:
            # If email/username or password is missing, return an error message
            messages.error(request, "Have you leave a feild? Please fill out all feilds.")
            return redirect("Login")
    else:
        # If not a POST request, return the login page
        return render(request, "core/login.html")


@login_required(login_url='/core/public/u/login')
def Logout(request):
    """
    Logout function to handle user logout.

    Args:
        request: HttpRequest object representing the current request.

    Returns:
        HttpResponseRedirect: Redirects the user to the homepage after logout.

    """
    logout(request)
    return redirect('/')



@login_required(login_url='/core/public/u/login')
def create_list(request):
    """
    View function to handle the creation of a new list object.
    
    Parameters:
    - request: HttpRequest object
    
    Returns:
    - If the request method is POST and the user is authenticated, creates a new List object 
      with the provided data and redirects to the home page.
    - If the request method is not POST or the user is not authenticated, redirects to the home page.
    """
    # Check if the request method is POST
    if request.method == "POST":
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve data from POST request
            title = request.POST.get("title")
            description = request.POST.get("description")
            image_a = request.FILES.get("imagea")
            image_b = request.FILES.get("imageb")

            # Determine if images are provided
            if image_a is None and image_b is None:
                # If no images are provided, create the list without images
                ListApp.objects.create(user=request.user, title=title, description=description)
            elif image_a is not None and image_b is None:
                # If only imagea is provided, save one image
                ListApp.objects.create(user=request.user, title=title, description=description, image_a=image_a)
            elif image_a is None and image_b is not None:
                # If only imageb is provided, save one image
                ListApp.objects.create(user=request.user, title=title, description=description, image_b=image_b)
            else:
                # If both images are provided, save both images
                ListApp.objects.create(user=request.user, title=title, description=description, image_a=image_a, image_b=image_b)
            
            
            # Redirect to home page upon successful creation
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
      
        return JsonResponse(data={"error": f"An unexpected error occurred, {e}"}, status=500)

def list_details(request, id):
    
    try:
        list_data = ListApp.objects.get(id=id, user=request.user)
    except Exception as e:
        return JsonResponse(data={"Error":"Object not found"}, status=400)
    
    response = {
        "title":list_data.title,
        "description": list_data.description,
        "imagea":list_data.image_a,
        "imageb":list_data.image_b, 
        "datecreated":list_data.date_created,
        'mark_as_completed':list_data.mark_as_completed
    }
    return JsonResponse(data=response, status=200)

    

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
    """
    View function to mark a list item as completed.

    Parameters:
    - request: The HTTP request object.
    - id: The ID of the list item to mark as completed.

    Returns:
    - Redirects to the 'm-completed' URL if successful.
    - Redirects to the home page ('/') if the list item is not found.
    """
    try:
        product_fetch = ListApp.objects.get(id=id)
        if product_fetch:
            product_fetch.mark_as_completed = True
            product_fetch.save()
            return redirect("m-completed")
        else:
            messages.error(request, "List not found")
            return redirect('/')
    except Exception as e:
        messages.error(request, f"Error occurred: {e}")
        return redirect('/')

def list_unmarked(request, id):
    """
    View function to mark a list item as not completed.

    Parameters:
    - request: The HTTP request object.
    - id: The ID of the list item to mark as not completed.

    Returns:
    - Redirects to the home page ('/') if successful or if the list item is not found.
    """
    try:
        product_fetch = ListApp.objects.get(id=id)
        if product_fetch:
            product_fetch.mark_as_completed = False
            product_fetch.save()
            return redirect("/")
        else:
            messages.error(request, "List not found")
            return redirect('/')
    except Exception as e:
        messages.error(request, f"Error occurred: {e}")
        return redirect('/')



@login_required(login_url='/core/public/u/login')
def marked_as_completed(request):
    """
    View function to display lists marked as completed by the user.

    Retrieves the user's lists marked as completed and renders them in a template.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered HTML response containing completed lists or an error message.

    """
    try:
        user = request.user
        user_account = User.objects.get(email=user)
        if user_account is not None:
            prod = ListApp.objects.filter(user=user_account)
            return render(request, "core/marked_as_completed.html", {"Lists":prod})
        else:
            return render(request, "core/marked_as_completed.html", {"Error":"No list found!"})
    except Exception as e:
        return render(request, "oops.html", {"Error":e})


def search_list(request):
    """
    View function to perform a search on lists.

    Retrieves lists based on a search query and renders them in a template.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered HTML response containing search results or an empty response.

    """
    query = request.GET.get('q')
    if query:
        # Perform search using case-insensitive contains lookup on title and description fields
        search_results = ListApp.objects.filter(title__icontains=query, user=request.user) | \
                         ListApp.objects.filter(description__icontains=query, user=request.user)
                         
    else:
        search_results = None

    return render(request, 'core/search.html', {'search_results': search_results, 'query': query})


def social_data(request):
    """
    View function to display social data.

    Renders social data in a template.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered HTML response containing social data.

    """
    posts = SocialPost.objects.all().order_by("-id")
    response = {
        "socialpost":posts
    }
    return render(request, 'core/social.html', response)


@login_required(login_url='/core/public/u/login')
def account(request):
    """
    View function to handle user account operations.

    Performs operations related to the user account such as updating information.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered HTML response for the account page.

    """
    try:
        if request.method == "POST":
            # Retrieving form data
            profile_pic = request.FILES.get('profilepic', None)
            first_name = request.POST.get("firstname", None)
            last_name = request.POST.get("lastname", None)
            age = request.POST.get("age", None)
            address = request.POST.get("address", None)
            # Attempt to retrieve user object
            try:
                user = User.objects.get(email=request.user)
            except User.DoesNotExist:
                # Redirect to account page if user does not exist
                return redirect('account')

            # Update user information
            if profile_pic:
                user.profile_pic = profile_pic
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if age:
                user.age = age
            if address:
                user.address = address
           
            # Save updated user object
            user.save()
            # Redirect back to account page after successful update
            return redirect("account")
        else:
            # Render account page for GET requests
            
            return render(request, 'core/account.html')
    except Exception as e:

        return redirect("account")


class List_Detail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(request, *args, **kwargs):
        id= kwargs.get("id")
        try:
            list_data = ListApp.objects.get(id=id)
        except Exception as e:
            return Response({"Error":f"Object not found {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializers = ListSerailizer(instance=list_data)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class PreList_Detail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(request, *args, **kwargs):
        id= kwargs.get("id")
        try:
            list_data = Prefdefinelist.objects.get(id=id)
        except Exception as e:
            return Response({"Error":f"Object not found {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializers = PrelistSerializer(instance=list_data)
        return Response(serializers.data, status=status.HTTP_200_OK)


@login_required(login_url='/core/public/u/login')
def create_post(request):
   
    # Check if the request method is POST
    if request.method == "POST":
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve data from POST request
            trending = request.POST.get('trending')
            poppular = request.POST.get('popular')
            description = request.POST.get("description")
            image_a = request.FILES.get("imagea")
            image_b = request.FILES.get("imageb")
            # Determine if images are provided
            if image_a is None and image_b is None:
                # If no images are provided, create the list without images
                post = SocialPost.objects.create(user=request.user, description=description)
                if poppular == "on":
                    post.is_popular = True
                if trending == "on":
                    post.is_trending = True
                post.save()
            elif image_a is not None and image_b is None:
                # If only imagea is provided, save one image
                post=SocialPost.objects.create(user=request.user, description=description, image_a=image_a)
                if poppular == "on":
                    post.is_popular = True
                if trending == "on":
                    post.is_trending = True
                post.save()
            elif image_a is None and image_b is not None:
                # If only imageb is provided, save one image
                post=SocialPost.objects.create(user=request.user, description=description, image_b=image_b)
                if poppular == "on":
                    post.is_popular = True
                if trending == "on":
                    post.is_trending = True
                post.save()
            else:
                # If both images are provided, save both images
                post=SocialPost.objects.create(user=request.user, description=description, image_a=image_a, image_b=image_b)
                if poppular == "on":
                    post.is_popular = True
                if trending == "on":
                    post.is_trending = True
                post.save()

            # Redirect to home page upon successful creation
            return redirect("post")
        else:
            # If user is not authenticated, redirect to home page
            return redirect("post")
    else: 
        # If request method is not POST, redirect to home page
        return redirect("post")

@login_required(login_url='/core/public/u/login')
def update_postlist(request, id):
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
       
        if request.method == "POST":
            # Update the list item
            try:
                post_data = SocialPost.objects.get(id=id)
            except ObjectDoesNotExist as e:
                return JsonResponse(data={'error': f"Post not exist with ID {id}"}, status=404)
            trending = request.POST.get('trending')
            poppular = request.POST.get('popular')
            description = request.POST.get('description')
            
            # Handle file uploads
            image_a = request.FILES.get('imagea')
            image_b = request.FILES.get('imageb')
            
            if trending  :
                post_data.is_trending = True
            if poppular  :
                post_data.is_popular = True
            post_data.description = description 
            
            # Update images only if provided in the request
            if image_a:
                post_data.image_a = image_a
            if image_b:
                post_data.image_b = image_b
            
            post_data.save()
            return redirect("post")
    except Exception as e:
        # Return a generic error message
      
        return JsonResponse(data={"error": f"An unexpected error occurred, {e}"}, status=500)


def post_del(request, id):
    """
    Delete a specific Post item.

    Parameters:
    - request: HTTP request object
    - id: ID of the list item to delete

    Returns:
    - Redirect response
    """
    try:
        product_fetch = SocialPost.objects.get(id=id, user=request.user)
        if product_fetch:
            product_fetch.delete()
            return redirect("post")
        else:
            messages.error(request, "post not found")
            return redirect('post')
    except Exception as e:
        messages.error(request, f"Error occurred {e}")
        return redirect('post')


class SharePost(APIView):

    def get(self, request, slug):  # Add 'self' as the first argument

        try:
            post = SocialPost.objects.get(slug=slug)
        except SocialPost.DoesNotExist:
            return Response({"Error":"Post for this slug not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PostSerializer(instance=post)  # Renamed 'serializers' to 'serializer'

        return Response(serializer.data, status=status.HTTP_200_OK)
