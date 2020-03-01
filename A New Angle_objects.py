##############################################################################
## Design:																	##
## - Block 1: 100ms views, give verbal estimate of target distance			##
## - 10 sec view of empty room (+ human avatars for familiar size)			##
## - Block 2: 100ms views, give verbal estimate of target distance			##
## - Block 3: 5000ms views, give verbal estimate of target distance			##									
##############################################################################	

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


#Oculus setup code
hmd = oculus.Rift()
viz.link(hmd.getSensor(), viz.MainView)
viz.MainView

viz.setMultiSample(8)
viz.go()

viz.clearcolor(.5,.5,.5)

#For testing without headset
#view = viz.MainView
#view.eyeheight(1.65)

# Setup navigation node and link to main view
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
viewLink.preMultLinkable(hmd.getSensor())

#Oculus will automatically sense the height of the participant and adjust the view
profile = hmd.getProfile()
global height
height = profile.eyeHeight - .13 #after much testing, this seems to be most accurate to real world height
navigationNode.setPosition([0,height,0])

# Setup heading reset key
KEYS = { 'reset': 'r'}
vizact.onkeydown(KEYS['reset'], hmd.getSensor().reset)

def participantInfo():
	#Add an InfoPanel with a title bar
	participantInfo = vizinfo.InfoPanel('',title='Participant Information',align=viz.ALIGN_CENTER, icon=False)

	#Add ID field
	textbox_id = participantInfo.addLabelItem('ID',viz.addTextbox())
	participantInfo.addSeparator(padding=(10,10))
	
	#Add eye height field
	textbox_EH = participantInfo.addLabelItem('Eye Height (m)',viz.addTextbox())
	participantInfo.addSeparator(padding=(10,10))
	
	#Add age field
	textbox_age = participantInfo.addLabelItem('Age',viz.addTextbox())
	participantInfo.addSeparator(padding=(10,10))

	#Add gender field
	radiobutton_male = participantInfo.addLabelItem('Male',viz.addRadioButton(0))
	radiobutton_female = participantInfo.addLabelItem('Female',viz.addRadioButton(0))
	radiobutton_other = participantInfo.addLabelItem('Non-Binary',viz.addRadioButton(0))
	participantInfo.addSeparator()
	
	#Add units field
	radiobutton_feet = participantInfo.addLabelItem('Feet',viz.addRadioButton(1))
	radiobutton_meters = participantInfo.addLabelItem('Meters',viz.addRadioButton(1))
	participantInfo.addSeparator()

	#Add submit button aligned to the right and wait until it's pressed
	submitButton = participantInfo.addItem(viz.addButtonLabel('Submit'),align=viz.ALIGN_RIGHT_CENTER)
	yield viztask.waitButtonUp(submitButton)

	#Collect participant data
	global data
	data = viz.Data()
	data_id = textbox_id.get()
	data_EH = textbox_EH.get()
	data_age = textbox_age.get()
	
	if radiobutton_male.get() == viz.DOWN:
		data.gender = 'm'
	elif radiobutton_female.get()==viz.DOWN:
		data.gender = 'f'
	else:
		data.gender = 'nb'
		
	if radiobutton_feet.get() == viz.DOWN:
		data.units = 'ft'
	else:
		data.units = 'm'	

	participantInfo.remove()

	global IDNum
	IDNum = int(data_id)
	print IDNum
	global age
	age = float(data_age)
	global EHNum
	EHNum = float(data_EH)
	print age
	print EHNum
	print data.gender
	print data.units
	
