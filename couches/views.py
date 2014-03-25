from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from forms import NewCouchForm, RequestCouchForm, SearchCouchForm, DecideCouchRequestForm
from models import Couch, CouchRequest

@login_required
def new_couch(request):
    if request.method == 'POST':
        form = NewCouchForm(request.POST, host=request.user)
        if form.is_valid():
            couch = form.save()
            return redirect('couches:couch_detail', couch.id)
    else:
        form = NewCouchForm()
    
    return render(request, 'couches/new_couch.html', {
        'form': form,
    })

@login_required
def request_couch(request, couch_id):
    couch = get_object_or_404(Couch, pk=couch_id)
    if couch.host == request.user:
        raise Exception("You cannot request your own couch")  # CHANGE this
    
    if request.method == 'POST':
        form = RequestCouchForm(request.POST, requester=request.user)
        if form.is_valid():
            couch_request = form.save(commit=False)
            couch_request.couch = couch
            couch_request.requester = request.user
            couch_request.save()
            return redirect('couches:couch_detail', couch_request.couch.id)
    else:
        # make sending lots of requests easy by filling in the data from the last
        requests_by_user = CouchRequest.objects.filter(requester=request.user)
        initial = {}
        if requests_by_user:
            last_request = requests_by_user.reverse()[0]
            initial = {
                'message': last_request.message,
                'earliest_arrival': last_request.earliest_arrival,
                'latest_arrival': last_request.latest_arrival,
                'earliest_departure': last_request.earliest_departure,
                'latest_departure': last_request.latest_departure,
            }
        form = RequestCouchForm(initial=initial)
        
    return render(request, 'couches/request_couch.html', {
        'form': form, 
        'couch': couch,
    })


class CouchDetailView(DetailView):
    model = Couch
    template_name = 'couches/couch_detail.html'
    
def search_couch(request):
    if request.GET:
        form = SearchCouchForm(request.GET)
        if form.is_valid():
            results = form.get_results()
            return render(request, 'couches/search_results.html', {
                'form': form, 
                'results': results,
            })
    else:
        form = SearchCouchForm()
    return render(request, 'couches/search_couch.html', {
        'form': form,
    })

# ------------ THIS IS ESSENTIALLY GARBAGE ------------
def search_couch_map(request):
    if request.GET:
        form = SearchCouchForm(request.GET)
        if form.is_valid():
            results = form.get_results()
            from gmapi import maps
            from gmapi.forms.widgets import GoogleMap
            from django import forms
            class MapForm(forms.Form):
                map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))
            
            if form.cleaned_data.get('near_to'):
                coords = [form.cleaned_data.get('near_to')[i] for i in (0,1)]
                ctr = maps.LatLng(coords[0], coords[1])
                borders = (0.0,0,0,0,0,0,1,2,4,8,16,30,50,100,200,400,800,1600)
                zoom=20
                for b in borders:
                    if form.cleaned_data.get('max_distance')>=b:
                        zoom -=1
                
                #zoom = 1/form.cleaned_data.get('max_distance')**0.2
            else:
                ctr = maps.LatLng(45,5)
                zoom=3
                
            gmap = maps.Map(opts = {
                'center': ctr,
                'mapTypeId': maps.MapTypeId.ROADMAP,
                'zoom': zoom,
                'mapTypeControlOptions': {
                    'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })
            
            markers = []
            for r in results:
                if r.coordinates:
                    markers.append(maps.Marker(opts={'map':gmap, 'position':maps.LatLng(r.latitude,r.longitude),'url':r.get_absolute_url()}))
                    #markers[-1].
                    maps.event.addListener(markers[-1], 'mouseover', 'myobj.markerOver')
                    maps.event.addListener(markers[-1], 'mouseout', 'myobj.markerOut')
                    maps.event.addListener(markers[-1], 'click', 'myobj.markerClick')
                    info = maps.InfoWindow({
                        'content': str('Couch at {0}, hosted by <b>{1}</b>').format(r.float_coordinates,r.host.username),
                        'disableAutoPan': True
                    })
                    info.open(gmap, markers[-1])
            
            return render(request, 'couches/search_results_map.html', {
                'form': form, 
                'results': results,
                'mform': MapForm(initial={'map':gmap})
            })
    else:
        form = SearchCouchForm()
    return render(request, 'couches/search_couch.html', {
        'form': form,
    })
# ----------------- END OF GARBAGE (I hope so) ------------

@login_required
def request_inbox(request):
    couch_requests = CouchRequest.objects.filter(couch__host=request.user).order_by('-id')
    return render(request, 'couches/request_inbox.html', {
        'couch_requests':couch_requests,
    })

@login_required
def request_outbox(request):
    couch_requests = CouchRequest.objects.filter(requester=request.user).order_by('-id')
    return render(request, 'couches/request_outbox.html', {
        'couch_requests':couch_requests,
    })

@login_required
def accept_request(request, couch_request_id):
    couch_request = get_object_or_404(CouchRequest, pk=couch_request_id, couch__host=request.user)
    if couch_request.decision:
        return redirect('couches:request_inbox')
    
    if request.method == 'POST':
        form = DecideCouchRequestForm(request.POST, instance=couch_request, decision=1)
        if form.is_valid():
            form.save()
            return redirect('couches:request_inbox')
    else: 
        form = DecideCouchRequestForm()
    
    return render(request, 'couches/accept_request.html', {
        'couch_request':couch_request,
        'form': form
    })

@login_required
def decline_request(request, couch_request_id):
    couch_request = get_object_or_404(CouchRequest, pk=couch_request_id, couch__host=request.user)
    if couch_request.decision:
        return redirect('couches:request_inbox')
    
    if request.method == 'POST':
        form = DecideCouchRequestForm(request.POST, instance=couch_request, decision=-1)
        if form.is_valid():
            form.save()
            return redirect('couches:request_inbox')
    else: 
        form = DecideCouchRequestForm()
    
    return render(request, 'couches/decline_request.html', {
        'couch_request':couch_request,
        'form': form
    })

@login_required
def set_status(request, couch_id, action='deactivate'):
    couch = get_object_or_404(Couch, pk=couch_id, host=request.user)
    if action == 'activate': 
        couch.activate()
    else:
        couch.deactivate()
    return redirect('couches:couch_detail', couch_id)