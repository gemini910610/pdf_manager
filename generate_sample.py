import os
import json
import random

os.mkdir('sample json')

for i in range(1, 10):
    os.mkdir(f'sample json/學生{i}')

    for j in range(1, 4):
        with open(f'sample json/學生{i}/第{j}次考試.json', 'w') as file:
            json.dump({
                '國文': random.randint(0, 100),
                '英文': random.randint(0, 100),
                '數學': random.randint(0, 100),
                '自然': random.randint(0, 100),
                '社會': random.randint(0, 100)
            }, file)
