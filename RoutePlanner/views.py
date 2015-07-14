from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from RoutePlanner.forms import UserForm, RouteForm
from RoutePlanner.models import UserProfile, BikeWay, BikeWayManager, LocationManager, Route

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    print "bikeway manager to be initialized"
    bikeway_manager = BikeWayManager()
    allBikeWays = list(bikeway_manager.bikeways)
    
    print "route manager to be initialized"
    location_manager = LocationManager()
    
    if (request.GET.get('update')):
        bikeway_manager.update_data()
    
    updateTime = bikeway_manager.instance.get_time()
    print updateTime
    bikeWayCoords = []
    # put all the bikeway segments into one list
    for b in allBikeWays:
        
        coordList = b[2]
         
        bikeWayCoords+=coordList # dirty fix- revisit this later
    
    context_dict = {'allBikeWays': bikeWayCoords,
                    'updateTime': updateTime}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'RoutePlanner/index.html', context_dict)

TEMPLATE_DIRS = ('<workspace>/MegaByke/',)


# register page taken and modified from http://www.tangowithdjango.com/
def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = UserProfile()
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
            'RoutePlanner/register.html',
            {'user_form': user_form, 'registered': registered} )
    
    
# login page taken and modified from http://www.tangowithdjango.com/    
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/RoutePlanner/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your MegaByke account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'RoutePlanner/login.html', {})

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/RoutePlanner/')

def about(request):
    return render(request, 'RoutePlanner/about.html', {})

def account(request):
    if request.user.is_authenticated():
        current_user = request.user
        route_list = list(Route.objects.filter(userprofile=current_user.userprofile))
    else:
        route_list = [];
        
    return render(request, 'RoutePlanner/account.html', 
                  {'route_list': route_list})

# plot route
def plot_route(request):

    # If it's a HTTP POST, we're interested in processing form data.
    print "processing plot route request"
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.

        route_form = RouteForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)

        # If the form is valid
        if route_form.is_valid():
            print "form is valid"
            # Save the route form data to the database.
            route = route_form.save()
            
            # save the current route the user profile, if logged in
            if request.user.is_authenticated():
                current_user = request.user
                current_profile = current_user.userprofile
                #TODO: add check for if the user has 20
                route.userprofile = current_profile
                
            route.save()
            

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print route_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        print "wrong request type"
        route_form = RouteForm()

    # Render the template depending on the context.
    return HttpResponseRedirect('/RoutePlanner/')
    # TODO: actually handle this properly instead of going back to the main page
    # return render(request,
            # TODO: actually handle this properly instead of going back to the main page
            # 'RoutePlanner/route.html',
            # {'route_form': route_form} )
    