# coding=utf-8
cities = {'Москва': 'moskva',
          'Санкт-Петербург': 'sankt-peterburg',
          'Астрахань': 'astrahan',
          'Барнаул': 'barnaul',
          'Волгоград': 'volgograd',
          'Воронеж': 'voronezh',
          'Екатеринбург': 'ekaterinburg',
          'Ижевск': 'izhevsk',
          'Иркутск': 'irkutsk',
          'Казань': 'kazan',
          'Калининград': 'kaliningrad',
          'Краснодар': 'krasnodar',
          'Красноярск': 'krasnoyarsk',
          'Набережные Челны': 'naberezhnye_chelny',
          'Нижний Новгород': 'nizhniy_novgorod',
          'Новосибирск': 'novosibirsk',
          'Омск': 'omsk',
          'Оренбург': 'orenburg',
          'Пермь':'perm',
          'Растов-на-Дону': 'rostov-na-donu',
          'Самара': 'samara',
          'Саратов': 'saratov',
          'Ставрополь': 'stavropol',
          'Тольятти': 'tolyatti',
          'Тула': 'tula',
          'Тюмень': 'tyumen',
          'Уьляновск': 'ulyanovsk',
          'Уфа': 'ufa',
          'Челябинск': 'chelyabinsk',
          'Ярославль': 'yaroslavl'}



#
# # Test the function with different formats
# print(get_city("Самара"))  # Should return 'samara'
# print(get_city("сАмАрА"))  # Should also return 'samara'