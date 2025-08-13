


document.getElementById("guestLog").addEventListener("click", async () => {
    const username = document.getElementById("guest").value;
    const password = document.getElementById("guest").value;
    const email = document.getElementById("guest@guest.com").value;

    try {
        const response = await fetch("/user", {        // relative URL if same container
            method: "POST",
            headers: {
                "Content-Type": "application/json"   // important!
            },
            body: JSON.stringify({                    // send your data as JSON
                username: username,
                password: password,
                email: email
            })
        });

        const data = await response.text();          // your route returns plain text "Success"
        console.log("Response from API:", data);
        alert(data);
    } catch (err) {
        console.error("Error calling API:", err);
    }
});
