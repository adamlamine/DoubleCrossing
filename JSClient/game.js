for(var i = 0; i < cloudModels.length; i++){
	clouds.push(new Cloud(i));
}

var draw = function(){
	
	context.clearRect(0,0,window.innerWidth, window.innerHeight);
	
	for (var i = 0; i < bloodSplatters.length; i++){
		var bloodSplatter = bloodSplatters[i];
		bloodSplatter.display();
	}
	
	for(var i = 0; i < playerArray.length; i++){
		var player = playerArray[i];
		player.drawSword();
		player.draw();
		player.walkAnim();	
		player.strikeSword();
		player.kiss();
		player.jump();
		player.miss();
	}
	
	for(var i = 0; i < playingDeathAnims.length; i++){
		var anim = playingDeathAnims[i];
		if(anim.playing){
			anim.play();
		} else {
			playingDeathAnims.splice(i, 1);
		}
	}
	
	
	//DRAW BACKGROUND
	bgContext.clearRect(0,0,window.innerWidth, window.innerHeight);
    bgContext.drawImage(backgroundImg, 0, 0,  window.innerWidth, window.innerWidth/2);
	
	
	//DRAW CLOUDS
	for (var i = 0; i < clouds.length; i++){
		var cloud = clouds[i];
		cloud.display();
	}

	//DRAW FLOOR
	bgContext.drawImage(floorImg, 0,  window.innerWidth*0.405,  window.innerWidth, window.innerWidth/10.38);



}



setInterval(draw, 10);


