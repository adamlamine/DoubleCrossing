var bgCanvas, bgContext, canvas, context;

var backgroundImg = new Image();
backgroundImg.src = 'RESOURCES/Graphics/Background/Background.png';
var gradient = new Image();
gradient.src = 'RESOURCES/Graphics/Character/gradient.png';

var playerModelLeft = [];
var playerModelRight = [];
var ownModelLeft = [];
var ownModelRight = [];
var heartModel = [];

var swordHandle = new Image();
var swordBlade = new Image();
swordHandle.src = 'RESOURCES/Graphics/Character/Sword/handle.png'
swordBlade.src = 'RESOURCES/Graphics/Character/Sword/blade.png'


for (var i = 0; i < 7; i++){
	playerModelLeft.push(new Image());
	playerModelRight.push(new Image());
	ownModelLeft.push(new Image());
	ownModelRight.push(new Image());
	
	playerModelLeft[i].src = 'RESOURCES/Graphics/Character/Normal/1/' + i + '.png';
	playerModelRight[i].src = 'RESOURCES/Graphics/Character/Normal/-1/' + i + '.png';
	ownModelLeft[i].src = 'RESOURCES/Graphics/Character/Own/1/' + i + '.png';
	ownModelRight[i].src = 'RESOURCES/Graphics/Character/Own/-1/' + i + '.png';
}

for (var j = 0; j < 4; j++){
	heartModel.push(new Image());
	heartModel[j].src = 'RESOURCES/Graphics/Character/Hearts/' + j + '.png';
}

var kissSound = new Audio('RESOURCES/Audio/Character/Kiss/kiss_1.mp3');
var jumpSounds = [];
var deathSounds = [];
var attackSounds = [];
var missSounds = [];
var hitSounds = [];
var stepSounds = [];
var ambienceSounds = new Audio('RESOURCES/Audio/Ambience/Surreal_1.mp3');


for(var k = 1; k <= 4; k++){
	jumpSounds.push(new Audio('RESOURCES/Audio/Character/Jump/jmp_'+ k + '.mp3'));
}

for(var i = 1; i <= 3; i++){
	deathSounds.push(new Audio('RESOURCES/Audio/Character/Death/death_'+ i + '.mp3'));
}

for(var i = 1; i <= 4; i++){
	attackSounds.push(new Audio('RESOURCES/Audio/Character/Attack/atk_'+ i + '.mp3'));
}

for(var i = 1; i <= 8; i++){
	missSounds.push(new Audio('RESOURCES/Audio/Attack/Miss/miss_'+ i + '.mp3'));
}

for(var i = 1; i <= 3; i++){
	hitSounds.push(new Audio('RESOURCES/Audio/Attack/Hit/hit_'+ i + '.mp3'));
}

for(var i = 1; i <= 10; i++){
	stepSounds.push(new Audio('RESOURCES/Audio/Footsteps/step_'+ i + '.mp3'));
}


