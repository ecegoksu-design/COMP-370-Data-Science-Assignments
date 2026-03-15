import pandas as pd
import csv
from datetime import datetime
from collections import defaultdict
import json

def calculate_monthly_averages():
    monthly_data = defaultdict(lambda: defaultdict(list))
    
    with open('2024_incidents.csv', 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                if not row.get('Closed Date') or not row.get('Created Date'):
                    continue
                    
                created = datetime.strptime(row['Created Date'].split()[0], '%Y-%m-%d')
                closed = datetime.strptime(row['Closed Date'].split()[0], '%Y-%m-%d')
                zipcode = row.get('Incident Zip', '').strip()
                
                if not zipcode or zipcode == 'UNKNOWN' or closed < created:
                    continue
                
                response_hours = (closed - created).total_seconds() / 3600
                
                month_key = closed.strftime('%Y-%m')
                monthly_data[month_key]['all'].append(response_hours)
                monthly_data[month_key][zipcode].append(response_hours)
                
            except (ValueError, KeyError):
                continue
    
    result = {}
    for month, data in monthly_data.items():
        result[month] = {
            'all': sum(data['all']) / len(data['all']) if data['all'] else 0,
            'by_zipcode': {}
        }
        for zipcode, times in data.items():
            if zipcode != 'all' and times:
                result[month]['by_zipcode'][zipcode] = sum(times) / len(times)
    
    with open('monthly_response_data.json', 'w') as f:
        json.dump(result, f)
    
    print("Pre-processing complete!")

if __name__ == '__main__':
    calculate_monthly_averages()