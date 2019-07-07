import asyncio
class BaseDeDatos:
	#base_de_datos = pack.BaseDeDatos("usuarios")
	def __init__(self, archivo="test"):
		self.archivo = archivo.replace(".json", "") + ".json"
		open(self.archivo, "a")

	def leer(self):
		archivo = open(self.archivo, "r").read() 
		db = eval(archivo)
		print(db)

	def obtener(self):
		archivo = open(self.archivo, "r").read() 
		db = eval(archivo)
		return db

	def escribir(self, datos):
		archivo = open(self.archivo, "w")
		texto = str(datos)
		archivo.write(texto)

	async def leer_async(self, tiempo1=10, tiempo2=1):
		archivo = open(self.archivo, "r").read() 
		await asyncio.sleep(tiempo1)
		db = eval(archivo)
		await asyncio.sleep(tiempo2)
		print(db)

	async def obtener_async(self, tiempo1=10, tiempo2=1):
		archivo = open(self.archivo, "r").read() 
		await asyncio.sleep(tiempo1)
		db = eval(archivo)
		await asyncio.sleep(tiempo2)
		return db

	async def escribir_async(self, datos, tiempo1=10, tiempo2=1):
		archivo = open(self.archivo, "w")
		await asyncio.sleep(tiempo1)
		texto = str(datos)
		await asyncio.sleep(tiempo2)
		archivo.write(texto)