
document.getElementById("loginBut").addEventListener("click", async function(e) {

	console.log("button hit");
	e.preventDefault(); // Stops page from refreshing itself

	let username = document.getElementById("username").value;
	let password = document.getElementById("password").value;

	login(username, password);
});

async function login(username, password){


	try {
		let response = await fetch("/users", {
		    method: "POST",
		    headers: {
			"Content-Type": "application/json"
		    },
		    body: JSON.stringify({username, password})
		});

		const data = await response.json()
		if (!response.ok){
			// Display error message to user
			console.log("login failed")
			return;
		}

		
		const token = data.token;
		const role = data.role;
		localStorage.setItem("token", token);
		console.log("login success");

		const payload = JSON.parse(atob(token.split('.')[1]));
		console.log("ROLE = " + role)

		// Add token so we can verify the users role
		switch (role){
			case "ADMIN":
				window.location.href = "/adminLogged";
				break;
			case "USER":
				window.location.href = "/userLogged";
				break;
			case "GUEST":
				window.location.href = "/guestLogged"
				break;
			default:
				window.location.href = "/guestLogged"
		}

	}

	catch (e){
		console.error("login error:", e);
		window.location.href = "/500";	
	}
	
}


document.getElementById("signup").addEventListener("click", async function(e) {

	e.preventDefault(); // Stops page from refreshing itself

	let username = document.getElementById("username").value;
	let password = document.getElementById("password").value;
	let email = document.getElementById("email").value;

	let response = await fetch("/user", {
	    method: "POST",
	    headers: {
		"Content-Type": "application/json"
	    },
	    body: JSON.stringify({username, password, email})
	});

	const data = await response.json()
	if (!response.ok){
		// Display error message to user
		console.log("signup failed")
		return;
	}

	window.location.href = `/confirmation?user=${username}`;	
});

