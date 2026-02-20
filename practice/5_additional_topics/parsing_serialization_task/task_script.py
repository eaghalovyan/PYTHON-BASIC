import os
import json
import statistics
import xml.etree.ElementTree as ET




def process_weather_data(source_dir, output_file):
    all_cities = {}

    for city_name in os.listdir(source_dir):
        city_path = os.path.join(source_dir, city_name)

        if os.path.isdir(city_path):
            for file_name in os.listdir(city_path):
                if file_name.endswith('json'):
                    with open(os.path.join(city_path, file_name), 'r') as f:
                        city_json = json.load(f)
                        hourly_list = city_json.get("hourly", [])

                        temps = [hour["temp"] for hour in hourly_list]
                        winds = [hour["wind_speed"] for hour in hourly_list]
                        all_cities[city_name] = {
                            "mean_temp": round(statistics.mean(temps), 2),
                            "max_temp": round(max(temps), 2),
                            "min_temp": round(min(temps), 2),
                            "mean_wind_speed": round(statistics.mean(winds), 2),
                            "max_wind_speed": round(max(winds), 2),
                            "min_wind_speed": round(min(winds), 2),
                        }
    cities = list(all_cities.keys())
    country_mean_temp = round(statistics.mean([c['mean_temp'] for c in all_cities.values()]), 2)  
    country_mean_wind_speed = round(statistics.mean([c["mean_wind_speed"] for c in all_cities.values()]), 2) 

    warmest_place = max(all_cities, key = lambda x: all_cities[x]["mean_temp"])
    coldest_place = min(all_cities, key = lambda x: all_cities[x]["mean_temp"])
    windies_place = max(all_cities, key = lambda x: all_cities[x]["mean_wind_speed"])


    #Creating XML

    root = ET.Element("weather")
    root.set("country", "Spain")
    root.set("date", "2021-09-25")

    summary = ET.SubElement(root, "summary")
    summary.set("mean_temp", str(country_mean_temp))
    summary.set("mean_wind_speed", str(country_mean_wind_speed))
    summary.set("coldest_place", str(coldest_place))
    summary.set("warmiest_place", str(warmest_place))
    summary.set("windiest_place", str(windies_place))

    city_elements = ET.SubElement(root, "cities")
    for name, stats in all_cities.items():
        city_tag = ET.SubElement(city_elements, name)
        for key, value in stats.items():
            city_tag.set(key, str(value))


    xml_string = ET.tostring(root, encoding = 'unicode')
    
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(xml_string)


if __name__ == "__main__":
    
    source_dir = "./source_data"
    output_xml = "weather_report.xml"

    if os.path.exists(source_dir):
        process_weather_data(source_dir, output_xml)
        print(f"XML report generated: {output_xml}")
    else:
        print(f"Error: Directory {source_dir} not found.") 