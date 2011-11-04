function oerbookmarklet(){
//var $=jQuery;
var URL = window.location.href;
var TITLE = document.title;
var DESCRIPTION = ''
var meta = document.getElementsByTagName('meta')
for (var i = 0; i < meta.length; i++){
    name = meta[i].getAttribute('name');
    if (name == 'description'){
        var DESCRIPTION = meta[i].getAttribute('content');
        break;
    }
}


var LICENSE = ''
var anchors = document.getElementsByTagName('a')
for (var i = 0; i < anchors.length; i++){
    rel = anchors[i].getAttribute('rel');
    if (rel == 'license'){
        var LICENSE = anchors[i].getAttribute('href');
        //var LICENSE_TITLE = anchors[i].getAttribute('href');
        break;
    }
}
/*
 * <a class="license" href="http://creativecommons.org/licenses/by-sa/3.0/" rel="license">
 * <img alt="Creative Commons Attribution-ShareAlike 3.0 Unported License" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png">
 * </a>
 * 
 * <meta content="...." name="description" />
 */

iframe_location = 'http://localhost:8001/add_bookmark/?title=' + TITLE + '&url=' + URL + '&licence=' + LICENSE + '&description=' + DESCRIPTION
try{
    jQuery.fancybox({
            'showCloseButton': true,
            'type': 'iframe',
            'href': iframe_location,
            'transitionIn': 'none',
            'transitionOut': 'none',
            'titleShow': true,
            'title': 'Add FavOERite',
        }
    );
}
catch(e){
    //alert('an error was recorded: ' + e + '\n\nRedirecting instead');
    window.location=iframe_location;
    }  
}

