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
		
		
    document.getElementById("menu2").classList.add("current");
    document.getElementById("menu2.2").classList.add("current");
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
		
    // build column list
    console.log(itemsratio);
    var columnlist = [];
    for (var i = 0; itemsratio.length > i; i++) {
         var currentitem = itemsratio[i];
         for (res in currentitem.RatioTable) {
             if (columnlist.indexOf(res)<0) {
                 columnlist.push(res);
             }
         }
    }
    columnlist.sort();
    var htmltablehead = '<tr><th>Name</th>';
    for (var i = 0; columnlist.length > i; i++) {
        htmltablehead += '<th>'+columnlist[i]+'</th>';
    }
    htmltablehead += '<th>Details</th></tr>';
    console.log(columnlist);
    // build HTML table body
    var htmltablebody = '';
    for (var i = 0; itemsratio.length > i; i++) {
        var currentitem = itemsratio[i];
        if (currentitem.requiPremium) {
            var temp_p = '1';
        } else {
            var temp_p = '0';
        }
        htmltablebody += '<tr><td>'+currentitem.name+'|'+currentitem.transModeColor+'|'+temp_p+'</td>';
        for (var j = 0; columnlist.length > j; j++) {
            var temp_res = columnlist[j];
            var temp_val = currentitem.RatioTable[temp_res];
            if (temp_val) {
                htmltablebody += '<td>'+(parseFloat(temp_val)*20*60).toFixed(4)+'</td>'; // with 20 fps
            } else {
                htmltablebody += '<td></td>';
            }
        }
        htmltablebody += '<td>'+currentitem.className+'</td></tr>';
    }
    
    document.getElementById('maintable').innerHTML = '<thead>'+htmltablehead+'</thead><tbody>'+htmltablebody+'</tbody><tfoot>'+htmltablehead+'</tfoot>';
    
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
				leftColumns: 0
			},
			order: [[ 0, 'asc' ]],
			columnDefs: [
				{
					"targets": 0,
					"render": function ( data, type, full ) {
           var temp_n = data.split('|')[0];
           var temp_c = data.split('|')[1];
           var temp_p = data.split('|')[2];
           
						var thisName = '<span style="border-left: 6px solid ' + temp_c + '; padding-left: 5px;">'+temp_n+'</span>';
						var reallink = temp_n.replace(/\s+/g, '');
						if (temp_p=='1') {
							thisName += ' <span class="premium">&#x2605;<span class="premium-text">Premium</span></span>';
            }
						return '<a class="item-details-link" href="#'+reallink+'">'+thisName+'</a>';
					}
				},
				{
					"targets": -1,
					"render": function ( data, type, full ) {
						return '<a class="item-details-link" href="#'+data+'">Details</a>';
					},
					"searchable": false,
					"orderable": false,
					"className":      'details-control'
				}
			],
			initComplete: function(settings, json) {
				/* Show the table after everything is loaded*/
				$( "#loading-overlay" ).hide( "fast" );


				/* Open Item Description if hash on url */
				if (window.location.hash) {
					//console.log(window.location.hash);
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
		
		/* Table: add an index for each row 
		oTable.on( 'order.dt search.dt', function () {
			oTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
				cell.innerHTML = i+1;
			} );
		} ).draw();
		*/
		
		
		/* Add a button to clear text */
		$(document).on('click', 'button#cleart', function() {
			var searchval = $(this).text();
			searchval = '';
			setSearchVal(searchval);
			$('#searchdatalist').trigger('input');
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
