from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render
import json
import requests
import math

def alias_sproc_output(sproc_output):
	output = {}
	output['price'] = sproc_output['selling_price_dollar_cnt']
	output['yearly_taxes'] = sproc_output['tax_paid_amt']
	output['restimate'] = sproc_output['zestimate_dollar_cnt']
	output['zpid'] = sproc_output['property_id']
	output['bedrooms'] = sproc_output['bedrooms']
	output['bathrooms'] = sproc_output['bathrooms']
	output['latitude'] = sproc_output['latitude'] * math.pow(10, -6)
	output['longitude'] = sproc_output['longitude'] * math.pow(10, -6)

	return output

def get_fake_data():
	downtown_properties = [{'address' : 'fake address', 'latitude' : 47.6062, 'longitude' : -122.3321, 'price' : 150000, 'yearly_taxes' : 3000, 'restimate' : 1400, 'zpid' : 48725241}]
	south_lake_properties = [{'address' : 'fake address 2', 'latitude' : 47.6222, 'longitude' : -122.3371,'price' : 200000, 'yearly_taxes' : 4000, 'restimate' : 2200, 'zpid' : 92570232}, 
	{'address' : 'fake address 3', 'latitude' : 47.6252, 'longitude' : -122.3311, 'price' : 100000, 'yearly_taxes' : 1500, 'restimate' : 900, 'zpid' : 88877172}]
	neighborhood_list = [
		{'name' : 'South Lake Union', 'id' : 'south_lake_union', 'properties' : south_lake_properties, 'neighborhood_attributes' : {}}, 
		{'name' : 'Capitol Hill', 'id' : 'capitol_hill', 'properties' : [], 'neighborhood_attributes' : {}}, 
		{'name' : 'Beacon Hill', 'id' : 'beacon_hill','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'University District', 'id' : 'university_district','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'Queen Anne', 'id' : 'queen_anne','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'Downtown', 'id' : 'downtown','properties' : downtown_properties, 'neighborhood_attributes' : {}},
		{'name' : 'West Seattle', 'id' : 'west_seattle','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'Magnolia', 'id' : 'magnolia','properties' : [], 'neighborhood_attributes' : {}}
	]

	neighborhood_dict = {}
	for neighborhood in neighborhood_list:
		neighborhood_dict[neighborhood['id']] = neighborhood

	return neighborhood_dict

def get_mortgage_rate():
	mortgageQuery = 'https://mortgageapi.develop.zillow.net/getCurrentRates?partnerId=RD-QNNRMHN'
	response = requests.get(mortgageQuery).content
	mortgage_rate = json.loads(response)['rates']['default'].get('rate')

	return mortgage_rate

def home(request, *args, **kwargs):
	neighborhood_region_ids = [250206, 250017, 250692, 252248, 250780, 250788, 272001, 271808, 251709, 250050]

	neighborhood_dict = get_fake_data()
	mortgage_rate = get_mortgage_rate()
	neighborhood_dict['mortgage_rate'] = mortgage_rate


	context = {'neighborhood_dict' : neighborhood_dict, 'neighborhood_json' : json.dumps(neighborhood_dict)}

	return render(request, "index.html", context)

