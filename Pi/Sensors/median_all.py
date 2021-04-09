import os

if __name__ == '__main__':
	# check the config (if it exists)
	try:
		f = open('/etc/sensing/sensing.config','r')
		style = f.readline().rstrip()
		if style=="arrows":
			# run the arrows
			os.system("sudo python3 /home/pi/scripts/median_arrows.py")
		else:
			# run the circles
			os.system("sudo python3 /home/pi/scripts/median_circles.py")
	except FileNotFoundError:
		# file does not exist, continue as is.
		os.system("sudo python3 /home/pi/scripts/median_arrows.py")
		pass