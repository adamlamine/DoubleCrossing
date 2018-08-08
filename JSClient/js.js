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



class DummyGame{
	
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

var dg = new DummyGame();
setInterval (dg.stillAliveLoop, 200)

class DummyPlayer{
	
	constructor(ID){
		this.ID = ID;
		this.xPos = (window.innerWidth/2);
		this.yPos = (window.innerHeight/2);
	}

    draw(){
        context.fillRect(this.xPos ,this.yPos , 100, 100);
		console.log(this.xPos)
    }

}

var playerArray = []




var connection = new WebSocket('ws://192.168.0.24:5555');
window.addEventListener('keydown', dg.onKeyDown, false);
window.addEventListener('keyup', dg.onKeyUp, false);



connection.onmessage = function (event) {
	var msg = event.data;
	var gameState = JSON.parse(msg);
	//console.log(gameState)
	var gameStateSize = Object.keys(gameState).length
	
	if(playerArray.length < gameStateSize){
		playerArray.push(new DummyPlayer());
	} else if(playerArray.length > gameStateSize){
		playerArray.pop();	
	}
	
	for(var i = 0; i < playerArray.length; i++){
		playerArray[i].xPos = gameState["Player " + (i+1)]["xPos"];
		playerArray[i].yPos = gameState["Player " + (i+1)]["yPos"];
	}


}


var loop = function(){
	context.clearRect(0, 0, canvas.width, canvas.height);
	
	for(var i = 0; i < playerArray.length; i++){
		playerArray[i].draw()
	}
	
}


setInterval(loop, 20)