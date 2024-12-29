# svgplayer

This is a very simple svg video player with a bootstrap 5 HTML
front-end, and a Flask python backend.


## installation
````
$ pip install -r requirements.txt
````

## run the server
````
$ python app.py
````

## convert png to mp4
````
$ ffmpeg -framerate 1 -i png_frames/circle_%d.png -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4
````