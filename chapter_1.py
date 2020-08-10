import geonamescache
import re
import csv

gc = geonamescache.GeonamesCache()

gc_city_dict = gc.get_cities()

def create_alt_names_dict():
    global alt_names_dict
    alt_names_dict = {}
    for city in list(gc_city_dict.items()):
        alt_names = city[1]['alternatenames']
        my_city = city[1]['name']
        my_list = [my_city]
    #    for alt_name in alt_names:
    #        if len(alt_name) > 2:
    #            my_list.append(alt_name)
        search_names = '|'.join(my_list)
        search_names = '\\b' + search_names + '\\b'
        regex = re.compile(search_names)
        alt_names_dict[city[0]] = regex


def find_city(text):
    result = []
    for city_names in list(alt_names_dict.items()):
        regexp = city_names[1]
        if regexp.search(text) != None:
            key = city_names[0]
            country = gc_city_dict[city_names[0]]['countrycode']
            city = gc_city_dict[city_names[0]]['name']
            result.append([key, country, city, text])
    return result


def main():
    create_alt_names_dict()
    result = []
    file = open('.\data\headlines.txt', 'r')
    for line in file.readlines():
        result.extend(find_city(line.rstrip()))
    file.close()
    csv.writer(open(".\output\city_mapped_disease.csv", 'w', newline='')).writerows(result)

if __name__ == '__main__':
    main()
