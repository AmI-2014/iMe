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
<style>
#div1	{
		/*background:url(immagini/cartabuona.png); */
		background-color:#FFFFD1;
		}
		
</style>
<?php $nivo->render_includes(); ?>
</head>
<div id="fb-root"></div>

<body>


<style>
#div1	{
         color:#000000; /*colore scritte */
         background-colour: #FFFFD1;
		 border-radius: 0px 0px 32px 32px;
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
            <li><a href='documentation.php'><span>Documentation</span></a></li>
   			<li class='active' ><a href='aboutus.php'><span>About Us</span></a></li>
		</ul>
	</div>
	
    <div id="div1">
    <p style="font-family:'Poiret One', cursive"> <font size="5px"><label style="color:#000000"><center><a href="https://www.facebook.com/andreabarbasso?fref=ts">Andrea Barbasso on FB</a>   <p>"Computer Engineering student addicted to videogames, comics, TV series, music, and each nerd stuff you could ever imagine. In his free time, he uses to study."</p> <a href= "https://www.facebook.com/andrea.bistolfi"> Andrea Bistolfi on FB </a> <p> "Media engineering student which loves art in all its forms from books to videogames. In his free time, he drawns and practise sport" </p>   <a href="https://www.facebook.com/gallifn?fref=ts">Filippo Galli on FB</a><p> "Electric Engineering and musician, he is stubborn and determinate. In his free time he plays drum and composes." </p></label></center> </font></p> </div>
    
    
       
    
</div>
</body>
</html>