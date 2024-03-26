from ultralytics import YOLO
from object_area import mask_areas
from train import train
from edamam_API import edamam
from color_filter import filter

trainer = train() #import trainer
model = trainer.get_model() #inputs previously trained weights into model

class nutrient_analyzer (mask_areas):
    def __init__(self, model, image_path):
        self.edamam = edamam()
        super().__init__(model, image_path)
        
    def predict(self):
        classes = super().predict( )
        class_types = []
        for item in classes:
            if item not in class_types:
                class_types.append(item)
        return class_types
    
    def plot_masks(self, show):
        super().plot_masks(show)
        
    def calculate_percentages_items(self):
        combined_percentages_classes = []
        percentages = super().calculate_percentages()
        class_types = self.predict()
        
        for class_type in class_types:
            total_percent = 0
            for percent in percentages: #percent[1] is the percentage, percent[0] is object associated with the percent
                if percent[0] == class_type:
                    total_percent += float(percent[1])
            combined_percentages_classes.append([class_type, total_percent])
                  
        return combined_percentages_classes #contains each class found in the image, and what percent of the entire meal it is
        
    def calculate_percentages_nutrients(self):
        percentages = self.edamam.find_quantities(self.calculate_percentages_items())
        return percentages
    
    def print_whole_meal_nutrients(self):
        whole_meal_nutrients = (self.calculate_percentages_nutrients())[1]
        protein = f"Total protein: {whole_meal_nutrients[0]}% of your meal"
        fat = f"Total fat: {whole_meal_nutrients[1]}% of your meal"
        carb = f"Total carbohydrates: {whole_meal_nutrients[2]}% of your meal"
        sugar = f"Total sugar: {whole_meal_nutrients[3]}% of your meal"
        fiber = f"Total dietary fiber: {whole_meal_nutrients[4]}% of your meal" 
        return (f"\033[4mEntire Meal\033[0m\n{protein}\n{fat}\n{carb}\n{sugar}\n{fiber}\n")
    
    def print_each_food_nutrients(self):
        each_food_nutrients = (self.calculate_percentages_nutrients())[0]
        to_print_list = []
        for food_item in each_food_nutrients:
            item = food_item[0].capitalize()
            protein = f"Protein: {food_item[1][0]}%"
            fat = f"Fat: {food_item[1][1]}%"
            carb = f"Carbohydrates: {food_item[1][2]}%"
            sugar = f"Sugar: {food_item[1][3]}%"
            fiber = f"Dietary fiber: {food_item[1][4]}%"
            to_print_list.append(f"\033[4m{('Total '+item)}\033[0m\n{protein}\n{fat}\n{carb}\n{sugar}\n{fiber}\n")
        return to_print_list
    
    
imageName = str(input("Enter image name (include .jpg): "))
image_dir = 'C:\\Daniel\\Python\\Nutrition YOLO\\Training_files\\Raw_imgs\\' + imageName
nutrient_analyzer = nutrient_analyzer(model, image_dir)

#filter = filter()
#filter.saturate(image_dir)

nutrient_analyzer.picture(imageName)
nutrient_analyzer.plot_masks(True)
each_food_nutrients = nutrient_analyzer.print_each_food_nutrients()
whole_meal_nutrients = nutrient_analyzer.print_whole_meal_nutrients()

print("")

for food_item in each_food_nutrients:
    print(food_item)
print(whole_meal_nutrients)



  

