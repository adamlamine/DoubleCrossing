var draw = function(){
	
	context.clearRect(0,0,window.innerWidth, window.innerHeight);

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
	
	//DRAW BACKGROUND
	bgContext.clearRect(0,0,window.innerWidth, window.innerHeight);
    bgContext.drawImage(backgroundImg, 0, 0,  window.innerWidth, window.innerWidth/2);

}



setInterval(draw, 10);

var checkAudio = function(){
	
	for(var i = 0; i < playerArray.length; i++){
		var player = playerArray[i];
		
		for (var i = 0; i < deathSounds.lenght; i++){
			if (player.deathSounds[i].paused){
				player.deathSoundPlaying = false;
			} else{
				player.deathSoundPlaying = true;
				break;
			}
		}
	
		for (var i = 0; i < stepSounds.lenght; i++){
			if (player.stepSounds[i].paused){
				player.stepSoundPlaying = false;
			} else{
				player.stepSoundPlaying = true;
				break;
			}
		}
		
		for (var i = 0; i < jumpSounds.lenght; i++){
			if (player.jumpSounds[i].paused){
				player.jumpSoundPlaying = false;
			} else{
				player.jumpSoundPlaying = true;
				break;
			}
		}

		for (var i = 0; i < attackSounds.lenght; i++){
			if (player.attackSounds[i].paused){
				player.attackSoundPlaying = false;
			} else{
				player.attackSoundPlaying = true;
				break;
			}
		}
		
		for (var i = 0; i < stepSounds.lenght; i++){
			if (player.hitSounds[i].paused){
				player.hitSoundPlaying = false;
			} else{
				player.hitSoundPlaying = true;
				break;
			}
		}

		for (var i = 0; i < missSounds.lenght; i++){
			if (player.missSounds[i].paused){
				player.missSoundPlaying = false;
			} else{
				player.missSoundPlaying = true;
				break;
			}
		}
	}
	
}

setInterval(checkAudio, 100);