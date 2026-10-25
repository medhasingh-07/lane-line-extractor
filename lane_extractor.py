import cv2
import numpy as np

print("Lane Detection Program")
image_path = input("Enter image filename (e.g. road.jpg)")

image = cv2.imread(image_path)
if image is None:
	print("Couldnt find the image.")
	exit()

height, width = image.shape[:2]
print(f"Loaded image Resolution = {width}X{height}")
cv2.imwrite("original_image.jpg", image)
print("Image loaded successfully")

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_white= np.array([0,0,150], dtype = np.uint8)
upper_white = np.array([180, 50, 255], dtype = np.uint8)
white_mask = cv2.inRange(hsv_image, lower_white, upper_white)

lower_yellow = np.array([10,50,80],dtype = np.uint8)
upper_yellow = np.array([40,255,255], dtype = np.uint8)
yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

combined_mask = cv2.bitwise_or(white_mask,yellow_mask)
color_filtered = cv2.bitwise_and(image, image, mask=combined_mask)

cv2.imwrite("color_filtered.jpg", color_filtered)
print("Filtered out all colors but white and yellow lines")

 
gray = cv2.cvtColor(color_filtered, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5),0)
cv2.imwrite("blurred_image.jpg", blur)
print("Smoothes out the edges")

edges = cv2.Canny(blur, 100,200)
cv2.imwrite("canny_edges.jpg", edges)
print("Edge Detection done")


road_polygon = np.array([
[int(width*0.05) , height],
[int(width*0.40), int(height*0.50)], 
[int(width*0.60), int(height*0.50)], 
[int(width*0.95), height]
], dtype=np.int32)
mask=np.zeros_like(edges)
cv2.fillPoly(mask,[road_polygon], 255)
final= cv2.bitwise_and(edges,mask)
cv2.imwrite("roi.jpg", final)
print("Dynamic Region of Interest")
