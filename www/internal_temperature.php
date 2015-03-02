<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7; IE=EmulateIE9">
    <!--[if IE]><script src="../excanvas.js"></script><![endif]-->
<title> B32 Lab temperature</title>
<script type="text/javascript"
  src="./dygraph-combined.js"></script>
</head>
<body>
<h1> B32 Lab Temperature Data</h1>
<p>To zoom on the graph highlight the region you would like to zoom in on, this works with both the X and Y axis.  To return the graph to showing all data double click on it</p>
<div id="tempdiv"></div>
<script type="text/javascript">
  g = new Dygraph(
    document.getElementById("tempdiv"),
        "http://wsn.ecs.soton.ac.uk/wais-sensors/internal_temperature_data.py",{
        lengend: "always",
        showRoller: true,
        strokeWidth: 2,
        height: 600,
        width: 800,
        }
    );
</script>
<p>This is from the internal temperature sensor so will be higher than the real temperature</p>
</body>
</html>

