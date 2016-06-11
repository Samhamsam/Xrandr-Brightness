#!/usr/bin/python3

import subprocess
import configparser
import os
import sys
import getopt
import math



def main(argv):

	if(len(sys.argv) == 1):#if no argument
		print("Please put a correct parameter: error")
		sys.exit()
	
	plusminuszehn = 0.0
	
	try:
		opts, args = getopt.getopt(argv, "rh", ["runter", "hoch"])
	
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
		
	for o,a in opts:
		print(o)
		#reduce brightness
		if o in ("-r", "--runter"):
			plusminuszehn = -0.1
		#increase brightness
		elif o in ("-h", "--hoch"):
			plusminuszehn = 0.1
		else:
			print("Fehler")
			sys.exit()
		

	config = configparser.ConfigParser()
	config_file = os.path.join(os.path.dirname(__file__), 'helligkeitspeicher.ini')
	config.read(config_file)
	momentanhelligkeit = config['speicher']['zahl']
	
	
	if(((momentanhelligkeit <= '1.0') and (plusminuszehn == 0.1)) or ((momentanhelligkeit > '0.4') and (plusminuszehn == -0.1))):
		helligkeit = float(momentanhelligkeit) + plusminuszehn
		momentanhelligkeit = helligkeit
		bashCommand = " xrandr --output DP1 --brightness " + str(helligkeit)
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
		helligkeitVGA = helligkeit + 0.1
#		for second monitor
#		bashCommand = " xrandr --output VGA1 --brightness " + str(helligkeitVGA)
#		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#		output = process.communicate()[0]
		config['speicher']['zahl'] = str(helligkeit)
		with open(config_file, 'w') as configfile:
			config.write(configfile)
	else:
		pass


if __name__=="__main__":
	main(sys.argv[1:])
