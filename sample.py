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
		self.buttonobj = {}
		print('creating buttons')
		for button in buttons:
			self.buttonobj[button['controlID']] = beam_interactive2.Button(
				control_id=button['controlID'],
				text=button['text'],
				cost=button.get('cost', 0),
				position=button['position'],
				meta=button.get('meta', {"SoundPath": {"value": "it is a mystery.webm"}}))
			print("{} <= {}".format(button['controlID'], self.buttonobj[button['controlID']]._data['meta']._data['SoundPath']['value']))

			self.buttonobj[button['controlID']].on('mousedown', lambda call:self.buttonPress(call))
			await self.interactive.scenes['default'].create_controls(self.buttonobj[button['controlID']])
		await self.interactive.set_ready()
		print('#####################')
		print('new button meta values')
		for button in buttons:
			print("{} <= {}".format(button['controlID'], self.buttonobj[button['controlID']]._data['meta']._data['SoundPath']['value']))


	async def buttonPress(self, call):
		#print(call.__dict__)
		#print('playing ' + audioFile)
		print(self.buttonobj[call._payload['params']['input']['controlID']]._data['meta']._data)
		#._data['meta']._data['SoundPath']['value']
		#subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-v", "quiet", self.buttonobj[call._payload['params']['input'['controlID']]]._data['meta']._data['SoundPath']['value']])

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