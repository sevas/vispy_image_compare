# -*- coding: utf-8 -*-
# vispy: gallery 30
# -----------------------------------------------------------------------------
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Display an Image
================

Simple use of SceneCanvas to display an Image.

"""

import sys
from vispy import scene
from vispy import app
from vispy.io import load_data_file, read_png

from skimage.data import chelsea
from skimage.filters import gaussian
from vispy.scene.visuals import InfiniteLine
from image_compare_visual import ImageCompare

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 800, 600
canvas.show()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()

# Create the image
im1 = chelsea()
im2 = gaussian(im1, sigma=1.9)
im2 = (im2 * 255).astype('uint8')
interpolation = 'nearest'

image = ImageCompare(data1=im1, data2=im2, interpolation=interpolation,
                            parent=view.scene, method='subdivide')
w = im1.shape[1]
sep = InfiniteLine(pos=w/2, color=(1.0, 0.0, 0.0, 0.5), vertical=True, parent=view.scene)

canvas.title = 'image compare'

# Set 2D camera (the camera will scale to the contents in the scene)
view.camera = scene.PanZoomCamera(aspect=1)
# flip y-axis to have correct aligment
view.camera.flip = (0, 1, 0)
view.camera.set_range()
view.camera.zoom(0.1, (250, 200))

# get interpolation functions from Image
names = image.interpolation_functions
names = sorted(names)
act = 17


# Implement key presses
@canvas.events.key_press.connect
def on_key_press(event):
    global act
    if event.key in ['Left', 'Right']:
        if event.key == 'Right':
            step = 1
        else:
            step = -1
        act = (act + step) % len(names)
        interpolation = names[act]
        image.interpolation = interpolation
        canvas.title = 'Spatial Filtering using %s Filter' % interpolation
        canvas.update()

@canvas.events.mouse_move.connect
def on_mouse_move(event):

    sep.set_data(pos=event.pos[0])
    print(event.pos[0])
    image.split_x = event.pos[0] / 640
    canvas.update()


if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()
