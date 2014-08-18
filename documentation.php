<!DOCTYPE html>
<?php
    include("/nivo-slider/nivoslider.php");
    $nivo=new NivoSlider('nivo-slider/nivoslider',618,236);     // base path is same directory
 
    //$nivo->add_slide(ImagePath,URL,Caption);
    $nivo->add_slide('nivo-slider/imgs/poli.jpg','','');
    $nivo->add_slide('nivo-slider/imgs/poli2.jpg','','');  
    $nivo->add_slide('nivo-slider/imgs/poli4.jpg','','');
    $nivo->add_slide('nivo-slider/imgs/portal.jpg','','');
     
?>
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Treasure Hunting</title>
<link type="text/css" href="style.css" rel="stylesheet" />
<link href="menu_source/stylesmenù.css" rel="stylesheet" type="text/css">
<?php $nivo->render_includes(); ?>
</head>

<body>
<style>

#div1	{
         color:#000000;
         background:url(immagini/cartadoc.jpg);
		 border-radius: 0px 0px 32px 32px;
		 text-align:justify;
		 
		 }
		 

</style>

<div id="header">
		<h1 style="font-family: 'Poiret One', cursive;" ><label style="color:#FF6810">The Treasure Hunting Project</label> <label style="color:#00CCFF">by Ime</label></h1>
</div>
<div id="colonna">
	<div id='cssmenu'>
		<ul>
   			<li><a href='index.php'><span>Home</span></a></li>
   			<li><a href='video.php'><span>Video</span></a></li>
            <li class='active'><a href='documentation.php'></span>Documentation</span></a></li>
   			<li><a href='aboutus.php'><span>About Us</span></a></li>
            
		</ul>
	</div>
    <div id="div1">
      	<div id="div1" style="padding-bottom: 0%;">
    <p> The Treasure Hunting Project is composed by two main systems:

The first of these is the mobile application which , throughout a GUI, lets the players to join the game and displays riddles, checkpoints, statistics and other important informations to the participants. 

The second one is the server, localized on a PC, that communicates with a SQL database, containing a list of checkpoints and related coordinates, and sends it to the mobile Android application. </p>


<p><b>Functional requirements </b>:
<em>
<br>- Lobby --> group of players;
<br>- Provides checkpoint's list;
<br>- Cooperative games (initially);
<br>- Appoints Bonus/malus ;
<br>- Appoints Riddles; </em> </p>
 
<p><b>Non Functional requirements </b>:
<em>
<br>- Smarthphones connected to the Internet all the time;
<br>- GPS running all the time;
<br>- Server and SQL database on a PC, functioning as server and accessibile thanks to No-IP.
</em>
</p>  
<p>

<!-- IMMAGINE DA SISTEMARE E INSEREMENTO VIDEO YOUTUBE
<img src="immagini\structure.png" ></p>
 <!--<iframe width="560" height="315" src="//www.youtube.com/embed/oftbLiCnBtE" frameborder="0" allowfullscreen></iframe>-->

<p><center>iMe project developers:</center></p>

<p style="font-family:'Poiret One', cursive"> <font size="5px"><label style="color:#FFFFFF"><center><a href="https://github.com/AndreaBarbasso">Andrea Barbasso</a> <a href="https://github.com/Bisto92">Andrea Bistolfi</a>  <a href="https://github.com/philipjk">Filippo Galli</a></label></center> </font></p> 
        
    </div>
  
</div>
</body>
</html>