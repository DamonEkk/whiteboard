const joinButton = document.getElementById("joinRoom")
const createButton = document.getElementById("createRoom")


createButton.addEventListener("click", () =>{
	createRoom();
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


