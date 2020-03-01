import viz
import vizact
import vizinfo
import viztask
import numpy
import numpy as np
import random
from random import *
from numpy import random
from numpy import array
import vizshape
import vizfx
import vizinfo
import oculus
import time
import projector
import statistics
from statistics import mean

#Oculus setup code
hmd = oculus.Rift()
viz.link(hmd.getSensor(), viz.MainView)
viz.MainView

viz.setMultiSample(8)
viz.go()

#Get RGB value for image and divide number by 250 to get the proportion of that color 
viz.clearcolor(.5,.5,.5)

# Setup navigation node and link to main view
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
viewLink.preMultLinkable(hmd.getSensor())

#Oculus will automatically sense the height of the participant and adjust the view
profile = hmd.getProfile()
global height
height = profile.eyeHeight - .13 
navigationNode.setPosition([0,height,0])

# Setup heading reset key
KEYS = { 'reset': 'r'}
vizact.onkeydown(KEYS['reset'], hmd.getSensor().reset)

#Load textures
plaster = viz.addTexture('CeilingLarge.jpg')
wallpaper = viz.addTexture('WallpaperLarge.jpg')
wallpaperlong = viz.addTexture('WallpaperLong.jpg')
carpet = viz.addTexture('CarpetLarge3.jpg')
wood = viz.addTexture('Door.jpg')
mask_img = viz.addTexture('Masktiny.jpg')

#Create skylight
viz.MainView.getHeadLight().disable()
sky_light = viz.addLight(euler=(0,90,0)) #euler = yaw, pitch, roll
sky_light.position(2,0,-1,0)
sky_light.color(viz.WHITE)
sky_light.intensity(2)

#Create backlight
back_light = viz.addLight(euler=(0,215,0)) #euler = yaw, pitch, roll
back_light.position(-2,0,4,0)
back_light.color(viz.WHITE)
back_light.intensity(.75)

#Create frontlight?
front_light = viz.addLight(euler=(0,45,0)) #euler = yaw, pitch, roll
front_light.position(-2,0,4,0)
front_light.color(viz.WHITE)
front_light.intensity(1.5)

#Creating all parts of scene
#Creating all parts of scene
global ground
ground = vizshape.addPlane(size=[10,45]) #set constant size of 40 m wide, 45 m deep. Extra 5m in depth allows for 5m to extend behind participants' view
ground.setPosition(0,0,17.5) #set constant position to begin at viewpoint and set z dimension so 5m is behind participant view and 40m extends in front
ground.texture(carpet)
ground.disable(viz.RENDERING)

global farwall
farwall = vizshape.addPlane(size=[10,2.69], axis = vizshape.AXIS_Z, cullFace=False) #set default size to 2.69m tall by 40 m wide, aligned with Z axis
farwall.setPosition(0,1.345,40)
farwall.texture(wallpaper)
farwall.disable(viz.RENDERING)

global leftwall
leftwall = vizshape.addPlane(size=[45,2.69], axis = vizshape.AXIS_X, cullFace=False) #set constant size of 40 m deep by 2.69 m high, aligned with X axis
leftwall.setPosition(-5,1.345,17.5)
leftwall.texture(wallpaperlong)
leftwall.disable(viz.RENDERING)

global rightwall
rightwall = vizshape.addPlane(size=[45,2.69], axis = vizshape.AXIS_X, cullFace=False) #set constant size of 40 m deep by 2.69 m high, aligned with X axis
rightwall.setPosition(5,1.345,17.5)
rightwall.texture(wallpaperlong)
rightwall.disable(viz.RENDERING)

global ceiling
ceiling = vizshape.addPlane(size=[10,45], cullFace=False) #set constant size of 40 m wide by 40 m deep
ceiling.setPosition(0,2.69,17.5) #set constant position of 2.69 m high, with 40 m in front of participant and 5m behind (matching ground)
ceiling.texture(plaster)
ceiling.disable(viz.RENDERING)

global backwall
backwall = vizshape.addPlane(size=[10,2.69], axis = vizshape.AXIS_Z, cullFace=False) #set default size to 2.69m tall by 40 m wide, aligned with Z axis
backwall.setPosition(0,1.345,-5)
backwall.texture(wallpaper)
backwall.disable(viz.RENDERING)

