var neighborhood_dict;
		var map;
		var markers = [];

		var default_price = '$200,000';
		var default_cap_rate = '2%';
		var default_cash_flow = '$2,000';
		var default_cash_on_cash = '5%';	
		var infoWindow;

		$(document).ready(function() {
		// create global info window that pops up when a property is clicked
		infoWindow = new google.maps.InfoWindow({disableAutoPan: true});

		// parse serialized json object containing neighborhood data
		var escaped_json = '{{neighborhood_json}}';
		var cleansed_json = escaped_json.replace(new RegExp('&quot;', 'g'), '\"');

		neighborhood_dict = JSON.parse(cleansed_json);

		// initialize tooltips for filter form
		var yearly_cash_flow = 'Total income - total expenses (including mortgage payment)';
		$('#cash_flow').attr('title', yearly_cash_flow);
		$('#cash_flow').tooltip({});

		var cap_rate = 'Total income - total expenses (excluding mortgage payment) / offer price';
		$("#cap_rate").attr('title', cap_rate);
		$('#cap_rate').tooltip({});

		var cash_on_cash = 'Total income - total expenses (including mortgage payment) / total capital expenditure';
		$("#cash_on_cash").attr('title', cash_on_cash);
		$('#cash_on_cash').tooltip({});

		// disable filter handler
		$('#disable_filters').click(function(e) {
			$('#price').prop('disabled', true)
			$('#cash_flow').prop('disabled', true);
			$('#cap_rate').prop('disabled', true);
			$('#cash_on_cash').prop('disabled', true);
			
			$('#apply_filter').html('Enable Filters');
		});

		$('#apply_filter').click(function(e) {
			$('#price').prop('disabled', false)
			$('#cash_flow').prop('disabled', false);
			$('#cap_rate').prop('disabled', false);
			$('#cash_on_cash').prop('disabled', false);

			$('#apply_filter').html('Apply Filters');
			
		});

		// block page refresh on form submit and apply filter to displayed properties
		$("#filter_form").submit(function(e) {
			e.preventDefault();
			var active_pane = $('#neighborhood_panes').find(".active")[0];
			neighborhoodClickHandler($(active_pane).attr('id'));
		});

	});
	 // initialize google map centered on seattle
	 function initMap() {
	 	var seattle = {lat: 47.6062, lng: -122.3321};

	 	map = new google.maps.Map(document.getElementById('map'), {
	 		zoom: 14,
	 		center: seattle
	 	});
	 };
	 // assumes 30 year fixed mortgage with 20% down at the current prevailing rate (pulled from pogo)
	 function getMonthlyMortgage(price) {
	 	var monthly_rate = parseFloat(neighborhood_dict['mortgage_rate']) / (12.0 * 100.0);
		var monthly_mortgage = .8 * price * ((monthly_rate * Math.pow((1 + monthly_rate), 30 * 12)) / (Math.pow((1 + monthly_rate), 30 * 12) - 1));
		return monthly_mortgage;
	 };
	// check whether a given property satisifes the user's filter metrics
	function filter(property) {
		if ($('#price').val() != '' && !$('#price').prop('disabled')) {
			var max_price = parseFloat($('#price').val());
			if (max_price < property.price) {
				return false;
			}
		}

		if ($('#cap_rate').val() != '' && !$('#cap_rate').prop('disabled')) {
			var min_cap_rate = parseFloat($('#cap_rate').val()) / 100.0;
			var property_cap_rate = (property.restimate * 12 - property.yearly_taxes) / property.price;
			if (min_cap_rate > property_cap_rate) {
				return false;
			}
		}

		if ($('#cash_flow').val() != '' && !$('#cash_flow').prop('disabled')) {

			var monthly_mortgage = getMonthlyMortgage(property.price);
			var min_yearly_cash_flow = Number($('#cash_flow').val().replace(/[^0-9\.]+/g,""));
			var property_cash_flow = (property.restimate * 12) - property.yearly_taxes - (monthly_mortgage * 12);
			
			if (min_yearly_cash_flow > property_cash_flow) {
				return false;
			} 

		}

		if ($('#cash_on_cash').val() != '' && !$('#cash_on_cash').prop('disabled')) {
			var min_cash_on_cash = parseFloat($('#cash_on_cash').val()) / 100.0;
			var monthly_mortgage = getMonthlyMortgage(property.price);

			var property_cash_on_cash = (property.restimate * 12 - property.yearly_taxes - monthly_mortgage * 12) / (property.price * .2);
			if (min_cash_on_cash > property_cash_on_cash) {
				return false;
			}
		}


		return true;
	};
	// delete all markers on the map each time a new neighborhood is selected
	function deleteMarkers() {
		for (var i = 0; i < markers.length; i++) {
			var marker = markers[i];
			marker.setMap(null);
		};
		markers = [];
	};

	// add the appropriate properties to the map each time a new neighborhood is selected
	function neighborhoodClickHandler(id) {
		deleteMarkers();

		var properties = neighborhood_dict[id].properties;

		var count = 0.0;
		var total_lat = 0.0;
		var total_long = 0.0;
		for (var i = 0; i < properties.length; i++) {
			var property = properties[i];
			if (filter(property)) {
				count++;

				var latitude = parseFloat(property.latitude);
				total_lat += latitude;
				var longitude = parseFloat(property.longitude);
				total_long += longitude;

				addMarker(property);
			}
		};
		if (count > 0) {

			var avg_lat = total_lat / count;
			var avg_long = total_long / count;

			var latlng = new google.maps.LatLng(avg_lat, avg_long);

			map.setCenter(latlng);

		}
	};
	function formatToDollars(dollars) {
		return '$' + dollars.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
	}

	// add a marker to the map
	function addMarker(property) {
		var latitude = parseFloat(property.latitude)
		var longitude = parseFloat(property.longitude)

		var latlng = new google.maps.LatLng(latitude, longitude);

		var marker = new google.maps.Marker({
			position: latlng,
			title: name,
			map: map
		});

		marker.addListener('click', function() {
			var monthly_mortgage = getMonthlyMortgage(property.price);

			content_string = '<div>Address: ' + property.address + '<br>';
			content_string += 'Price: ' + formatToDollars(property.price) + '<br>';
			content_string += 'Rent: ' + formatToDollars(property.restimate) + '<br>';

			var cash_flow = parseInt(property.restimate * 12) - parseInt(property.yearly_taxes) - parseInt(monthly_mortgage * 12);
			content_string += 'Yearly Cash Flow: ' + formatToDollars(cash_flow);
			content_string += '<br><a href="http://www.zillow.com/homes/' + property.zpid + '_zpid/">Zillow Home Detail Page</a>';
			infoWindow.close();

			infoWindow.setContent(content_string);

			infoWindow.open(map, marker);
		});

		markers.push(marker);
	}