#open data file & record par data
def Data ():
	global datafile
	datafile = open("NewAngleData/%d.txt" % (IDNum), "w")
	datafile.write("Participant %d " % (IDNum))
	datafile.write('\n')
	datafile.write("Age EyeHeight Gender Units")
	datafile.write('\n')
	datafile.write("%d " % (age))
	datafile.write("%d " % (EHNum))
	datafile.write("%s " % (data.gender))
	datafile.write("%s" % (data.units))

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
global ground
ground = vizshape.addPlane(size=[10,45]) #set constant size of 10 m wide, 45 m deep. Extra 5m in depth allows for 5m to extend behind participants' view
ground.setPosition(0,0,17.5) #set constant position to begin at viewpoint and set z dimension so 5m is behind participant view and 40m extends in front
ground.texture(carpet)
ground.disable(viz.RENDERING)

global farwall
farwall = vizshape.addPlane(size=[10,2.69], axis = vizshape.AXIS_Z, cullFace=False) #set default size to 2.69m tall by 10 m wide, aligned with Z axis
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
ceiling = vizshape.addPlane(size=[10,45], cullFace=False) #set constant size of 10 m wide by 40 m deep, 5 m behind participant
ceiling.setPosition(0,2.69,17.5) #set constant position of 2.69 m high, with 40 m in front of participant and 5m behind (matching ground)
ceiling.texture(plaster)
ceiling.disable(viz.RENDERING)

global backwall
backwall = vizshape.addPlane(size=[10,2.69], axis = vizshape.AXIS_Z, cullFace=False) #set default size to 2.69m tall by 10 m wide, aligned with Z axis
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
	
#Practice
def practice ():
	practice_text = viz.addText3D('Practice trials',pos = [-2.5,1.7,20])
	practice_text.color(0,0,0)
	yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
	practice_text.remove()
	targets = [5,12,24]
	while len(targets)>0:
		global k
		k = 0
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
		if targ == 5:
			size = .102012
		if targ == 12:
			size = .24483
		if targ == 24:
			size = .48966
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
			x = random.choice([0,90,180])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		for z in np.asarray(R_people):
			x = random.choice([0,180,270])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)
		targets.remove(targ)	
		en_env()
		tic = time.time()
		yield viztask.waitTime(.01) #this is necessary to keep the headset display on for the duration of time.sleep. Can't use time.sleep for any longer than 100 ms or so bc it pauses tracking
		time.sleep(.09) #this is necessary to be as precise as possible in the display time. Still not perfect bc of unknown processing time of background functions
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
		viz.callback(viz.KEYDOWN_EVENT,KeyEvents)#press Enter (main keyboard) if the participant misses the target and the target will be appended back into the list. 
		yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
		if k == 1:
			targets.append(targ)
		
		
def Block1 ():	
	datafile.write('\n')
	datafile.write('Block1')
	global dum
	dum = random.choice([2.5,3.5,38])
	targets = [4.8,6.2,7.6,9,10.4,11.8,13.2,14.6,17.4,20.2,23,25.8,30,float(dum),float(dum)]
	while len(targets)>0:
		global k
		k = 0
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
		datafile.write('\n')
		datafile.write('%f' % (targ))
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
			x = random.choice([0,90,180])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		for z in np.asarray(R_people):
			x = random.choice([0,180,270])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)
		targets.remove(targ)	
		en_env()
		tic = time.time()
		yield viztask.waitTime(.01)
		time.sleep(.09) 
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
		datafile.write(' %f' % (toc - tic))
		viz.callback(viz.KEYDOWN_EVENT,KeyEvents)
		yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
		if k == 1:
			targets.append(targ)
			datafile.write(' targ missed')
			

