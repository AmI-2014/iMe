<?php
	include("nivoslider.php");
	$nivo=new NivoSlider('nivoslider',618,246);		// base path is same directory

	//$nivo->add_slide(ImagePath,URL,Caption);
	$nivo->add_slide('imgs/nemo.jpg','','');
	$nivo->add_slide('imgs/toystory.jpg','http://www.google.com','Awesome JQuery Slider');	
	$nivo->add_slide('imgs/up.jpg','','');
	$nivo->add_slide('imgs/walle.jpg','','');
	
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<?php $nivo->render_includes(); ?>
<title>Integrating Nivoslider with PHP</title>
</head>

<body>
<?php $nivo->render_slides() ?>
</body>
</html>