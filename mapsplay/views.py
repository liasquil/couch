from django import forms
from django.shortcuts import render, render_to_response
from gmapi import maps
from gmapi.forms.widgets import GoogleMap


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))


def index(request):
    gmap = maps.Map(opts = {
        'center': maps.LatLng(28, 0),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 2,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    #k = maps.Marker({'label':'asdf'})
    #k.setPosition(maps.LatLng(38,-97))
    #k.setMap(gmap)
    
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(28, -97),
    })
    maps.event.addListener(marker, 'click', 'myobj.markerClick')
    maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
    info = maps.InfoWindow({
        'content': 'Hello!',
        'disableAutoPan': True
    })
    info.open(gmap, marker)
    
    marker2 = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(27, -97),
    })
    maps.event.addListener(marker, 'click', 'myobj.markerClick')
    maps.event.addListener(marker2, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker2, 'mouseout', 'myobj.markerOut')
    info2 = maps.InfoWindow({
        'content': 'Hello!',
        'disableAutoPan': True
    })
    info2.open(gmap, marker2)
    
    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('mapsplay/index.html', context)