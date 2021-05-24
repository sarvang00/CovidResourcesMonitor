from guests.models import ProposedAvailability, ProposedLead
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User

from .models import Availability, Lead, LeadType, Resource, Location

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from datetime import datetime

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def teamDashboard(request):
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

    return render(request, 'teams/team-dashboard.html', context=context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def addLeads(request):
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

    return render(request, 'teams/team-add.html', context=context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def modifyLeads(request):
    if request.method == "POST":
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

        lead_to_edit = request.POST['lead_to_edit']

        resources = Resource.objects.all()
        resources_count = dict()
        for resource in resources:
            resource_id = str(resource.id)
            resources_count[resource_id] = request.POST[resource_id]

        lead_to_edit = Lead.objects.filter(id=lead_to_edit).all()[0]

        lead_to_edit.lead_name = lead_name
        lead_to_edit.contact_num = contact_num
        lead_to_edit.full_address = full_address
        lead_to_edit.gmaps_url = gmaps_url
        lead_to_edit.email = lead_email
        lead_to_edit.lead_type = lead_type
        lead_to_edit.comments = lead_comments
        lead_to_edit.last_updated = datetime.now()

        lead_to_edit.save()

        for resource_id, entry in resources_count.items():
            availability = Availability.objects.filter(lead=lead_to_edit, resource_type__id=resource_id).all()[0]
            availability.available_count = entry
            availability.save()

        messages.success(request, "Data updated!")

        return redirect('modifyleads')
    else:
        leads = Lead.objects.all()
        availabilities = Availability.objects.all()
        
        context= {
            'leads': leads,
            'availabilities': availabilities
        }

        return render(request, 'teams/team-modify.html', context=context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def verifyLeads(request):
    if request.method == "POST":
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

        proposed_lead_to_edit = request.POST['lead_to_edit']

        resources = Resource.objects.all()
        resources_count = dict()
        for resource in resources:
            resource_id = str(resource.id)
            resources_count[resource_id] = request.POST[resource_id]

        proposed_lead_to_edit = ProposedLead.objects.filter(id=proposed_lead_to_edit).all()[0]

        action_to_take = request.POST['approveordelete']
        
        if action_to_take=='approved':
            # save to db
            selected_location = Location.objects.filter(state=selectedState, region=selectedRegion).all()[0]
            lead_to_save = Lead(lead_name=lead_name, contact_num=contact_num, location=selected_location, full_address=full_address, gmaps_url=gmaps_url, email=lead_email, lead_type=lead_type, source=False, verified_by=request.user, comments=lead_comments, last_updated=datetime.now())
            lead_to_save.save()

            new_lead_made = Lead.objects.filter(lead_name=lead_name, contact_num=contact_num, location=selected_location, full_address=full_address, gmaps_url=gmaps_url, email=lead_email, lead_type=lead_type, source=False).all()[0]

            for resource_id, entry in resources_count.items():
                pr_availability = ProposedAvailability.objects.filter(lead=proposed_lead_to_edit, proposed_resource_type__id=resource_id).all()[0]
                new_resource = Resource.objects.filter(id=resource_id).all()[0]
                new_availability = Availability(lead=new_lead_made, resource_type=new_resource, available_count=entry)
                new_availability.save()
                pr_availability.delete()
            
            proposed_lead_to_edit.delete()
        else:
            for resource_id, entry in resources_count.items():
                pr_availability = ProposedAvailability.objects.filter(lead=proposed_lead_to_edit, proposed_resource_type__id=resource_id).all()[0]
                pr_availability.delete()
            proposed_lead_to_edit.delete()

        return redirect('verifyleads')
    else:
        resources = Resource.objects.all()
        proposed_leads = ProposedLead.objects.all()
        proposed_availabilities = ProposedAvailability.objects.all()

        context = {
            'pr_leads' : proposed_leads,
            'pr_availabilities' : proposed_availabilities,
            'resources': resources
        }

        return render(request, 'teams/team-verify.html', context=context)


@login_required(login_url='/login/')
def addVerifiedLead(request):
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

        if Lead.objects.filter(lead_name=lead_name, contact_num=contact_num, email=lead_email).exists():
            messages.error(request, "Data with same lead, number and email id already exists.")
            return redirect('addleads')
        else:
            # First, we add the lead
            selected_location = Location.objects.filter(state=selectedState, region=selectedRegion).all()[0]
            lead = Lead(lead_name=lead_name, contact_num=contact_num, location=selected_location, full_address=full_address, gmaps_url=gmaps_url, email=lead_email, lead_type=lead_type, source=True, verified_by = request.user, comments=lead_comments, last_updated=datetime.now())
            lead.save()

            # Now we add the data and use the added lead for reference
            lead_for_data = Lead.objects.filter(lead_name=lead_name, contact_num=contact_num, location=selected_location, full_address=full_address, gmaps_url=gmaps_url, email=lead_email, lead_type=lead_type, source=True, verified_by = request.user).all()[0]
            for res_id, count_value in resources_count.items():
                res_id = int(res_id)
                count_value = int(count_value)
                resource_type = Resource.objects.filter(id=res_id).all()[0]
                availability = Availability(lead=lead_for_data, resource_type=resource_type, available_count=count_value)
                availability.save()
            
            # Finally we acknowledge and redirect
            messages.success(request, "Lead data add request added.")
            return redirect('addleads')


@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def adminControls(request):
    resources = Resource.objects.all()
    categories = list()
    
    for resource in resources:
        categories.append(resource.category)

    categories = list(set(categories))

    context_categories = {
        'categories' : categories
    }

    return render(request, 'teams/admin-dashboard.html', context=context_categories)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def registerUser(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
                return redirect('admincontrols')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is laready in use!')
                    return redirect('admincontrols')
                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(
                        request, 'User is now registered and can log in')
                    return redirect('admincontrols')
        else:
            messages.error(request, 'Passwords donot match')
            return redirect('admincontrols')
    else:
        return redirect('admincontrols')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('dashboard')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def addCategory(request):
    if request.method == 'POST':
        category = request.POST['category']
        subcategory = request.POST['subcategory']

        if Resource.objects.filter(category=category).exists():
            messages.error(request, 'This category already exists!')
            return redirect('admincontrols')
        else:
            resource = Resource(category=category, sub_category=subcategory)
            resource.save()

            
            added_resource = Resource.objects.filter(category=category, sub_category=subcategory).all()[0]
            leads = Lead.objects.all()
            for lead in leads:
                new_availability = Availability(lead=lead, resource_type=added_resource, available_count=0)
                new_availability.save()

            messages.success(request, 'Added a new category')
            return redirect('admincontrols')
    else:
        return redirect('admincontrols')

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='/login/')
def addSubCategory(request):
    if request.method == 'POST':
        category = request.POST['category']
        subcategory = request.POST['subcategory']

        resources_exist = Resource.objects.filter(category=category).exists()
        resources = Resource.objects.filter(category=category).all()

        if resources_exist:
            for resource in resources:
                if resource.sub_category == subcategory:
                    messages.error(request, 'This sub-category already exists in this category!')
                    return redirect('admincontrols')

            resource = Resource(category=category, sub_category=subcategory)
            resource.save()

            added_resource = Resource.objects.filter(category=category, sub_category=subcategory).all()[0]
            leads = Lead.objects.all()
            for lead in leads:
                new_availability = Availability(lead=lead, resource_type=added_resource, available_count=0)
                new_availability.save()


            messages.success(request, 'Added a new sub-category') 
            return redirect('admincontrols')
        
        else:
            messages.error(request, 'The category does not exist!')
            return redirect('admincontrols')

    else:
        return redirect('admincontrols')
