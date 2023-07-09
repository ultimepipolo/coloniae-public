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
		"BuildingCategories"];
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




	/* name = item name */
	function linkTo(name, type) {
		console.log(name, type);
		return '<a class="opendesc" href="#' + type + '-' + identify(name) + '">' + name + '</a>';
	}

	/* update url */
	function updateUrlParameter(uri, key, value) {
		// remove the hash part before operating on the uri
		var i = uri.indexOf('#');
		var hash = i === -1 ? ''  : uri.substr(i);
		uri = i === -1 ? uri : uri.substr(0, i);

		var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
		var separator = uri.indexOf('?') !== -1 ? "&" : "?";

		if (!value) {
			// remove key-value pair if value is empty
			uri = uri.replace(new RegExp("([?&]?)" + key + "=[^&]*", "i"), '');
			if (uri.slice(-1) === '?') {
				uri = uri.slice(0, -1);
			}
			// replace first occurrence of & by ? if no ? is present
			if (uri.indexOf('?') === -1) uri = uri.replace(/&/, '?');
		} else if (uri.match(re)) {
			uri = uri.replace(re, '$1' + key + "=" + value + '$2');
		} else {
			uri = uri + separator + key + "=" + value;
		}
		return uri + hash;
	}
	function updateURL(key,value) {
		window.history.pushState(
			"object or string", 
			"My Colony Reference - Online Encyclopedia", 
			updateUrlParameter(window.location.href, encodeURI(key), encodeURI(value)));
	}

	/* get the URL search variable and convert to object */
	function searchToObject() {
		var pairs = window.location.search.substring(1).split("&"),
			obj = {},
			pair,
			i;

		for ( i in pairs ) {
			if ( pairs[i] === "" ) continue;

			pair = pairs[i].split("=");
			obj[ decodeURIComponent( pair[0] ) ] = decodeURIComponent( pair[1] );
		}

		return obj;
	}
	var searchObj = searchToObject();
	$(document).ready(function() {
		
		
    document.getElementById("menu1").classList.add("current");
    document.getElementById("menu1.1").classList.add("current");
	document.getElementById("tableform").style.display = "inline";
		
		
		screenWidth = $(window).width();
		screenHeigh = $(window).height()
		if (screenWidth >= 920)
			var tableSize = (Math.round($(window).height()) - 301);
		else if (screenWidth >= 580)
			var tableSize = (Math.round($(window).height()) - 240);
		else
			var tableSize = (Math.round($(window).height()) - 286);
		
		var dynamicSize = (tableSize * 100 / screenHeigh);
		
		//$('#ref-version-number').append(" "+referenceVersion+"");
		//$('#game-version-number').append(" "+meta.dataVersion+"");
		/*console.log(items);
		console.log(itemLinks);*/
   
		$('#maintable').DataTable({
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
			data: items,
			columns: [
				{ /* 0 (Col 0) */
					data: null,
     title:"#",
					searchable: false,
					orderable: false,
					className:      'row-index',
					width: "1em",
					targets: 0
				},
				{ /* 1 (Col 1) */
					name: "Name", data: "name",title:"Name" },
				{ /* 2 (Col 2) */
					name: "Type", data: "type",title:"Type" },
				{ /* 3 (Col 3) */
					name: "BuildingCategories", data: "buildCategoriesObj",title:"Categories"
				},
				{ /* 4 (Col 4) */
					name: "ReleaseVersion", data: "releaseVersion",title:"Release Version"
				},
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
					"mData": "type",
					"mRender": function ( data, type, full ) {
						return '<a class="tofilter" href="#">'+data.toLowerCase().replace(/\b[a-z]/g, function(letter) {
							return letter.toUpperCase();
						})+'</a>';
					}
				},
				{
					"aTargets": [3],
					"mData": "buildCategoriesObj",
					"mRender": function ( data, type, full ) {
						var text = '';
						if (data && typeof data === 'object') {
							for (var i = 0; i < data.length; i++) {
								if (i > 0)
									text += ', ';
								text += '<span>'+data[i]+'</span>';
							};
						}
						
						return text;
					}
				},
        {
					"aTargets": [4],
					"mData": "releaseVersion",
					"mRender": function ( data, type, full ) {
						return data;
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

				/* Set the search field if in URL */
				if (searchObj['search']) {
					setSearchVal(decodeURI(searchObj['search']));
					this.api().search(decodeURI(searchObj['search'])).draw();
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
		/* Close Item Description */
		$(document).on('click', 'a.item-details-close', function() { 
			$( "#item-description" ).hide( "slow" );
		});

		oTable = $('#maintable').DataTable();   //pay attention to capital D, which is mandatory to retrieve "api" datatables' object, as @Lionel said
		/* Initialize filters */
		yadcf.init(oTable, [/*
			{column_number : 0 },
			{column_number : 1 },*/
			{column_number : 2, filter_type: 'select', filter_default_label: 'All Types', filter_reset_button_text: false},
	    	{column_number : 3, text_data_delimiter: ",", filter_default_label: "Categories", filter_reset_button_text: false}
	    	], {filters_position: "footer", filters_tr_index: 1});
		/* Table: add an index for each row */
		oTable.on( 'order.dt search.dt', function () {
			oTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
				cell.innerHTML = i+1;
			} );
		} ).draw();
		
		if (searchObj) {
			var presetFilters = [];
			for (var filterName in searchObj){
				if (filterableColumnNames.indexOf(filterName) > -1) {
					var filterID = oTable.column(filterName+':name').index();
					presetFilters.push([filterID, searchObj[filterName]]);
				}
			}
			
			yadcf.exFilterColumn(oTable, presetFilters);
		}

		/* Update URL when filter selection */
		$(document).on('change', 'select.yadcf-filter', function() { 
			var colID = $(this).attr('id');
			colID = colID.replace('yadcf-filter--maintable-', '');
			var columns = oTable.settings().init().columns;
			var columnFilterName = columns[colID].name;
			var columnFilterVal = yadcf.exGetColumnFilterVal(oTable,colID);
			updateURL(columnFilterName, columnFilterVal);
		});

		/* Add a button to clear filters */
		$(document).on('click', 'button#clearf', function() { 
			yadcf.exResetAllFilters(oTable);
			oTable.search(decodeURI(searchObj['search'])).draw();
			for (var i = 0; i < filterableColumnNames.length; i++) {
				updateURL(filterableColumnNames[i], '');
			};
		});

		
		/* Add a button to clear text */
		$(document).on('click', 'button#cleart', function() {
			var searchval = $(this).text();
			searchval = '';
			setSearchVal(searchval);
			$('#searchdatalist').trigger('input');
		});



		$(document).on('click', 'a.tofilter', function() { 
			var searchval = $(this).text();
			if (searchval == 'All')
				searchval = '';
			else
				searchval = '"'+searchval+'"';
			setSearchVal(searchval);
			$('#searchdatalist').trigger('input');
			$( "#item-description" ).hide( "slow" );
		});

		function setSearchVal(searchval) {
			$("#searchdatalist").val(searchval);
		}
		$('#searchdatalist').on('input', function() {
			// add search filter
			updateURL('search', $(this).val());
			oTable.search($(this).val()).draw();
		});

		
	});
}
