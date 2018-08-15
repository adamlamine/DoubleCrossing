//playerArray
//yourID
//context (für canvas zeichnen)

var draw = function(){
	
	context.clearRect(0, 0, canvas.width, canvas.height);
	
	for(var i = 0; i < playerArray.length; i++){
		
		if(playerArray[i].ID === yourID){
			playerArray[i].color = "#FF0000";
		}
		
		playerArray[i].draw();
	}
	
}

setInterval(draw, 20);