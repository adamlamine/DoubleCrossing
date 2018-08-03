
class DummyGame{
	
	constructor(){
		this.canvas = document.getElementById("canvas");
		
	}

    onKeyDown(e) {
        console.log(e.keyCode);

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
        console.log(e.keyCode);

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


}

var dg = new DummyGame();

var connection = new WebSocket('ws://127.0.0.1:5555');
window.addEventListener('keydown', dg.onKeyDown, false);
window.addEventListener('keyup', dg.onKeyUp, false);





//var init = function(){
//	canvas.style.position = "absolute"
//	canvas.style.height = window.innerHeight + "px"
//	canvas.style.width = window.innerWidth + "px"
//	canvas.style.background = "black"
//}
//
//var resize = function(){
//	canvas.style.position = "absolute"
//	canvas.style.height = window.innerHeight + "px"
//	canvas.style.width = window.innerWidth + "px"
//}
//
//class Player{
//	
//	constructor() {
//		this.xPos = 50
//		this.yPos = 50
//    }
//
//	
//	
//	
//}