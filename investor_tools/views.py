from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
import requests

def home(request, *args, **kwargs):
    '''
    Beacon Hill - 250050
    Capitol Hill - 250206
    Downtown - 271849
    Magnolia - 271990
    South Lake Union - 271987
    University District - 272001
    Waterfront - 344018
    Pioneer Square - 271963
    '''
    neighborhood_region_ids = [250050, 250206, 271849, 271990, 271987, 272001, 344018, 271963]

    downtown_properties = [{'address' : 'fake address', 'latitude' : 47.6062, 'longitude' : -122.3321, 'price' : 150000, 'yearly_taxes' : 3000, 'restimate' : 3000, 'zpid' : 48725241}]
    south_lake_properties = [{'address' : 'fake address 2', 'latitude' : 47.6222, 'longitude' : -122.3371,'price' : 200000, 'yearly_taxes' : 4000, 'restimate' : 2500, 'zpid' : 92570232}, 
    {'address' : 'fake address 3', 'latitude' : 47.6252, 'longitude' : -122.3311, 'price' : 100000, 'yearly_taxes' : 1500, 'restimate' : 900, 'zpid' : 88877172}]
    neighborhood_list = [
        {'name' : 'Capitol Hill', 'id' : 'capitol_hill', 'properties' : [], 'neighborhood_attributes' : {}}, 
        {'name' : 'South Lake Union', 'id' : 'south_lake_union', 'properties' : south_lake_properties, 'neighborhood_attributes' : {}}, 
        {'name' : 'Beacon Hill', 'id' : 'beacon_hill','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'University District', 'id' : 'university_district','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'Queen Anne', 'id' : 'queen_anne','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'Downtown', 'id' : 'downtown','properties' : downtown_properties, 'neighborhood_attributes' : {}},
        {'name' : 'West Seattle', 'id' : 'west_seattle','properties' : [], 'neighborhood_attributes' : {}},
        {'name' : 'Magnolia', 'id' : 'magnolia','properties' : [], 'neighborhood_attributes' : {}}
    ]

    mortgageQuery = 'https://mortgageapi.develop.zillow.net/getCurrentRates?partnerId=RD-QNNRMHN'
    response = requests.get(mortgageQuery).content
    mortgage_rate = json.loads(response)['rates']['default'].get('rate')

    neighborhood_dict = {}
    for neighborhood in neighborhood_list:
        neighborhood_dict[neighborhood['id']] = neighborhood
        neighborhood_dict['mortgage_rate'] = mortgage_rate

    context = {'neighborhood_dict' : neighborhood_dict, 'neighborhood_json' : json.dumps(neighborhood_dict)}

    return render(request, "index.html", context)