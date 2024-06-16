import pyautogui
import time
import random
import cv2
import pytesseract
import numpy as np
import math

# 1 - intrare torghast
# 7 - intrare skoldus

def read_folder(coord_file_name):
    with open(coord_file_name, "r") as file:
        vector = [line.strip() for line in file]
    return vector
def read_screen_area(left, top, width, height):
    screenshot = pyautogui.screenshot()
    
    img_np = np.array(screenshot)
    
    area = (left, top, left + width, top + height)
    cropped_image = img_np[area[1]:area[3], area[0]:area[2]]
    
    grayscale_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    
    text = pytesseract.image_to_string(grayscale_image)
    return text.strip()

def read_current_location():
    left = 1023
    top = 810
    width = 1134 - left
    height = 835 - top

    text = read_screen_area(left, top, width, height)
    return text
def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    angle = math.degrees(math.atan2(dy, dx))
    angle = (angle + 360 + 90) % 360

    return angle
def calculate_distance(a,b):
    distance = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    return distance
def remake_vector(vector):
    vector2 = []
    for element in vector:
        coords = []
        i=0
        while i < len(element):
            coords.append([float(element[i:i+5]),float(element[i+6:i+11])])
            i = i + 14
        vector2.append(coords)
    return vector2
def verify(nodes=[]):
    for el in nodes[0:len(nodes)-2]:
        if nodes[len(nodes)-1] == el:
            return False
    return True
def pathfinding(nodes,start_position,end_position):
    closest = nodes[0][0]
    for element in nodes:
        step = element[0]
        if calculate_distance(closest,start_position) > calculate_distance(step,start_position):
            closest = step
    path = []
    path.append(closest)
    i=0
    while path[len(path)-1] != end_position or len(path) == 0:
        for element in nodes:
            if element[0] == path[len(path)-1]:
                step = element
        if len(step) > 1:
            closest = step[1]
            for element in step[1:]:
                if calculate_distance(closest,end_position) > calculate_distance(element,end_position) and verify(nodes) == True:
                    closest = element
                    step.remove(closest)
        else:
            path.pop(len(path)-1)
        path.append(closest)
        if i==4:
            return path
        i=i+1
    return path
    #nu verifica daca end_position face parte din nodes
    #nu schimba ruta si nu verifica sa nu mearga in cerc
    
        

#time.sleep(2)

#reading the nodes
coord_file_name = "torghast_coords.txt"
vector = read_folder(coord_file_name)
vector = remake_vector(vector)

#initialization of the start and goal
current_location = '17.03, 47.10' #read_current_location()
start_position = [float(current_location[0:5]) , float(current_location[7:12])]
end_position = [50.00, 27.00]

print(pathfinding(vector,start_position,end_position))


#while path[len(path)-1] != end_position :
    

