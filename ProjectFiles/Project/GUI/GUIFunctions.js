/*********************************************************
	Developer: Leon Tran
	Date: 04/09/17
	Contact: leontran95@gmail.com
	
	Version: 8
	Updates: Converting back to Google Maps API, because 
	of performance issues with MapBox and the PI
		-East & West Command implemented
		-Adding Help Modal
		-Updates Map when recieving new GUI Commands
		-Changed Help from modal to new page
	
**********************************************************/

var prevSeqNum = -1;
var prevLocation = 'null';
var prevJson = 'null';

var selectedIndex = 0;
var selectedDone = false;
var slideIndex = 0;

var listLength = 0;
var locationList = document.getElementById('locationList');
var listModal = document.getElementById('selectionModal');
//var helpModal = document.getElementById('helpModal')
var map;
var mapTypeID = 'hybrid';

var marker;

/* Polls the .json file every second to update the contents on the GUI*/
window.onload = function(){poll();};

/* Polls a .json file every second to update the Display*/						
function poll(){
	var page = window.location.pathname.substr(window.location.pathname.lastIndexOf('/') + 1);
	page = page.split('.')[0];
	
	//Updates the Maps content only if it is on the map else only look for commands
	if(page == 'map'){
		checkCookie();
		carousel();
		initMap();
		
		var mapCookie = Cookies.getJSON('mapCookie');
		updateContent(mapCookie);	
		setInterval(function(){$.post('LocationInfo.json' ,function(data){ 
										/* Comment out if on Desktop */
										if(JSON.stringify(prevJson) != JSON.stringify(data)){
											prevJson = data;
											selectedIndex = 0;
											updateAllInfo(data,false);
										}  
										
										/* Comment out if on PI*/
										/* if(prevJson != data){
											prevJson = data;
											selectedIndex = 0;
											updateAllInfo(data,false);
										}   */  
										
										});
							   $.post('GUICom.json' ,function(data){ 
										checkCommand(data);});		
								},1100);
	}
	else{
		setInterval(function(){$.post('GUICom.json' ,function(data){ 
										checkCommand(data);});		
								},1000);
	}
}

/* Initializes the Google Map API, able to set location, zoom level, and default controls.*/
function initMap(){
	/* Fetches the most recent data from the cookies*/
	var mapCookie = Cookies.getJSON('mapCookie');
	var selectedIndexCookie = Cookies.getJSON('selectedIndexCookie');
 
	var zoomLevel = (mapCookie.Type == 'Country')   ? 5 :
					(mapCookie.Type == 'Continent') ? 2 :
					(mapCookie.Type == 'City')	    ? 10 :
					5;
					
	var mapAdjustment = (mapCookie.Type == 'Country')   ? 7 :
						(mapCookie.Type == 'Continent') ? 7 :
						(mapCookie.Type == 'City')	    ? .3 :
						3.5;
					
	map = new google.maps.Map(document.getElementById('map'),
									{
										zoom: zoomLevel,
										center: {lat: mapCookie.Lat, lng: mapCookie.Lng+mapAdjustment},
										mapTypeId: selectedIndexCookie.mapTypeID,
										mapTypeControl: false,
										mapTypeControlOptions: {
											style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
											position: google.maps.ControlPosition.TOP_CENTER
										},
										zoomControl: false,
										zoomControlOptions: {
											position: google.maps.ControlPosition.LEFT_CENTER
										},
										scaleControl: true,
										streetViewControl: false,
										streetViewControlOptions: {
											position: google.maps.ControlPosition.LEFT_TOP
										},
										fullscreenControl: false
									});
	marker = new google.maps.Marker({
          position: {lat: mapCookie.Lat, lng: mapCookie.Lng},
          map: map
        });
}

/* Determiens if there is a Cookie and if there isn't then create a cookie file
 with the Default Location*/
