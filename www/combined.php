<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7; IE=EmulateIE9">
    <!--[if IE]><script src="../excanvas.js"></script><![endif]-->
<title> B32 Lab (SHT25 Sensor) Temperature &amp; Humidity Data</title>
<script type="text/javascript"
  src="./dygraph-combined.js"></script>
</head>
<body>
<h1> B32 Lab (SHT25 Sensor) Temperature &amp; Humidity Data</h1>
<p>To zoom on the graph highlight the region you would like to zoom in on, this works with both the X and Y axis.  To return the graph to showing all data double click on it</p>
<h2>Temperature</h2>
<div id="tempdiv"></div>
<script type="text/javascript">
  g = new Dygraph(
    document.getElementById("tempdiv"),
        "http://<?php echo $_SERVER['SERVER_NAME'];?>/wais-sensors/temperature_data.py",{
        lengend: "always",
        showRoller: true,
        strokeWidth: 2,
        height: 600,
        width: 800,
        ylabel: "Temperature (C)",
        xlabel: "Date",
         // add highlight for weekends
        underlayCallback: function (canvas, area, g) {
            canvas.fillStyle = "rgba(227,238,242,1.0)";
            function highlight_period(x_start, x_end) {
                var canvas_left_x = g.toDomXCoord(x_start);
                var canvas_right_x = g.toDomXCoord(x_end);
                var canvas_width = canvas_right_x - canvas_left_x;
                canvas.fillRect(canvas_left_x, area.y, canvas_width, area.h);
            }
            var min_data_x = g.getValue(0, 0);
            var max_data_x = g.getValue(g.numRows() - 1, 0);
            var d = new Date(min_data_x);
            var dow = d.getUTCDay();
            var ds = d.toUTCString();
            var w = min_data_x;
            if (dow == 0) {
                highlight_period(w, w + 43200000);
            }
            while (dow != 6) {w += 86400000;
                d = new Date(w);
                dow = d.getUTCDay();
            }
            w -= 43200000;
            while (w < max_data_x) {
                var start_x_highlight = w;
                var end_x_highlight = w + 172800000;
                if (start_x_highlight < min_data_x) {
                    start_x_highlight = min_data_x;
                }
                if (end_x_highlight > max_data_x) {
                    end_x_highlight = max_data_x;
                }
                highlight_period(start_x_highlight, end_x_highlight);
                w += 604800000;
            }
       }
        }
    );
</script>
<h2>Humidity</h2>
<div id="humdiv"></div>
<script type="text/javascript">
  g = new Dygraph(
    document.getElementById("humdiv"),
        "http://<?php echo $_SERVER['SERVER_NAME'];?>/wais-sensors/humidity_data.py",{
        lengend: "always",
        showRoller: true,
        strokeWidth: 2,
        height: 600,
        width: 800,
        ylabel: "Temperature (C)",
        xlabel: "Date",
         // add highlight for weekends
        underlayCallback: function (canvas, area, g) {
            canvas.fillStyle = "rgba(227,238,242,1.0)";
            function highlight_period(x_start, x_end) {
                var canvas_left_x = g.toDomXCoord(x_start);
                var canvas_right_x = g.toDomXCoord(x_end);
                var canvas_width = canvas_right_x - canvas_left_x;
                canvas.fillRect(canvas_left_x, area.y, canvas_width, area.h);
            }
            var min_data_x = g.getValue(0, 0);
            var max_data_x = g.getValue(g.numRows() - 1, 0);
            var d = new Date(min_data_x);
            var dow = d.getUTCDay();
            var ds = d.toUTCString();
            var w = min_data_x;
            if (dow == 0) {
                highlight_period(w, w + 43200000);
            }
            while (dow != 6) {w += 86400000;
                d = new Date(w);
                dow = d.getUTCDay();
            }
            w -= 43200000;
            while (w < max_data_x) {
                var start_x_highlight = w;
                var end_x_highlight = w + 172800000;
                if (start_x_highlight < min_data_x) {
                    start_x_highlight = min_data_x;
                }
                if (end_x_highlight > max_data_x) {
                    end_x_highlight = max_data_x;
                }
                highlight_period(start_x_highlight, end_x_highlight);
                w += 604800000;
            }
       }
        }
    );
</script>

</body>
</html>

