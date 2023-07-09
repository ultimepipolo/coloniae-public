
/* ------------------------display formatting (start)--------------------------- */
	var formatProperty = function (propertyType, propertyData, orientation) {
		var propertyType = propertyType || 'unknown';
		var orientation = orientation || 'vertical';
		var tHtml = '';
		/* property specific formattage */
		if (propertyType == 'description' && propertyData) {
			tHtml += '<dt class="note"><i>' + window.appStrings.en[propertyData] + '</i></dt>';
		}
		/* CARACTERISTICS */
		/* buildings */
		if (propertyType == 'tilesize' && propertyData) {
			tHtml += '<dt>Tile size </dt><dd>' + propertyData.tileSize + ' (' + propertyData.tileWidth + 'x' + propertyData.tileHeight + ')</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'releaseversion') {
       if (propertyData == '') {
  			 tHtml += '<dt>Release version </dt><dd>unknown</dd>';
       } else {
  			 tHtml += '<dt>Release version </dt><dd>' + propertyData + '</dd>';
       }
  		 $('#charac-header').show();
		}
		if (propertyType == 'buildLimit' && propertyData) {
			tHtml += '<dt>Building limited to ' + propertyData+ '.</dt>';
			$('#charac-header').show();
		}
		if (propertyType == 'isConsulate' && propertyData) {
			tHtml += '<dt>This building is a consulate.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'isCapitol' && propertyData) {
			tHtml += '<dt>This building is a capitol.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'isEmbassy' && propertyData) {
			tHtml += '<dt>This building is an embassy.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'onlineTradeDepot' && propertyData) {
			tHtml += '<dt>This building is an online trade depot.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'isCommsHubBldg' && propertyData) {
			tHtml += '<dt>This building is a communications Hub.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'acceptsWorkers' && propertyData) {
			if (propertyData.acceptsWorkers) {
				tHtml += '<dt>Workers</dt><dd class="worker">' + propertyData.acceptsWorkers+ '</dd>';
				if (propertyData.occupation)
				tHtml += '<dt>Occupation</dt><dd class="worker">' + propertyData.occupation+ '</dd>';
				if (propertyData.requiresWorkers)
					tHtml += '<dt>Workers needed</dt><dd class="worker">' + (propertyData.requiresWorkers == true ? 'Yes' : 'No' ) + '</dd>';
				else
					tHtml += '<dt>Workers needed</dt><dd class="worker">No</dd>';
			}
			else
				tHtml += '<dt>Workers</dt><dd class="worker">No</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'providesShelter' && propertyData) {
			tHtml += '<dt>Max Colonist</dt><dd>+' + propertyData + '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'heals' && propertyData) {
			tHtml += '<dt>This building can heal ' + propertyData + ' colonists.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'requiresIQ' && propertyData) {
			tHtml += '<dt>This building requires a ' + propertyData + ' IQ.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'educates' && propertyData) {
			tHtml += '<dt>This building can educate ' + propertyData + ' colonists.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'providesIQ' && propertyData) {
			tHtml += '<dt>This building provides a ' + propertyData + ' IQ.</dt><dd></dd>';
			$('#charac-header').show();
		}
		if ((propertyType == 'entertains' || propertyType == 'takesTourists') && propertyData.entertainmentCost) {
			if (propertyData.entertains)
				tHtml += '<dt>Guests</dt><dd class="guest">' + propertyData.entertains + ' Guests</dd>';
			if (propertyData.takesTourists)
				tHtml += '<dt>(Max) Tourists</dt><dd class="guest">' + propertyData.takesTourists + ' Tourists</dd>';
			tHtml += '<dt>Admission fee</dt><dd class="generate">$' + propertyData.entertainmentCost + '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'storesObj' && propertyData) {
			for (resource in propertyData)
				tHtml += '<dt>Max <a class="item-details-link" href="#' + identify(resource) + '">' + resource + '</a></dt><dd class="store">+' + propertyData[resource] + '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'earthTaxValue' && typeof(propertyData) !== 'undefined') {
			tHtml += '<dt>Motherland Tax</dt><dd class="consume">-$' + propertyData + '</dd>';
			$('#charac-header').show();
		}
		/* resources */
		if (propertyType == 'resourceLimited' && propertyData.resourceLimited) {
			tHtml += '<dt>Storage Limit</dt><dd class="store">' + propertyData.resourceLimited + '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'resourcebasePrice' && propertyData.resourcebasePrice) {
			tHtml += '<dt>Base Price</dt><dd class="worker">' + propertyData.resourcebasePrice + ' $</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'resourcetoxicRate' && propertyData.resourcetoxicRate) {
			tHtml += '<dt>Toxic Rate</dt><dd class="consume">' + propertyData.resourcetoxicRate + '</dd>';
			$('#charac-header').show();
		}
		if ((propertyType == 'storedbylist') && (propertyData.type == 'resource')) {
			var sbHtml = '';
			for (var i = items.length - 1; i >= 0; i--) {
				if (items[i].storesObj) {
					if (items[i].storesObj[propertyData.name])
						sbHtml += '<a class="item-details-link" href="#' + identify(items[i].name) + '"">' + items[i].name + '</a><i class="store"> +' + items[i].storesObj[propertyData.name] + '</i><br>';
				}
			};
			if (sbHtml.length) {
				tHtml += '<dt class="store">Stored by</dt><dd>' + sbHtml + '</dd><br>';
			}
			$('#charac-header').show();
		}
		if (propertyType == 'LinksProcesses' && propertyData) {
			itemLinksProcesses.sort(compareValues('src','desc'));
			var hbHtml = '';
			for (var i = itemLinksProcesses.length - 1; i >= 0; i--) {
				if (propertyData.name == itemLinksProcesses[i].dst && itemLinksProcesses[i].type == 'harvests')
					hbHtml += '<a class="item-details-link" href="#' + identify(itemLinksProcesses[i].src) + '"">' + itemLinksProcesses[i].src + '</a><br>';
			};
			if (hbHtml.length) {
				tHtml += '<dt class="processed">Harvested by</dt><dd>' + hbHtml + '</dd>';
				$('#charac-header').show();	
			}
			var prHtml = '';
			for (var i = itemLinksProcesses.length - 1; i >= 0; i--) {
				if (propertyData.name == itemLinksProcesses[i].dst && itemLinksProcesses[i].type == 'refinesObj')
					prHtml += '<a class="item-details-link" href="#' + identify(itemLinksProcesses[i].src) + '"">' + itemLinksProcesses[i].src + '</a><br>';
			};
			if (prHtml.length) {
				tHtml += '<dt class="processed">Collected in</dt><dd>' + prHtml + '</dd><br>';
				$('#charac-header').show();	
			}
			var impHtml = '';
			itemLinksProcesses.sort(compareValues('src','desc'));
			for (var i = itemLinksProcesses.length - 1; i >= 0; i--) {
				if (propertyData.name == itemLinksProcesses[i].dst && itemLinksProcesses[i].type == 'canImportObj')
					impHtml += '<a class="item-details-link" href="#' + identify(itemLinksProcesses[i].src) + '"">' + itemLinksProcesses[i].src + '</a><br>';
			};
			if (impHtml.length) {
				tHtml += '<dt class="worker">Imported by</dt><dd>' + impHtml + '</dd>';
				$('#charac-header').show();	
			}
			var expHtml = '';
			itemLinksProcesses.sort(compareValues('src','desc'));
			for (var i = itemLinksProcesses.length - 1; i >= 0; i--) {
				if (propertyData.name == itemLinksProcesses[i].dst && itemLinksProcesses[i].type == 'canExportObj')
					expHtml += '<a class="item-details-link" href="#' + identify(itemLinksProcesses[i].src) + '"">' + itemLinksProcesses[i].src + '</a><br>';
			};
			if (expHtml.length) {
				tHtml += '<dt class="worker">Exported by</dt><dd>' + expHtml + '</dd>';
				$('#charac-header').show();	
			}
		}
		/* deposits */
		if (propertyType == 'depProvides' && propertyData.depProvides) {
			tHtml += '<dt>Provides</dt><dd><a class="item-details-link" href="#' + identify(propertyData.depProvides) + '">' + propertyData.depProvides + '</a></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'depCapacity' && propertyData.depCapacity) {
			tHtml += '<dt>Capacity</dt><dd class="store">' + propertyData.depCapacity + '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'depSpreadRate' && propertyData.depSpreadRate) {
			tHtml += '<dt>Spread Rate</dt><dd class="generate">' + propertyData.depSpreadRate + '</dd>';
			$('#charac-header').show();
		}
		/* vehicles and pavements */
		if (propertyType == 'harvests' && propertyData.harvests) {
			tHtml += '<dt class="processed">Harvests</dt><dd class="harvest"><a class="item-details-link" href="#' + identify(propertyData.harvests) + '">' + propertyData.harvests + '</a></dd>';
			tHtml += '<dt>Capacity</dt><dd class="store">' + propertyData.capacity + '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'driveSpeedMod' && propertyData) {
			tHtml += '<dt>Vehicle Speed</dt><dd>' + propertyData+ '</dd>';
			$('#charac-header').show();
		}
		/* races civs and maps */
		if (propertyType == 'difficulty' && propertyData) {
			tHtml += '<dt>Difficulty: </dt><dd>' + propertyData+ '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'narcotics'  && propertyData) {
			if (propertyData[0])
			tHtml += '<dt>Narcotics</dt><dd>';
			for (var i = propertyData.length - 1; i >= 0; i--) {
				if (i != propertyData.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		/* --------------------------------------------------------------ici mettre le remplacement de playable civs for map */
		/* Links 2*/
		if (propertyType == 'links2' && propertyData) {
			// playable civs for race
			var pcHtml = '';
			for (var i = itemLinks2.length - 1; i >= 0; i--) {
				if (propertyData.name == itemLinks2[i].dst && 'race' == itemLinks2[i].type)
					pcHtml += '<a class="item-details-link" href="#' + identify(itemLinks2[i].src) + '"">' + itemLinks2[i].src + '</a><br>';
			};
			if (pcHtml.length) {
				tHtml += '<dt>Playable Civilizations</dt><dd>' + pcHtml + '</dd>';
				$('#charac-header').show();
			}
			// playable civs for maps
			var pwHtml = '';
			for (var i = itemLinks2.length - 1; i >= 0; i--) {
				if (propertyData.name == itemLinks2[i].dst && 'availablemaps' == itemLinks2[i].type)
					pwHtml += '<a class="item-details-link" href="#' + identify(itemLinks2[i].src) + '"">' + itemLinks2[i].src + '</a><br>';
			};
			if (pwHtml.length) {
				tHtml += '<dt>Playable with</dt><dd>' + pwHtml + '</dd>';
				$('#charac-header').show();
			}
		}
		if (propertyType == 'race' && propertyData) {
			tHtml += '<dt>Race</dt><dd><a class="item-details-link" href="#' + identify(propertyData) + '">' + propertyData + '</a></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'startingColonists' && propertyData) {
			tHtml += '<dt>Colonists on start: </dt><dd>' + propertyData+ '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'availableMaps'  && propertyData) {
			var list = propertyData.sort(function(a, b) { return b.localeCompare(a); });
			if (list[0])
			tHtml += '<dt>Available Maps</dt><dd>';
			for (var i = list.length - 1; i >= 0; i--) {
				if (i != list.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(list[i]) + '">' + list[i] + '</a>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'terrainFeatures'  && propertyData) {
			if (propertyData[0])
			tHtml += '<dt>Deposits on map</dt><dd>';
			for (var i = propertyData.length - 1; i >= 0; i--) {
				if (i != propertyData.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(propertyData[i].name) + '">' + propertyData[i].name + '</a>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'startingTechs' && propertyData) {
			tHtml += '<dt>Starting Technologies</dt><dd>'
			for (var i = propertyData.length - 1; i >= 0; i--) {
				if (i != propertyData.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'startingBuildings'  && propertyData) {
			if (propertyData[0])
			tHtml += '<dt>Starting Buildings</dt><dd>';
			for (var i = propertyData.length - 1; i >= 0; i--) {
				if (i != propertyData.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'startingBuilding' && propertyData) {
			tHtml += '<dt>Starting Building: </dt><dd><a class="item-details-link" href="#' + identify(propertyData) + '">' + propertyData + '</a></dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'startingVehicles'  && propertyData) {
			var list = propertyData.sort(function(a, b) { return b.localeCompare(a); });
			if (list[0])
			tHtml += '<dt>Starting Vehicles</dt><dd>';
			for (var i = list.length - 1; i >= 0; i--) {
				if (i != list.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(list[i]) + '">' + list[i] + '</a>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'refinesObj' && propertyData) {
			tHtml += '<dt class="processed">Resource';
			if (propertyData.length > 1)
				tHtml += 's';
			tHtml +=' collected (Refines)</dt><dd>';
			for (var i = 0; i < propertyData.length; i++) {
				if (i > 0)
					tHtml += ', ';
				tHtml += '<span class="processed"><a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a></span>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'canImportObj' && propertyData) {
			tHtml += '<dt class="processed">Can Import</dt><dd>';			
			for (var i = 0; i < propertyData.length; i++) {
				if (i > 0)
					tHtml += ', ';
				tHtml += '<span class="processed"><a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a></span>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		if (propertyType == 'canExportObj' && propertyData) {
			tHtml += '<dt class="processed">Can Export</dt><dd>';		
			for (var i = 0; i < propertyData.length; i++) {
				if (i > 0)
					tHtml += ', ';
				tHtml += '<span class="processed"><a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a></span>';
			};
			tHtml += '</dd>';
			$('#charac-header').show();
		}
		/* RESOURCE PRODUCED */
		if (propertyType == 'providesUtilityObj' && propertyData) {
			for (resource in propertyData)
				tHtml += '<dt>Max ' + resource + '</dt><dd class="store">+' + propertyData[resource] + '</dd>';
			$('#prod-header').show();
		}
		if (propertyType == 'generate' && propertyData.generates) {
			tHtml += '<dt><a class="item-details-link" href="#' + identify(propertyData.generates) + '">' + propertyData.generates + '</a></dt><dd class="generate">+' + propertyData.generateAmount + ' /round</dd>';
			tHtml += '<dt>Round duration</dt><dd>' + propertyData.generateTime + ' ticks</dd>';
			if (propertyData.requiresWorkers) {
				tHtml += '<dt>All Workers Round</dt><dd>' + (Math.round(propertyData.generateTime / propertyData.acceptsWorkers * 100) / 100) + ' ticks</dd>';
				tHtml += '<dt>Output All Workers</dt><dd class="generate">' + (Math.round(propertyData.generateAmount/(propertyData.generateTime / propertyData.acceptsWorkers) * 100000) / 100000) + ' /tick</dd>';
				tHtml += '<dt><i>or</i></dt><dd class="generate">' + (Math.round(propertyData.generateAmount/(propertyData.generateTime / propertyData.acceptsWorkers) * 120000000) / 100000) + ' /min</dd>';
				$('#generateorsmelt').show();
				
			} else {
				tHtml += '<dt>Output / Tick</dt><dd class="generate">' + (Math.round(propertyData.generateAmount/propertyData.generateTime * 100000) / 100000) + '</dd>';
				tHtml += '<dt>Output / Min</dt><dd class="generate">' + (Math.round(propertyData.generateAmount/propertyData.generateTime * 120000000) / 100000) + '</dd>';
			}
			$('#prod-header').show();
		}
		/* RESOURCE TRANSFORMED */
		if (propertyType == 'smeltssObj' && propertyData.smeltssObj) {
			tHtml += '';
			if (propertyData.smeltsIn) {
				for (var i = 0; i < propertyData.smeltsIn.length; i++) {
					if (i>0) 
						tHtml += '<dt>& <a class="item-details-link" href="#' + identify(propertyData.smeltsIn[i]) + '">' + propertyData.smeltsIn[i] + '</a></dt><dd class="consume">1</dd>';
					else 
						tHtml += '<dt>Smelt <a class="item-details-link" href="#' + identify(propertyData.smeltsIn[i]) + '">' + propertyData.smeltsIn[i] + '</a></dt><dd class="consume">1</dd>';
				}
			}
			if (propertyData.smeltsOut) {
				for (var i = 0; i < propertyData.smeltsOut.length; i++) {
					if (i>0) 
						tHtml += '<dt>(or) <a class="item-details-link" href="#' + identify(propertyData.smeltsOut[i]) + '">' + propertyData.smeltsOut[i] + '</a></dt><dd class="generate">' + propertyData.smeltssObj.ratio + ' /round</dd>';
					else 
						tHtml += '<dt>Into <a class="item-details-link" href="#' + identify(propertyData.smeltsOut[i]) + '">' + propertyData.smeltsOut[i] + '</a></dt><dd class="generate">' + propertyData.smeltssObj.ratio + ' /round</dd>';
				}
			}
			tHtml += '<dt>Round duration</dt><dd>' + propertyData.smeltssObj.time + ' ticks</dd>';
			if (propertyData.requiresWorkers) {
				tHtml += '<dt>All Workers Round</dt><dd>' + (Math.round(propertyData.smeltssObj.time / propertyData.acceptsWorkers * 100) / 100) + ' ticks</dd>';
				tHtml += '<dt>Output All Workers</dt><dd class="generate">' + (Math.round(propertyData.smeltssObj.ratio/(propertyData.smeltssObj.time / propertyData.acceptsWorkers) * 100000) / 100000) + ' /tick</dd>';
				tHtml += '<dt><i>or</i></dt><dd class="generate">' + (Math.round(propertyData.smeltssObj.ratio/(propertyData.smeltssObj.time / propertyData.acceptsWorkers) * 120000000) / 100000) + ' /min</dd>';
				$('#generateorsmelt').show();
			} else {
				tHtml += '<dt>Output / Tick </dt><dd class="generate">' + (Math.round(propertyData.smeltssObj.ratio/propertyData.smeltssObj.time * 100000) / 100000) + '</dd>';
				tHtml += '<dt>Output / Min </dt><dd class="generate">' + (Math.round(propertyData.smeltssObj.ratio/propertyData.smeltssObj.time * 120000000) / 100000) + '</dd>';
			}
			$('#transf-header').show();
		}
		/* UTILITIES TO OPERATE */
		if (propertyType == 'requiresUtilityObj' && typeof(propertyData) !== 'undefined') {
			for (resource in propertyData)
				tHtml += '<dt>' + resource + '</dt><dd class="consume">-' + propertyData[resource] + '</dd>';
			$('#utility-header').show();
		}
		if (propertyType == 'requiresFuelObj' && typeof(propertyData) !== 'undefined') {
			var resource =  propertyData.resource.split(",");
			for (var i = 0; i < resource.length; i++) {
				if (i>0) 
					tHtml += '<dt>& <a class="item-details-link" href="#' + identify(resource[i]) + '">' + resource[i] + '</a></dt><dd class="consume">-1 /round</dd>';
				else 
					tHtml += '<dt><a class="item-details-link" href="#' + identify(resource[i]) + '">' + resource[i] + '</a></dt><dd class="consume">-1 /round</dd>';		
			}
			tHtml += '<dt>Round duration</dt><dd>' + propertyData.rate + ' ticks</dd>';
			tHtml += '<dt>Fuel input</dt><dd class="consume">' + (Math.round(-1/propertyData.rate * 100000) / 100000) + ' /tick</dd>'
			tHtml += '<dt><i>or</i></dt><dd class="consume">' + (Math.round(-1/propertyData.rate * 120000000) / 100000) + ' /min</dd>'
			$('#utility-header').show();
		}
		/* REQUIREMENTS*/
		if (propertyType == 'requiresStage' && propertyData.raw != 99) {
			tHtml += '<dt>' + propertyData.display + '</dt><dd>' + propertyData.amount + ' Atmosphere</dd>';
			/*tHtml += '<dt>' + propertyData.display + '</dt><dd>' + (stages[propertyData.raw] != undefined ? stages[propertyData.raw] + ' Atmosphere' : '') + '</dd>';*/
			$('#require-header').show();
		}
		if (propertyType == 'reqIndependence') {
			tHtml += '<dt>Independence</dt><dd>' + (propertyData == false ? ' Not required</dd>' : ' Required</dd>');
			$('#require-header').show();
		}
		if (propertyType == 'requiresTech' && propertyData) {
			tHtml += '<dt>Technologies required</dt><dd>'
			for (var i = propertyData.length - 1; i >= 0; i--) {
				if (i != propertyData.length - 1)
					tHtml += '<br>';
				if (propertyData[i].includes('|')) {
					var tmpreq = propertyData[i].split("|");
						for (var j = tmpreq.length - 1; j >= 0; j--) {
							if (j != tmpreq.length - 1)
								tHtml += ' or ';
							tHtml += '<a class="item-details-link" href="#' + identify(tmpreq[j]) + '">' + tmpreq[j] + '</a>';
						}
				}
				else
				tHtml += '<a class="item-details-link" href="#' + identify(propertyData[i]) + '">' + propertyData[i] + '</a>';
			};
			tHtml += '</dd>';
			$('#require-header').show();
		}
		if (propertyType == 'cibt') {
			tHtml += '<dt>Can I build this?</dt><dd href="javascript:void()" class="item-details-link" onclick="javascript:open_cibt();" style="color: #a0ccd3;cursor: pointer;">Check now</dd>';
			$('#require-header').show();
		}
		/* COSTS AND SELL */
		if (propertyType == 'cost' && propertyData) {
			for (resource in propertyData) {
				tHtml += '<dt><a class="item-details-link" href="#' + identify(resource) + '">' + resource + '</a></dt><dd class="consume">-' + propertyData[resource] + '</dd>';
				$('#cost-header').show();
			}
		}
		if (propertyType == 'sellValue' && propertyData) {
			for (resource in propertyData) {
				tHtml += '<dt><a class="item-details-link" href="#' + identify(resource) + '">' + resource + '</a></dt><dd class="generate">' + propertyData[resource] + '</dd>';
				$('#sell-header').show();
			}
		}
		/* LINKS */
		if (propertyType == 'links' && propertyData) {
			// built by
			var bfHtml = '';
			for (var i = itemLinks.length - 1; i >= 0; i--)
				if (propertyData.name == itemLinks[i].dst && 'canBuild' == itemLinks[i].type)
					bfHtml += '<a class="item-details-link" href="#' + identify(itemLinks[i].src) + '"">' + itemLinks[i].src + '</a><br>';
			if (bfHtml.length) {
				tHtml += '<dt>Built by</dt><dd>' + bfHtml + '</dd>';
				$('#links-header').show();
			}
			// upgrade from
			var upfHtml = '';
			for (var i = itemLinks.length - 1; i >= 0; i--)
				if (propertyData.name == itemLinks[i].dst && 'upgradeTo' == itemLinks[i].type)
					upfHtml += '<a class="item-details-link" href="#' + identify(itemLinks[i].src) + '"">' + itemLinks[i].src + '</a><br>';
			if (upfHtml.length) {
				tHtml += '<dt>Upgrade from</dt><dd>' + upfHtml + '</dd>';		
				$('#links-header').show();
			}
			// upgrade to
			for (var i = itemLinks.length - 1; i >= 0; i--)
				if (propertyData.name == itemLinks[i].src && 'upgradeTo' == itemLinks[i].type) {
					tHtml += '<dt>Upgrade to</dt><dd><a class="item-details-link" href="#' + identify(itemLinks[i].dst) + '"">' + itemLinks[i].dst + '</a></dd>';
					$('#links-header').show();
				}
			// needed for
			var nfHtml = '';
			itemLinks.sort(compareValues('dst','desc'));
			for (var i = itemLinks.length - 1; i >= 0; i--)
				if (propertyData.name == itemLinks[i].src && 'neededFor' == itemLinks[i].type)
					nfHtml += '<a class="item-details-link" href="#' + identify(itemLinks[i].dst) + '"">' + itemLinks[i].dst + '</a><br>';
			if (nfHtml.length) {
				tHtml += '<dt>Needed for</dt><dd>' + nfHtml + '</dd>';
				$('#links-header').show();
			}
		}
		/* Can build */
		if (propertyType == 'producesObj' && propertyData) {
			tHtml += '<dt>Can build</dt><dd>';
			var list = propertyData.sort(function(a, b) { return b.localeCompare(a); });
			for (var i = list.length - 1; i >= 0; i--) {
				if (i != list.length - 1)
					tHtml += '<br>';
				tHtml += '<a class="item-details-link" href="#' + identify(list[i]) + '">' + list[i] + '</a>';
			};
			tHtml += '</dd>';
				$('#links-header').show();
		}
		/* Produced by and consumed by with ratios */
		if ((propertyType == 'RatioTable') && (propertyData.type == 'resource')) {
			var rtpHtml = '';
			var rtmHtml = '';
			for (var i = items.length - 1; i >= 0; i--) {
				if (items[i].type == 'building') {
					if ((items[i].RatioTable[propertyData.name]) && (items[i].RatioTable[propertyData.name] > 0))
						rtpHtml += '<a class="item-details-link" href="#' + identify(items[i].name) + '"">' + items[i].name + '</a><i class="generate"> ' + parseFloat((items[i].RatioTable[propertyData.name])*1200).toFixed(2) + ' /min</i><br>';
					if ((items[i].RatioTable[propertyData.name]) && (items[i].RatioTable[propertyData.name] < 0))
						rtmHtml += '<a class="item-details-link" href="#' + identify(items[i].name) + '"">' + items[i].name + '</a><i class="consume"> ' + parseFloat((items[i].RatioTable[propertyData.name])*1200).toFixed(2) + ' /min</i><br>';
				}
			};
			if (rtpHtml.length) {
				tHtml += '<dt class="generate">Produced by</dt><dd>' + rtpHtml + '</dd><br>';
				$('#links-header').show();
			}
			if (rtmHtml.length) {
				tHtml += '<dt class="consume">Consumed by</dt><dd>' + rtmHtml + '</dd>';
				$('#links-header').show();
			}
		}
		/* End of the property */
		if (tHtml.length == 0)
			return tHtml;
		if (orientation == 'vertical')
			tHtml = '<dl class="item-property">' + tHtml;
		else
			tHtml = '<dl class="dl-horizontal item-property">' + tHtml;
		tHtml += '</dl>';
		return tHtml;
	}
/* ------------------------display formatting (end)--------------------------- */


/* ------------------------display printing (start)--------------------------- */
	var printDescription = function (className) {
		var className = className || 'unknown';
		for (var i = items.length - 1; i >= 0; i--) {
			if (className == items[i].className) {
				console.log('found item', items[i]);
				window._current_item = items[i];
				var descData = items[i];
				var myElement = document.querySelector(".icon");
				if (descData.tileIconWidth) {
					var tmpImg = new Image();
					tmpImg.src = imageFolder + descData.image;
					var iconheight = tmpImg.height;
					var newratio = 64 / iconheight;
					var newwidth = (descData.tileIconWidth * newratio);					
										
					myElement.style.width = '' + newwidth + 'px';
					myElement.style.overflow = 'hidden';
				}
				else {
					myElement.style.height = 'auto';
					myElement.style.width = 'auto';
					myElement.style.overflow = 'initial';					
				}
				
				$('#item-image').attr('src', imageFolder + descData.image);
				
				var thisName = descData.name + '&nbsp; <small class="note">';
				if (descData.requiPremium == true)
					thisName += '<span class="premium">Premium</span> ';
				thisName += descData.type + '</small>'
				$('#item-name').html(thisName);
				$('#item-descriptionstring .item-properties').html(formatProperty('description', descData.description));
				/* CARACTERISTICS */
				/* buildings */
				if (descData.type == 'building' || descData.type == 'pavement') {
					$('#item-charac-tilesize .item-properties').html(formatProperty('tilesize', descData, 'h'));
				}
				$('#item-charac-releaseversion .item-properties').html(formatProperty('releaseversion', descData.releaseVersion, 'h'));
				$('#item-charac-buildlimit .item-properties').html(formatProperty('buildLimit', descData.buildLimit));
				$('#item-charac-consulate .item-properties').html(formatProperty('isConsulate', descData.isConsulate));
				$('#item-charac-capitol .item-properties').html(formatProperty('isCapitol', descData.isCapitol));
				$('#item-charac-embassy .item-properties').html(formatProperty('isEmbassy', descData.isEmbassy));
				$('#item-charac-tradedepot .item-properties').html(formatProperty('onlineTradeDepot', descData.onlineTradeDepot));
				$('#item-charac-comshub .item-properties').html(formatProperty('isCommsHubBldg', descData.isCommsHubBldg));
				if (descData.type == 'building') {
					$('#item-charac-workers .item-properties').html(formatProperty('acceptsWorkers', descData, 'h'));
					try{
						$('#item-requirements-cibt .item-properties').html(formatProperty('cibt', {}));
					} catch (e) {
						//do nothing
					}
				}
				$('#item-charac-provideshelter .item-properties').html(formatProperty('providesShelter', descData.providesShelter, 'h'));
				$('#item-charac-canheal .item-properties').html(formatProperty('heals', descData.heals));
				$('#item-charac-requiresiq .item-properties').html(formatProperty('requiresIQ', descData.requiresIQ));
				$('#item-charac-educates .item-properties').html(formatProperty('educates', descData.educates));
				$('#item-charac-providesiq .item-properties').html(formatProperty('providesIQ', descData.providesIQ));
				$('#item-charac-entertain .item-properties').html(formatProperty('entertains', descData, 'h'));
				$('#item-charac-entertain .item-properties').html(formatProperty('takesTourists', descData, 'h'));
				$('#item-charac-storage .item-properties').html(formatProperty('storesObj', descData.storesObj, 'h'));
				$('#item-charac-tax .item-properties').html(formatProperty('earthTaxValue', descData.earthTaxValue, 'h'));;
				/* resources */
				$('#item-charac-resourceLimited .item-properties').html(formatProperty('resourceLimited', descData, 'h'));
				$('#item-charac-resourcebasePrice .item-properties').html(formatProperty('resourcebasePrice', descData, 'h'));
				$('#item-charac-resourcetoxicRate .item-properties').html(formatProperty('resourcetoxicRate', descData, 'h'));
				$('#item-charac-harvestedby .item-properties').html(formatProperty('LinksHarvest', descData));
				if (descData.type == 'resource') {
					$('#item-charac-storedbylist .item-properties').html(formatProperty('storedbylist', descData));
					$('#item-charac-proceesedlists .item-properties').html(formatProperty('LinksProcesses', descData));
				}
				/* deposits */
				$('#item-depprovides .item-properties').html(formatProperty('depProvides', descData, 'h'))
				$('#item-depcapacity .item-properties').html(formatProperty('depCapacity', descData, 'h'));
				$('#item-depspreadrate .item-properties').html(formatProperty('depSpreadRate', descData, 'h'));
				/* vehicles and pavements */
				$('#item-charac-harvestkappa .item-properties').html(formatProperty('harvests', descData, 'h'));
				$('#item-charac-drivespeed .item-properties').html(formatProperty('driveSpeedMod', descData.driveSpeedMod, 'h'));
				/* races civs and maps */
				$('#item-charac-difficulty .item-properties').html(formatProperty('difficulty', descData.difficulty));
				$('#item-charac-narcotics .item-properties').html(formatProperty('narcotics', descData.narcotics));
				//* --------------------------------------------------------------ici mettre le remplacement de playable civs for map */
				$('#item-charac-links2 .item-properties').html(formatProperty('links2', descData));
				$('#item-charac-race .item-properties').html(formatProperty('race', descData.race));
				$('#item-charac-startingcolonists .item-properties').html(formatProperty('startingColonists', descData.startingColonists));
				$('#item-charac-availablemaps .item-properties').html(formatProperty('availableMaps', descData.availableMaps));
				$('#item-charac-startingdeposits .item-properties').html(formatProperty('terrainFeatures', descData.terrainFeatures));
				$('#item-charac-startingtechs .item-properties').html(formatProperty('startingTechs', descData.startingTechs));
				$('#item-charac-startingbuildings .item-properties').html(formatProperty('startingBuildings', descData.startingBuildings));
				$('#item-charac-startingbuilding .item-properties').html(formatProperty('startingBuilding', descData.startingBuilding));
				$('#item-charac-startingvehicles .item-properties').html(formatProperty('startingVehicles', descData.startingVehicles));
				/* RESOURCE COLLECTED */
				$('#item-prod-refines .item-properties').html(formatProperty('refinesObj', descData.refinesObj));
				$('#item-prod-imports .item-properties').html(formatProperty('canImportObj', descData.canImportObj));
				$('#item-prod-exports .item-properties').html(formatProperty('canExportObj', descData.canExportObj));
				/* RESOURCE PRODUCED */
				$('#item-prod-provideutility .item-properties').html(formatProperty('providesUtilityObj', descData.providesUtilityObj, 'h'));
				$('#item-prod-generate .item-properties').html(formatProperty('generate', descData, 'h'));
				/* RESOURCE TRANSFORMED */
				$('#item-prod-smelt .item-properties').html(formatProperty('smeltssObj', descData, 'h'));
				/* UTILITIES TO OPERATE */
				$('#item-prod-requtility .item-properties').html(formatProperty('requiresUtilityObj', descData.requiresUtilityObj, 'h'));
				$('#item-prod-reqfuel .item-properties').html(formatProperty('requiresFuelObj', descData.requiresFuelObj, 'h'));
				/* REQUIREMENTS*/
				$('#item-requirements-stage .item-properties').html(formatProperty('requiresStage', descData.requiresStage));
				$('#item-requirements-independence .item-properties').html(formatProperty('reqIndependence', descData.reqIndependence));
				$('#item-requirements-tech .item-properties').html(formatProperty('requiresTech', descData.requiresTech));
				/* COSTS AND SELL */
				$('#item-requirements-cost .item-properties').html(formatProperty('cost', descData.cost, 'h'));
				$('#item-requirements-sell .item-properties').html(formatProperty('sellValue', descData.sellValue, 'h'));
				/* LINKS */
				$('#item-links-links .item-properties').html(formatProperty('links', descData));
				$('#item-links-canbuild .item-properties').html(formatProperty('producesObj', descData.producesObj));
				if (descData.type == 'resource') {
					$('#item-linksratio .item-properties').html(formatProperty('RatioTable', descData));
				}
			}
		};
	}
/* ------------------------display printing (end)--------------------------- */