function checkCookie(){
	var mapCookie = Cookies.getJSON('mapCookie');
	var selectedIndexCookie = Cookies.getJSON('selectedIndexCookie');
	
	/* Default Location if cookie is undefined*/
	if(mapCookie == 'undefined' || mapCookie == undefined || JSON.stringify(mapCookie).length < 10){
			mapCookie = Cookies.set('mapCookie',{'Name':'San Diego',
												'FullName':'San Diego, California, United States',
												'Population': '1,337',
												'Lat':32.7157,
												'Lng':-117.16,
												'Type': 'City',
												'Currency': 'USD', 
												'ExchangeRate':'$1 -> 1 USD',
												'Weather': 'Tropical and Subtropical Steppe Climate', 
												'Languages': 'English', 
												'Country': 'United States', 
												'Continent': 'North America', 
												'Message': 'Some message',
												'GunDeathRate' : '1337',
												'Lunch' : '$9.00',
												'Housing' : '$1500'
											  },{ expires: 1, path: '' });
	}
	
	if(selectedIndexCookie == 'undefined'|| selectedIndexCookie == undefined){
		Cookies.set('selectedIndexCookie',{'selectedIndex' : 0, 
											'mapTypeID' : mapTypeID},{ expires: 1, path: '' })
		selectedIndexCookie = Cookies.getJSON('selectedIndexCookie');	
	}
	
	selectedIndex = selectedIndexCookie.selectedIndex;
}

/* Updates all the info on the GUI including Table contents and Images */
function updateAllInfo(location, isMap){
	/*Comment out only if on PI */
	//location = JSON.parse(location);
	
	if(location == null){
		return;
	}
	
	/* Updates Content if it is a different location*/
	if(prevLocation != location[selectedIndex].FullName || isMap){
		prevLocation = location[selectedIndex].FullName;
		updateModal(location,'false');
			
		if(isMap){
			updateContent(location[selectedIndex]);
		}	
	}	
}

/* Fills in the location details on the page */
function updateContent(location){		

	/* Update Main Details about Location */
	if(location.Type != 'Country' && location.Type != 'Continent'){
		updateAttribute('Grid00_Content',location.FullName.substring(0,location.FullName.lastIndexOf(',')));
		updateTableContent('Grid11','Country',location.Country);
	}
	else{
		if(location.Type == 'Country'){
			updateTableContent('Grid11','Continent',location.Continent);
		}
		else{
			updateTableContent('Grid11','Location','Earth');
		}
		updateAttribute('Grid00_Content',location.FullName);
	}

	/* Updates the Content of the Table and makes it blank if there is no data */
	updateTableContent('Grid10','Population',location.Population);
	
	if(location.Languages == undefined || location.Languages == '' || location.Languages == 'undefined' ||
	   location.ExchangeRate == undefined || location.ExchangeRate == '' || location.ExchangeRate == 'undefined'){
		updateTableContent('Grid20','','');
		updateTableContent('Grid21','','');	
	}
	else{
		updateTableContent('Grid20','Language',location.Languages);
		
		if(location.Country == 'United States'){
			updateTableContent('Grid21','Currency','USD');
		}
		else{
			var exchangeRate = location.ExchangeRate.split(' ');
			exchangeRate[2] = Number(exchangeRate[2]).toFixed(2);
			exchangeRate[1] = '=';
			exchangeRate[0] = '1.00 USD';
			exchangeRate = exchangeRate.join(' ');
			
			updateTableContent('Grid21','Exchange Rate',exchangeRate);
		}
			
	}
	updateTableContent('Grid30','Climate',location.Weather);
	
	
	/* Update Details about Location */
	if(location.Type != 'Country' && location.Type != 'Continent'){
		updateAttribute('Grid00D_Content',location.FullName.substring(0,location.FullName.lastIndexOf(',')));
		updateTableContent('Grid10D','Avg Medium Apartment Rent', location.Housing);
		updateTableContent('Grid20D','Avg Lunch Price', location.Lunch);
		updateTableContent('Grid30D','Gun Death per 100k People/Year', location.GunDeathRate);
	}
	else{
		updateAttribute('Grid00D_Content',location.FullName);
		updateTableContent('Grid10D','',location.MoreInfo);
		updateTableContent('Grid20D','Avg Lunch Price', location.Lunch);
		updateTableContent('Grid30D','Gun Death per 100k People/Year', location.GunDeathRate);
	}


	/* Updates the Images on the Slideshow */
	updateImageSrc('Image',location.FullName);
	
	var zoomLevel = (location.Type == 'Country')   ? 5 :
					(location.Type == 'Continent') ? 2 :
					(location.Type == 'City')	  ?  10 :
					5;	
					
	var mapAdjustment = (location.Type == 'Country')   ? 7 :
						(location.Type == 'Continent') ? 7 :
						(location.Type == 'City')	    ? .3 :
						3.5;
						
	map.setCenter({lat: location.Lat, lng: location.Lng+mapAdjustment});
	map.setZoom(zoomLevel);
	
	/*Remove the previous Marker */
	marker.setMap(null);
	marker = new google.maps.Marker({
          position: {lat: location.Lat, lng: location.Lng},
          map: map ,
		  animation: google.maps.Animation.Drop
        }); 

	/* Creates Cookies to store the current Location and Index */
	Cookies.remove('mapCookie', { path: '' });
	Cookies.set('mapCookie',location,{ expires: 1, path: '' })
	Cookies.set('selectedIndexCookie',{'selectedIndex' : selectedIndex, 
									   'mapTypeID' : mapTypeID},{ expires: 1, path: '' })
}

