import speech_recognition as sr
from ctypes import *
import pyaudio
import os
from subprocess import call
import subprocess
import sys


#Following code surpresses the annoying ALSA error messages
#For future reference, ALSA error messages can be ignored. Doesn't do anything bad
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
	pass
	
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


asound = cdll.LoadLibrary('libasound.so.2')
#Set the error handler
asound.snd_lib_error_set_handler(c_error_handler)


#Main stuff begins now

# Basic Commands:
	# left add point- index: 0
	# left subtract point - index: 1
	# right add point - index: 2
	# right subtract point - index: 3
	# reset - index: 4
	# cancel - index: 5
# Intermediate Commands:
	# Names
	# Amount of Players
	# ...
# Advanced Implementations:
	# Speech to text
	# Analyze current scores and speak (ie Matchpoint! or Winner <Player>)
	# ...

left_score = 0
right_score = 0	
commands_list = ["left", "left sub", "right", "right sub", " reset points", "cancel", "exit"]

#there may not be any point in using dicts but I want to experiment
""" commands = {
	"left point": None
	"left subtract": None
	"right point": None
	"right subtract": None
	"reset points": None
	"cancel": None
	
} """

def voice_command(is_command):
	
	# Nested method used to bypass try/except to get the audio variable
	def microphone():
		try:
			with sr.Microphone() as source:
				sr.Recognizer().adjust_for_ambient_noise(source)
				audio = sr.Recognizer().listen(source, timeout=3)
			return audio
		except sr.WaitTimeoutError:
				print("Voice command timed out. Please try again.")
				microphone()
	
	#it'll keep looping until it gets a proper response
	while True:
		try:
			print("Speak a command::")
			response = sr.Recognizer().recognize_google(microphone())
		    # This is so when the user speaks a command, it checks the list of commands to see if it is valid
			if response not in commands_list and is_command:
				continue
			return response
		except sr.RequestError:
			pass
		    # API was unreachable or unresponsive
		    #print("Error: API unavailable. Please try again.") 
		except sr.UnknownValueError:
			pass
		    # speech was unintelligible
		    #print("Error: Speech was unintelligble. Please try again.")
		except AssertionError:
			pass
			#print("Error: Incorrect instance of variable, most likely audio data. Please try again.")
			
        
# makes sure that 
def basic_commands():
			
	audio = voice_command(True)

	global left_score
	global right_score
		
	if audio == commands_list[0]:
		print(commands_list[0])
		left_score += 1
		print("inside left_score: " + str(left_score))
	elif audio == commands_list[1] and left_score > 0:
		print(commands_list[1])
		left_score -= 1
	elif audio == commands_list[2]:
		print(commands_list[2])
		right_score += 1
	elif audio == commands_list[3] and right_score > 0:
		print(command[3])
		right_score -= 1
	elif audio == commands_list[4]:
		print(commands_list[4])
		left_score = 0
		right_score = 0
	elif audio == commands_list[5]:
		print(commands_list[5])
		return
	

def clear():

	_ = call('clear' if os.name == 'posix' else 'cls')
	
	
#tomorrow test this out then apply with subproccess and figlet
#afterwards apply stopping conditions


# why have i not used dicts before they are so useful

stringy = f"L : {left_score} -- {right_score} : R"
subprocess.Popen(["figlet", stringy])

while True:
	
	# put to sleep until someone talks?
	start = voice_command(False)
	if start == "exit":
		sys.exit()

	basic_commands()
	clear()
	subprocess.Popen(["figlet", f"L : {left_score} -- {right_score} : R"])
		
	
		
		
		
		
		
		
		
		
		
