<!DOCTYPE html>

<?php
    include("/nivo-slider/nivoslider.php");
    $nivo=new NivoSlider('nivo-slider/nivoslider',618,236);     // base path is same directory
 
    //$nivo->add_slide(ImagePath,URL,Caption);
    $nivo->add_slide('nivo-slider/imgs/poli.jpg','','');
    $nivo->add_slide('nivo-slider/imgs/poli2.jpg','','');  
    $nivo->add_slide('nivo-slider/imgs/poli4.jpg','','');
    $nivo->add_slide('nivo-slider/imgs/logoteam.jpg','','');
?>
<html>

<head>
<link href='http://fonts.googleapis.com/css?family=Rajdhani' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Signika+Negative:400,600,700' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Roboto+Condensed:400,300italic,700' rel='stylesheet' type='text/css'>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Treasure Hunting</title>
<link type="text/css" href="style.css" rel="stylesheet" />
<link href="menu_source/stylesmenù.css" rel="stylesheet" type="text/css">
<link href='http://fonts.googleapis.com/css?family=Poiret+One' rel='stylesheet' type='text/css'>
<?php $nivo->render_includes(); ?>

</head>

<body>
<div id="header">
	<h1 style="font-family: 'Poiret One', cursive;" ><label style="color:#FF6810">The Treasure Hunting Project</label> <label style="color:#00CCFF">by Ime</label></h1>
</div>

<div id="colonna">

	<div id='cssmenu'>
		<ul>
   			<li class='active'><a href='index.php'><span>Home</span></a></li>
   			<li><a href='video.php'><span>Video</span></a></li>
             <li><a href='documentation.php'><span>Documentation</span></a></li>
   			<li><a href='aboutus.php'><span>About Us</span></a></li>
   			<!--<li class='last'><a href='#'><span>Pippo</span></a></li> -->
		</ul>
	</div>
	<div id="div1" style="padding-bottom: 0%;">
    <p> Improvements in technology have in the latest years lead to a new vision of gaming which introduce the player in incredible scenarios, where computer graphics and artificial intelligence take the user in another dimension, from time to time more realistic and enjoyable.</p>

<p><em>Our purpose anyway is different, our clue is to bring software and technology in the scenarios of the real world and not vice-versa, and to exploit the greatest GPU available in the market: the users' brain!</em> </p></em> </p>
<p style="font-family: 'Poiret One', cursive;"><strong><label style="color:#FFFFFF"> <font size="9"> "Are you ready for the quest!?"</font></label></strong></p>  
<?php $nivo->render_slides() ?>
    </div>
    
 <div id="div3" class="outer">
      <section id="div3" class="inner">
        

<p>Mainly the game consists in a treasure hunt controlled by a central computer which works as creator of the paths and clues to solve in order to find the treasure and win the match, but don't worry, you're always under control! In fact the central computer will communicate to you all the needed informations through an application on your mobile phone, from which you'll be able to set checkpoints, paths, and locations for outdoor gaming. Anyway this doesn't end here! If you're nerd and proud of it, by using our ready-to-use hardware (a set of sensors and Raspberry PI) and adding a pair more settings, even indoor gaming will not be a limit.
</p>
<p> <b><label style="color:#ffffff">FEATURES:</b></label></b>

<br>- The AI can encrypting clues and sendind riddles
<br>- Changing checkpoints in RT
<br>- Slowing down clues in RT
<br>- Taking the time to balance the game

<br> <i>Others features and videos are coming. We are working! </i>


</p>
<p><center>iMe project developers:</center></p>

<p style="font-family:'Poiret One', cursive"> <font size="5px"><label style="color:#FFFFFF"><center><a href="https://github.com/AndreaBarbasso">Andrea Barbasso</a> <a href="https://github.com/Bisto92">Andrea Bistolfi</a>  <a href="https://github.com/philipjk">Filippo Galli</a></label></center> </font></p>
      </section>
  </div>


      
       
</div>

</body>


</html>
