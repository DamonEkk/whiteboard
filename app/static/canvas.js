const canvas = document.getElementById("room-0");
const sizeInput = document.getElementById("size");
const colourSelect = document.getElementById("colour");
const ctx = canvas.getContext("2d");
//const undo = document.querySelector('button[name="Undo"]');

canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

let currentRoom = 1;
let roomCount = 1;
let drawing = false; // Drawing is disabled when we arnt holding mousedown
let drawSize = 6;
let idNum = 0;
let drawColour = colourSelect.value;
let stroke = []; // current stroke points
let history = []; // History used for undo functionality
ctx.lineCap = "round";


// prevents <enter> from resetting the page, not the best fix for it.
document.querySelector(".selection-form").addEventListener("submit", (e) => {
 e.preventDefault(); 
});

// Clears the canvas
clear.addEventListener("click", () => {
clear_page();
});


undo.addEventListener("click", () => {
clear_page();
console.log(history);
// might wanna move this into a shared location later.
//for (int i = 0; i < history.length; i++){
		
//} Might be better to wait till websockets are a thing and make this global due to clearing the whole page.

});


// Changes the colour event. 
colourSelect.addEventListener("change", () => {
drawColour = colourSelect.value;
});


// Changes the size of the brush event.
sizeInput.addEventListener("change", () => {
drawSize = parseInt(sizeInput.value);
});


// Hold mouse down and enables drawing.
canvas.addEventListener("mousedown", () => {
drawing = true;
ctx.beginPath();
});


// Stop Drawing when you let go of mouse.
canvas.addEventListener("mouseup", () => {
drawing = false;

// For saving keystrokes, used for websockets and undo.
let currentStroke = {
	strokeId: generate_stroke_ID(),
	colour: drawColour,
	size: drawSize,
	points: stroke,
	room: currentRoom
}
stroke = [];
history.push(currentStroke);


});


// Drawing mechanic when drawing it true and mouse is moving.
canvas.addEventListener("mousemove", (e) => {
if (!drawing) return;
ctx.lineWidth = drawSize; // Size 
ctx.strokeStyle = drawColour;	


let point = [e.offsetX, e.offsetY]

stroke.push(point)

ctx.lineTo(e.offsetX, e.offsetY);
ctx.stroke();
ctx.moveTo(e.offsetX, e.offsetY);
});


function generate_stroke_ID(){
return idNum++;	
}


function removed_stroke_ID(){
idNum--;
}


function get_highest_stroke(){
return history[history.length - 1]
}

function clear_page(){
ctx.clearRect(0, 0, canvas.width, canvas.height); //clear page
}


