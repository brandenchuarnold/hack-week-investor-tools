from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

def home(request, *args, **kwargs):

    cap_hill_properties = [{'address' : 'fake address', 'latitude' : 47.6062, 'longitude' : -122.3321}]
    south_lake_properties = [{'address' : 'fake address 2', 'latitude' : 47.6092, 'longitude' : -122.3371}, {'address' : 'fake address 3', 'latitude' : 47.6052, 'longitude' : -122.3311}]
    neighborhood_list = [
        {'name' : 'Capitol Hill', 'id' : 'capitol_hill', 'properties' : cap_hill_properties, 'neighborhood_attributes' : {}}, 
        {'name' : 'South Lake Union', 'id' : 'south_lake_union', 'properties' : south_lake_properties, 'neighborhood_attributes' : {}}, 
        {'name' : 'Beacon Hill', 'id' : 'beacon_hill','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'University District', 'id' : 'university_district','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'Queen Anne', 'id' : 'queen_anne','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'Pioneer Square', 'id' : 'pioneer_square','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'West Seattle', 'id' : 'west_seattle','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'Magnolia', 'id' : 'magnolia','properties' : [], 'neighborhood_attributes' : {}}
    ]

    neighborhood_dict = {}
    for neighborhood in neighborhood_list:
        neighborhood_dict[neighborhood['id']] = neighborhood

    context = {'neighborhood_dict' : neighborhood_dict, 'neighborhood_json' : json.dumps(neighborhood_dict)}

    return render(request, "index.html", context)
