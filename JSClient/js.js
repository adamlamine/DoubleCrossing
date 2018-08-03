var canvas = document.getElementById("canvas")



var connection = new WebSocket('ws://127.0.0.1:5555');

connection.onopen = function () {
	setInterval(sendStuff, 100);
};

var sendStuff = function() {
	connection.binaryType = 'blob';
	console.log("Sende Nachricht.")

	connection.send("TEST")
}












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