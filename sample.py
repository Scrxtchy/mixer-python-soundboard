import beam_interactive2, asyncio
import requests
import json
import subprocess
import os
from sys import argv

def run(shit):
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(shit.loop())
	finally:
		print('end-prog')
		loop.stop()


class example():
	def __init__(self):
		self.interactive = None

	async def setup(self):
		try:
			with open('auth.txt', 'r') as auth: #<----- Remember to put your interactive token in auth.txt~~ https://interactive.mixer.com/request
				mixerInteractive = await beam_interactive2.State.connect(
					authorization="Bearer " + auth.read(),
					project_version_id=42489,
					project_sharecode="rheo1hre")
		except Exception as e:
			print("Error connecting;", e)
			return

		self.interactive = mixerInteractive
		self.interactive.on('error', lambda e: self.fatal_error(e))
		self.interactive.on('giveInput', lambda call: self.keypress(call))
		self.interactive.pump_async()
		print('async started')
		await self.setupControls()

	async def setupControls(self):
		with open("schematic.json") as schematic:
			buttons = json.loads(schematic.read())
		for button in buttons['soundboard']:
			tempButton = beam_interactive2.Button(
				control_id=button['control_id'],
				text=button['text'],
				cost=button['cost'],
				position=button['position'])
			tempButton.on('mousedown', lambda call:self.buttonPress(call, os.getcwd() + '/audio/' + button['SoundPath']))
			await self.interactive.scenes['default'].create_controls(tempButton)
			del tempButton
		
		await self.interactive.set_ready()


	async def buttonPress(self, call, audioFile):
		print('playing ' + audioFile)
		subprocess.call(["ffplay", "-nodisp", "-autoexit", "-v", "quiet", audioFile])

	async def keypress(self, call):
		pass
		#print('keypress')
		#print(call)

	async def loop(self):
		print('loop')
		await self.setup()
		while True:
			await asyncio.sleep(1)

	def fatal_error(self, e):
		self._running = False
		raise e

run(example())