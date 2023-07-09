$("#menu-toggle").click(function(e) {
		e.preventDefault();
		$("#wrapper").toggleClass("toggled");
});
var imgSource = imageFolder;
window.addEventListener("load",initApp,false);

function initApp() {
	/*var stages = [];
	$.each(window.ColonyGame.meta.gameStages, function(index, data) {
		stages.push(data.threshold);
	});*/
	
		screenWidth = $(window).width();
		screenHeigh = $(window).height();
		if (screenWidth >= 580) {
			var tableSize = (Math.round($(window).height()) - 132);
			document.getElementById("indexcontainer").style.height = '' + tableSize + 'px';
		}
		if (screenWidth >= 920) {
			var tableSize = (Math.round($(window).height()) - 190);
			document.getElementById("indexcontainer").style.height = '' + tableSize + 'px';
		}
		
	
/* ------------------------parsing (start)--------------------------- */
/* buildings before terrains before tiles */
/* tech before races and factions */
/* planet type after deposit and techs*/
	var meta = {
		dataVersion: window.ColonyGame.meta.buildVersion,
		imgSource: imgSource
	};
	//add resources ok
	$.each(window.ColonyGame.resources, function(index, obj) {
		addItem(obj, 'resource');
		addDataToList('resource', obj);
	});
	//add vehicles
	$.each(window.ColonyGame.vehicles, function(index, obj) {
		addItem(obj, 'vehicle');
		addDataToList('vehicle', obj);
	});
	//add buildings
	$.each(window.ColonyGame.buildings, function(index, obj) {
		addItem(obj, 'building');
		addDataToList('building', obj);
	});
	//add terrains ok
	$.each(window.ColonyGame.terrains, function(index, obj) {
		addItem(obj, 'deposit');
		addDataToList('deposit', obj);
	});
	//add techs ok
	$.each(window.ColonyGame.technology, function(index, obj) {
		addItem(obj, 'technology');
		addDataToList('technology', obj);
	});
	//add planets ok
	$.each(window.ColonyGame.mapTypes, function(index, obj) {
		addItem(obj, 'map');
		addDataToList('map', obj);
	});
	//add races ok
	$.each(window.ColonyGame.races, function(index, obj) {
		addItem(obj, 'race');
		addDataToList('race', obj);
	});
	//add factions ok
	$.each(window.ColonyGame.civilizations, function(index, obj) {
		addItem(obj, 'civilization');
		addDataToList('civilization', obj);
	});
	//add tiles
	$.each(window.ColonyGame.tiles, function(index, obj) {
		addItem(obj, 'tile');
		addDataToList('tile', obj);
	});
	items.sort(compareValues('name','desc')); 
	itemLinks.sort(compareValues('src','desc')); 
	var stageBG = ['#95a5a6', '#1abc9c', '#2ecc71', '#3498db'];
/* ------------------------parsing (end)--------------------------- */


	$(document).ready(function() {
		
		
	document.getElementById("menu0").classList.add("current");
	document.getElementById("page-content-wrapper").style.padding = "15px";
		
		
		

		$( "#loading-overlay" ).hide( "fast" );
			/*initComplete: function(settings, json) {
				 Show the table after everything is loaded
				$( "#loading-overlay" ).hide( "fast" );*/


				/* Open Item Description if hash on url */
				if (window.location.hash) {
					console.log(window.location.hash);
					var className = window.location.hash.substring(1);
					openItemDesc(className);
				}

				
			/*}*/
		
		
		
		/* Open Item Description */
		function openItemDesc(className) { 
			var className = className || null;
			$('.item-properties').html('');
			$('#charac-header').hide();
			$('#prod-header').hide();
			$('#transf-header').hide();
			$('#utility-header').hide();
			$('#generateorsmelt').hide();
			$('#require-header').hide();
			$('#cost-header').hide();
			$('#sell-header').hide();
			$('#links-header').hide();

			printDescription(className);
			if ($("#item-description").is(":visible")) {
				
				$('html, body').animate({
					scrollTop: $("#item-description").offset().top -20
				}, 600);
			} else {
				$( "#item-description" ).show( "slow" );
			}
		};
		$(document).on('click', 'a.item-details-link', function(){
			var className = $(this).attr('href').substring(1);
			openItemDesc(className);
		});
		/* Close Item Description */
		$(document).on('click', 'a.item-details-close', function() { 
			$( "#item-description" ).hide( "slow" );
		});

		
		
		

		

		


		

		
	});
}