def Block2 ():
	datafile.write('\n')
	datafile.write('Block2')
	global dum2
	if dum == 2.5:
		dum2 = random.choice([3.5,38])
	if dum == 38:
		dum2 = random.choice([2.5,3.5])
	if dum == 3.5:
		dum2 = random.choice([2.5,38])
	targets = [4.8,6.2,7.6,9,10.4,11.8,13.2,14.6,17.4,20.2,23,25.8,30,float(dum2),float(dum2)]
	while len(targets)>0:
		global k
		k = 0
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
		datafile.write('\n')
		datafile.write('%f' % (targ))
		sphere = vizshape.addSphere((size),20,20)
		sphere.color(1.02,.444,0)
		sphere.setPosition([0,(size),(targ)])
		shadow = vizshape.addCircle((size),20)
		shadow.color([.05,.05,.05])
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
			x = random.choice([0,90,180])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		for z in np.asarray(R_people):
			x = random.choice([0,180,270])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)
		targets.remove(targ)	
		en_env()
		tic = time.time()
		yield viztask.waitTime(.01) 
		time.sleep(.09) 
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
		datafile.write(' %f' % (toc - tic))
		viz.callback(viz.KEYDOWN_EVENT,KeyEvents)  
		yield viztask.waitKeyDown(viz.KEY_KP_ENTER)		
		if k == 1:
			targets.append(targ)
			datafile.write(' targ missed')
		
def Block3 ():
	datafile.write('\n')
	datafile.write('Block3')
	global dum3
	if dum == 2.5 and dum2 == 3.5:
		dum3 = 38
	if dum == 2.5 and dum2 == 38:
		dum3 = 3.5
	if dum == 3.5 and dum2 == 2.5:
		dum3 = 38
	if dum == 3.5 and dum2 == 38:
		dum3 = 2.5
	if dum == 38 and dum2 == 2.5:
		dum3 = 3.5
	if dum == 38 and dum2 == 3.5:
		dum3 = 2.5
	targets = [4.8,6.2,7.6,9,10.4,11.8,13.2,14.6,17.4,20.2,23,25.8,30,float(dum3),float(dum3)]
	while len(targets)>0:
		global k
		k = 0
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
		P1 = random.choice([-3.75,-2.75,-1.75,.75,1.75,2.75,3.75,5.25])
		P2 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
		P3 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
		L_people = []
		L_people.append(P1)
		L_people.append(P2)
		L_people.append(P3)
		P4 = random.choice([-3.75,-2.75,-1.75,.75,1.75,2.75,3.75,5.25])
		P5 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
		P6 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
		R_people = []
		R_people.append(P4)
		R_people.append(P5)
		R_people.append(P6)
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
		datafile.write('\n')
		datafile.write('%f' % (targ))
		sphere = vizshape.addSphere((size),20,20)
		sphere.color(1.02,.444,0)
		sphere.setPosition([0,(size),(targ)])
		shadow = vizshape.addCircle((size),20)
		shadow.color([.05,.05,.05]) 
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
			object = random.choice([1,2,3])
			if object == 1:
				x = random.choice([0,90,180])
				person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
				person.setPosition([-4.25,0,float(z)])
				person.state(1)
				people.append(person)
			if object == 2:
				x = random.choice([0,90,180])
				person = viz.addAvatar('vcc_male.cfg',euler=(float(x),0,0))
				person.setPosition([-4.25,0,float(z)])
				person.state(1)
				people.append(person)
			if object == 3:
				x = random.choice([0,90,180])
				person = viz.addAvatar('vcc_male2.cfg',euler=(float(x),0,0))
				person.setPosition([-4.25,0,float(z)])
				person.state(1)
				people.append(person)
		for z in np.asarray(R_people):
			object = random.choice([1,2,3])
			if object == 1:
				x = random.choice([0,180,270])
				person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
				person.setPosition([4.5,0,float(z)])
				person.state(1)
				people.append(person)
			if object == 2:
				x = random.choice([0,180,270])
				person = viz.addAvatar('vcc_male.cfg',euler=(float(x),0,0))
				person.setPosition([4.5,0,float(z)])
				person.state(1)
				people.append(person)
			if object == 3:
				x = random.choice([0,180,270])
				person = viz.addAvatar('vcc_male2.cfg',euler=(float(x),0,0))
				person.setPosition([4.5,0,float(z)])
				person.state(1)
				people.append(person)
		targets.remove(targ)
		en_env()
		tic = time.time()
		yield viztask.waitTime(5.5) #Actually is closer to 5 seconds 
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
		datafile.write(' %f' % (toc - tic))
		viz.callback(viz.KEYDOWN_EVENT,KeyEvents)  
		yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
		if k == 1:
			targets.append(targ)
			datafile.write(' targ missed')
			
		
