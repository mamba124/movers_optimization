import os
import pandas as pd

def validate_launch_time():
    start = os.environ.get("START")
    finish = os.environ.get("FINISH")
    if not start:
        start = 16
    if not finish:
        finish = 8
    start_time = int(start)
    finish_time = int(finish)
    return start_time, finish_time


def check_table():
    if "stats.csv" not in os.listdir():
        df = pd.DataFrame(columns=['Success', 'Date', 'Link', 'Processed Time', 'Accessed Time', 'Answered/Quote was posted at', 'Name if exists'])
        df.to_csv('stats.csv', index=False)
    else:
        df = pd.read_csv("stats.csv")
        return df

def make_a_record(current_session, new_row):
    df = check_table()
    new_row_df = pd.Series({'Success': new_row.success,
                            'Date': new_row.date,
                            'Link': new_row.link,
                            'Processed Time': new_row.processed,
                            'Accessed Time': new_row.accessed,
                            'Answered/Quote was posted at': new_row.answered,
                            'Name if exists': new_row.name})
    df.append(new_row_df)
    df.to_csv("stats.csv", index=False)
    
    
class RecordClass:
    def __init__(self):
        self.success = None
        self.date = None
        self.link = None
        self.processed = None
        self.accessed = None
        self.answered = None
        self.name = None