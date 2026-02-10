# ifa_website

The files should be uploaded to webpages.ifa.hawaii.edu in directory /www/users/mbottom

as such

from inside /Users/mbottom/Desktop/projects/new_website/ifa_website

execute

scp -r * mbottom@webpages.ifa.hawaii.edu:/www/users/mbottom

use the galileo password

to get the html code for the images,
go to powerpoint and hit export/jpeg and put it in /images2/photos_for_website
run generate_images_html.py	 and then replace in index.html from "<!-- REPLACE HERE WITH SCRIPT OUTPUT FROM GENERATE_IMAGES_HTML.PY-->"
to "<!-- STOP REPLACE HERE WITH SCRIPT OUTPUT-->" with what the generate_images_html.py output.  it will randomize the images.

