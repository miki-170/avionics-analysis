import pandas as pd
from pathlib import Path
import re
import calendar
import os

class data_reading:
    def __init__(self, table_number, start=2015, end=2026):
        self.year_start = start
        self.year_end = end
        self.number = table_number

        self.dest = Path(f"data/clean/Table_{self.number}")

        self.data = self._read_data()
        self._date_extracter()
        

    def _read_data(self):
        table = pd.DataFrame()
        for year in range(self.year_start, self.year_end + 1):
            for month in calendar.month_name[1:]:
                dir = f'data/raw/{year}/{month.lower()}/'
                regex = re.compile(rf'_Table_{self.number:02d}_.*\.csv')
                try:
                    matches = [file for file in os.listdir(dir) if regex.match(file)]
                    
                    if matches:
                        new_table = pd.read_csv(dir +matches[0])
                        table = pd.concat([table,new_table])
                    
                except FileNotFoundError:
                    continue
                
        return table.reset_index(drop=True)

    def _date_extracter(self):
        if 'reporting_period' in self.data.columns:
            name = 'reporting_period'
        elif 'this_period' in self.data.columns:
            name ='this_period'
        else:
            raise ValueError("Different date column than expected.")
        
        exctraced = self.data[name].astype(str).str.extract(r'(20\d{2})0*(\d{2})')

        exctraced.columns = ['year','month']
        
        self.data ['date'] = pd.to_datetime(exctraced['year'] + exctraced['month'], format='%Y%m')
        
        self.data.drop(columns=[name],inplace=True)
       
        
    @property
    def save(self):
        self.dest.mkdir(parents=True,exist_ok=True)
        print(self.data)
        self.data.to_csv(self.dest / "combined.csv", index=False)
    

