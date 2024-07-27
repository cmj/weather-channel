# wpg-weatherchan
This creates the old-school looking weather channel that was common on Winnipeg cable TV into the 1990s.

![Example of the result, captured from the analog video output](https://github.com/probnot/wpg-weatherchan/blob/master/example1.jpg?raw=true)
![Example of the result, captured from the analog video output](https://github.com/probnot/wpg-weatherchan/blob/master/example2.jpg?raw=true)

## Usage

This was written in Python 3.x

This uses 'NOAA' to get the weather data from the National Weather Serivce. It can be found here: ([https://github.com/michaeldavie/env_canada](https://github.com/paulokuong/noaa)). 
It also uses the fonts VCR OSD Mono (https://www.dafont.com/vcr-osd-mono.font) and 7-Segment Normal (https://blogfonts.com/7-segment-normal.font).

It was tested on a Raspberry Pi 2B running Raspberry Pi OS (full w/desktop). 

The Composite video output in the Raspberry Pi runs at 720x480, so I recommend setting the display to this and not 640x480.

If you're launching this from an SSH session, I recommend doing so through a script file with the following:
>python future.py > /tmp/future.txt (required in version 2.1+, plan is to integrate this into main program later) 
>
>export DISPLAY=:0.0
>
>python3 wpg-USAver.py


## License

This code is available under the terms of the [MIT License]
