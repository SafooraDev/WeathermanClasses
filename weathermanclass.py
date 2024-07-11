import os
import argparse
import csv

# Mapping of month numbers to their corresponding names
Month_Map = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

class WeatherData:
    def __init__(self, data_folder, city):
        self.data_folder = data_folder
        self.city = city

    def read_weather_data(self, file_path):
        try:
            if not os.path.exists(file_path):
                print(f"File does not exist: {file_path}")
                return
            data = []
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    data.append(tuple(row))
            return data
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

    def get_files(self):
        full_path = os.path.join(self.data_folder, self.city)
        if not os.path.exists(full_path):
            return []
        
        files = [os.path.join(full_path, f) for f in os.listdir(full_path) \
            if f.endswith('.txt')]
        return files

class WeatherSummary:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def yearly_summary(self, year):
        all_files = self.weather_data.get_files()
        data_list = [self.weather_data.read_weather_data(file) for file in all_files 
                     if f"{self.weather_data.city}_{year}" in file]
        data_list = [data for data in data_list if data is not None]
        if not data_list:
            raise ValueError("No data files found for the specified year and city")
    
        data = [item for sublist in data_list for item in sublist]

        data = [row for row in data if len(row) > 5 and row[2] \
            and row[3] and row[5] and row[2] != 'Mean TemperatureC']

        if not data:
            raise ValueError("No valid data found for the specified year and city")

        highest_temp = max(data, key=lambda x: float(x[2]))
        lowest_temp = min(data, key=lambda x: float(x[3]))
        highest_humidity = max(data, key=lambda x: float(x[5]))
        
        return {
            'Highest Temperature': (highest_temp[2], highest_temp[0]),
            'Lowest Temperature': (lowest_temp[3], lowest_temp[0]),
            'Highest Humidity': (highest_humidity[5], highest_humidity[0])
        }

    def monthly_summary(self, year, month):
        month_str = Month_Map[month]
        file_path = os.path.join(self.weather_data.data_folder, self.weather_data.city, 
                                 f"{self.weather_data.city}_{year}_{month_str}.txt")

        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            raise ValueError(f"No data file found for {year}/{month_str} in {self.weather_data.city}")
        
        data = self.weather_data.read_weather_data(file_path)
        if data is None:
            raise ValueError(f"Failed to read data file for {year}/{month_str} in {self.weather_data.city}")

        data = [row for row in data if len(row) > 6 and row[2].isdigit() and row[3].isdigit() and row[6].isdigit()]

        if not data:
            raise ValueError("No valid data found for the specified month and year")

        avg_highest_temp = sum(float(row[2]) for row in data) / len(data)
        avg_lowest_temp = sum(float(row[3]) for row in data) / len(data)
        avg_humidity = sum(float(row[6]) for row in data) / len(data)
        
        return {
            'Average Highest Temperature': avg_highest_temp,
            'Average Lowest Temperature': avg_lowest_temp,
            'Average Humidity': avg_humidity
        }

class WeatherCharts:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def draw_horizontal_bar_charts(self, year, month):
        month_str = Month_Map[month]
        file_path = os.path.join(self.weather_data.data_folder, self.weather_data.city, 
                                 f"{self.weather_data.city}_{year}_{month_str}.txt")
        
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            raise ValueError(f"No data file found for {year}/{month_str} in {self.weather_data.city}")
        
        data = self.weather_data.read_weather_data(file_path)
        if data is None:
            raise ValueError(f"Failed to read data file for {year}/{month_str} in {self.weather_data.city}")
        
        for row in data:
            if row[2] and row[3] and row[2].isdigit() and row[3].isdigit():  # Ensure there are values for max and min temperatures
                date = row[0]
                high_temp = int(float(row[2]))
                low_temp = int(float(row[3]))
                print(f"\033[1;30;40m {date} \033[1;31;40m {'+' * high_temp} \033[1;30;40m {high_temp}C")
                print(f"\033[1;30;40m {date} \033[1;34;40m {'+' * low_temp} \033[1;30;40m {low_temp}C")

    def draw_combined_bar_chart(self, year, month):
        month_str = Month_Map[month]
        file_path = os.path.join(self.weather_data.data_folder, self.weather_data.city, 
                                 f"{self.weather_data.city}_{year}_{month_str}.txt")
        
        if not os.path.exists(file_path):
            raise ValueError(f"No data file found for {year}/{month_str} in {self.weather_data.city}")
        
        data = self.weather_data.read_weather_data(file_path)
        if data is None:
            raise ValueError(f"Failed to read data file for {year}/{month_str} in {self.weather_data.city}")
        
        for row in data:
            if row[2] and row[3] and row[2].isdigit() and row[3].isdigit():  # Ensure there are values for max and min temperatures
                date = row[0]
                high_temp = int(float(row[2]))
                low_temp = int(float(row[3]))
                print(f"\033[1;30;40m {date} \033[1;34;40m {'+' * low_temp}  \033[1;31;40m {'+' * high_temp} 
                      \033[1;30;40m {low_temp}C - {high_temp}C \033[1;30;40m")

def main():
    parser = argparse.ArgumentParser(description='Weather Analysis Tool')
    parser.add_argument('-e', '--yearly', type=int, help='Yearly summary')
    parser.add_argument('-a', '--monthly', nargs=2, type=int, help='Monthly summary')
    parser.add_argument('-c', '--chart', nargs=2, type=int, help='Draw bar charts')
    parser.add_argument('data_folder', type=str, help='Path to the weather data files')
    parser.add_argument('city', type=str, help='City for weather data (Dubai_weather, lahore_weather, Murree_weather)')
    
    args = parser.parse_args()
    
    weather_data = WeatherData(args.data_folder, args.city)
    weather_summary = WeatherSummary(weather_data)
    weather_charts = WeatherCharts(weather_data)
    
    if args.yearly:
        summary = weather_summary.yearly_summary(args.yearly)
        print(f"Highest Temperature: {summary['Highest Temperature'][0]}C on {summary['Highest Temperature'][1]}")
        print(f"Lowest Temperature: {summary['Lowest Temperature'][0]}C on {summary['Lowest Temperature'][1]}")
        print(f"Highest Humidity: {summary['Highest Humidity'][0]}% on {summary['Highest Humidity'][1]}")
    
    if args.monthly:
        year, month = args.monthly
        summary = weather_summary.monthly_summary(year, month)
        print(f"Average Highest Temperature: {summary['Average Highest Temperature']}C")
        print(f"Average Lowest Temperature: {summary['Average Lowest Temperature']}C")
        print(f"Average Humidity: {summary['Average Humidity']}%")
    
    if args.chart:
        year, month = args.chart
        weather_charts.draw_horizontal_bar_charts(year, month)
        weather_charts.draw_combined_bar_chart(year, month)

if __name__ == '__main__':
    main()
