const canvas = document.getElementById("room");
const sizeInput = document.getElementById("size");
const colourSelect = document.getElementById("colour");
const ctx = canvas.getContext("2d");

const params = new URLSearchParams(window.location.search);
const roomID = params.get("roomID");
const token = params.get("token");

canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

let drawNum = 1;
let currentPage = 1;
let roomCount = 1;
let drawing = false; // Drawing is disabled when we arnt holding mousedown
let drawSize = 6;
let idNum = 0;
let drawColour = colourSelect.value;
let stroke = []; // current stroke points
let history = []; // History used for undo functionality
ctx.lineCap = "round";

exportButton.addEventListener("click", () => {
	
});

// prevents <enter> from resetting the page, not the best fix for it.
document.querySelector(".selection-form").addEventListener("submit", (e) => {
 e.preventDefault(); 
});

// Clears the canvas
clear.addEventListener("click", () => {
	clear_page();
	clear_strokes_page(currentPage); //Clears history of page strokes
});


undo.addEventListener("click", () => {
clear_page();
console.log(history);
// might wanna move this into a shared location later.
//for (int i = 0; i < history.length; i++){
		
//} Might be better to wait till websockets are a thing and make this global due to clearing the whole page.

});
	
// "Creates" a new page, clears page and 
addPageButton.addEventListener("click", () => {
	clear_page();
	currentPage++;
	changePage.value++;
});


// Changes the colour event. 
colourSelect.addEventListener("change", () => {
	drawColour = colourSelect.value;
});

changePage.addEventListener("change", () => {
	if (!(changePage.value == currentPage) || !(changePage.value == null)){
		currentPage = changePage.value;
		clear_page();
		draw_strokes(currentPage);
	}
});

exportButton.addEventListener("click", async () => {
    if (!token) {
        console.log("Not logged in");
        return;
    }

    try {
	   
        const response = await fetch("/room/export", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                history: history,
                canvasHeight: canvas.height,
                canvasWidth: canvas.width
            })
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
        window.URL.revokeObjectURL(url);

    } catch (err) {
        console.error("Error: ", err);
    }
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
		canvas: roomID,
		// add username here
		drawId: drawNum,
		strokeId: generate_stroke_ID(),
		colour: drawColour,
		size: drawSize,
		points: stroke,
		page: parseInt(currentPage)
	}
	stroke = [];
	history.push(currentStroke);
	console.log(currentStroke);
	drawNum++;
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

function clear_strokes_page(page){
	history = history.filter(drawStroke => drawStroke.page != page);		
}


// This is using global lists, probably would pass a list of strokes in reality
function draw_strokes(page){
	cPage = history.filter(drawStroke => drawStroke.page == page);

	saveSize = drawSize;
	saveColour = drawColour;

	for (i = 0; i < cPage.length; i++){
		ctx.beginPath();

		for (k = 0; k < cPage[i].points.length; k++){
			pointX = cPage[i].points[k][0];
			pointY = cPage[i].points[k][1];
			ctx.lineWidth = cPage[i].drawSize; // Changing the size to saved size
			ctx.strokeStyle = cPage[i].drawColour;	// Changing the colour to saved colour


			ctx.lineTo(pointX, pointY);
			ctx.stroke();
			ctx.moveTo(pointX, pointY);

		}
	}
		ctx.lineWidth = drawSize;
		ctx.strokeStyle = drawColour;	 
}

function draw_all_pages(strokes){
	return
}
