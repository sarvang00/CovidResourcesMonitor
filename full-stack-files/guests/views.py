from django.shortcuts import render, redirect
from django.contrib import messages, auth
from teams.models import Location, Resource, LeadType, Lead, Availability
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
    if request.method == "POST":
        # Filtering states
        locations = Location.objects.all()

        states = list()
    
        for location in locations:
            states.append(location.state)
        
        states = list(set(states))

        location_ids = list()

        # Getting and making sense of POST requests
        state = request.POST['selectedState']

        try:
            region = request.POST['selectedRegion']
        except:
            region = "all"
        
        category = request.POST['selectCategory']

        selected_lead_type = request.POST['selectLeadType']
        lead_type = ""

        if selected_lead_type == "all":
            # it is all
            lead_type = "all"
        else:
            # need to filter
            lead_type = LeadType.objects.filter(type=selected_lead_type).all()[0].id

        print("State: ", state, " region: ", region, " catrgory: ", category, " lead type: ", lead_type)

        # Getting the right location
        if state=="all":
            locations = Location.objects.all()
        else:
            locations = Location.objects.filter(state=state).filter(region=region).all()
            
            for selected_loc in locations:
                location_ids.append(selected_loc.id)
        
               
        # Filtering categories and resources
        resources = Resource.objects.all()

        categories = list()

        for resource in resources:
            categories.append(resource.category)
        
        categories = list(set(categories))

        resources = Resource.objects.filter(category=category).all()

        # Making a list of resources ids
        resources_ids = list()
        for selectedResource in resources:
            resources_ids.append(selectedResource.id)

        # Making a list of sub-categories
        sub_cats = list()

        for resource in resources:
            sub_cats.append(resource.sub_category)
        
        sub_cats = list(set(sub_cats))

        # Lead types
        lead_types = LeadType.objects.all()

        # Filtering leads and availabilities
        if state=="all":
            # for all locations
            if lead_type=="all":
                # only need to filter availabilities
                leads = Lead.objects.all()
            else:
                # check for particular lead type
                leads = Lead.objects.filter(lead_type__id=lead_type).all()
        else:
            # for a particular location
            if lead_type=="all":
                # only need to filter availabilities
                leads = Lead.objects.filter(location__id__in=location_ids).all()
            else:
                # check for particular lead type
                leads = Lead.objects.filter(location__id__in=location_ids).filter(lead_type__id=lead_type).all()
        
        # Getting lead ids
        lead_ids = list()
        for selectedLead in leads:
            lead_ids.append(selectedLead.id)

        # Filtering availabilities via leads and resources
        availabilties = Availability.objects.filter(lead__id__in=lead_ids).filter(resource_type__id__in=resources_ids).all()

        context= {
            'locations' : locations,
            'resources': resources,
            'sub_categories': sub_cats,
            'leads': leads,
            'availabilies': availabilties,
            'states': states,
            'categories': categories,
            'lead_types': lead_types
        }

    else:
        # Filtering all locations
        locations = Location.objects.all()
        
        # Filtering resources and category
        resources = Resource.objects.all()
        
        categories = list()

        for resource in resources:
            categories.append(resource.category)
        
        categories = list(set(categories))

        resources = Resource.objects.filter(category=categories[0]).all()

        sub_cats = list()

        for resource in resources:
            sub_cats.append(resource.sub_category)
        
        sub_cats = list(set(sub_cats))

        # Filtering states
        states = list()
    
        for location in locations:
            states.append(location.state)
        
        states = list(set(states))

        # Filtering lead ids
        location_ids = list()
        for location in locations:
            location_ids.append(location.id)

        leads = Lead.objects.filter(location__id__in=location_ids)
        lead_ids = list()
        for lead in leads:
            lead_ids.append(lead.id)

        # Filtering resource ids
        resource_ids = list()
        for resource in resources:
            resource_ids.append(resource.id)

        # Availabilities
        availabilties = Availability.objects.filter(lead__id__in=lead_ids).filter(resource_type__id__in=resource_ids).all()

        # Lead types
        lead_types = LeadType.objects.all()
        
        context= {
            'locations' : locations,
            'resources': resources,
            'sub_categories': sub_cats,
            'leads': leads,
            'availabilies': availabilties,
            'states': states,
            'categories': categories,
            'lead_types': lead_types
        }

    return render(request, 'guests/guest-dashboard.html', context=context)

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

        lead_type = LeadType.objects.filter(type=lead_type).all()[0]

        for resource in resources:
            resource_id = str(resource.id)
            resources_count[resource_id] = request.POST[resource_id]

        if ProposedLead.objects.filter(lead_name=lead_name, contact_num=contact_num, email=lead_email).exists():
            messages.error(request, "Data with same lead, number and email id already exists.")
            return redirect('contribute')
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

