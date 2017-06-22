""" A python program to calculate how much percentage of a hollow shape does a solid image correctly fill """
import cv2
import os
import time
t0 = time.time()

image_A = "Layer001b.jpg"
image_B = "Layer002b.jpg"
mask_1 = "Mask001"
mask_2 = "Mask002"

def process():
    global image_A, image_B, mask_1, mask_2

    os.system("convert %s -morphology Close Disk abc.jpg" % image_A) # Closing any holes in the background
    os.system("convert %s -morphology Close Disk pqr.jpg" % image_B) 
    os.system("convert abc.jpg -median 15 abc.jpg") # Applying median filtering of radius 15 to remove remaining noise
    os.system("convert pqr.jpg -median 15 pqr.jpg")
    os.system("convert abc.jpg -blur x1 -threshold 50% abc.jpg") # Smoothing edges (radius: area under consideration when applying blur x sigma: how much you want to spread a pixel)and binarizing image to remove any light noise remaining
    os.system("convert pqr.jpg -blur x1 -threshold 50% pqr.jpg")
    os.system("convert abc.jpg -trim trim.jpg") # trim image to remove any cluster of pixels of same intensity and limit to only image   
    os.system("convert pqr.jpg -trim trim3.jpg")

    os.system("convert %s.svg -alpha off -fill red -opaque white %sb.svg" % (mask_1, mask_1)) # Make bg & fg red keeping image border white
    os.system("convert %s.svg -alpha off -fill red -opaque white %sb.svg" % (mask_2, mask_2))
    # Make the entire image yellow (area within image will not be affected), then change color inside image from red to black 
    os.system("convert %sb.svg -alpha off -fill yellow -draw 'color 0,0 floodfill' -fill black -opaque red %sb.jpg" % (mask_1, mask_1))
    os.system("convert %sb.svg -alpha off -fill yellow -draw 'color 0,0 floodfill' -fill black -opaque red %sb.jpg" % (mask_2, mask_2))
    # Make all the yellow portion of the image white (filled black image on white background)
    os.system("convert %sb.jpg -alpha off -fill yellow -draw 'color 0,0 floodfill' -fill white -opaque yellow %sb.jpg" % (mask_1, mask_1))
    os.system("convert %sb.jpg -alpha off -fill yellow -draw 'color 0,0 floodfill' -fill white -opaque yellow %sb.jpg" % (mask_2, mask_2))
    # Apply median filtering of radius 15 to remove noise
    os.system("convert %sb.jpg -median 15 %sb.jpg" % (mask_1, mask_1))
    os.system("convert %sb.jpg -median 15 %sb.jpg" % (mask_2, mask_2))
    # smooth the image edges and binarize it to remove any light noise, then trim it to remove any wasted space and put image properties within a text file to extract dimensions later
    os.system("convert %sb.jpg -blur x1 -threshold 50%% %sb.jpg" % (mask_1, mask_1))
    os.system("convert %sb.jpg -trim trim2.jpg" % mask_1)
    os.system("identify trim2.jpg > abc.txt")
    os.system("convert %sb.jpg -blur x1 -threshold 50%% %sb.jpg" % (mask_2, mask_2)) 
    os.system("convert %sb.jpg -trim trim4.jpg" % mask_2)
    os.system("identify trim4.jpg > pqr.txt")
    f1 = open("abc.txt", 'r')
    f2 = open("pqr.txt", 'r')
    l1 = f1.readlines() # Getting identification data from text files
    l2 = f2.readlines()
    f1.close()
    f2.close()
    dim1 = l1[0].split()[2] # Getting the dimensions of trim2.jpg and trim4.jpg
    dim2 = l2[0].split()[2] 
    os.system("convert -resize %s trim.jpg trim.jpg" % dim1) 
    os.system("convert -resize %s trim3.jpg trim3.jpg" % dim2)
    

def similarity():
    global t0
    image_1 = 'trim.jpg'
    image_2 = 'trim2.jpg'
    image_3 = 'trim3.jpg'
    image_4 = 'trim4.jpg'
    
    image1 = cv2.imread(image_1, 0)
    image2 = cv2.imread(image_2, 0)
    image3 = cv2.imread(image_3, 0)
    image4 = cv2.imread(image_4, 0)

    hist1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0, 256])
    hist3 = cv2.calcHist([image3], [0], None, [256], [0, 256])
    hist4 = cv2.calcHist([image4], [0], None, [256], [0, 256])

    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    hist3 = cv2.normalize(hist3, hist3).flatten()
    hist4 = cv2.normalize(hist4, hist4).flatten()

    d = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    e = cv2.compareHist(hist3, hist4, cv2.HISTCMP_BHATTACHARYYA)
    d = (1-d)*100
    e = (1-e)*100
    print(d,e)
    print("-----Time taken: ", time.time()-t0, " seconds-----")
      
if __name__ == "__main__":
    process()
    similarity()
    
