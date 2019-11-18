import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
import cv2

def getIntersetion(l1, l2, toPrint = False):
	def lineParams(p1, p2):
		if(p1[0] == p2[0]):
			raise("You can't take lines parallel to the image plane")
		m = (p1[1] - p2[1])/(p1[0] - p2[0])
		c = p1[1] - m * p1[0]
		return [m , c]
	def lines(params):
		return "y = " + str(params[0]) + "*x + " + str(params[1])
	def intersectionPoints(par1, par2):
		if(par1[0] == par2[0]):
			raise("the lines shouldn't be parallel!!!")		
		x = (par1[1] - par2[1])/(par2[0] - par1[0])
		y = par1[0]*x + par1[1]
		return (x, y)
	params1 = lineParams(l1[0], l1[1])
	params2 = lineParams(l2[0], l2[1])
	if(toPrint):
		print("The first line equation is " + lines(params1))
		print("The second line equation is " + lines(params2))
		print("------------------------------------------------------------------------------------------")
	return intersectionPoints(params1, params2)


def getVanishingPoints(nLines = 4):
	plt.title("Click the start and end cordinates for "+str(nLines//2)+" set of parallel lines(Total " +str(nLines)+" lines).")
	points = plt.ginput(nLines*2)
	vanishingPoints = []
	for i in range(0, len(points), nLines):
		A1 = points[i]
		A2 = points[i+1]
		B1 = points[i+2]
		B2 = points[i+3]
		plt.plot([A1[0], A2[0]], [A1[1], A2[1]], marker = 'o')
		plt.plot([B1[0], B2[0]], [B1[1], B2[1]], marker = 'o')
		vanishingPoints.append(getIntersetion([A1, A2], [B1, B2], True))
	return vanishingPoints

def getPointsForObj():
	points = plt.ginput(n = 2, timeout = 0)
	top = points[0]
	bottom = points[1]
	plt.plot([top[0], bottom[0]], [top[1], bottom[1]], marker = 'o')
	return top, bottom

def getHeight(height, refTop, refBottom, heightPlt):
	return height * (np.linalg.norm(np.array(heightPlt)-np.array(refBottom))*1.0/np.linalg.norm(np.array(refTop)-np.array(refBottom)))

image = scipy.misc.imread("img.jpg")
N = int(input("Enter the number of objects for which you want to get the height: "))
plt.imshow(image)
vanishingPoints = getVanishingPoints()
plt.imshow(image)
plt.title("Click the coordinates for the pole(ref obj) (Top - Bottom)")
pole_top, pole_bottom = getPointsForObj()
poleHeight = 1.65
heights = ""
for i in range(1, N+1):
	plt.title("Click the coordinates of the obj-"+str(i)+" for which height is to be calculated (Top - Bottom)")
	obj_top, obj_bottom = getPointsForObj()

	vlPoint = getIntersetion([pole_bottom, obj_bottom], [vanishingPoints[0], vanishingPoints[1]])
	toGetHeightPlt = getIntersetion([pole_top, pole_bottom], [obj_top, vlPoint])
	
	plt.plot([vlPoint[0], toGetHeightPlt[0]], [vlPoint[1], toGetHeightPlt[1]], marker = 'o')
	plt.plot([obj_bottom[0], vlPoint[0]], [obj_bottom[1], vlPoint[1]], marker = 'o')
	plt.plot([obj_top[0], vlPoint[0]], [obj_top[1], vlPoint[1]], marker = 'o')

	objHeight = getHeight(poleHeight, pole_top, pole_bottom, toGetHeightPlt)
	print("Height of the obj"+str(i)+" : " + str(objHeight))
	heights += "Height of obj-" + str(i) + ": " + str(objHeight) + "\n"

print("\n----------------------------------------------------\n")
forCameraHeight = getIntersetion([pole_bottom, pole_top], [vanishingPoints[0], vanishingPoints[1]])
cameraHeight = getHeight(poleHeight, pole_top, pole_bottom, forCameraHeight)
print("Height of camera : "+ str(cameraHeight))
heights += "Height of camera"+ ": " + str(cameraHeight) + "\nThe dotted line is the vanishing line"
plt.title("")
plt.text(0, 0, heights)
plt.plot([vanishingPoints[0][0], vanishingPoints[1][0]], [vanishingPoints[0][1], vanishingPoints[1][1]], color='red', marker = 'o', linestyle='dashed')
plt.show()