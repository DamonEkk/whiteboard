const joinButton = document.getElementById("joinRoom")
const createButton = document.getElementById("createRoom")
const token = localStorage.getItem("token")
const stressButton = document.getElementById("stressButton");

if (token){
    const payload = JSON.parse(atob(token.split('.')[1]));

    if (payload.role !== "ADMIN"){
        window.location.href = "/"; 
    }
}
else {
    window.location.href = "/";
}


createButton.addEventListener("click", () =>{
	createRoom();
});

stressButton.addEventListener("click", async (e) => {

   e.preventDefault(); 

    try {
        const response = await fetch("/admin/stress", { 
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            }
        });



        if (!response.ok) {
            throw new Error("Error 500");
        }

        const pdfBlob = await response.blob();
        const url = window.URL.createObjectURL(pdfBlob);
        const a = document.createElement("a");

        a.href = url;
        a.download = "canvas_export.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();

    } 

    catch (err) {
        console.error("Error: ", err);
    }
});




function createRoom(){
	roomSeed = (Date.now() >> 4)
	const token = localStorage.getItem("token")
	if (token){
		window.location.href = "/canvas?token=" + token + "&roomID=" + roomSeed; 
	}
	else{
		window.location.href = "/canvas?roomID=" + roomSeed;
	}
}


