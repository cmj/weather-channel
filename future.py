from noaa_sdk import NOAA
import linecache as lc
n = NOAA()
res = n.get_forecasts('97035', 'US')
for i in res:
   results = str(i)
   print(results)
