import pandas as pd
import json

def set_mark_model(brand, name):
    # df = pd.read_json('D:/inmanage-site/test_backend/cars_and_models.json')
    # filtered_df = df[df['name'] == brand]
    # print(filtered_df)
    with open('./сars_parser/parser/cars_and_models.json') as file:
        data = json.load(file)

    for car in data.values():
        if car['name'] == brand:
            if name in car['models']:
                index = car['models'].index(name)
                return car['request_name'], car['request_models'][index]

    return None


