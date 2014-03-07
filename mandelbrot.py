#!/usr/bin/env python

import pygame
import math
import cmath

# Mandelbrot iteration
def nextMandelbrot(i, c):
	i=i*i+c
	return i


# Initialize screen etc
pygame.init()
X=800
Y=600
screen = pygame.display.set_mode((X,Y))
pygame.display.set_caption("Sawkko draws Mandelbrot")
screen.fill( (255,255,255) )
pygame.display.flip()

# draw_ready tells whether we've finished drawing our picture or not
draw_ready=False

# We're drawing points [min_x,max_y] x [min_y, max_y] on the complex plane
# We'll be modifying these when the screen is clicked to zoom in

min_x=-2.5
min_y=-1.5
max_x=1.5
max_y=1.5
zoom=0 # Number of zoomings we have done. we want to do more iterations when we've zoomed in

while(True):
	if(draw_ready):
		#if the picture we're drawing is already drawn
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.image.save(screen, 'YourMandelbrot.png')
				pygame.quit()
				
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# Set the location of mouse click as the new center point and zoom
				center_x, center_y = event.pos
				center_y = (float)(center_y)/Y
				center_x = (float)(center_x)/X
				center_x *=(max_x-min_x)
				center_y *=(max_y-min_y)
				center_x+=min_x
				center_y+=min_y
				lenx = max_x-min_x
				leny = max_y-min_y                
				#mouse 1 zoom in
				if event.button==1:

					min_x=center_x-(0.15*lenx)
					max_x=center_x+(0.15*lenx)
					min_y=center_y-(0.15*leny)
					max_y=center_y+(0.15*leny)
					zoom+=1
				
				
				#mouse 2 zoom out
				elif event.button==3:
					min_x=center_x-(1.25*lenx)
					max_x=center_x+(1.25*lenx)
					min_y=center_y-(1.25*leny)
					max_y=center_y+(1.25*leny)
					zoom-=1
					
				# Start drawing again
				draw_ready=False
				
	if(not draw_ready):
		itmax = 100+20*zoom   # maximum number of iterations we will do
		# Draw the image
		for a in range(X):
			for b in range(Y):
				iteration = 0
				# Map the points on screen to complex plane [min_x,max_x] x [min_y, max_y] 
				# with  min * (1-t) + max * t where t = a/X etc
				j = complex(max_x * ((float)(a)/X) + min_x * (1-((float)(a)/X)), max_y * ((float)(b)/Y) + min_y * (1-((float)(b)/Y)))
				i = complex(max_x * ((float)(a)/X) + min_x * (1-((float)(a)/X)), max_y * ((float)(b)/Y) + min_y * (1-((float)(b)/Y)))


				# Check how many times we can iterate with max 100
				while abs(i) < 4 and iteration < itmax:
					i=nextMandelbrot(i,j)
					iteration+=1
				
				color = 255*iteration/itmax
				pygame.draw.line(screen, (color,0,255-color), [a,b],[a+1,b],1)
			
			pygame.display.flip()
	
		# Stop drawing
		draw_ready=True
