function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

function didAddPopup(name,newId,newRepr) {
    $("#"+name).trigger('didAddPopup',[html_unescape(newId),html_unescape(newRepr)]);
}

function showAddAnotherPopup(trigger) {
	var div = trigger.replace('add_id_','');
	$("#"+div).load('/lookup/'+div+'/add/').dialog({
													modal:true,
													width: 300,
													buttons: {
															"Create an author": function() {
																  var dialog_window = $( this );
																  var object = $("#add_author").serialize();
																  $.post("/lookup/"+div+"/add/", object, function(data) {
																  	if (data.substring(0, 5) == "valid")
																  	{
																  		var split_data = data.split('||');
																  		didAddPopup('id_'+div,split_data[1],split_data[2]);
																	    dialog_window.dialog( "close" );
																	}
																	else
																	{
																		$("#"+div).html(data);
																	}
																  });
															},
															Cancel: function() {
																$( this ).dialog( "close" );
															}
														},
													});
    return false;
}