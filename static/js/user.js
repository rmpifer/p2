
$("#createUser").submit(function(event) {
	event.preventDefault();

	var checkUsername = document.getElementById("new_username_input").value;
	var checkFirstName = document.getElementById("new_firstname_input").value;
	var checkLastName = document.getElementById("new_lastname_input").value;
	var checkPassword1 = document.getElementById("new_password1_input").value;
	var checkPassword2 = document.getElementById("new_password2_input").value;
	var checkEmail = document.getElementById("new_email_input").value;
	var message = [];

	if (checkUsername.length < 3){
		message.append({"message": "Usernames must be at least 3 characters long"});
	}
	if (!checkUsername.match("^[a-zA-Z0-9]*$")){
		message.append({"message": "Usernames may only contain letters, digits, and underscores"});
	}

	//Check is a valid Password
	if ((checkPassword1.length) < 8){
		message.append({"message": "Passwords must be at least 8 characters long"});
	}
	if (!checkPassword1.match("^(?=.*[a-zA-z])(?=.*\d)")){
		message.append({"message": "Passwords must contain at least one letter and one number"});
	}
	if (!checkPassword1.match("^[a-zA-Z0-9]*$")){
		message.append({"message": "Passwords may only contain letters, digits, and underscores"});
	}
	if (checkPassword1 != checkPassword2){
		message.append({"message": "Passwords do not match"});
	}

	//Check is a valid Email
	if (!checkEmail.match("[^@]+@[^@]+\.[^@]+")){
		message.append({"message": "Email address must be valid"});
	}	
		

	if (checkUsername.length > 20){
		message.append({"message": "Username must be no longer than 20 characters"});
	}	
	if (checkFirstName.length > 20){
		message.append({"message": "Firstname must be no longer than 20 characters"});
	}
	if (checkLastName.length > 20){
		message.append({"message": "Lastname must be no longer than 20 characters"});
	}		
	if (checkEmail.length > 40){
		message.append({"message": "Email must be no longer than 40 characters"});
	}

	if (message.length == 0){

		$.ajax({
			type: "POST",
			contentType: "application/json; charset=UTF-8",
			data: JSON.stringify({
				username: checkUsername,
				firstname: checkFirstName,
				lastname: checkLastName,
				password1: checkPassword1,
				password2: checkPassword2,
				email: checkEmail
			}),
			url: "http://class6.eecs.umich.edu/w8ahkxll/p3/api/v1/user",
			success: function(data) { window.location.replace("http://class6.eecs.umich.edu/w8ahkxll/p3/login")},
			error: function(error) {}
		});
	}
	else{
		//add pclass errors
	}

});

$("#updateUser").submit(function(event) {
	event.preventDefault();

	$.ajax({
		type: "GET",
		contentType: "application/json; charset=UTF-8",
		data: JSON.stringify(),
		url: "http://class6.eecs.umich.edu/w8ahkxll/p3/api/v1/user",
		success: function(data) {
			var checkFirstName = document.getElementById("update_firstname_input").value;
			var checkLastName = document.getElementById("update_lastname_input").value;
			var checkPassword1 = document.getElementById("update_password1_input").value;
			var checkPassword2 = document.getElementById("update_password2_input").value;
			var checkEmail = document.getElementById("update_email_input").value;

			//Check is a valid Password
			if ((checkPassword1.length) < 8){
				message.append({"message": "Passwords must be at least 8 characters long"});
			}
			if (!checkPassword1.match("^(?=.*[a-zA-z])(?=.*\d)")){
				message.append({"message": "Passwords must contain at least one letter and one number"});
			}
			if (!checkPassword1.match("^[a-zA-Z0-9]*$")){
				message.append({"message": "Passwords may only contain letters, digits, and underscores"});
			}
			if (checkPassword1 != checkPassword2){
				message.append({"message": "Passwords do not match"});
			}

			//Check is a valid Email
			if (!checkEmail.match("[^@]+@[^@]+\.[^@]+")){
				message.append({"message": "Email address must be valid"});
			}	
				

			if (checkFirstName.length > 20){
				message.append({"message": "Firstname must be no longer than 20 characters"});
			}
			if (checkLastName.length > 20){
				message.append({"message": "Lastname must be no longer than 20 characters"});
			}		
			if (checkEmail.length > 40){
				message.append({"message": "Email must be no longer than 40 characters"});
			}

			if (message.length == 0){

				$.ajax({
					type: "PUT",
					contentType: "application/json; charset=UTF-8",
					data: JSON.stringify({
						username : data['username'],
						firstname: checkFirstName,
						lastname: checkLastName,
						password1: checkPassword1,
						password2: checkPassword2,
						email: checkEmail
					}),
					url: "http://class6.eecs.umich.edu/w8ahkxll/p3/api/v1/user",
					success: function(data) { console.log("success") },
					error: function(error) {}
				});
			}
			else{
				//add pclass errors
			}
		},
		error: function(error) {}
	});



});
