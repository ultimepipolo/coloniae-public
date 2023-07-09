
	var items = [];
	var itemscost = [];
	var itemstechs = [];
	var itemsratio = [];
	var itemsstore = [];	
	var itemSmallInfo = [];
	var itemLinks = [];
	var itemLinks2 = [];
	var itemLinksProcesses = [];

/* ------------------------small functions--------------------------- */	
var identify = function(name) {
		return name.replace(/\s+/g, '');
	};	
var resPerTile = function(tilesize, resource) {
		if (tilesize && tilesize > 1) {
		return ' <span class="amount-per-tile">(' + Math.round(resource/tilesize * 100) / 100 + '/t)</span>';
		}
		return '';
	};
function addLink(src, dst, type, srctype, dsttype) {
		for (var i = 0; i < itemLinks.length; i++) {
			if (itemLinks[i].src == src && itemLinks[i].dst == dst && itemLinks[i].type == type)
				return;
		};
		itemLinks.push({src: src, dst: dst, type:type, srctype:srctype, dsttype:dsttype});
	}	
function addLink2(src, dst, type, srctype, dsttype) {
		for (var i = 0; i < itemLinks2.length; i++) {
			if (itemLinks2[i].src == src && itemLinks2[i].dst == dst && itemLinks2[i].type == type)
				return;
		};
		itemLinks2.push({src: src, dst: dst, type:type, srctype:srctype, dsttype:dsttype});
	}	
function addLinksHarvest(src, dst, type, srctype, dsttype) {
		for (var i = 0; i < itemLinksHarvest.length; i++) {
			if (itemLinksHarvest[i].src == src && itemLinksHarvest[i].dst == dst && itemLinksHarvest[i].type == type)
				return;
		};
		itemLinksHarvest.push({src: src, dst: dst, type:type, srctype:srctype, dsttype:dsttype});
	}	
function addLinksProcesses(src, dst, type, srctype, dsttype) {
		for (var i = 0; i < itemLinksProcesses.length; i++) {
			if (itemLinksProcesses[i].src == src && itemLinksProcesses[i].dst == dst && itemLinksProcesses[i].type == type)
				return;
		};
		itemLinksProcesses.push({src: src, dst: dst, type:type, srctype:srctype, dsttype:dsttype});
	}	
	
function calcTrueGenRate(colgenrate, touristdoorway, stargate, workers, name) {
    if (!colgenrate) { return 0; }
     var round_duration = colgenrate/2;
     if (workers>0 && (name=="Advanced Cloning Facility" || name=="Cloning Facility")) {
       round_duration = round_duration/workers;
     }
     var colonists_per_round = 1;
     if (touristdoorway) {
       colonists_per_round = 5; // random between 1 and 10
     }
     if (stargate) {
       colonists_per_round = 9; // random bewteen 1 and 18
     }
     return colonists_per_round/round_duration;
}
	
/* ------------------------function add item to list (start)--------------------------- */
	var addDataToList = function (typeName, typeData) {
		var itemData = {
			value: identify(typeData.name),
			label: typeData.name,
			desc: 'Stage ' + typeData.requiresStage + ' - ' + typeName,
			type: typeName,
			color: typeData.transModeColor ? typeData.transModeColor : '#000000'
		};
		if (typeName == 'building') {
			if (itemData.passable == true) {
				itemData.type = 'pavement';
				itemData.desc = 'Stage ' + typeData.requiresStage + ' - pavement';
			}
			if (itemData.color == '#000000') {
				itemData.color = '#c0392b';
			}
			itemData.desc += ' (' + typeData.tileWidth + 'x' + typeData.tileHeight + ')' ;
			var tmpCat = typeData.buildCategories.slice();
			if (tmpCat[0] == 'All Buildings') {
				tmpCat.shift()
			}
			tmpCat.toString();
			itemData.desc += ' - ' + tmpCat;
		} else if (typeName == 'Human Vehicle') {
			itemData.desc += '';
		} else if (typeName == 'Zolarg Worker') {
			itemData.desc += '';
		} else if (typeName == 'Technology') {
			if (itemData.color == '#000000') {
				itemData.color = '#9b59b6';
				itemData.desc += '';
			}
		}else if (typeName == 'Resource') {
			if (itemData.color == '#000000') {
				itemData.color = '#7dedd5';
				itemData.desc += '';
			}
		} else {
			itemData.desc += ' unknown type';
		}
		itemSmallInfo.push(itemData);
	}

	
