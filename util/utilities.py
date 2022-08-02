import re 
from components.City import City



def reformat_ascension_name(name):
    name = re.sub('III','', name)
    name = re.sub('II','', name)
    name = re.sub('(JR.)','',name)
    name = re.sub('\'', "", name)
    m = re.match("^(\s*\w*\-*)+,", name)
    print(name)
    if m:
        span = m.span()[1]
    lastname = name[:span-1]
    firstname = name[span+1:]
    return firstname.strip() + ' ' + lastname.strip()
    


def reformat_name(name):
    name = re.sub('III','', name)
    name = re.sub('JR.','',name)
    name = re.sub('(^\s*MD\s+)','',name)
    name = re.sub('(\w+\.)','',name)
    name = re.sub('(\,\s*\w+)','',name)
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