/* Displays Modal that contains additional location for the user to 
choose from.*/
function updateModal(list,show){	
	/* Displays the List*/
	if(show == 'true'){
		listModal.style.display = 'block';
	}
	
	/* Fills in the Content */
    for (var i = 0; i < list.length; i++) {
		if(i >9){ break;}
		updateAttribute('Loc'.concat(i+'Num'),i+1);
		updateAttribute('Loc'.concat(i),(list[i].FullName));
    }
	
	listLength = (list.length>10) ? 10 : list.length;
	
	/* Highlight the selected Index*/
    $('#Loc'.concat(0)).css('background-color', 'rgba(255, 212, 96, 0.53)');
	$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(255, 212, 96, 0.53)');	
}

/* Updates a specified element of the GUI */
function updateAttribute(ID,attribute){
	var fullID = '#'+ ID;	
	$(fullID).attr('data-messages', attribute);
	$(fullID).html( $(fullID).attr('data-messages') );
} 

function updateTableContent(ID,header,content){
	var headerID = '#'+ID +'_Header';
	var contentID = '#'+ID +'_Content';
	
	if(content == undefined || content == '' || content == 'undefined'){		
		$(headerID).attr('data-messages', '');
		$(headerID).html( $(headerID).attr('data-messages') );
		$(contentID).attr('data-messages', '');
		$(contentID).html( $(contentID).attr('data-messages') );
	}
	else{
		$(headerID).attr('data-messages', header);
		$(headerID).html( $(headerID).attr('data-messages') );
		$(contentID).attr('data-messages', content);
		$(contentID).html( $(contentID).attr('data-messages') );
	}
}

/* Updates the Image files*/
function updateImageSrc(ID,locationName){
	for(var i = 0; i< 3; i++){
		$('#'.concat(ID+i)).attr('src','Images/' + locationName + i + '.jpg');		
	}
} 

/* Check GUICommand.json to see what command to implement. If the SeqName
   is the same as the previous check, do nothing*/
