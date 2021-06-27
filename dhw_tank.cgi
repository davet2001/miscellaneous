#!/usr/bin/python3
#
# python cgi-bin file to generate an SVG image of a the temperature gradient of water tank.
# Dave T 27/6/2021
#
# Setup instructions
# (install apache2), then...
# sudo a2enmod cgid 
# sudo systemctl restart apache2
# sudo apt-get install python-svgwrite
#
# install this file to /usr/lib/cgi-bin/dhw_tank/dhw_tank.cgi
#
# to test:
# visit http://localhost/cgi-bin/dhw_tank/dhw_tank.cgi?temps=54.6,52.6,51.3,50.6,39.1,25.0&fmt=svg
#
# to use in homeassistant markdown card:
# ![Image](http://grey.local/cgi-bin/dhw_tank/dhw_tank.cgi?temps={{states('sensor.temperature1')}},{{states('sensor.temperature2')}},{{states('sensor.temperature3')}},{{states('sensor.temperature4')}},{{states('sensor.temperature5')}},{{states('sensor.temperature6')}},{{states('sensor.temperature7')}})

from svgwrite import Drawing, rgb, shapes, gradients
import cgi 
import io

# png format not supported yet
#from cairosvg import svg2png 

# Uncomment for more helpful debugging
# import cgitb
# cgitb.enable()

link = cgi.FieldStorage()

temps_str = link.getvalue("temps", "99.0,25.1")
temps = [float(t) for t in temps_str.split(",")]

fmt = link.getvalue("fmt", "svg")

T_WIDTH=90
T_HEIGHT=150 #(len(temps)-1)*(T_WIDTH/2)

COLD_COLOUR = (56, 85, 255)
HOT_COLOUR = (209, 0, 23)
COLD_TEMP = 30
HOT_TEMP = 50
FONT_HEIGHT = int(T_HEIGHT/12)
L_MARGIN = FONT_HEIGHT *3

def temp_to_color(temp: float):
    prop = (temp - COLD_TEMP)/ (HOT_TEMP-COLD_TEMP)
    if prop > 1:
        prop = 1
    elif prop < 0:
        prop = 0
    return rgb(
        COLD_COLOUR[0] + prop * (HOT_COLOUR[0] - COLD_COLOUR[0]),
        COLD_COLOUR[1] + prop * (HOT_COLOUR[1] - COLD_COLOUR[1]),
        COLD_COLOUR[2] + prop * (HOT_COLOUR[2] - COLD_COLOUR[2]),
    )

dwg = Drawing('noname.svg', size=(L_MARGIN + T_WIDTH, T_HEIGHT+FONT_HEIGHT), profile='tiny')

grad = gradients.LinearGradient((0, 0), (0, 1))
for i, temp in enumerate(temps):
    grad.add_stop_color(i/len(temps), temp_to_color(temp))
    dwg.add(dwg.text(temps[i],
        insert=(0,FONT_HEIGHT+T_HEIGHT*(i/(len(temps)-1))),
        stroke='none',
        fill='#777',
        font_size=f"{FONT_HEIGHT}px",
        font_family="Arial",
        opacity="1" if i==0 or i==len(temps)-1 else "0.2")
    )

dwg.defs.add(grad)
dwg.add(shapes.Rect((L_MARGIN,FONT_HEIGHT/2), (T_WIDTH, T_HEIGHT),
    rx=T_WIDTH/2, 
    stroke=rgb(10, 10, 16, '%'),
    fill=grad.get_paint_server(default='currentColor'),
    ))

if fmt=="svg":
    ramfilesvg = io.StringIO()
    dwg.write(ramfilesvg, pretty=True)
    print("Content-type:image/svg+xml\r\n")
    print(ramfilesvg.getvalue())
elif fmt=="png":
    print("Content-type:text/html\r\n")
    print(f"NOT IMPLEMENTED fmt={fmt}")
    # ramfilesvg = io.StringIO()
    # dwg.write(ramfilesvg)
    # ramfilepng = io.BytesIO()

    # svg2png(dwg.tostring(), write_to=ramfilepng, parent_width=L_MARGIN + T_WIDTH, parent_height=T_HEIGHT+FONT_HEIGHT)
    # print("Content-type:image/png\n")
    # print(ramfilepng.getvalue())
else:
    print("Content-type:text/html\r\n")
    print(f"NOT IMPLEMENTED fmt={fmt}")


