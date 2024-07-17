This script is to be used for building LED calibration coefficients from existing coefficient data. 
This should be used when you have a set of calibration data from the factory where each file contains the coefficients for the modules that were installed on a specific panel at the factory. 
After LED panels are used in the field, the modules are often rearranged from their factory installed positions, yet if you ever need to upload calibration data, you need to use a coefficient file that contains data for an entire panel, even if you only want to upload data to a specific module.
At this point you have 3 options:
1) Remove all modules (or use an empty panel) and install ONLY the target module, in it's factory position, and upload data. All data for modules that are physically missing will be ignored.
2) Locate all the modules that were installed on a panel at the factory, and reinstall all of them in their factory positions and upload data. The original coefficient file for that panel will work perfectly.
3) For situations where you don't want to (or can't) remove any modules from a panel, you can use this script to build a new coefficient file that sources data from each module's factory parent-panel and factory position. The data for each module will be placed into a new destination coefficient file based on each modules current position in the target panel.

You will need:
1) The horizontal and vertical resolution (in pixels) of a single panel of the type you are working with.
2) The module vertical and horizontal count of a single panel of the type you are working with.
3) The source panel serial number and factory position of each module being used.

The coefficient file is constructed one module at a time, starting at the top left module, and moving from left to right across each row. 

Example data is provided for two source panels.
Panel type: ROE Vanish 8
Pixel resolution: 112 x 112
Module count: 2 x 8
