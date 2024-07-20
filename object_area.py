#conda for better managing of installed packages, prevent dependency errors (when other packages are incompatible with one trying to install)
#installed pyTorch, underlying framework upon which ultralytics (YOLO model) is built 
#installed selenium, scrape images from the internet

import numpy as np
import matplotlib.pyplot as plt
import ultralytics
import cv2

from train import train

class mask_areas:
    def __init__(self, model, image_path):
        self.model = model
        self.image_path = image_path
        self.mask_areas_list = [] #list contains areas of each object/mask
    
    def check():
        ultralytics.checks()
        
    def predict(self):
        results = self.model.predict(self.image_path) #length of "results" is the number of pictures given to the model, NOT number of boxes
        result = results[0]

        #Return list of what classes were detected
        classes = []
        for box in (result.boxes):
            if box.conf.item()>=0.3:
                classes.append(result.names[box.cls.item()])
        return classes

    def picture(self, name):
        #Generate labeled picture
        self.model(self.image_path, conf = 0.3, save = True, project = "yolov8n-seg_picture-result")
        img = cv2.imread(f"yolov8n-seg_picture-result\\predict\\{name}")
        cv2.imshow('Result of Instance Segmentation', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def plot_masks(self, show):    
         #Load pre-trained model to generate labeled picture
        results = self.model(self.image_path, save = False, project = "yolov8n-seg_picture-result")
        result = results[0] #result is a list that contains information about each object detected
        
        #scale the axis in matplotlib
        x_axis, y_axis = self.scale_axis(result)
        
        #plot in matplotlib
        print("results", len(result))
        for i, _ in enumerate(result):
            #only graph if confidence score is high enough
            if result.boxes[i].conf.item() > 0.3:
                #get x and y coordinates of boundary of mask (segmentation result)
                x_coordinates = [pair[0] for pair in result.masks.xy[i]] #result.masks.xy contains mask boundaries of all objects detected
                y_coordinates = [pair[1] for pair in result.masks.xy[i]]

                #calculate area of this mask
                self.mask_areas_list.append(self.mask_area(x_coordinates, y_coordinates, result.names[result.boxes[i].cls.item()]))
                
                #plot the coordinates
                plt.plot(x_coordinates, y_coordinates, linewidth=2, marker='o', markersize=1, label='Mask Boundary')
            
                plt.xlabel('x coordinates')
                plt.ylabel('y coordinates')
                plt.title(self.predict())
        if show:
            plt.show()
        
    def calculate_percentages(self): 
        #calculate what percent of total area (sum of area of all objects) each object takes up
        #first run plot masks to set a value for mask_areas_list
        self.plot_masks(False) 
        object_areas = [area[1] for area in self.mask_areas_list]
        object_names = [name[0] for name in self.mask_areas_list]
        percentages = []
        total_area = np.sum(object_areas)
        
        for i, area in enumerate(object_areas):
            percentages.append(area/total_area)
        return list(zip(object_names, percentages))
            
    
    def mask_area(self, x_coordinates, y_coordinates, object):
        mask_area = self.shoelace(x_coordinates, y_coordinates)
        return str(object), float(mask_area)
        
    def scale_axis(self, result):
        #scale the axis
        image_dimensions = result.orig_shape
        x_axis = image_dimensions[1]
        y_axis = image_dimensions[0]
        plt.xlim(0, x_axis)
        plt.ylim(0, y_axis)
        plt.gca().invert_yaxis()
        return x_axis, y_axis
        
    def shoelace(self, x_coordinates, y_coordinates): #utilize shoelace theorem to find area (in pixels/units) of objects shoelace theorem uses each vertice of the object on a coordinate plane to find its area in units
        # A = 1/2 |(x1y2 + x2y3 + ... + xn-1yn + xny1) - (y1x2 + y2x3 + ... + yn-1xn + ynx1)|
        # let a = (x1y2 + x2y3 + ... + xn-1yn + xny1), let b = (y1x2 + y2x3 + ... + yn-1xn + ynx1)
        # A = 1/2 |a-b|
        x_coordinates_a = np.array(x_coordinates)
        y_coordinates_a = np.array(y_coordinates[1:] + [y_coordinates[0]])
        x_coordinates_b = np.array(x_coordinates[1:] + [x_coordinates[0]])
        y_coordinates_b = np.array(y_coordinates)
        a = np.sum(x_coordinates_a * y_coordinates_a)
        b = np.sum(x_coordinates_b * y_coordinates_b)
        area = (np.abs(a-b)/2)
        return area

if __name__ == "__main__": 
    trainer = train()
    model = trainer.get_model()
    image = str(input("Enter image name (include .jpg): "))
    image_dir = 'Training_files\\Raw_imgs\\' + image
    mask_areas = mask_areas(model, image_dir)
    mask_areas.picture()
    print(mask_areas.predict())
    print(mask_areas.calculate_percentages())






