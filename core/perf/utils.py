import random

def get_data():
    data={
        'L1':random.randint(0,5),
        'L2':random.randint(0,5),
        'L3':random.randint(0,5),
    }
    return data

def get_storage():
    # dict={
    #     'data1': random.randint(0,1000)/1000,
    #     'data2': 1,
    # }
    # dict.update({'porc':dict.get('data1')/dict.get('data2')})
    # return dict
    return random.randint(0,1000)