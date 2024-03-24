import requests

class edamam:
    def __init__(self):
        self.api_id = '4d0350f3'
        self.api_key = '5c836fae9650ae75b0fd0bcd2d574dec'
        self.base_url = 'https://api.edamam.com/api/nutrition-data'
    
    def get_nutrition_facts(self, food, portion):
        params = {
            'app_id': self.api_id,
            'app_key': self.api_key,
            'ingr': f'{portion} of {food}'
        }

        # Make the API request
        response = requests.get(self.base_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None

    def find_quantities(self, food):
        each_food_nutrients = []
        percentages_list = [food[1] for food in food]
        foods_list = [food[0] for food in food]
        
        #nutritional content of EACH food item as percentage
        for i, food in enumerate(foods_list):
            percentage = float(percentages_list[i]) #"percentage" represents what percentage of entire meal each foot item is
            nutrition_data = self.get_nutrition_facts(food, '100 g')
            if nutrition_data: #currently only considering main macro-nutrients, all outputs in percentages
                protein = round(nutrition_data['totalNutrients']['PROCNT']['quantity'], 2) #protein
                fat = round(nutrition_data['totalNutrients']['FAT']['quantity'], 2) #fat
                carbs = round(nutrition_data['totalNutrients']['CHOCDF']['quantity'], 2) #carbohydrates
                sugar = round(nutrition_data['totalNutrients']['SUGAR']['quantity'], 2) #sugar
                diet_fiber = round(nutrition_data['totalNutrients']['FIBTG']['quantity'], 2) #dietary fiber
                each_food_nutrients.append([food, [protein, fat, carbs, sugar, diet_fiber]])
        
        #nutritional content of ENTIRE MEAL as percentage
        whole_meal_nutrients = [0, 0, 0, 0, 0]
        for i, item in enumerate(each_food_nutrients):
            for j, nutrient_percent in enumerate(item[1]):
                whole_meal_nutrients[j] += (nutrient_percent*percentages_list[i])
        
        for i, value in enumerate(whole_meal_nutrients):
            whole_meal_nutrients[i] = round(value, 2)
        
        return each_food_nutrients, whole_meal_nutrients

if __name__ == "__main__":
    edamam = edamam()
    test_food_list = [('bread', 0.6), ('chicken', 0.2), ('cucumber', 0.1), ('egg', 0.1)]
    nutrients_list = edamam.find_quantities(test_food_list)
    print(nutrients_list)