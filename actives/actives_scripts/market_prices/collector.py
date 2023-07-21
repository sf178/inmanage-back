import subprocess
from datetime import datetime

path = 'python collector/main.py download --engine stock --market'
now = datetime.now()
date_str = now.strftime('%Y-%m-%d')

subprocess.call(f"{path} bonds --date {date_str}", shell=True)
subprocess.call(f"{path} shares --date {date_str}", shell=True)
subprocess.call(f"{path} index --date {date_str}", shell=True)
