from django.shortcuts import render, redirect
from django.contrib import messages, auth
from teams.models import Location, Resource
from .models import ProposedAvailability, ProposedLead
from datetime import datetime

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admincontrols')
        else:
            return redirect('teamdashboard')
    else:
        return redirect('dashboard')

def dashboard(request):
    return render(request, 'guests/guest-dashboard.html')

def contribute(request):
    if request.method == "POST":
        resources = Resource.objects.all()
        resources_count = dict()

        lead_name = request.POST['lead_name']
        contact_num = request.POST['contact_num']
        selectedState = request.POST['selectedState']
        selectedRegion = request.POST['selectedRegion']
        full_address = request.POST['full_address']
        gmaps_url = request.POST['gmaps_url']
        lead_email = request.POST['lead_email']
        lead_type = request.POST['lead_type']
        lead_comments = request.POST['lead_comments']

        for resource in resources:
            resource_id = str(resource.id)
            resources_count[resource_id] = request.POST[resource_id]

        if ProposedLead.objects.filter(lead_name=lead_name, contact_num=contact_num, email=lead_email).exists():
            messages.error(request, "Data with same lead, number and email id already exists.")
        else:
            # First, we add the lead
            selected_location = Location.objects.filter(state=selectedState, region=selectedRegion).all()[0]
            pr_lead = ProposedLead(lead_name=lead_name, contact_num=contact_num, proposed_location=selected_location, full_address=full_address, gmaps_url=gmaps_url, email=lead_email, lead_type=lead_type, source=False, comments=lead_comments, last_updated=datetime.now())
            pr_lead.save()

            # Now we add the data and use the added lead for reference
            lead_for_data = ProposedLead.objects.filter(lead_name=lead_name, contact_num=contact_num, proposed_location=selected_location, full_address=full_address, gmaps_url=gmaps_url, email=lead_email, lead_type=lead_type).all()[0]
            for res_id, count_value in resources_count.items():
                res_id = int(res_id)
                count_value = int(count_value)
                proposed_resource_type = Resource.objects.filter(id=res_id).all()[0]
                pr_availability = ProposedAvailability(lead=lead_for_data, proposed_resource_type=proposed_resource_type, available_count=count_value)
                pr_availability.save()
            
            # Finally we acknowledge and redirect
            messages.success(request, "Lead data add request recieved.")
            return redirect('contribute')
        
    else:
        # Filtering locations and states lists
        locations = Location.objects.all()
        states = list()
        
        for location in locations:
            states.append(location.state)
        
        states = list(set(states))

        # Filtering resources and category
        resources = Resource.objects.all()
        categories = list()

        for resource in resources:
            categories.append(resource.category)
        
        categories = list(set(categories))

        context= {
            'states': states,
            'locations' : locations,
            'categories': categories,
            'resources': resources
        }

        return render(request, 'guests/guest-contribute.html', context=context)
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'guests/login.html')

