import numpy as np
import cv2
import time
from scipy import signal

def SSD(left, right, h, w, halfBlockSize, disparityRange):
    offset_adjust = 255 / disparityRange
    for y in range(halfBlockSize, h - halfBlockSize):    
        if (y%10 == 0):
            print("Image row  " + str(y) +"/" +str(h) +" ( " + str(int(y * 100/h)) + "% )\n")      
        for x in range(halfBlockSize, w - halfBlockSize):
            best_offset = 0
            prev_ssd = 2147483647
            ssds = []
            numBlocks = 0
            for offset in range(disparityRange):               
                block = left[y - halfBlockSize : y+ halfBlockSize , x - halfBlockSize : x+ halfBlockSize]
                template = right[y - halfBlockSize : y+ halfBlockSize  , x - halfBlockSize - offset : x+ halfBlockSize - offset]
                if(template.shape != block.shape):
                    template = np.zeros(block.shape)
                numBlocks += 1
                ssdTemp = block - template
                ssdTemp = ssdTemp ** 2
                ssd = np.sum(ssdTemp)
                ssds.append(ssd)
                if ssd < prev_ssd:
                    prev_ssd = ssd
                    best_offset = offset
            
            depth[y, x] = best_offset * offset_adjust
            
    return depth

def Correlation(left, right, h, w, halfBlockSize, disparityRange):
    offset_adjust = 255 / disparityRange
    for y in range(halfBlockSize, h - halfBlockSize):    
        if (y%10 == 0):
            print("Image row  " + str(y) +"/" +str(h) +" ( " + str(int(y * 100/h)) + "% )\n")      
        for x in range(halfBlockSize, w - halfBlockSize):
            best_offset = 0
            prev_corr = 0
            corrs = []
            numBlocks = 0
            for offset in range(disparityRange):
            	temp = 0
            	corr = 0
            	block = left[y - halfBlockSize : y+ halfBlockSize , x - halfBlockSize : x+ halfBlockSize]
            	template = right[y - halfBlockSize : y+ halfBlockSize  , x - halfBlockSize - offset : x+ halfBlockSize - offset]
            	for i in range(-halfBlockSize,halfBlockSize):
            		for j in range(-halfBlockSize,halfBlockSize):
            			temp = (int(left[y+i,x+j]) - np.mean(block))*(int(right[y+i,x+j - offset]) - np.mean(template))
            			temp /= (np.std(block) * np.std(template))
            			corr += temp
            	corr /= (2*halfBlockSize + 1)
            	corrs.append(corr)
            	if corr > prev_corr:
            		prev_corr = corr
            		best_offset = offset
            
            depth[y, x] = best_offset * offset_adjust
            
    return depth
    
left = cv2.imread("tsukuba1.ppm",0)
right = cv2.imread("tsukuba2.ppm",0)
h, w = left.shape   
depth = np.zeros((h, w), np.uint8)
depth_corr = np.zeros((h, w), np.uint8)

disparityRange = 30
halfBlockSize = 3
blockSize = 2 * halfBlockSize + 1 

start_time_SSD = time.time()
depth = SSD(left, right, h, w, halfBlockSize, disparityRange)
cv2.imwrite("DepthMap_"+str(blockSize)+"_"+str(disparityRange)+"_ssd.png",depth)
time_SSD = time.time() - start_time_SSD
start_time_Corr = time.time()
depth_corr = Correlation(left, right, h, w, halfBlockSize, disparityRange)
cv2.imwrite("DepthMap_"+str(blockSize)+"_"+str(disparityRange)+"_corr.png",depth)
time_Corr = time.time() - start_time_Corr

print("Time taken for SSD is " + str(time_SSD))
print("Time taken for Correlation is " + str(time_Corr))
