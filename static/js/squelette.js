function formatBadges() { //only possible if badges_catalog was defined. shouldnt be called in squeleton
  if (!badges_catalog) { console.log('badges catalog not found');return;}
  var elems_to_change = document.getElementsByName('badge');
  for (var i=0; elems_to_change.length > i; i++) {
    var temp_elem = elems_to_change[i];
    var temp_ape_account = temp_elem.innerHTML.trim();
    if (badges_catalog.hasOwnProperty(temp_ape_account)) {
      for (var j=0; badges_catalog[temp_ape_account].length > j ; j++) {
        temp_elem.innerHTML += ' <span style="font-style:normal;font-size: .7em;padding: .35em"  class="ui '+badges_catalog[temp_ape_account][j].color+' label">'+badges_catalog[temp_ape_account][j].badgename+'</span>';
      }
    }
  }
}

function formatDates() {
  var elems_to_change = document.getElementsByName('date');
  for (var i=0; elems_to_change.length > i; i++) {
    var temp_elem = elems_to_change[i];
    var temp_date = temp_elem.innerHTML.trim();
    temp_elem.innerHTML = (new Date(Number(temp_date)*1000)).toLocaleString();
  }
  var elems_to_change = document.getElementsByName('ddate');
  for (var i=0; elems_to_change.length > i; i++) {
    var temp_elem = elems_to_change[i];
    var temp_date = temp_elem.innerHTML.trim();
    temp_elem.innerHTML = (new Date(Number(temp_date)*1000)).toLocaleDateString();
  }
}

function formatColonynames() {
  var elems_to_change = document.getElementsByName('colony-name');
  for (var i=0; elems_to_change.length > i; i++) {
    var temp_elem = elems_to_change[i];
    var temp_char = temp_elem.innerHTML.trim();
    temp_elem.innerHTML = char_to_name[temp_char];
  }
}

function formatLocaleString() {
  var elems_to_change = document.getElementsByName('updatelocalestring');
  for (var i=0; elems_to_change.length>i ; i++) {
      var temp_elem = elems_to_change[i];
      try {
        temp_elem.innerHTML = Number(temp_elem.innerHTML.trim()).toLocaleString();
      } catch (e) {}
  }
}

function formatThisName(temp_elem) {
  if (!badges_catalog) { console.log('badges catalog not found');return;}
  if (!temp_elem) {return null;}
  var temp_ape_account = temp_elem.trim();
  if (badges_catalog.hasOwnProperty(temp_ape_account)) {
    for (var j=0; badges_catalog[temp_ape_account].length > j ; j++) {
      temp_elem += ' <span style="font-style:normal;font-size: .7em;padding: .35em" class="ui '+badges_catalog[temp_ape_account][j].color+' label">'+badges_catalog[temp_ape_account][j].badgename+'</span>';
    }
  }
  return temp_elem;
}

function onWindowMessage(mess) {
  //console.log(mess);
  if (mess.data.msg == 'loadprofile'){
    $("<a />", {
			"href" : Flask.url_for('main.player', {"username":mess.data.data}),
			}).appendTo("body").click(function() {
				$(this).remove() 
			  })[0].click();
  }
  if (mess.data.func == 'onApeAppsLogin') {
    $("<a />", {
			"href" : Flask.url_for('perso.intlogin')+"?sida="+mess.data.data.sida+"&sidb="+mess.data.data.sidb+"&seguiurl="+window.location,
			}).appendTo("body").click(function() {
				$(this).remove() 
			  })[0].click();
  }
}

$( document ).ready(function() {
    console.log('document ready.');
    // add event listener
    window.addEventListener("message",onWindowMessage);
    // initialize search ---------------------------------------------------------
    var rawownerTags = [];
    var rawnameTags = [];
    var charTags = [];
    for (i in char_to_owner) {
        if (char_to_owner[i] != null) {
          if (!(rawownerTags.includes(char_to_owner[i]))) { // avoid duplicates
            rawownerTags.push(char_to_owner[i]);
          }
        }
    }
    for (i in char_to_name) {
        if (charTags.includes(charTags[i])) { continue; }
        if (char_to_name[i] == null) { continue; }
        charTags.push(i);
        rawnameTags.push(char_to_name[i].replace('(', '').replace(')', '')+' ('+char_to_owner[i]+')');
    }
    var categoryContent = [];
    for (pl = 0; rawownerTags.length>pl ; pl++) {
        categoryContent.push({category: 'Players', title: rawownerTags[pl], url:Flask.url_for("main.player", {"username": rawownerTags[pl]})});
    }
    for (cl = 0; rawnameTags.length>cl ; cl++) {
        categoryContent.push({category: 'Colonies', title: rawnameTags[cl], url:Flask.url_for("main.colonies", {"charter": charTags[cl]})});
    }
    for (ch = 0; charTags.length>ch ; ch++) {
        categoryContent.push({category: 'Charters', title: charTags[ch], url:Flask.url_for("main.colonies", {"charter": charTags[ch]})});
    }
    $.fn.search.settings.templates.categoryext = function(e, n) {
      thtml = '';
      cur_category = '';
      $.each(e.results, function( index, value ) {
        if (cur_category!=value.category) {
          if (cur_category=='') {
            thtml += '<div class="category"><div class="name">'+value.category+'</div><div class="results">'; // open new category
          } else {
            thtml += '</div></div><div class="category"><div class="name">'+value.category+'</div><div class="results">'; // open new category while closing last one
          }
          cur_category = value.category;
        }
        thtml += '<a class="result" href="'+value.url+'"><div class="content"><div class="title">'+value.title+'</div></div></a>'
      });
      thtml += '</div></div>'
      thtml += '<div class="message empty"><div class="header">Note</div><div class="description">Some results might be missing from here. If you do not find what you are looking for, try the <a href="'+Flask.url_for('tools.advanced_search')+'">advanced search</a>.</div></div>'
      return thtml;
      }
    ;
    $('#top_search').search({
        type: 'categoryext',
        source: categoryContent,
        onResults: function (response) {
            return response;
        }
    });
    // mobile menu dropdown init -------------------------------------------------
    $('#mobilemenudropdown').dropdown();
    // initialize modals ---------------------------------------------------------
    $('#modal_login').modal();
    // format dates and badges on the page ---------------------------------------
    formatDates();
    // connect to ape chat -------------------------------------------------------
    // load iframe only now
    if (_username) {
      console.log('connecting to ape chat');
      $('#ape_chat_iframe').on('load', function() {
        var retDat = {
          "msg": "xfercreddat",
          "data": {
            "sa": getCookie('sida'),
            "sb": getCookie('sidb'),
            "sc": 'F094907F-1D8E-0D96-302C-B5724F9FA2DF',
            "am": '423'
          }
        };
        this.contentWindow.postMessage(retDat,"*");
      });
      $('#ape_chat_iframe').attr('src', 'https://chat.ape-apps.com/?channel=Coloniae&embed=1&fh=b37d00&th=b37d00');
    }
});


function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}