//COPYPASTED VON https://gist.github.com/xposedbones/75ebaef3c10060a3ee3b246166caab56
Number.prototype.map = function (in_min, in_max, out_min, out_max) {
  return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
///COPYPASTA ENDE

var init = function(){
	canvas = document.getElementById("canvas");
	context = canvas.getContext("2d");
	
	
	bgCanvas = document.getElementById("bgCanvas");
	bgContext = bgCanvas.getContext("2d");
	
	bgCanvas.style.position = "absolute";

	
	bgCanvas.width = window.innerWidth;
	bgCanvas.height = window.innerWidth/2;
	
	bgCanvas.style.top = "0px";
	bgCanvas.style.left = "0px";
	bgCanvas.style.height = window.innerWidth/2 + "px";
	bgCanvas.style.width = window.innerWidth + "px";
	
	
	canvas.style.position = "absolute";
	canvas.style.top = "0px";
	canvas.style.left = "0px";
	canvas.style.height = window.innerWidth/2 + "px";
	canvas.style.width = window.innerWidth + "px";
	
	canvas.width = window.innerWidth;
	canvas.height = window.innerWidth/2;
	
	bgCanvas.style.background = "#5f772f";
	canvas.style.background = "rgba(0,0,0,0)";
	

}

init();

var resize = function(){
	canvas.style.position = "absolute";
	canvas.style.height = window.innerHeight + "px";
	canvas.style.width = window.innerWidth + "px";
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;
	
	bgCanvas.style.position = "absolute";
	bgCanvas.style.height = window.innerHeight + "px";
	bgCanvas.style.width = window.innerWidth + "px";
	bgCanvas.width = window.innerWidth;
	bgCanvas.height = window.innerHeight;
}

var onPlayerDeath = function(dyingPlayer){
	console.log(dyingPlayer.ID + " ist verstorben");
	
	hitSounds[Math.floor((Math.random() * 2) + 0)].play();
	deathSounds[Math.floor((Math.random() * 2) + 0)].play();
	
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
		this.frame = 0;
		this.kissFrame = 0;
		this.kissPartialFrame = 0;
		this.prevxPos = 0;
		this.prevStep = 0;
		this.speed = 0;
		this.partialFrame = 0;
		this.weaponLength = 0;
		this.swordAngle = 30;
		this.attacking = false;
		this.kissing = false;
		this.kissAnimationPlaying = false;
		this.strikingUpwards = false;
		this.jumping = false;
		this.jumpSoundPlaying = false;
		this.attackSoundPlaying = false;
		this.hitSoundPlaying = false;
		this.missSoundPlaying = false;
		this.deathSoundPlaying = false;
		this.stepSoundPlaying = false;
		this.self = this;
	}
	
	draw(){
		//DRAW PLAYER MODEL
		if(this.ID !== yourID){

			if(this.direction === -1){
				context.drawImage(playerModelLeft[this.frame], this.xPos, this.yPos + window.innerWidth/300, this.width, this.height*1.1);
			} else {
				context.drawImage(playerModelRight[this.frame], this.xPos, this.yPos + window.innerWidth/300, this.width, this.height*1.1);
			}
		
		} else {
			
			context.drawImage(gradient, this.xPos - this.width/2, this.yPos - this.height/2, this.width*2, this.height*2);

			if(this.direction === -1){
				context.drawImage(ownModelLeft[this.frame], this.xPos, this.yPos, this.width, this.height*1.1);
			} else {
				context.drawImage(ownModelRight[this.frame], this.xPos, this.yPos, this.width, this.height*1.1);
			}
		}
	}
	
	walkAnim(){
		//WALKING ANIM
		if(Math.abs(this.prevxPos - this.xPos) > 1){
			
			this.partialFrame += this.speed/30;
			
			if(Math.floor(this.partialFrame) < 6){
				this.frame = Math.floor(this.partialFrame);
			} else {
				this.frame = 0;
				this.partialFrame = 0;
				
				if(!this.jumping){
					stepSounds[Math.floor((Math.random() * 9) + 0)].play();
				}
			}
		} 
		
		else if(this.prevxPos === this.xPos){
			this.frame = 0;
		}
		
		this.prevxPos = this.xPos;
	}
	
	drawSword(){
		
		var bladeX = this.xPos + this.width/2;
		var bladeY = this.yPos + window.innerWidth/65;
		var bladeThickness = window.innerWidth/35;
		var rad = this.swordAngle*Math.PI/180;
		
		context.save();
		context.translate(bladeX, bladeY + bladeThickness / 2);
		context.rotate(rad);
		context.drawImage(swordBlade, 0, bladeThickness * (-0.5), this.weaponLength, bladeThickness);
		context.restore();
	}
	
	strikeSword(){
		
		var swordSpeed = 15;
		
		
		
		if(!this.attacking){
			//this.swordAngle = (this.direction === -1) ? -30: 210;
			if(this.direction === 1){
				this.swordAngle = 210;
			} else {
				this.swordAngle = -30;
			}
		}
		
		if(this.attacking){
			
			if(this.direction === 1){
				
				if( this.swordAngle < (370) && !this.strikingUpwards){
					this.swordAngle += swordSpeed;
				} else {
					this.strikingUpwards = true;
				}
				
				if(this.strikingUpwards && this.swordAngle > (330)){
					this.swordAngle -= swordSpeed;
				} 
				else if(this.swordAngle <= (330)){
					this.strikingUpwards = false;
				}
			
			} else {
				
				if( this.swordAngle > (-190) && !this.strikingUpwards){
					this.swordAngle -= swordSpeed;
				} else {
					this.strikingUpwards = true;
				}
				
				if(this.strikingUpwards && this.swordAngle < (-150)){
					this.swordAngle += swordSpeed;
				} 
				else if(this.swordAngle >= (-150)){
					this.strikingUpwards = false;
				}
				
			}
		}

	}

	kiss(){
		
		if(this.kissing && !this.kissAnimationPlaying){
			
			if(kissSound.paused){
				
				kissSound.play();
			
			}
				

			this.kissPartialFrame++;
			
			if(this.kissFrame < 4 && this.kissPartialFrame === 50){
				this.kissFrame++;
				this.kissPartialFrame = 0;
			} 
			
			if(this.kissFrame === 4) {
				this.kissFrame = 0;
			}
			
			console.log("kissing");
			context.drawImage(heartModel[this.kissFrame], this.xPos, this.yPos - this.height/1.5, this.width, this.height);
		
		}
		
	}
	
	jump(){
		
		
		if (this.jumping === true && !this.jumpSoundPlaying){
			jumpSounds[Math.floor((Math.random() * 3) + 0)].play();
			this.jumpSoundPlaying = true;
			
			self = this.self;
			setTimeout( function(){self.jumpSoundPlaying = false}, 500);
		}
	}
	
	miss(){
		if (this.attacking === true && !this.missSoundPlaying ){
			missSounds[Math.floor((Math.random() * 7) + 0)].play();
		}
	}
		
	
	

}



var playerArray = [];
var previousPlayerArray = [];
var yourID = undefined;
var joining = true;



var connection = new WebSocket('ws://192.168.0.24:5555');
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
		playerArray[j].width = window.innerWidth/20;
		playerArray[j].height = window.innerWidth/20;
		
		playerArray[j].xPos = gameState[j].xPos.map(0,1200,0, window.innerWidth);
		playerArray[j].yPos = gameState[j].yPos.map(0,600,0, window.innerWidth/2) + window.innerWidth/25;
		playerArray[j].direction = gameState[j].direction;
		playerArray[j].speed = gameState[j].speed;
		playerArray[j].weaponLength = gameState[j].weaponLength.map(0,1200,0, window.innerWidth);
		
		if(gameState[j].attacking === "False"){
			playerArray[j].attacking = false;
		} else if (gameState[j].kissing === "False"){
			playerArray[j].attacking = true;
		}
		
		if(gameState[j].kissing === "False"){
			playerArray[j].kissing = false;
		} else {
			playerArray[j].kissing = true;
		}
		
		if(gameState[j].jumping === "False"){
			playerArray[j].jumping = false;
		} else {
			playerArray[j].jumping = true;
		}
	}
			
	//Wenn DIESER Client das erste Mal diese Funktion ausführt, weise ihm seine ID zu (ID des zuletzt gejointen Client)
	if(joining){
		joining = false;
		yourID = gameState[0].yourID;
	}


}