global mask
mask = vizshape.addPlane(size=[10,10], axis = vizshape.AXIS_Z, cullFace=False)
mask.setPosition(0,0,2)
mask.texture(mask_img)
mask.disable(viz.RENDERING)

#Defining all constant parts of scene. Positions of walls moved to create different size rooms
def room (): 
	ground 
	farwall 
	leftwall 
	rightwall 
	backwall
	ceiling
	
#Enable environment
def en_env ():
	ground.enable(viz.RENDERING)
	farwall.enable(viz.RENDERING)
	backwall.enable(viz.RENDERING)
	leftwall.enable(viz.RENDERING)
	rightwall.enable(viz.RENDERING)
	ceiling.enable(viz.RENDERING)
	
#Disable environment
def dis_env ():
	ground.disable(viz.RENDERING)
	farwall.disable(viz.RENDERING)
	backwall.disable(viz.RENDERING)
	leftwall.disable(viz.RENDERING)
	rightwall.disable(viz.RENDERING)
	ceiling.disable(viz.RENDERING)

###########################################################################################################################################
## To execute thresholding:
## - Duration will begin at approx 20 ms. After each trial, at the fixation screen, press the up arrow to increase the duration by 10 ms
## - Continue until participant can reliably report the color of the target (no distance)
## - Press the Enter key (main keyboard, not keypad) to go to the next trial
## - Duration will begin at 120 ms. After each trial, press the down arrow key to decrease the duration by 10 ms
## - Continue until participant cannot reliably report the color of the target, then press enter
## - There will be 5 increasing and 5 decreasing trials, alternating one after the other
## - At the end of the trials, the program will calculate the average threshold duration
## - Take this number, round up to the nearest 5 ms and add 10 ms to use as short duration for experiment
###########################################################################################################################################

#Calibrate headset
def calibrate ():
	calibration = viz.addText3D('Please take a moment to calibrate the headset',pos = [-10,(float(height)+3),25])
	calibration.color(0,0,0)
	fixation = viz.addText3D('+',pos = [0,(float(height)),10])
	fixation.color(0,0,0)
	calibration.color(0,0,0)
	adjust = viz.addText3D('Adjust the position of the headset on your face and slide',pos = [-12.5,(float(height)-2.45),25])
	adjust.color(0,0,0)
	lever = viz.addText3D('the lever under your right eye until the plus sign is in focus',pos = [-12.5,(float(height)-4),25])
	lever.color(0,0,0)
	yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
	fixation.remove()
	calibration.remove()
	adjust.remove()
	lever.remove()
	
times = []	

targets = [4.8,6.2,7.6,9,10.4,11.8,13.2,14.6,17.4,20.2,23,25.8,30]
	