/* ------------------------function add item internally (start)--------------------------- */
	var addItem = function (itemData, type) {
		var itemData = itemData || {error: true};
		var type     = type || 'unknown';
		var tmpItem  = {
			name: itemData.name,
			className: identify(itemData.name),
			type: type,
			subtype: [],
			cost: {},
			image: '',
			tileWidth: -1,
			tileHeight: -1,
			tileSize: -1,
			requiresStage: {
				display: '-1',
				raw: -1
			},
			requiresTech: null,
			reqIndependence: false,
			buildCategoriesObj: null,
			tabledisplay: true
		};
		if (type == 'building') {
			if (itemData.buildCategories)
				tmpItem['buildCategoriesObj']   = itemData.buildCategories;
			/*if (itemData.transModeColor) {
				tmpItem['transModeColor']       = itemData.transModeColor;
			} else {
				tmpItem['transModeColor']       = '#c0392b';
			}*/
			if (itemData.passable == true) {
			/* Pavement */
				tmpItem.type                 = 'pavement';
				tmpItem['transModeColor']       = '#f2c0c0';
				tmpItem['driveSpeedMod']        = itemData.driveSpeedMod;
			/* End Pavement */
			} else {
			/* Building */
				tmpItem['transModeColor']       = '#a42d2e';
				tmpItem.RatioTable = {};
				tmpItem.rationable = false;
				if (itemData.stores) {
					tmpItem.subtype.push('storage');
					tmpItem['storesObj']          = {};
					for (var i = itemData.stores.length - 1; i >= 0; i--)
						tmpItem.storesObj[itemData.stores[i].resource] = itemData.stores[i].amount;
				}
				if (itemData.generates) {
					tmpItem['generates']          = itemData.generates;
					tmpItem['generateTime']       = itemData.generateTime;
					tmpItem['generateAmount']     = itemData.generateAmount;
					tmpItem.rationable = true;
					if (itemData.requiresWorkers || itemData.acceptsWorkers>0)
						var tmpratio = (Math.round(tmpItem.generateAmount/(tmpItem.generateTime / itemData.acceptsWorkers) * 100000) / 100000) ;
					else
						var tmpratio = (Math.round(tmpItem.generateAmount/tmpItem.generateTime * 100000) / 100000) ;
					if (tmpItem.RatioTable[tmpItem.generates]) {
						var oldratio = tmpItem.RatioTable[tmpItem.generates];
						tmpItem.RatioTable[tmpItem.generates] = oldratio + tmpratio;
					}
					else
						tmpItem.RatioTable[tmpItem.generates] =  tmpratio;
				}
				if (itemData.smelts) {
					tmpItem['smeltssObj']         = itemData.smelts;
					tmpItem.rationable = true;
					if (itemData.smelts.input) {
						tmpItem['smeltsIn'] = itemData.smelts.input.split(",");
						for (var i = tmpItem.smeltsIn.length - 1; i >= 0; i--) {
							if (itemData.requiresWorkers || itemData.acceptsWorkers>0)
								var tmpratio = (Math.round(-1/(tmpItem.smeltssObj.time / itemData.acceptsWorkers) * 100000) / 100000) ;
							else
								var tmpratio = (Math.round(-1/tmpItem.smeltssObj.time * 100000) / 100000) ;
							if (tmpItem.RatioTable[tmpItem.smeltsIn[i]]) {
								var oldratio = tmpItem.RatioTable[tmpItem.smeltsIn[i]];
								tmpItem.RatioTable[tmpItem.smeltsIn[i]] = oldratio + tmpratio;
							}
							else
								tmpItem.RatioTable[tmpItem.smeltsIn[i]] =  tmpratio;
						}	
					}
					if (itemData.smelts.output) {
						tmpItem['smeltsOut'] = itemData.smelts.output.split("|");
            var multiple = tmpItem.smeltsOut.length;
						for (var i = tmpItem.smeltsOut.length - 1; i >= 0; i--) {
							if (itemData.requiresWorkers || itemData.acceptsWorkers>0){
								var tmpratio = (Math.round(tmpItem.smeltssObj.ratio/(tmpItem.smeltssObj.time / itemData.acceptsWorkers) * 100000) / 100000) ;
							} else {
								var tmpratio = (Math.round(tmpItem.smeltssObj.ratio/tmpItem.smeltssObj.time * 100000) / 100000) ;
              }
              if (multiple>1) {
                tmpratio =  tmpratio/multiple;
              }
							if (tmpItem.RatioTable[tmpItem.smeltsOut[i]]) {
								var oldratio = tmpItem.RatioTable[tmpItem.smeltsOut[i]];
								tmpItem.RatioTable[tmpItem.smeltsOut[i]] = oldratio + tmpratio;
							} else {
								tmpItem.RatioTable[tmpItem.smeltsOut[i]] =  tmpratio;
              }
						}
          }
				}
				if (itemData.refines) {
					tmpItem['refinesObj']            = [];
					for (var i = itemData.refines.length - 1; i >= 0; i--)
						tmpItem.refinesObj.push(itemData.refines[i].output);
					tmpItem.refinesObj.sort(function(a, b) { return a.localeCompare(b); });
				}
				if (itemData.providesUtility) {
					tmpItem['providesUtilityObj'] = {};
					for (var i = itemData.providesUtility.length - 1; i >= 0; i--)
						tmpItem.providesUtilityObj[itemData.providesUtility[i].utility] = itemData.providesUtility[i].amount;
				}
				if (itemData.providesShelter)
					tmpItem['providesShelter']    = itemData.providesShelter;
				if (itemData.entertains) {
					tmpItem['entertains']         = itemData.entertains;
					tmpItem['entertainmentCost']  = itemData.entertainmentCost;
				}
				if (itemData.takesTourists) {
					tmpItem['takesTourists']      = itemData.takesTourists;
					tmpItem['entertainmentCost']  = itemData.entertainmentCost;
				}
				if (itemData.produces) {
          tmpItem.rationable = true;
					tmpItem['producesObj']        = itemData.produces;
        }
				if (itemData.requiresUtility) {
					tmpItem['requiresUtilityObj'] = {};
					for (var i = itemData.requiresUtility.length - 1; i >= 0; i--)
						tmpItem.requiresUtilityObj[itemData.requiresUtility[i].utility] = itemData.requiresUtility[i].amount;
				}
				if (itemData.requiresFuel) {
					tmpItem['requiresFuelObj']    = itemData.requiresFuel;
					tmpItem['fuelNeeded']		= itemData.requiresFuel.resource.split(",");
					tmpItem.rationable = true;
					for (var i = tmpItem.fuelNeeded.length - 1; i >= 0; i--) {
						var tmpratio = (Math.round(-1/tmpItem.requiresFuelObj.rate * 100000) / 100000) ;
						if (tmpItem.RatioTable[tmpItem.fuelNeeded[i]]) {
							var oldratio = tmpItem.RatioTable[tmpItem.fuelNeeded[i]];
							tmpItem.RatioTable[tmpItem.fuelNeeded[i]] = oldratio + tmpratio;
						}
						else
							tmpItem.RatioTable[tmpItem.fuelNeeded[i]] =  tmpratio;
					}	
				}
				if (itemData.acceptsWorkers) {
					tmpItem['acceptsWorkers']     = itemData.acceptsWorkers;
					if (itemData.occupation) {
						tmpItem['occupation']         = itemData.occupation;
					}
					else { tmpItem['occupation']    = 'Unskilled';
					}
				}
				if (itemData.buildLimit > 0)
					tmpItem['buildLimit']         = itemData.buildLimit;
				if (itemData.canImport)
					tmpItem['canImportObj']       = itemData.canImport.sort(function(a, b) { return a.localeCompare(b); });
				if (itemData.canExport)
					tmpItem['canExportObj']       = itemData.canExport.sort(function(a, b) { return a.localeCompare(b); });
				if (itemData.isConsulate == true)
					tmpItem.isConsulate      = itemData.isConsulate;
				if (itemData.isCapitol == true)
					tmpItem.isCapitol       = itemData.isCapitol;
				if (itemData.isEmbassy == true)
					tmpItem.isEmbassy      = itemData.isEmbassy;
				if (itemData.onlineTradeDepot == true)
					tmpItem.onlineTradeDepot       = itemData.onlineTradeDepot;
				if (itemData.isCommsHubBldg == true)
					tmpItem.isCommsHubBldg       = itemData.isCommsHubBldg;
				if (itemData.heals != '0')
					tmpItem.heals       = itemData.heals;
				if (itemData.requiresIQ != '0')
					tmpItem.requiresIQ       = itemData.requiresIQ;
				if (itemData.educates != '0')
					tmpItem.educates       = itemData.educates;
				if (itemData.providesIQ != '0')
					tmpItem.providesIQ       = itemData.providesIQ;
        if (itemData.requiresWorkers || itemData.acceptsWorkers>0) {
				  tmpItem['requiresWorkers']    = true;
        }
				tmpItem['giftCapacity']    = itemData.giftCapacity;
				tmpItem['colgen']    = calcTrueGenRate(itemData.colGenRate, itemData.touristDoorway, itemData.isStargate, itemData.acceptsWorkers, itemData.name);
        tmpItem['colGenRate'] = itemData.colGenRate;
        tmpItem['touristDoorway'] = itemData.touristDoorway;
        tmpItem['isStargate'] = itemData.isStargate;
			/* End Building */
			}
			if (itemData.sellValue) {
				tmpItem['sellValue']           = {};
				for (var i = itemData.sellValue.length - 1; i >= 0; i--)
					tmpItem.sellValue[itemData.sellValue[i].resource] = itemData.sellValue[i].amount;
			}
			tmpItem.tileWidth                = itemData.tileWidth;
			tmpItem.tileHeight               = itemData.tileHeight;
			tmpItem.tileSize                 = itemData.tileWidth * itemData.tileHeight;
			tmpItem['earthTaxValue']         = itemData.earthTaxValue;
			tmpItem.image                    = itemData.tile;
			tmpItem.tileIconWidth 			 = null;
			tmpItem.depCapacity			= null;
			tmpItem.depSpreadRate		= null;
			tmpItem.depProvides		= null;
		} else if (type == 'vehicle') {
			tmpItem.image                    = itemData.indicator;
			tmpItem['producesObj']           = itemData.produces;
			if (itemData.buildCategories)
				tmpItem['buildCategoriesObj']   = itemData.buildCategories;
				var tmpCat2 = itemData.buildCategories.slice();
				if (tmpCat2[0] == 'All Vehicles') {
					tmpItem.type = 'Human Vehicle';
					tmpItem['transModeColor']       = '#b4b4b4';
				}
				else if (tmpCat2[0] == 'All Workers') {
					tmpItem.type = 'Zolarg Worker';
					tmpItem['transModeColor']       = '#777777';
				}
			if (itemData.sellValue) {
				tmpItem['sellValue']           = {};
				for (var i = itemData.sellValue.length - 1; i >= 0; i--)
					tmpItem.sellValue[itemData.sellValue[i].resource] = itemData.sellValue[i].amount;
			}
			tmpItem['harvests']              = itemData.harvests;
			tmpItem['capacity']              = itemData.capacity;			
		} else if (type == 'technology') {
			tmpItem['transModeColor']        = '#ab69c6';
			tmpItem.image                    = itemData.icon;
			/* temp wart for one icon */
				if (tmpItem.name == 'Ultra Deep Excavation')
					tmpItem.tileIconWidth = 320;
		} else if (type == 'map') {
			tmpItem['transModeColor']           = '#75bc6c';
			tmpItem.image                       = itemData.icon;
			tmpItem.terrainFeatures			    = itemData.terrainFeatures.sort(compareValues('name','desc'));
			tmpItem.difficulty				    = itemData.difficulty;
			tmpItem.startingTechs				= itemData.startingTechs;
			tmpItem.startingResourceModifiers	= itemData.startingResourceModifiers;
			tmpItem.startingBuildings			= itemData.startingBuildings;
		} else if (type == 'race') {
			tmpItem['transModeColor']        = '#303891';
			tmpItem.image                    = itemData.defaultSprites[0];
			tmpItem.startingTechs			 = itemData.startingTechs;
			tmpItem.narcotics				 = itemData.narcotics;
		} else if (type == 'civilization') {
			tmpItem['transModeColor']        = '#f6af31';
			tmpItem.image                    = itemData.icon;	
			tmpItem.race                     = itemData.race;
			tmpItem.startingColonists        = itemData.startingColonists;	
			tmpItem.startingBuilding         = itemData.startingBuilding;	
			tmpItem.startingVehicles         = itemData.startingVehicles;	
			tmpItem.startingTechs            = itemData.startingTechs;	
			tmpItem.availableMaps            = itemData.availableMaps;					
		} else if (type == 'tile') {
			tmpItem['transModeColor']        = '#ab69c6';
			tmpItem.image                    = itemData.image;
			tmpItem.tileIconWidth 			 = itemData.tileWidth;	
			tmpItem.tabledisplay					 = false;	
			for (var i = items.length - 1; i >= 0; i--) {
				if (items[i].image == tmpItem.name) {
					items[i].image = tmpItem.image;
					items[i].tileIconWidth = tmpItem.tileIconWidth;
				}				
			}
		} else if (type == 'deposit') {
			tmpItem['transModeColor']        = '#856d3d';
			tmpItem.image                    = itemData.tile;
			tmpItem.tabledisplay					 = true;
			tmpItem.depCapacity			= itemData.capacity;
			tmpItem.depSpreadRate		= itemData.spreadRate;
			tmpItem.depProvides			= itemData.provides;
			for (var i = items.length - 1; i >= 0; i--) {
				if (items[i].name == tmpItem.name) {
					items[i].depProvides = tmpItem.depProvides;
					items[i].depCapacity = tmpItem.depCapacity;
					items[i].depSpreadRate = tmpItem.depSpreadRate;
					tmpItem.tabledisplay  = false;
				}				
			}
		/* temporary special treatment for Crystalline deposit
			if (tmpItem.name == 'Synthetic Crystalline Deposit') {
				for (var i = items.length - 1; i >= 0; i--) {
					if (items[i].name == 'Synthetic Crystalline') {
						items[i].depProvides = tmpItem.depProvides;
						items[i].depCapacity = tmpItem.depCapacity;
						items[i].depSpreadRate = tmpItem.depSpreadRate;
						tmpItem.tabledisplay  = false;
					}				
				}
			} */
		} else if (type == 'resource') {
			tmpItem['transModeColor']        = '#7dedd5';
			tmpItem.resourcecolor   	 = itemData.color;
			tmpItem.image         		 = itemData.icon;
			if (itemData.max =='-1')
				tmpItem.resourceLimited  = 'Yes';
			else
				tmpItem.resourceLimited  = 'No';
			if (itemData.basePrice)	
				tmpItem.resourcebasePrice        = itemData.basePrice;
			else
				tmpItem.resourcebasePrice        = '0';
			if (itemData.toxicRate)
				tmpItem.resourcetoxicRate        = itemData.toxicRate;
			else
				tmpItem.resourcetoxicRate        = '0';
		}
	/* Common properties */
		if (itemData.cost)
			for (var i = itemData.cost.length - 1; i >= 0; i--) {
				tmpItem.costable = true;
				tmpItem.cost[itemData.cost[i].resource] = itemData.cost[i].amount;
			}
		if (itemData.requiresStage) {
			tmpItem.requiresStage.display    = 'Stage '+ itemData.requiresStage;
			tmpItem.requiresStage.raw        = itemData.requiresStage;
			if (tmpItem.requiresStage.raw == '0')
				tmpItem.requiresStage.amount = '0';
			if (tmpItem.requiresStage.raw == '1')
				tmpItem.requiresStage.amount = '250 000';
			if (tmpItem.requiresStage.raw == '2')
				tmpItem.requiresStage.amount = '1 000 000';
			if (tmpItem.requiresStage.raw == '3')
				tmpItem.requiresStage.amount = '5 000 000';
			if (tmpItem.requiresStage.raw == '4')
				tmpItem.requiresStage.amount = '15 000 000';
			
		} else {
			tmpItem.requiresStage.display    = 'Stage 0';
			tmpItem.requiresStage.raw    	= '0';
			tmpItem.requiresStage.amount = '0';
		}
		tmpItem.requiresTech             = itemData.requiresTech;
		if (itemData.reqIndependence) {
			tmpItem.reqIndependence          = itemData.reqIndependence;
		}
		if (itemData.description) {
			tmpItem.description          = itemData.description;
		}
		tmpItem.requiPremium             = itemData.requiPremium;
   
   // add release version to the items
   if (changelog.hasOwnProperty(itemData.name)) {
     tmpItem.releaseVersion = changelog[itemData.name];
   } else {
     tmpItem.releaseVersion = '';
   }
   
	/* Add links between items */
		if (itemData.harvests) {
			if (typeof itemData.harvests === 'object')
				for (var i = itemData.harvests.length - 1; i >= 0; i--)
					addLinksProcesses(itemData.name, itemData.harvests[i], 'harvests', type, type);
			else 
				addLinksProcesses(itemData.name, itemData.harvests, 'harvests', type, type);
		}
		if (tmpItem.refinesObj) {
			if (typeof tmpItem.refinesObj === 'object')
				for (var i = tmpItem.refinesObj.length - 1; i >= 0; i--)
					addLinksProcesses(itemData.name, tmpItem.refinesObj[i], 'refinesObj', type, type);
			else 
				addLinksProcesses(itemData.name, tmpItem.refinesObj, 'refinesObj', type, type);
		}
		if (tmpItem.canImportObj) {
			if (typeof tmpItem.canImportObj === 'object')
				for (var i = tmpItem.canImportObj.length - 1; i >= 0; i--)
					addLinksProcesses(itemData.name, tmpItem.canImportObj[i], 'canImportObj', type, type);
			else 
				addLinksProcesses(itemData.name, tmpItem.canImportObj, 'canImportObj', type, type);
		}
		if (tmpItem.canExportObj) {
			if (typeof tmpItem.canExportObj === 'object')
				for (var i = tmpItem.canExportObj.length - 1; i >= 0; i--)
					addLinksProcesses(itemData.name, tmpItem.canExportObj[i], 'canExportObj', type, type);
			else 
				addLinksProcesses(itemData.name, tmpItem.canExportObj, 'canExportObj', type, type);
		}
		if (itemData.race) {
			if (typeof itemData.race === 'object')
				for (var i = itemData.race.length - 1; i >= 0; i--)
					addLink2(itemData.name, itemData.race[i], 'race', type, type);
			else 
				addLink2(itemData.name, itemData.race, 'race', type, type);
		}
		if (itemData.availableMaps) {
			if (typeof itemData.availableMaps === 'object')
				for (var i = itemData.availableMaps.length - 1; i >= 0; i--)
					addLink2(itemData.name, itemData.availableMaps[i], 'availablemaps', type, type);
			else 
				addLink2(itemData.name, itemData.availableMaps, 'availablemaps', type, type);
		}
		if (itemData.canUpgradeTo) {
			if (typeof itemData.canUpgradeTo === 'object')
				for (var i = itemData.canUpgradeTo.length - 1; i >= 0; i--)
					addLink(itemData.name, itemData.canUpgradeTo[i], 'upgradeTo', type, type);
			else 
				addLink(itemData.name, itemData.canUpgradeTo, 'upgradeTo', type, type);
		}
		if (itemData.requiresTech) {
			for (var i = 0; i < itemData.requiresTech.length; i++) {
				if (itemData.requiresTech[i].includes('|')) {
					var tmpreq = itemData.requiresTech[i].split("|");
						for (var j = tmpreq.length - 1; j >= 0; j--) {
							addLink(tmpreq[j], itemData.name, 'neededFor', 'technology', type);
						}		
				}
				else
				addLink(itemData.requiresTech[i], itemData.name, 'neededFor', 'technology', type);
			}
		}	
		if (itemData.produces)
			for (var i = 0; i < itemData.produces.length; i++) {
				var dsttype = itemSmallInfo.filter(function( obj ) {return obj.label == itemData.produces[i];});
				addLink(itemData.name, itemData.produces[i], 'canBuild', type, dsttype.length ? dsttype[0].type.toLowerCase() : 'undefined');
			}
		if (tmpItem.tabledisplay)
			items.push(tmpItem);
					
		if ((tmpItem.costable) || (tmpItem.requiresTech))
			itemscost.push(tmpItem);
		
		if (tmpItem.type == 'technology')
			itemstechs.push(tmpItem);
		
		if (tmpItem.rationable)
			itemsratio.push(tmpItem);
		
		if (tmpItem.storesObj)
			itemsstore.push(tmpItem);
		
		
	}
/* ------------------------function add item internally (end)--------------------------- */




