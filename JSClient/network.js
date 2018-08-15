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

var onPlayerDeath = function(dyingPlayer){
	console.log(dyingPlayer.ID + " ist verstorben");
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
		this.name = "Max Mustermann";
		this.xPos = (window.innerWidth/2);
		this.yPos = (window.innerHeight/2);
		this.width = 60;
		this.height = 60;
		this.ID = undefined;
		this.direction = 1;
		this.color = "#000000";
	}

    draw(){
		context.fillStyle = this.color;
        context.fillRect(this.xPos ,this.yPos , this.width, this.height);
		context.fillStyle = "#FFFFFF";
		
		if(this.direction === 1){
			context.fillRect(this.xPos + this.width*0.8 ,this.yPos + 20 , 10, 10);
		} else{
			context.fillRect(this.xPos + this.width*0.1 ,this.yPos + 20, 10, 10);
		}
		
    }

}

var playerArray = [];
var previousPlayerArray = [];
var yourID = undefined;
var joining = true;



var connection = new WebSocket('ws://127.0.0.1:5555');
window.addEventListener('keydown', gameInstance.onKeyDown, false);
window.addEventListener('keyup', gameInstance.onKeyUp, false);

var gameState

connection.onmessage = function (event) {
	
	var msg = event.data;
	gameState = JSON.parse(msg);
	
	previousPlayerArray = playerArray;
	
	//wenn mehr oder weniger spieler im gameState sind als im playerArray, baue das playerArray neu auf
	if((playerArray.length < gameState.length)||(playerArray.length > gameState.length)){
				
		playerArray = [];
		
		for(var i = 0; i < gameState.length; i++){
			playerArray.push(new Player());
			playerArray[i].ID = gameState[i].ID;
		}

	}
	
	if(playerArray < previousPlayerArray){
		
		//schaut, welche Spieler noch am Leben sind und entfernt sie aus dem previousPlayerArray
		for(var i = 0; i < previousPlayerArray.length; i++){
			
			for(var j = 0; j < playerArray.length; j++){
				
				if ( previousPlayerArray[i].ID === playerArray[j].ID ){
					previousPlayerArray.splice(i, 1);
				}
				
			}
				
				
		}
		
		//die übriggebliebenen sind gestorben -> onPlayerDeath
		for(var i = 0; i < previousPlayerArray.length; i++){
			onPlayerDeath(previousPlayerArray[i]);
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
		yourID = gameState[0].yourID;
	}


}
