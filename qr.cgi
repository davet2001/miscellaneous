#!/usr/bin/python3
# Local QR code generator
# Dave T 2022-01-02
#
# Setup:
# apache2 or similar running with cgi-bin active.
# Save this file to e.g. /usr/lib/cgi-bin/qr.cgi
# chmod +x /usr/lib/cgi-bin/qr.cgi
# sudo pip3 install qrcode cgi
#
# Test:
# visit the following url in your brower:
# http://localhost/cgi-bin/qr.cgi?s=my_url_encoded_string
# The returned image will be a SVG QR code of the given string.

import cgi
import io
import qrcode
import qrcode.image.svg

args = cgi.parse()
data = args['s'][0]

img = qrcode.make(data, image_factory = qrcode.image.svg.SvgImage)

ramfilesvg = io.BytesIO()
img.save(ramfilesvg)
print("Content-type:image/svg+xml\r\n")
print(ramfilesvg.getvalue().decode())
