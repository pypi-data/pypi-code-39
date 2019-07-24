class CMDApp:
	def __init__(self):
		self.commands = {}
		self.minimumArgs = {}
		self.quitCommands = ["q", "quit"]
		self.help = {}
		self.prompt = ">> "

	def setCommands(self, commands):
		self.commands = commands
	
	def setMinimumArgs(self, minimumArgs):
		self.minimumArgs = minimumArgs

	def setQuitCommands(self, quitCommands):
		self.quitCommands = quitCommands

	def setHelp(self, help):
		self.help = help

	def setPrompt(self, prompt):
		self.prompt = prompt

	def start(self):
		while True:
			command = input(self.prompt).split(" ")
			if command[0] in self.commands:
				if command[0] in self.minimumArgs and self.minimumArgs[command[0]] >= len(command):
					print(f'The command {command[0]} expects at least {self.minimumArgs[command[0]]} arguments.')
				else: self.commands[command[0]](command[1:])
			
			elif command[0] in self.quitCommands:
				break

			elif command[0] == "help":
				self.printHelp(command)

			elif command[0] == "?": 
				options = '\n\t'.join(list(self.commands.keys()))
				print(f'Possible options:\n\t{options}')
			
			else:
				print("Unrecognised command.")

	def printHelp(self, command):
		if len(command) == 1:
			for cmd, h in self.help.items():
				print(f'{cmd}: {h}')
			print("help: Display this help message.")
			print(f'{" | ".join(self.quitCommands)}: Exit app.')

		else:
			if command[1] in self.commands:
				print(f'{command[1]}: {self.help[command[1]]}')
			else:
				print("Unrecognised command for help.")

		