def view ():
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
	P1 = random.choice([-3.75,-2.75,-1.75,.75,1.75,2.75,3.75,5.25])
	P2 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
	P3 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
	L_people = []
	L_people.append(P1)
	L_people.append(P2)
	L_people.append(P3)
	P4 = random.choice([-3.75,-2.75,-1.75,.75,1.75,2.75,3.75,5.25])
	P5 = random.choice([9.25,10.25,11.25,12.25,18.25,19.25,20.25,21.25])
	P6 = random.choice([27.25,28.25,29.25,30.25,36.25,37.25,38.25,39.25])
	R_people = []
	R_people.append(P4)
	R_people.append(P5)
	R_people.append(P6)
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
		object = random.choice([1,2,3])
		if object == 1:
			x = random.choice([0,90,180])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		if object == 2:
			x = random.choice([0,90,180])
			person = viz.addAvatar('vcc_male.cfg',euler=(float(x),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
		if object == 3:
			x = random.choice([0,90,180])
			person = viz.addAvatar('vcc_male2.cfg',euler=(float(x),0,0))
			person.setPosition([-4.25,0,float(z)])
			person.state(1)
			people.append(person)
	for z in np.asarray(R_people):
		object = random.choice([1,2,3])
		if object == 1:
			x = random.choice([0,180,270])
			person = viz.addAvatar('vcc_female.cfg',euler=(float(x),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)
		if object == 2:
			x = random.choice([0,180,270])
			person = viz.addAvatar('vcc_male.cfg',euler=(float(x),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)
		if object == 3:
			x = random.choice([0,180,270])
			person = viz.addAvatar('vcc_male2.cfg',euler=(float(x),0,0))
			person.setPosition([4.5,0,float(z)])
			person.state(1)
			people.append(person)	
	en_env()
	tic = time.time()
	yield viztask.waitTime(10.5)
	toc = time.time()
	dis_env()	
	print 'View length: ', (toc-tic)
	for door in np.asarray(doors):
		door.remove()
	for person in np.asarray(people):
			person.remove()
		
def KeyEvents(key):
	global k
	if key == viz.KEY_RETURN:
		k += 1
		print 'targ appended'

def experiment ():
	yield participantInfo ()
	yield calibrate ()
	yield Data ()
	yield practice ()
	wait_text = viz.addText3D('Please wait for instructions.',pos = [-6,1.7,30])
	wait_text.color(0,0,0)
	yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
	wait_text.remove()
	exp_text = viz.addText3D('Get ready to start the experiment!',pos = [-6,1.7,30])
	exp_text.color(0,0,0)
	yield viztask.waitTime(2)
	exp_text.remove()
	yield Block1 ()
	end_block1 = viz.addText3D('End of the first block of trials. Please wait for instructions.',pos = [-12,1.7,35])
	end_block1.color(0,0,0)
	yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
	end_block1.remove ()
	yield viztask.waitTime(1)
	yield view ()
	start_block2 = viz.addText3D('Beginning second block of trials. Please wait for instructions.',pos = [-12,1.7,35])
	start_block2.color(0,0,0)
	yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
	start_block2.remove()
	yield viztask.waitTime(1)
	yield Block2 ()
	end_block2 = viz.addText3D('End of the second block of trials. Please wait for instructions.',pos = [-12,1.7,35])
	end_block2.color(0,0,0)
	yield viztask.waitKeyDown(viz.KEY_KP_ENTER)
	end_block2.remove ()
	yield viztask.waitTime(1)
	yield Block3 ()
	datafile.close()
	end_text = viz.addText3D('Please wait for instructions',pos = [-6,1.7,30])
	end_text.color(0,0,0)

viztask.schedule(experiment())