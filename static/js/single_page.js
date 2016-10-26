<script>
		function redirect(picid){

			if (picid == -1){
				return;
			}

			loadPic(picid);
			
			var stateContent = document.getElementById("content").innerHTML;

			history.pushState(stateContent, null, "http://0.0.0.0/8000/api/v1/album/"+picid);
		}


		function loadAlbum(albumid){

			$("#content").html("");
					
			$.ajax({
				type: "GET",
				contentType: "application/json; charset=UTF-8",
				data: JSON.stringify(),
				url: "http://0.0.0.0/8000/api/v1/album/"+albumid,
				success: function(data) { 
					var htmlContent;
					var access = data['access'];
					var albumid = data['albumid'];
					var created = data['created'];
					var lastupdated = data['lastupdated'];
					var pics = data['pics'];
					var title = data['title'];
					htmlContent = "<h1>" + title + "</h1>";
					var username = data['username'];
					htmlContent = htmlContent + "<h3>" + username + "</h3>";

					for (i = 0; i < pics.length; ++i){
						htmlContent = htmlContent + "<p onclick=\"redirect(" + pics[i]['picID']) + ")\"><img src=/static/images/images/" + pics[i]['picID'] + "." + pics[i]['format'] + "></p>";
						htmlContent = htmlContent + "<p>" + pics[i]['posted'] + "</p><p>" + pics[i]['caption'] + "</p>";
					}

					$.ajax({
						type: "GET",
						contentType: "application/json; charset=UTF-8",
						data: JSON.stringify(),
						url: "http://0.0.0.0/8000/api/v1/user",
						success: function(data){
							var sessionUser = data['username'];
							if(sessionUser == username){
								htmlContent = htmlContent + "<a href=\"http://0.0.0.0/8000/album/edit\" id=\"album_edit_" + albumid + "_link\">Edit</a>";
							}
						},
						error: function(error){}
					});

					$("#content").html(htmlContent);

				},
				error: function(error) { /*invalid album*/}
			});
		}





		function loadPic(picid){

			$("#content").html("");

			$.ajax({
				type: "GET",
				contentType: "application/json; charset=UTF-8",
				data: JSON.stringify(),
				url: "http://0.0.0.0/8000/api/v1/pic/"+ picid,
				success: function(data){
					var albumid = data['albumid'];
					var picid = data['picid'];
					var format = data['format'];
					var caption = data['caption'];
					var next = data['next'];
					var prev = data['prev'];

					htmlContent = "<p><img src=\"/static/images/images/" + picid + "." + format + "></p>";

					$.ajax({
						type: "GET",
						contentType: "application/json; charset=UTF-8",
						data: JSON.stringify(),
						url: "http://0.0.0.0/8000/api/v1/album/"+albumid,
						success: function(data) { 
							var username = data['username'];

							$.ajax({
								type: "GET",
								contentType: "application/json; charset=UTF-8",
								data: JSON.stringify(),
								url: "http://0.0.0.0/8000/api/v1/user",
								success: function(data){
									var sessionUser = data['username'];
									if(sessionUser == username){
										htmlContent = htmlContent + "<input type=\"text\" value=\"\" id=\"pic_caption_input\"><br>";
									}
									else{
										htmlContent = htmlContent + "<p>" + caption + "</p>";
									}
								},
								error: function(error){
									htmlContent = htmlContent + "<p>" + caption + "</p>";
								}
							});
						},
						error: function(error){}
					});

					htmlContent = htmlContent + "<p onclick=\"redirect(" + prev + ")\">Prev</p>";
					htmlContent = htmlContent + "<p onclick=\"redirect(" + next + ")\">Prev</p>";


					$("#content").html(htmlContent);
				},
				error: function(error){}
			});
		}




		$("#pic_caption_input").submit(function(event){

			event.preventDefault();

			var queryString = url ? url.split('?')[1];
			if (queryString){
				var picid = queryString.split('=')[1];
			}
			else{
				//return error
			}


		});

		window.onpopstate = function(event){

			document.getElementById("content").innerHTML = event.state.stateVariable;

		}


	$(document).ready(function(event) {

		var stateContent = document.getElementById("content").innerHTML;

		history.replaceState(stateContent, null, window.location.href);

		var url = window.location.href;

		if (window.location.href.search("albumid") != -1){
			var queryString = url ? url.split('?')[1];
			if (queryString){
				var albumid = queryString.split('=')[1];
			}
			else{
				//return error
			}

			loadAlbum(albumid);
		}
		else if (window.location.href.search("picid") != -1){
			var queryString = url ? url.split('?')[1];
			if (queryString){
				var picid = queryString.split('=')[1];
			}
			else{
				//return error
			}

			loadPic(picid);
		}
	});

</script>