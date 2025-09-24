
const username = "{{msg}}";


document.getElementById("confirmation").addEventListener("submit", async function(e) {

	console.log("button hit");
	e.preventDefault(); // Stops page from refreshing itself

	let code = document.getElementById("code").value;

	try{
		const response = await fetch ("/confirm", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify({username, code})
		});
	}

	const data = await response.json();

});