def trial_up ():
	global k
	k = 0
	global x
	x = 0
	for i in range (100):
		yield viztask.waitTime(.5)
		ready_text = viz.addText3D('Get ready!',pos = [-2,1.7,20])	
		ready_text.color(0,0,0)
		yield viztask.waitTime(1)
		ready_text.remove ()
		yield viztask.waitTime(2)	
		yield room ()
		doors = []
		D1 = random.choice([-4.25,-3.25,-2.25,-1.25])
		D2 = random.choice([4.75,5.75,6.75,7.75])
		D3 = random.choice([13.75,14.75,15.75,16.75])
		D4 = random.choice([22.75,23.75,24.75,25.75])
		D5 = random.choice([31.75,32.75,33.75,34.75])
		L_doors = []
		L_doors.append(D1)
		L_doors.append(D2)
		L_doors.append(D3)
		L_doors.append(D4)
		L_doors.append(D5)
		D7 = random.choice([-4.25,-3.25,-2.25,-1.25])
		D8 = random.choice([4.75,5.75,6.75,7.75])
		D9 = random.choice([13.75,14.75,15.75,16.75])
		D10 = random.choice([22.75,23.75,24.75,25.75])
		D11 = random.choice([31.75,32.75,33.75,34.75])
		R_doors = []
		R_doors.append(D7)
		R_doors.append(D8)
		R_doors.append(D9)
		R_doors.append(D10)
		R_doors.append(D11)
		people = []
		P1 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
		P2 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
		L_people = []
		L_people.append(P1)
		L_people.append(P2)
		P3 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
		P4 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
		R_people = []
		R_people.append(P3)
		R_people.append(P4)
		targ = random.choice(targets)
		if targ == 2.5:
			size = .051006
		if targ == 3.5:
			size = .071409	
		if targ == 4.8:
			size = .097932
		if targ == 6.2:
			size = .126495
		if targ == 7.6:
			size = .155059
		if targ == 9:
			size = .183622
		if targ == 10.4:
			size = .212186
		if targ == 11.8:
			size = .240749
		if targ == 13.2:
			size = .269313
		if targ == 14.6:
			size = .297876
		if targ == 17.4:
			size = .355003
		if targ == 20.2:
			size = .41213
		if targ == 23:
			size = .469257
		if targ == 25.8:
			size = .526384
		if targ == 30:
			size = .612075
		if targ == 38:
			size = .775295
		print targ
		sphere = vizshape.addSphere((size),20,20)
		sphere.color(1.02,.444,0)
		sphere.setPosition([0,(size),(targ)])
		shadow = vizshape.addCircle((size),20)
		shadow.color([.05,.05,.05]) #proportion of 1 for amount of each color (red, green, blue). 0,0,0 = black, 1,1,1 = white.
		shadow.setEuler([0,90,0])
		shadow.setPosition([0,.001,(targ)])
		for z in np.asarray(L_doors):
			door = vizshape.addBox(size=[.04445,2.13,.91])  
			door.texture(wood)
			door.setPosition([-4.9733,1.065,float(z)])
			doors.append(door)
			doorknob = vizshape.addSphere(radius=.045,axis=vizshape.AXIS_X)
			doorknob.color(viz.YELLOW)
			doorknob.setPosition(-4.9396,1,(float(z)-.3364))
			doors.append(doorknob)
		for z in np.asarray(R_doors):
			door = vizshape.addBox(size=[.04445,2.13,.91])  
			door.texture(wood)
			door.setPosition([4.9683,1.065,float(z)])
			doors.append(door)
			doorknob = vizshape.addSphere(radius=.045,axis=vizshape.AXIS_X)
			doorknob.color(viz.YELLOW)
			doorknob.setPosition(4.9396,1,(float(z)-.3364))
			doors.append(doorknob)	
		for z in np.asarray(L_people):
			o = random.choice([0,90,180])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(o),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		for z in np.asarray(R_people):
			o = random.choice([0,180,270])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(o),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)	
		en_env()
		tic = time.time()
		yield viztask.waitTime(.005) 
		time.sleep(.005+x)
		toc = time.time ()
		mask.enable(viz.RENDERING)
		dis_env()
		sphere.remove ()
		shadow.remove ()
		for person in np.asarray(people):
			person.remove()
		for door in np.asarray(doors):
			door.remove()
		yield viztask.waitTime(1)
		mask.disable(viz.RENDERING)
		print toc - tic
		viz.callback(viz.KEYDOWN_EVENT,KeyEvents)
		yield viztask.waitKeyDown(viz.KEY_KP_ENTER) 
		if k == 1:
			break
	times.append(toc - tic)		
	print times
		
