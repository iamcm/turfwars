



<div class="col-xs-6">
	<div id="map-canvas" style="width:500px;height:500px"></div>
</div>
<div class="col-xs-6">
	<div class="row">
		%if len(vd['users']) > 0:
			<h3>Potential challengers detected!</h3>
		%end
	</div>

	%for u in vd['users']:
		<div class="row">
			<a href="/challenge/{{u._id}}" class="btn btn-default pull-right">Challenge!</a>
			{{u.email}}
		</div>
	%end
</div>


%def js():
<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=true"></script>

<script type="text/javascript">

var initialLocation;

function initialize() {
	var myOptions = {
		zoom: 6,
    	center: new google.maps.LatLng(50, -3),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);

	// Try W3C Geolocation (Preferred)
	if(navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
			map.setCenter(initialLocation);
		});
	}

	google.maps.event.addListener(map, 'click', function(obj) {
		if(obj && obj.latLng) {
			$.post('/log/location', {
				'lat':obj.latLng.lat(),
				'lng':obj.latLng.lng()
			});

			window.location.reload();
		}
	});
}

initialize();

</script>
%end

%rebase base vd=vd, js=js