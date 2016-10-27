
$("#nav_logout").submit(function(event) {
	event.preventDefault();


	$.ajax({
		type: "POST",
		contentType: "application/json; charset=UTF-8",
		data: JSON.stringify(),
		url: "http://class6.eecs.umich.edu/w8ahkxll/p3/api/v1/logout",
		success: function(data) { window.location.replace("http://class6.eecs.umich.edu/w8ahkxll/p3")},
		error: function(error) {}
	});

});
