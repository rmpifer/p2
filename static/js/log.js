
$("#submitLogin").submit(function(event) {
	event.preventDefault();

	$.ajax({
		type: "POST",
		contentType: "application/json; charset=UTF-8",
		data: JSON.stringify({
			"username": document.getElementById("login_username_input").value,
			"password": document.getElementById("login_password_input").value
		}),
		url: "http://class6.eecs.umich.edu/w8ahkxll/p3/api/v1/login",
		success: function(data) { window.location.replace("http://class6.eecs.umich.edu/w8ahkxll/p3/")},
		error: function(error) {console.log("invalid")}
	});

});
