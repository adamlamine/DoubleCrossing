var canvas, context;

var init = function(){
	canvas = document.getElementById("canvas");
	context = canvas.getContext("2d");
	
	canvas.style.position = "absolute";
	canvas.style.height = window.innerHeight + "px";
	canvas.style.width = window.innerWidth + "px";
	
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	
	canvas.style.background = "white";
}

init();

var resize = function(){
	canvas.style.position = "absolute";
	canvas.style.height = window.innerHeight + "px";
	canvas.style.width = window.innerWidth + "px";
	
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
}



class Game{
	
	constructor(){

	}

    onKeyDown(e) {

        if(e.keyCode == 37){
            connection.send("PLAYERCOMMAND: LEFT_DOWN");
        }
        if(e.keyCode == 39){
            connection.send("PLAYERCOMMAND: RIGHT_DOWN");
        }
        if(e.keyCode == 38){
            connection.send("PLAYERCOMMAND: UP_DOWN");
        }
        if(e.keyCode == 40){
            connection.send("PLAYERCOMMAND: DOWN_DOWN");
        }
        if(e.keyCode == 32){
            connection.send("PLAYERCOMMAND: SPACE_DOWN");
        }

    }

    onKeyUp(e) {

        if(e.keyCode == 37){
            connection.send("PLAYERCOMMAND: LEFT_UP");
        }
        if(e.keyCode == 39){
            connection.send("PLAYERCOMMAND: RIGHT_UP");
        }
        if(e.keyCode == 38){
            connection.send("PLAYERCOMMAND: UP_UP");
        }
        if(e.keyCode == 40){
            connection.send("PLAYERCOMMAND: DOWN_UP");
        }
        if(e.keyCode == 32){
            connection.send("PLAYERCOMMAND: SPACE_UP");
        }

    }
	
	stillAliveLoop(){
		connection.send("STILL ALIVE");
	}

}

var gameInstance = new Game();
setInterval (gameInstance.stillAliveLoop, 200)

class Player{
	
	constructor(ID){
		this.ID = ID;
		this.xPos = (window.innerWidth/2);
		this.yPos = (window.innerHeight/2);
		this.ID = undefined;
		this.direction = 1;
		this.color = "#000000";
	}

    draw(){
		context.fillStyle = this.color;
        context.fillRect(this.xPos ,this.yPos , 100, 100);
    }

}

var playerArray = []
var yourID = undefined;
var joining = true;



var connection = new WebSocket('ws://192.168.0.24:5555');
window.addEventListener('keydown', gameInstance.onKeyDown, false);
window.addEventListener('keyup', gameInstance.onKeyUp, false);

var gameState

connection.onmessage = function (event) {
	
	var msg = event.data;
	gameState = JSON.parse(msg);
	
	//wenn mehr oder weniger spieler im gameState sind als im playerArray, baue das playerArray neu auf
	if((playerArray.length < gameState.length)||(playerArray.length > gameState.length)){
		
		playerArray = [];
		
		for(var i = 0; i < gameState.length; i++){
			playerArray.push(new Player());
			playerArray[i].ID = gameState[i].ID;
		}

	}
	
	//Weise den einzelnen Players ihre Parameter zu
	for(var j = 0; j < playerArray.length; j++){
		playerArray[j].xPos = gameState[j].xPos;
		playerArray[j].yPos = gameState[j].yPos;
		playerArray[j].direction = gameState[j].direction;
	}
			
	//Wenn DIESER Client das erste Mal diese Funktion ausführt, weise ihm seine ID zu (ID des zuletzt gejointen Client)
	if(joining){
		joining = false;
		yourID = gameState[gameState.length-1].ID;
	}


}

var loop = function(){
	context.clearRect(0, 0, canvas.width, canvas.height);
	
	//zeichnen des Spielers
	for(var i = 0; i < playerArray.length; i++){
		if(playerArray[i].ID == yourID){
			playerArray[i].color = "#FF0000";
		} else {
			playerArray[i].color = "#000000";
		}
		
		playerArray[i].draw();
	}
	
}


setInterval(loop, 20);