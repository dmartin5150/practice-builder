import re 
from components.City import City





def reformat_name(name):
    name = re.sub('(\w+\.)','',name)
    name = re.sub('(\,\s*\w+)','',name)
    name = re.sub('(III)','', name)
    name = re.sub('(JR.)','',name)
    return name.strip().upper().split(' ')


def get_url(surgeon_name,city):
    filtered_name = reformat_name(surgeon_name)
    print(filtered_name)
    city_name = city.get_name()
    print(city)
    state = city.get_state()
    x_coord = city.get_x()
    y_coord = city.get_y()
    return f'https://doctor.webmd.com/results?q={filtered_name[0]}%20{filtered_name[-1]}&sortby=bestmatch&pt={x_coord},{y_coord}&city={city_name}&state={state}'

def get_location_url(url):
    url = re.sub('overview','appointments',url)
    return url

