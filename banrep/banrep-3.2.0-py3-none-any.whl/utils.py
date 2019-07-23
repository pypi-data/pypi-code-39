# coding: utf-8
"""Módulo para funciones de interacción con el sistema."""
from pathlib import Path
import random


def crear_directorio(nombre):
    """Crea nuevo directorio si no existe.

    Si no es ruta absoluta será creado relativo al directorio de trabajo.

    Parameters
    -------------
    nombre : str | Path
        Nombre de nuevo directorio a crear.

    Returns
    ---------
    Path
        Ruta absoluta del directorio.
    """
    ruta = Path(nombre).resolve()

    if not ruta.is_dir():
        ruta.mkdir(parents=True, exist_ok=True)

    return ruta


def iterar_rutas(directorio, aleatorio=False, recursivo=False, exts=None):
    """Itera rutas de archivos en directorio.

    Puede ser o no recursivo, en orden o aleatorio, limitando extensiones.

    Parameters
    ----------
    directorio : str | Path
        Directorio a iterar.
    aleatorio : bool
        Iterar aleatoriamente.
    recursivo: bool
        Iterar recursivamente.
    exts: Iterable
        Solo considerar estas extensiones.

    Yields
    ------
    Path
        Ruta de archivo.
    """
    absoluto = Path(directorio).resolve()

    if recursivo:
        rutas = (r for r in absoluto.glob("**/*"))
    else:
        rutas = (r for r in absoluto.iterdir())

    rutas = (r for r in rutas if r.is_file() and not r.name.startswith("."))

    if exts:
        rutas = (r for r in rutas if r.suffix in exts)

    todas = sorted(rutas)
    if aleatorio:
        random.shuffle(todas)

    yield from todas
