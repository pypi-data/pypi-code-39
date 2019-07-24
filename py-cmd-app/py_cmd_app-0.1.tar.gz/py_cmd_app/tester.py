from main import CMDApp

def tF(args):
	print(f't {args}')

def cF(args):
	print(f'c {args}')

def gF(args):
	print(f'g {args}')

app = CMDApp()

app.setCommands({
	"t": tF,
	"c": cF,
	"g": gF
})

app.setMinimumArgs({
	"t": 3,
	"c": 2
})

app.setHelp({
	"t": "The t command",
	"c": "The c command",
	"g": "The g command"
})


app.setPrompt("> ")
app.start()