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
	var filterableColumnNames = [
		"Name",
		"Type",
		"Req1",
		"Req2",
		"Req3"];
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
		
		
    document.getElementById("menu3").classList.add("current");
    document.getElementById("menu3.1").classList.add("current");
	document.getElementById("tableform").style.display = "inline";
		
		
		
		
		var datatest = 100;
		$('#btn_ZoomIn').click(function () {
			
			document.getElementById("techpic").style.height = "auto";
			datatest = datatest + (datatest/10);
			$('#techpic').animate({
				'width': '' +datatest+ '%'
			}, 200);
			
		});

		
		$('#btn_ZoomOut').click(function () {
			
			document.getElementById("techpic").style.height = "auto";
			datatest = datatest - (datatest/10);
			$('#techpic').animate({
				'width': '' +datatest+ '%'
			}, 200);
			
		});
	

		$('#btn_ZoomAll').click(function () {
			
			datatest = 100;
			$('#techpic').animate({
				'width': '' +datatest+ '%',
				'height': '' +datatest+ '%'
			}, 200);
			
		});
	

		$('#btn_ZoomReset').click(function () {
			
			datatest = 100;
			document.getElementById("techpic").style.width = "100%";
			document.getElementById("techpic").style.height = "auto";
		});
			
    });
		
		screenWidth = $(window).width();
		screenHeigh = $(window).height()
		if (screenWidth >= 920)
			var tableSize = (Math.round($(window).height()) - 631);
		else if (screenWidth >= 580)
			var tableSize = (Math.round($(window).height()) - 521);
		else
			var tableSize = (Math.round($(window).height()) - 417);
		
		var dynamicSize = (tableSize * 100 / screenHeigh);
		
		
		
		
		$('#techstable').DataTable({
			dom: '<"top">rt<"bottom"ip><"clear">',
			hideEmptyCols: true,
			lengthChange: true,
			paging: false,
			pageResize: true,
			scrollX: true,
		        scrollY: '' + dynamicSize + 'vh',
		        scrollCollapse: true,
			fixedColumns: {
				leftColumns: 1
			},
			data: itemstechs,
			columns: [
				{ /* 0 (Col 0) */
					data: null,
					searchable: false,
					orderable: false,
					className:      'row-index',
					width: "1em",
					targets: 0
				},
				{ /* 1 (Col 1) */
					name: "Name", data: "name",
					orderable: false },
				{ /* 2 (Col 2) */
					name: "Req1", data: "requiresTech.0",
					orderable: false },
				{ /* 3 (Col 3) */
					name: "Req2", data: "requiresTech.1",
					orderable: false },
				{ /* 4 (Col 4) */
					name: "Req3", data: "requiresTech.2",
					orderable: false },
				{ /* XX (Last Col) */
					data: "className",
					searchable: false,
					orderable: false,
					className:      'details-control',
					defaultContent: ''
				}
			], 
			order: [[ 1, 'asc' ]],
			aoColumnDefs: [
				{
					"aTargets": [1],
					"mData": "name",
					"mRender": function ( data, type, full ) {
						var thisName = '<span style="border-left: 6px solid ' + full.transModeColor + '; padding-left: 5px;">'+data+'</span>';
						var reallink = data.replace(/\s+/g, '');
						if (full.requiPremium == true)
							thisName += ' <span class="premium">&#x2605;<span class="premium-text">Premium</span></span>';
						return '<a class="item-details-link" href="#'+reallink+'">'+thisName+'</a>';
					}
				},
				{
					"aTargets": [2],
					"mData": "requiresTech.0",
					"mRender": function ( data, type, full ) {
						var reqString = '';
						if (data) {
							var reqArray = data.split("|");
							for (var j = reqArray.length - 1; j >= 0; j--) {
							if (j != reqArray.length - 1)
								reqString += ' <b>or</b> ';
							reqString += reqArray[j];
							}
						}
						return reqString;
					}
				},
				{
					"aTargets": [3],
					"mData": "requiresTech.1",
					"mRender": function ( data, type, full ) {
						var reqString = '';
						if (data) {
							var reqArray = data.split("|");
							for (var j = reqArray.length - 1; j >= 0; j--) {
							if (j != reqArray.length - 1)
								reqString += ' <b>or</b> ';
							reqString += reqArray[j];
							}
						}
						return reqString;
					}
				},
				{
					"aTargets": [4],
					"mData": "requiresTech.2",
					"mRender": function ( data, type, full ) {
						var reqString = '';
						if (data) {
							var reqArray = data.split("|");
							for (var j = reqArray.length - 1; j >= 0; j--) {
							if (j != reqArray.length - 1)
								reqString += ' <b>or</b> ';
							reqString += reqArray[j];
							}
						}
						return reqString;
					}
				},
				{
					"aTargets": [5],
					"mData": "name",
					"mRender": function ( data, type, full ) {
						return '<a class="item-details-link" href="#'+data+'">Details</a>';
					}
				}
			],
			initComplete: function(settings, json) {
				/* Show the table after everything is loaded*/
				$( "#loading-overlay" ).hide( "fast" );

				/* Open Item Description if hash on url */
				if (window.location.hash) {
					console.log(window.location.hash);
					var className = window.location.hash.substring(1);
					openItemDesc(className);
				}
			}
		});
		
		
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
	
		$('#techpic').click( function () {
			window.onhashchange = function() { 
				var className = window.location.hash.substring(1);
				openItemDesc(className);
			}	
		});
	
		/* Close Item Description */
		$(document).on('click', 'a.item-details-close', function() { 
			$( "#item-description" ).hide( "slow" );
			history.pushState({}, null, "techs_h.html");
		});

		oTable = $('#techstable').DataTable();   //pay attention to capital D, which is mandatory to retrieve "api" datatables' object, as @Lionel said
		/* Table: add an index for each row */
		oTable.on( 'order.dt search.dt', function () {
			oTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
				cell.innerHTML = i+1;
			} );
		} ).draw();
		
	
		
	
}
