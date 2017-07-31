# Image-Similarity-Checker
Checks how much percentage of a hollow shape does a solid image correctly fit/resemble
- Uses Python 3.x, OpenCV 3 for python (import cv2) and ImageMagick
- The hollow image and the solid image have same shapes, but can be of different sizes and orientation. The program takes care of that by resizing and de-skewing and also removes noise in both the images if any.
# Usage
Firstly logon to a OpenCV environment:

    workon cv
    
Next, run the program, keeping the image files (both noise and hollow ones) in the same directory as the program:

    python3 imageComparator.py (for Ubuntu)
    python imageComparator.py (for Windows)
    
