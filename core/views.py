from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse


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
                    # Redirect to the app page
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
                return redirect("App")
            else:
                # If authentication fails, return an error message
                return HttpResponse("Invalid email/username or password. Please try again.")
        else:
            # If email/username or password is missing, return an error message
            return HttpResponse("Please provide both email/username and password.")
    else:
        # If not a POST request, return the login page
        return render(request, "core/login.html")

def main(request):
    return render(request, "core/app.html")