// JavaScript Document
var coordinates, checkpoints=[], riddlerIndex, maxRiddler, riddlerShuffler=[], riddlerCheckName=[], riddlerViewer=[], actualCheckpointIndex=-1, foundACheckpointLately=1, CNAME, COORDS, HOWCLOSE=-1, totalScore=0, myScore=0, maxTime=600, timeLeft=600, maxScorePerPerson=0, winningScore=0, distance=999.99, finishedCheckpoints=0, toPrint="", funct, standStillCounter, standStillCoords;
//Local Storage Variables: PlayerID, PlayerUsername, NumOfPlayers
var server="http://188.153.39.89:8080";
function printCoords()
{
	document.getElementById("coords").innerHTML="Latitude: "+window.coordinates.latitude+"<br>Longitude: "+window.coordinates.longitude;
}
function getCoords()
{
    if (navigator.geolocation) 
	{
		navigator.geolocation.getCurrentPosition(geo_success,geo_error,{enableHighAccuracy:true}); 
	}
	else alert("GPS not working, not supported or not enabled.");
}
function geo_success(pos)
{
  	var crd = pos.coords;
	var x={latitude:0,longitude:0}
  	x.latitude=crd.latitude;
  	x.longitude=crd.longitude;
	window.coordinates=x;
}
function geo_error(){}
function coordsToString(){if (window.coordinates!=null) return (window.coordinates.latitude+", "+window.coordinates.longitude);
else return "error";}

function evaluateDistance()
{
	var R=6371 //km
	var K=Math.PI/180;
	window.COORDS.replace(" ","");
	var trimmed=window.COORDS.split(",");
	var y=((window.coordinates.latitude)-(parseFloat(trimmed[0])))*K;
	var x=(((window.coordinates.longitude)-(parseFloat(trimmed[1])))*K)*Math.cos((((window.coordinates.latitude)+(parseFloat(trimmed[0])))*K)/2);
	var res=Math.floor((Math.sqrt(x*x+y*y)*R*1000));
	window.distance = res;
}
function findMaluses()
{if (window.finishedCheckpoints==0){
	var mediumSecondsForCheckpointForPlayer = (window.maxTime/window.winningScore)*window.localStorage.getItem("NumOfPlayers");
	if (((window.maxTime-window.timeLeft)/mediumSecondsForCheckpointForPlayer)<window.myScore)
	{
		var i=Math.floor(Math.random()*100);
		if (i<60) standStillMalus();
		else if (i<90) changeCheckpointMalus();
		else minusScoreMalus();
	}
	else document.getElementById("malus").innerHTML="<center><h2>Malus: None!</h2><br></center>";
}}
function getCheckpoints(){
	$.post( server+"/GetCheckpoints/", {id: window.localStorage.getItem("PlayerID")}).done(function( data ) {
		var numCheckPerPlayer=0;
		$.each( data, function(key,val) {window.checkpoints.push(val);numCheckPerPlayer+=1;});
		window.maxScorePerPerson=numCheckPerPlayer;
		window.winningScore=(numCheckPerPlayer/2)*window.localStorage.getItem("NumOfPlayers");
		nextCheckpoint();
		})	
}
function playerInit(username){
	$.post( server+"/PlayerInit/", { name: username} ).done(function(data) {
		if (data>0) {
			window.localStorage.setItem("PlayerID",data);
			window.localStorage.setItem("PlayerUsername",username);alert("Username set!");document.getElementById("yourUsernameIs").innerHTML="<h6><center>Your username is "+window.localStorage.getItem("PlayerUsername")+"</center></h6>";}
		else if (data="NOK") alert("Username already in use! Please select another one.");
		else alert("No internet connection!");})
	}
function createLobby(lName, nCheck, range, startCoords, difficulty){
	$.post( server+"/CreateLobby/", { name: lName, id: window.localStorage.getItem("PlayerID")} ).done(function( data ) {
		if (data=="OK") setGameInfo(lName, nCheck, range, startCoords, difficulty);
		else if (data=="NOK") alert("Lobby name is already been picked! Choose another one.");
		else alert("No internet connection!");})
	}
function joinLobby(lName){
	$.post( server+"/JoinLobby/", { name: lName, id: window.localStorage.getItem("PlayerID")} ).done(function( data ) {
		if (data=="OK") {alert("Lobby found! Joining now!"); 
		window.localStorage.setItem("LobbyName",lName); 
		window.location.href="lobby.html";}
		else if (data=="NOK") alert("Lobby not found!");
		else alert("No internet connection!");})
	}
function setGameInfo(lName, nCheck, range, startCoords, difficulty){
	$.post(server+"/SearchForCheckpoints/", { lobby: lName, first: nCheck, second: range, third: startCoords, fourth: difficulty}).done(function(data){
	if (data>=0) {window.localStorage.setItem("LobbyName",lName); alert("Lobby successfully created!"); window.location.href="masterlobby.html";}
	else alert("No internet connection!");})
	}
//This was just for testing purposes
//function getGameStartDate(lobbyName){
	//$.getJSON( server+"/JoinLobby/", function( data ) {
		//var items = [];
		//$.each( data, function(key,val) {
		//if(val.pk==lobbyName) items.push(val);});
		//alert(items[0].fields.game_start_date);});
		//}
function getPlayers(){
	$.post( server+"/Ranking/", {id: window.localStorage.getItem("PlayerID"), checked: 0}).done(function( data ) {
		var names="", howmany=0;
		$.each( data, function(key,val) {names+=val[0]+"<br>";howmany+=1});
		document.getElementById("players").innerHTML="<h2>"+names+"</h2>";
		window.localStorage.setItem("NumOfPlayers",howmany);
		})
	}
