import sys
import os
import math

def traverseDir(dir,extension):
	files = []
	try:
		for entry in os.scandir(dir):
			#if entry.is_dir():
			#	files_temp = traverseDir(entry.path)
			#	if files_temp:
			#		files.extend(files_temp)
			if entry.is_file():
				#print(entry.path.split(".")[-1])
				if(str(entry.path.split(".")[-1])) == extension:
					files.append(entry.path)
	except:
		pass
	return files

def modIDtoCoords(mod_id,total_mods,mods_high):
	y = (mod_id-1) % mods_high
	x = math.floor((mod_id-1)/mods_high)
	return(x,y)

#dir is same directory where this script is executed
dir = os.path.dirname(os.path.realpath(__file__))

#type of coefficient files
filetype = "ccCoef"
coefficients = traverseDir(dir,"ccCoef")

print(coefficients)

#if len(sys.argv) != 2:
#	print("usage: combine.py SERIAL.ccCoef")
#	exit(1)

#promt user for new destination coefficient file
destination_file = input("Please enter a new name for the coefficient file : ")
#destination_file = "V8000M004071_combined"

#prompt user for width and height of panel in pixels
width = int(input("In one panel, how many pixels wide? "))
height = int(input("In one panel, how many pixels high? "))		
#width = 112
#height = 112

#prompt user for number of modules (x, y)
mods_wide = int(input("In one panel, how many modules wide? "))
mods_high = int(input("In one panel, how many modules high? "))
#mods_wide = 2
#mods_high = 8


mod_width = width / mods_wide
mod_height = height / mods_high
mod_pixel_count = mod_width * mod_height
total_pixels = width * height
total_mods = mods_wide * mods_high

print("Single mod pixel width = ",mod_width)
print("Single mod pixel height = ",mod_height)
print("Single mod pixel count = ",mod_pixel_count)
print("Total modules = ",total_mods)
print("Total pixels = ",total_pixels)

#build up a new destination panel, using source modules, one at a time
destination_modules = []

print("############################")
for x in range(mods_wide):
	for y in range(mods_high):
		#select a source panel for each module
		#print("mod location : ",(x,y))
		#print("mod ID : ",((x*mods_high)+y)+1)
		current_mod_id = ((x*mods_high)+y)+1
		print("Building Module #",current_mod_id," - x,y coordinates within panel = ",(x,y))
		source_mod_tile_serial = input("Please enter source panel serial number : ")
		##source_mod_tile_serial = "V8000M004071"
		
		source_mod_prompt = "Please enter source module ID# (1-"+str(total_mods)+") based on it's location within the source panel : "
		source_mod_location = int(input(source_mod_prompt))
		##source_mod_location = 1
		
		destination_modules.append((source_mod_tile_serial,source_mod_location))

#print(destination_modules)


#list to fill and then sort
to_be_sorted = []
#select source coefficient file, and source module, select target module
with open(destination_file+".ccCoef","w") as dest:
	for destination_modules_count,i in enumerate(destination_modules):
		for c in coefficients:
			if i[0] in c:
				source_mod_coords = modIDtoCoords(i[1],total_mods,mods_high)
				destination_mod_coords = modIDtoCoords(destination_modules_count+1,total_mods,mods_high)
				print("[+] building destination mod #",str(destination_modules_count+1))
				print("[+] matching coefficient file found")
				print("[+] need to source coefficients for pixels on module #",i[1])
				print("[+] need to source from coord ",source_mod_coords)
				print("[+] set destination origin coord ",destination_mod_coords)
				print("[+] ",c)
				#open appropriate source coefficient file
				with open(c) as f:
					inputlist = f.read().splitlines()
					pixel_x_count = 0
					pixel_y_count = 0
					for count, line in enumerate(inputlist):
						#write first 3 lines to destination as header, but only when reading from the first modules ccCoef file
						if count <= 2 and destination_modules_count == 0:
							# .ccCoef files need carraige return 0x0D0A
							dest.write(line+"\n")
						#everything after header
						elif count >= 3:
							#select appropriate lines based on pixel coords on the correct source module
							if (source_mod_coords[0]*mod_width) <= int(line.split(",")[0]) < ((source_mod_coords[0]+1)*mod_width) and (source_mod_coords[1]*mod_height) <= int(line.split(",")[1]) < ((source_mod_coords[1]+1)*mod_height):
								#adjust LED coordinates from source file, to match destination
								pixel_x = destination_mod_coords[0]*mod_width+pixel_x_count
								pixel_y = destination_mod_coords[1]*mod_height+pixel_y_count
								#print(str(int(pixel_x))+", "+str(int(pixel_y)))
								
								
								if pixel_x_count < mod_width-1:
									pixel_x_count += 1
								else:
									pixel_x_count = 0
									pixel_y_count += 1
								
								
								newline = line.split(",")
								#print("source coords = ",newline[0],", ",newline[1])
								#determine source module origin, and difference between current coord and original origin
								#determine destination origin, and apply coord offset
								newline[0] = str(int(pixel_x))
								newline[1] = str(int(pixel_y))
								adjustedline = ",".join(newline)
								#print(adjustedline)
								#dest.write(adjustedline+"\r\n")
								to_be_sorted.append(adjustedline.split(","))
					f.close()
				#input("Press Enter to continue...")
	#sort the list of coefficients in order of pixel to match original structure
	#print(to_be_sorted[0])
	#print(len(to_be_sorted))
	sorted_list = sorted(to_be_sorted, key=lambda k: [int(k[1]), int(k[0])])
	#sorted_list = sorted(to_be_sorted)
	#print(len(sorted_list))
	#print(sorted_list[14])
	#write sorted list to file one line at a time
	for sorted_line in sorted_list:
		dest.write(",".join(sorted_line)+"\n")
		#print(",".join(sorted_line))
	dest.close()



#complete step for all possible modules
#rewrite pixel numbers for new coefficient file		