function checkCommand(command){
	
	/*Comment out only if on PI */
	//command = JSON.parse(command);

	if(prevSeqNum != command.SeqNum){
		prevSeqNum = command.SeqNum
		
		/* Determines the Option Number to Select*/
		var optionNum = 1;	
		if(command.GUICommand.includes('Option')){
			selectedIndex = command.GUICommand.substring(6) -1; 
			command.GUICommand = 'selectItem'
		}
		else if(command.GUICommand.toLowerCase().includes('zoom')&& listModal.style.display == 'block'){
			command.GUICommand = (command.GUICommand.includes('In'))   ? 'down' : 
								 (command.GUICommand.includes('Out')) ? 'up':
								 'selectItem';
		}
					
		switch(command.GUICommand){
			case 'zoomOut':
				if(map.getZoom()-3<1){
					map.setZoom(1);
				}
				else{
					map.setZoom(map.getZoom() - 3);
				}
				break;
			case 'zoomIn':
				map.setZoom(map.getZoom() + 3);
				break;	
			case 'defaultZoom':
				map.setZoom(10);
				break;
			case 'East':
				var center = map.getCenter();
				map.setCenter({lat: center.lat(), lng: center.lng()+5})
				break;
			case 'West':
				var center = map.getCenter();
				map.setCenter({lat: center.lat(), lng: center.lng()-5})
				break;	
			case 'switchView':
				mapTypeID = (mapTypeID == 'hybrid') ? 'TERRAIN' : 'hybrid';
				map.setMapTypeId(google.maps.MapTypeId[mapTypeID]);
				break;
			case 'ShowList':
				listModal.style.display = 'block';
				
				/* Deselect the previous location */
				for(var i = 0; i< listLength; i++){
						$('#Loc'.concat(i)).css('background-color', 'rgba(50, 55, 78, 0.66)');
						$('#Loc'.concat(i+'Num')).css('background-color', 'rgba(50, 55, 78, 0.66)');
				}	
				selectedIndex = 0;
				$('#Loc'.concat(selectedIndex)).css('background-color', 'rgba(255, 212, 96, 0.53)');
				$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(255, 212, 96, 0.53)');	
				
				/* Times out after 2:30 minute */
				setTimeout(function() { listModal.style.display = 'none';}, 180000);
				break;
			case 'selectItem':
			
				$('#Loc'.concat(selectedIndex)).css('background-color', 'rgba(255, 212, 96, 0.53)');
				$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(255, 212, 96, 0.53)');

				/* Close List View & Deselect the selected option*/
				for(var i = 0; i< listLength; i++){
					$('#Loc'.concat(i)).css('background-color', 'rgba(50, 55, 78, 0.66)');
					$('#Loc'.concat(i+'Num')).css('background-color', 'rgba(50, 55, 78, 0.66)');
				}	
				updateAllInfo(prevJson,true);	
			
				
				listModal.style.display = 'none';
				//helpModal.style.display = 'none';
				break;
			case 'up':		
				/* Deselect the previous location */
				$('#Loc'.concat(selectedIndex)).css('background-color', 'rgba(50, 55, 78, 0.66)');
				$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(50, 55, 78, 0.66)');

				/* Highlight the location above the current one */
				selectedIndex = (selectedIndex == 0) ? listLength-1: selectedIndex-1;
				$('#Loc'.concat(selectedIndex)).css('background-color', 'rgba(255, 212, 96, 0.53)');
				$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(255, 212, 96, 0.53)');

				break;
			case 'down':
				/* Deselect the previous location */
				$('#Loc'.concat(selectedIndex)).css('background-color', 'rgba(50, 55, 78, 0.66)');
				$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(50, 55, 78, 0.66)');

				/* Highlight the location below the current one */
				selectedIndex = (selectedIndex == listLength-1) ? 0: selectedIndex+1;
				$('#Loc'.concat(selectedIndex)).css('background-color', 'rgba(255, 212, 96, 0.53)');
				$('#Loc'.concat(selectedIndex+'Num')).css('background-color', 'rgba(255, 212, 96, 0.53)');
				break;
			default:
				var page = window.location.pathname.substr(window.location.pathname.lastIndexOf('/') + 1)
							.split('.')[0];
				pageNavigation(page,command.GUICommand);	
		}
	}
}

/* Determines which page to navigate to*/
function pageNavigation(currentPage,requestedPage){
	
	switch(requestedPage){
		case currentPage:	
			if(currentPage == 'map'){
				selectedIndex = 0;
				updateAllInfo(prevJson,true);	
				listModal.style.display = 'none';
				//helpModal.style.display = 'none';
				document.getElementById('details').style.display = 'none';
				document.getElementById('mainInfo').style.display = 'block';	
			}						
			break;
		case 'map':
			window.location.href = 'map.html';
			updateAllInfo(prevJson,true);	
			break;
		case 'welcome':
			window.location.href = 'welcome.html';
			break;
		case 'idle':
			window.location.href = 'idle.html';
			break;
		case 'about':
			window.location.href = 'about.html';
			break;
		case 'arnold':
			window.location.href = 'arnold.html';
			break;
		case 'goodbye':
			window.location.href = 'goodbye.html';
			break;
		case 'details':
			document.getElementById('details').style.display = 'block';
			document.getElementById('mainInfo').style.display = 'none';
			break;
		case 'help':
			window.location.href = 'help.html';
			break;
		case 'globetrotters' :
			window.location.href = 'globetrotters.html';
			break;
		default:
	}
}

function carousel() {
    var i;
    var x = document.getElementsByClassName('imgSlides');
    for (i = 0; i < x.length; i++) {
       x[i].style.display = 'none';  
    }
    slideIndex++;
    if (slideIndex > x.length) {slideIndex = 1}    
    x[slideIndex-1].style.display = 'block';  
    setTimeout(carousel, 7000); // Change image every 2 seconds
}
