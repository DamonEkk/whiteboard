
document.getElementById("login").addEventListener("submit", async function(e) {
	e.preventDefault();

	let username = document.getElementById("username").value;
	let password = document.getElementById("password").value;

	try {
		let response = await fetch("/users", {
		    method: "POST",
		    headers: {
			"Content-Type": "application/json"
		    },
		    body: JSON.stringify({ username, password });
		}

		const data = await response.json
		if (!response.ok){
			// Display error message to user
			return;
		}

		const token = data.token;
		localStorage.setItem("jwt_token", token);

		const payload = JSON.parse(atob(token.split('.')[1])); 
		switch (payload){
			case "ADMIN":
				window.location.href = "/"
				break;
			case "USER":
				window.location.href = "/"
				break;
			case "GUEST":
				window.location.href = "/"
				break;
			default:
				window.location.href = "/"
		}

	}

	catch (e){
		window.location.href = "/501"	
	}
	
});