function hasGameStarted(){
	$.post( server+"/GameStatus/", {id: window.localStorage.getItem("PlayerID")}).done(function( data ) {
		if (data=="True") window.location.href="playing.html";
		})
	}
function startGame(){
	$.post( server+"/BeginFinish/", {yes_no: "True", id: window.localStorage.getItem("PlayerID")}).done(function( data ){
		if (data=="OK") document.getElementById("starting").innerHTML="<h5><center>Game starting!</center></h5>";
		else alert("Something went wrong! Try again!");})
		}
function endGame(){
	$.post( server+"/BeginFinish/", {yes_no: "", id: window.localStorage.getItem("PlayerID")})}
function countDown(){window.timeLeft-=1;if (window.timeLeft<=0) endGame();}
function hasGameEnded(){
	$.post( server+"/GameStatus/", {id: window.localStorage.getItem("PlayerID")}).done(function( data ) {
		if (data=="False")
		{ranking();
		if (window.totalScore>=window.winningScore) alert("Good Job! YOU'VE WON!");
		else alert("You LOSE!");
		window.location.href="index.html";
		}})}
function areYouThere(){
	if (window.foundACheckpointLately==0){
		if (window.finishedCheckpoints==0){
			if (window.distance<=window.HOWCLOSE){
				window.foundACheckpointLately=1; addPoint();}}}
}
function nextCheckpoint(){
	if (window.foundACheckpointLately==1){
		window.actualCheckpointIndex+=1;
		var i=window.actualCheckpointIndex;
		if (i<window.maxScorePerPerson)
		{
			window.CNAME=window.checkpoints[i].fields.name;
			window.COORDS=window.checkpoints[i].fields.coordinates;
			window.HOWCLOSE=parseInt(window.checkpoints[i].fields.prox);
		}
		else {window.finishedCheckpoints==1; alert("You finished all your checkpoints! Wait for the others!");}
		riddler();
		window.foundACheckpointLately=0;}
}
function ranking(){ //Without viewing the whole rankings, it might be an available space problem 
	$.post( server+"/Ranking/", {id: window.localStorage.getItem("PlayerID"), checked: window.myScore}).done(function( data ) {
		var totpoints=0;
		$.each( data, function(key,val) {totpoints+=val[1];});
		window.totalScore=totpoints;
		if (window.totalScore>=window.winningScore) endGame();
		})
	}
function addPoint(){
	window.myScore+=1;
	ranking();
	nextCheckpoint();
}
function printInfos(){
	document.getElementById("gameInfos").innerHTML="<center><h2>Checkpoints found: "+window.totalScore+"/"+window.winningScore+"</h2><br><h3>Time left: "+window.timeLeft+"</h3><br></center><br>"
}
function printCheckpoint(){
	document.getElementById("game").innerHTML="<center><h2>Next Checkpoint:</h2><br><h3>"+window.toPrint+"</h3><br><h4>Distance from checkpoint: "+window.distance+"m</h4></center><br>";
}
function riddler(){
	window.toPrint="";
	window.riddlerIndex=0;
	window.maxRiddler=CNAME.length;
	var temp=[], temp2=[], i;
	for (i=0; i<window.maxRiddler;i++) temp.push(i);
	window.riddlerShuffler=shuffle(temp);
	for (i=0; i<window.maxRiddler;i++) temp2.push(0);
	window.riddlerViewer=temp2;
	window.riddlerCheckName=window.CNAME.split("");
}
function shuffle(o){
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
}
function revealLetters(){
	if(window.riddlerIndex<window.maxRiddler){
		var j=window.riddlerIndex, i;
		window.toPrint="";
		window.riddlerViewer[window.riddlerShuffler[j]]=1;
		for(i=0;i<window.maxRiddler;i++)
		{
			if (window.riddlerViewer[i]==1) window.toPrint+=window.riddlerCheckName[i];
			else window.toPrint+="-";
		}
		window.riddlerIndex+=1;
}}

function standStillMalus()
{
	document.getElementById("malus").innerHTML="<center><h2>Malus: STAND STILL FOR 30 SECONDS! Or you will lose one point!</h2><br></center>";
	window.standStillCounter=30;
	window.standStillCoords=window.coordinates;
	window.funct=window.setInterval("standStill()",1000);
}
function changeCheckpointMalus()
{
	nextCheckpoint();
	document.getElementById("malus").innerHTML="<center><h2>Malus: Haha! We changed your checkpoint on the fly!</h2><br></center>";
}
function minusScoreMalus()
{
	window.myScore-=1;
	ranking();
	document.getElementById("malus").innerHTML="<center><h2>Malus: How unfortunate! You lost one point!</h2><br></center>";
}
function standStill(){
	window.standStillCounter-=1;
	if (window.standStillCounter<=0)
	{
		clearInterval(window.funct);
		document.getElementById("malus").innerHTML="<center><h2>Malus: None!</h2><br></center>";
	}
	else if (evaluateStillDistance()>10)
	{
		clearInterval(window.funct);
		minusScoreMalus();
	}
}
function evaluateStillDistance()
{
	var R=6371 //km
	var K=Math.PI/180;
	var y=((window.coordinates.latitude)-(window.standStillCoords.latitude))*K;
	var x=(((window.coordinates.longitude)-(window.standStillCoords.longitude))*K)*Math.cos((((window.coordinates.latitude)+(window.standStillCoords.latitude))*K)/2);
	var res=Math.floor((Math.sqrt(x*x+y*y)*R*1000));
	return res;
}