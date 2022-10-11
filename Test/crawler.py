from numpy import row_stack
from selenium import webdriver
import time
import csv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', keep_alive = True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
# driver = webdriver.Firefox
time.sleep(2.)
# driver.get("https://www.google.com")
# driver.get('http://127.0.0.1:5000/base')


csv_header = ['manufacturer', 'model', 'year', 'version', 'power(kW)', 'fuel_date', 'odometer', 'trip_distance(km)',
              'quantity(kWh)', 'fuel_type', 'tire_type', 'city', 'motor_way', 'country_roads', 'driving_style',
              'consumption(kWh/100km)', 'A/C', 'park_heating', 'avg_speed(km/h)', 'ecr_deviation', 'fuel_note']


def initialize_csv_reader(path):
    csv_file = open(path, mode='a', newline='')
    writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    writer.writerow(csv_header)
    return writer, csv_file


def append_to_csv(record, csv_file, writer):
    writer.writerow(record)
    csv_file.flush()


# put your target vehicle's URL here
# url = 'https://www.spritmonitor.de/en/detail/786327.html'
# url = 'https://www.spritmonitor.de/en/detail/621275.html' # i-MiEV 2013
# url = 'https://www.spritmonitor.de/en/detail/456655.html' # i-MiEV 2011
# url = 'https://www.spritmonitor.de/en/detail/679341.html' # E-Golf 2014
# url = 'https://www.spritmonitor.de/en/detail/547003.html' # Opel Ampera ePionier 2012
# url = 'https://www.spritmonitor.de/en/detail/783303.html' # Kia Soul EV 2016
# url = 'https://www.spritmonitor.de/en/detail/507166.html' # Opel Ampera ePionier (2) 2012
# url = 'https://www.spritmonitor.de/en/detail/1001953.html' # Hyundai Ioniq Electric 2018
# url = 'https://www.spritmonitor.de/en/detail/838493.html' # Mercedes B250e 2015
# url = 'https://www.spritmonitor.de/en/detail/861231.html' # E-Golf 2015
# url = 'https://www.spritmonitor.de/en/detail/1254131.html' # Hyundai Ioniq Electric  Roadrunner 2018
# url = 'https://www.spritmonitor.de/en/detail/882000.html' # Opel Ampera-e 2017
# url = 'https://www.spritmonitor.de/en/detail/761029.html' # Tesla Model S 2015
# url = 'https://www.spritmonitor.de/en/detail/786327.html' # E-Golf 2016
# url = 'https://www.spritmonitor.de/en/detail/1021778.html' # Nissan Leaf ZE0 2013
# url = 'https://www.spritmonitor.de/en/detail/979560.html' # Nissan Leaf Black Edition 2017
# url = 'https://www.spritmonitor.de/en/detail/867239.html' # Tesla Model S75D 2017
# url = 'https://www.spritmonitor.de/en/detail/1067960.html' # i-MiEV 2014
url = 'https://www.spritmonitor.de/en/detail/1071765.html' # E-Golf 2018
# url = 'https://www.spritmonitor.de/en/detail/894077.html' # Hyundai Ioniq Premium 2017
# rewrite the factory's defined energy consumption rate 
model = 'E_Golf'
year_built = 2018
# manufacturer_ecr = 12.5 # i-MiEV 2013-2014
# manufacturer_ecr = 13.5 # i-MiEV 2011
# manufacturer_ecr = 12.7 # E-Golf 2014-2015
# manufacturer_ecr = 13.5 # Opel Ampera ePionier 2012
# manufacturer_ecr = 14.3 # Kia Soul EV 2016
# manufacturer_ect = 11.5 # Hyundai Ioniq Electric 2017-2018
# manufacturer_ecr = 16.6 # Mercedes B250e 2015
# manufacturer_ecr = 16.5 # Opel Ampera-e 2017
# manufacturer_ecr = 16.1 # Tesla Model S 2015
# manufacturer_ecr = 12.7 # E-Golf 2016
# manufacturer_ecr = 15.0 # Nissan Leaf ZE0 2013 - Black Edition 2017
# manufacturer_ecr = 14.8 # Tesla Model S75D 2017
manufacturer_ecr = 12.9 # E-Golf 2018
csv_path = f"./{model}_{year_built}.csv"

writer, csv_file = initialize_csv_reader(path=csv_path)
# driver = webdriver.Chrome(keep_alive=True)
driver.get(url=url)
time.sleep(2.)
# details = driver.find_element_by_id(id_="vehicledetails")
details = driver.find_element(by = 'id', value = 'vehicledetails')
# vehicle = str(details.find_element_by_xpath(xpath="//h1").text)
vehicle = str(details.find_element(by = 'xpath', value = '//h1').text)
vehicle = vehicle.split(sep=" - ")

manufacturer = vehicle[0].strip()
model = vehicle[1].strip()
version = vehicle[2].strip()

engine_power = None
try:
    details_txt = str(details.text).split()
    for word in range(0, len(details_txt) - 1):
        if details_txt[word] == "kW":
            engine_power = details_txt[word - 1]
except:
    pass