def trial_down ():
	global k
	k = 0
	global x
	x = 0
	for i in range (100):
		yield viztask.waitTime(.5)
		ready_text = viz.addText3D('Get ready!',pos = [-2,1.7,20])	
		ready_text.color(0,0,0)
		yield viztask.waitTime(1)
		ready_text.remove ()
		yield viztask.waitTime(2)	
		yield room ()
		doors = []
		D1 = random.choice([-4.25,-3.25,-2.25,-1.25])
		D2 = random.choice([4.75,5.75,6.75,7.75])
		D3 = random.choice([13.75,14.75,15.75,16.75])
		D4 = random.choice([22.75,23.75,24.75,25.75])
		D5 = random.choice([31.75,32.75,33.75,34.75])
		L_doors = []
		L_doors.append(D1)
		L_doors.append(D2)
		L_doors.append(D3)
		L_doors.append(D4)
		L_doors.append(D5)
		D7 = random.choice([-4.25,-3.25,-2.25,-1.25])
		D8 = random.choice([4.75,5.75,6.75,7.75])
		D9 = random.choice([13.75,14.75,15.75,16.75])
		D10 = random.choice([22.75,23.75,24.75,25.75])
		D11 = random.choice([31.75,32.75,33.75,34.75])
		R_doors = []
		R_doors.append(D7)
		R_doors.append(D8)
		R_doors.append(D9)
		R_doors.append(D10)
		R_doors.append(D11)
		people = []
		P1 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
		P2 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
		L_people = []
		L_people.append(P1)
		L_people.append(P2)
		P3 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
		P4 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
		R_people = []
		R_people.append(P3)
		R_people.append(P4)
		targ = random.choice(targets)
		if targ == 2.5:
			size = .051006
		if targ == 3.5:
			size = .071409	
		if targ == 4.8:
			size = .097932
		if targ == 6.2:
			size = .126495
		if targ == 7.6:
			size = .155059
		if targ == 9:
			size = .183622
		if targ == 10.4:
			size = .212186
		if targ == 11.8:
			size = .240749
		if targ == 13.2:
			size = .269313
		if targ == 14.6:
			size = .297876
		if targ == 17.4:
			size = .355003
		if targ == 20.2:
			size = .41213
		if targ == 23:
			size = .469257
		if targ == 25.8:
			size = .526384
		if targ == 30:
			size = .612075
		if targ == 38:
			size = .775295
		print targ
		sphere = vizshape.addSphere((size),20,20)
		sphere.color(1.02,.444,0)
		sphere.setPosition([0,(size),(targ)])
		shadow = vizshape.addCircle((size),20)
		shadow.color([.05,.05,.05]) #proportion of 1 for amount of each color (red, green, blue). 0,0,0 = black, 1,1,1 = white.
		shadow.setEuler([0,90,0])
		shadow.setPosition([0,.001,(targ)])
		for z in np.asarray(L_doors):
			door = vizshape.addBox(size=[.04445,2.13,.91])  
			door.texture(wood)
			door.setPosition([-4.9733,1.065,float(z)])
			doors.append(door)
			doorknob = vizshape.addSphere(radius=.045,axis=vizshape.AXIS_X)
			doorknob.color(viz.YELLOW)
			doorknob.setPosition(-4.9396,1,(float(z)-.3364))
			doors.append(doorknob)
		for z in np.asarray(R_doors):
			door = vizshape.addBox(size=[.04445,2.13,.91])  
			door.texture(wood)
			door.setPosition([4.9683,1.065,float(z)])
			doors.append(door)
			doorknob = vizshape.addSphere(radius=.045,axis=vizshape.AXIS_X)
			doorknob.color(viz.YELLOW)
			doorknob.setPosition(4.9396,1,(float(z)-.3364))
			doors.append(doorknob)	
		for z in np.asarray(L_people):
			o = random.choice([0,90,180])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(o),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		for z in np.asarray(R_people):
			o = random.choice([0,180,270])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(o),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)	
		en_env()
		tic = time.time()
		yield viztask.waitTime(.01) 
		time.sleep(.09+x)
		toc = time.time ()
		mask.enable(viz.RENDERING)
		dis_env()
		sphere.remove ()
		shadow.remove ()
		for door in np.asarray(doors):
			door.remove()
		for person in np.asarray(people):
			person.remove()
		yield viztask.waitTime(1)
		mask.disable(viz.RENDERING)
		print toc - tic
		viz.callback(viz.KEYDOWN_EVENT,KeyEvents)
		yield viztask.waitKeyDown(viz.KEY_KP_ENTER) 
		if k == 1:
			break
	times.append((toc - tic)+.01)		
	print times
					
def KeyEvents(key):
	global x
	if key == viz.KEY_UP:
		x += .01
		print '+.01'
	if key == viz.KEY_DOWN:
		x -= .01
		print '-.01'
	global k
	if key == viz.KEY_RETURN:
		k += 1
		print 'stop'	
		
def task ():
	yield calibrate ()
	yield trial_up()
	print 'end trial 1'
	yield trial_down()
	print 'end trial 2'
	yield trial_up()
	print 'end trial 3'
	yield trial_down()
	print 'end trial 4'
	yield trial_up()
	print 'end trial 5'
	yield trial_down()
	print 'end trial 6'
	yield trial_up()
	print 'end trial 7'
	yield trial_down()
	print 'end trial 8'
	yield trial_up()
	print 'end trial 9'
	yield trial_down()
	print 'end trial 10'
	average = mean(times)
	print 'Final Threshold:', average
	end_text = viz.addText3D('Please wait for instructions',pos = [-6,1.7,20])
	end_text.color(0,0,0)
	
viztask.schedule(task)		