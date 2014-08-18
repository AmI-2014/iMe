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
<link href='http://fonts.googleapis.com/css?family=Poiret+One' rel='stylesheet' type='text/css'>
<style>
#div1	{
         background-color: #FFFF99;
		 color:#BF1010;

		 }
		 
#div2	{
         background-color: #FFFF99;
		 color:#000000;
		 }
		 
</style>
<?php $nivo->render_includes(); ?>
<script src="Scripts/AC_RunActiveContent.js" type="text/javascript"></script>
</head>

<body>
<div id="header">
		<h1 style="font-family: 'Poiret One', cursive;" ><label style="color:#FF6810">The Treasure Hunting Project</label> <label style="color:#00CCFF">by Ime</label></h1>
</div>
<div id="colonna">
	<div id='cssmenu'>
		<ul>
   			<li><a href='index.php'><span>Home</span></a></li>
   			<li class='active'><a href='video.php'><span>Video</span></a></li>
            <li><a href='documentation.php'><span>Documentation</span></a></li>
            <li> <a href='aboutus.php'><span>About Us</span></a></li>
   
		</ul>
	</div>
    <div id="div1">
      <p style="font-family:'Poiret One', cursive"><font size="5px"><label style="color:#C11543"><center> ENJOY THIS PREVIEW!</label></center> </font></p>
     <!--   <video width="640" height="480" controls>
        	<source src="video/Tutti Gli uomini del presidente.mp4"> <!-- il player c'è basta mettere un video nellla cartella apposita*/
            Your browser does not support the video tag. 
        </video> -->
        
<object width="600" height="350" data="https://www.youtube.com/v/pSu3vVCXZd0" type="application/x-shockwave-flash"><param name="src" value="http://www.youtube.com/v/pSu3vVCXZd0" /></object>


    </div>
   	<div id="div2">
    	
        <p><center>iMe project developers:</center></p>

<p style="font-family:'Poiret One', cursive"> <font size="5px"><label style="color:#FFFFFF"><center><a href="https://github.com/AndreaBarbasso">Andrea Barbasso</a> <a href="https://github.com/Bisto92">Andrea Bistolfi</a>  <a href="https://github.com/philipjk">Filippo Galli</a></label></center> </font></p>
        
    </div>
</div>
</body>
</html>
