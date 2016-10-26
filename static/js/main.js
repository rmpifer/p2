
	$("#nav_logout").submit(function(event) {
		event.preventDefault();


		$.ajax({
			type: "POST",
			contentType: "application/json; charset=UTF-8",
			data: JSON.stringify(),
			url: "http://0.0.0.0/8000/api/v1/logout",
			success: function(data) { window.location.replace("http://0.0.0.0/8000")},
			error: function(error) {}
		});

	});
