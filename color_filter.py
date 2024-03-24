import cv2
import numpy as np

#purpose to make edges of objects more defined
class filter:
    def saturate(self, img_path):
        # Load the image
        image = cv2.imread(img_path)
        #save original copy of image
        cv2.imwrite(f'{img_path[0:img_path.find(".")]}_originalCopy.jpg',image)

        # Convert the image from BGR to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Increase the saturation
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1.80, 0, 255).astype(np.uint8)
        #hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1.80, 0, 255).astype(np.uint8)
        
        # Convert the image back to BGR
        saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        
        # Split the image into its channels
        b, g, r = cv2.split(saturated_image)
        # Apply a contrast enhancement or saturation adjustment to the red channel
        enhanced_r = np.clip(r * 1.1, 0, 255).astype(np.uint8)
        # Merge the channels back together
        enhanced_image = cv2.merge((b, g, enhanced_r))
        
        print('Saturated')
        cv2.imwrite(img_path, enhanced_image)
        cv2.imshow('Original', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow('Enhanced', enhanced_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    filter = filter()
    filter.saturate('C:\\Daniel\\Nutrition YOLO\\Training_files\\Raw_imgs\\banana2.jpg')
    