page_number = 1
while True:
    this_page = (url + '?page=%d') % page_number
    driver.get(url=this_page)

    try:
        #table = driver.find_element_by_xpath(xpath="//table[@class='itemtable']/tbody")
        #rows = table.find_elements_by_xpath(xpath=".//tr")
        table = driver.find_element(by = 'xpath', value = "//table[@class='itemtable']/tbody")
        rows = table.find_elements(by = 'xpath', value = ".//tr")
        #print(rows[0].get_attribute(name="innerHTML"))
    except:
        print("we have reached the end!")
        driver.close()
        exit()
    for row in rows:

        # features = row.find_elements_by_xpath(xpath=".//td")
        features = row.find_elements(by = 'xpath', value = ".//td")

        #if features[0].get_attribute(name="class") == "fueldate":
        #    fuel_date = features[0].text
        #else:
        #    fuel_date = None
        #print("fuel_date is:", fuel_date)

        fuel_date = features[0].get_attribute(name="innerHTML")
        print("fuel_date is:", fuel_date)

        # check whether this is a fueling record, or go to the next record directly
        if fuel_date is None:
            continue

        #if features[1].get_attribute(name="class") == "fuelkmpos":
        #    odometer = features[1].text
        #    if odometer.find('.') != -1:
        #        odometer = int(float(odometer) * 1000)
        #    else:
        #        pass
        #else:
        #    odometer = None
        #print("odometer is:", odometer)

        odometer = features[1].get_attribute(name="innerHTML")
        if odometer is not '':
            if odometer.find('.') != -1:
                odometer = int(float(odometer) * 1000)
            print("odometer is:", odometer)
        else:
            # skip this row
            continue

        #if features[2].get_attribute(name="class") == "trip":
        #    distance = features[2].text
        #    try:
        #        distance = float(distance.replace(',', '.'))
        #    except:
        #        pass
        #else:
        #    distance = None
        #print("trip distance is:", distance)

        distance = features[2].get_attribute(name="innerHTML")
        try:
            distance = float(distance.replace(',', '.'))
        except:
            continue
        print("trip distance is:", distance)

        #if features[3].get_attribute(name="class") == "quantity":
        #    quantity = features[3].text
        #    try:
        #        quantity = float(quantity.replace(',', '.'))
        #    except:
        #        pass
        #else:
        #    quantity = None
        #print("quantity is:", quantity)

        quantity = features[3].get_attribute(name="innerHTML")
        try:
            quantity = float(quantity.replace(',', '.'))
        except:
            continue
        print("quantity is:", quantity)

        if features[4].get_attribute(name="class") == "fuelsort":
            fuel_type = features[4].get_attribute(name="onmouseover").split(sep="'")[1]
        else:
            fuel_type = None
        print("fuel type is:", fuel_type)

        if features[5].get_attribute(name="class") == "tire":
            try:
                tire_img = features[5].find_element(by = 'xpath', value = ".//img")
                tire_type = tire_img.get_attribute(name="onmouseover").split(sep="'")[1]
            except:
                tire_type = None
        else:
            tire_type = None
        print("tire type is:", tire_type)

        if features[6].get_attribute(name="class") == "street":
            try:
                street_imgs = features[6].find_elements(by = 'xpath', value = ".//img")
                city = country_roads = motor_way = 0
                for street_img in street_imgs:
                    if street_img.get_attribute(name="onmouseover").split(sep="'")[1] == 'City':
                        city = 1
                    if street_img.get_attribute(name="onmouseover").split(sep="'")[1] == 'Motor-way':
                        motor_way = 1
                    if street_img.get_attribute(name="onmouseover").split(sep="'")[1] == 'Country roads':
                        country_roads = 1
            except:
                city = country_roads = motor_way = None
        else:
            city = country_roads = motor_way = None
        print("streets are:", motor_way, city, country_roads)

        if features[7].get_attribute(name="class") == "style":
            try:
                style_img = features[7].find_element(by = 'xpath', value = ".//img")
                style = style_img.get_attribute(name="onmouseover").split(sep="'")[1]
            except:
                style = None
        else:
            style = None
        print("driving style is:", style)

        if features[9].get_attribute(name="class") == "consumption":
            try:
                consumption = features[9].get_attribute(name="onmouseover").split("'")[1].split(" ")[0]
                consumption = float(consumption.replace(',', '.'))
            except:
                consumption = None
        else:
            consumption = None
        print("consumption is:", consumption)

        avg_speed = None
        AC = park_heating = 0
        fuel_note = None
        if features[10].get_attribute(name="class") == "fuelnote":
            try:
                fuel_note_imgs = features[10].find_elements(by = 'xpath', value = ".//img")

                for fuel_note_img in fuel_note_imgs:
                    if fuel_note_img.get_attribute(name='alt') == 'Bordcomputer':
                        bordcomputer = fuel_note_img.get_attribute(name="onmouseover").split("'")[1]
                        words = bordcomputer.split()
                        for word in words:
                            if word.find("Consumption") != -1:
                                idx = words.index(word)
                                consumption = words[idx + 1]
                                consumption = float(consumption.replace(',', '.'))
                            elif word.find("Quantity") != -1:
                                idx = words.index(word)
                                quantity = words[idx + 1]
                                quantity = float(quantity.replace(',', '.'))
                            elif word.find("speed") != -1:
                                idx = words.index(word)
                                avg_speed = words[idx + 1]
                                avg_speed = float(avg_speed.replace(',', '.'))
                            else:
                                pass
                    elif fuel_note_img.get_attribute(name='alt') == 'A/C':
                        AC = 1
                    elif fuel_note_img.get_attribute(name='alt') == 'Park heating':
                        park_heating = 1
                    else:
                        fuel_note = fuel_note_img.get_attribute(name="onmouseover").split("'")[1]
            except:
                fuel_note = None
        else:
            fuel_note = None
        print("fuel note is:", fuel_note)

        # calculate the energy consumption rate deviation
        try:
            ecr_deviation = consumption - manufacturer_ecr
            print("ECR deviation is:", ecr_deviation)
        except:
            ecr_deviation = None

        this_record = [manufacturer, model, year_built, version, engine_power, fuel_date, odometer, distance, quantity,
                       fuel_type, tire_type, city, motor_way, country_roads, style, consumption, AC, park_heating,
                       avg_speed, ecr_deviation, fuel_note]

        append_to_csv(record=this_record, csv_file=csv_file, writer=writer)
    page_number += 1