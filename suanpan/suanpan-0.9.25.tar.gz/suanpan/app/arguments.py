# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import app
from suanpan.imports import imports

Int = imports("suanpan.{}.arguments.Int".format(app.MODE))
Float = imports("suanpan.{}.arguments.Float".format(app.MODE))
Bool = imports("suanpan.{}.arguments.Bool".format(app.MODE))
String = imports("suanpan.{}.arguments.String".format(app.MODE))
List = imports("suanpan.{}.arguments.List".format(app.MODE))
ListOfString = imports("suanpan.{}.arguments.ListOfString".format(app.MODE))
ListOfInt = imports("suanpan.{}.arguments.ListOfInt".format(app.MODE))
ListOfFloat = imports("suanpan.{}.arguments.ListOfFloat".format(app.MODE))
ListOfBool = imports("suanpan.{}.arguments.ListOfBool".format(app.MODE))
IntOrFloat = imports("suanpan.{}.arguments.IntOrFloat".format(app.MODE))
IntFloatOrString = imports("suanpan.{}.arguments.IntFloatOrString".format(app.MODE))
BoolOrString = imports("suanpan.{}.arguments.BoolOrString".format(app.MODE))
StringOrListOfFloat = imports(
    "suanpan.{}.arguments.StringOrListOfFloat".format(app.MODE)
)
Json = imports("suanpan.{}.arguments.Json".format(app.MODE))

File = imports("suanpan.{}.arguments.File".format(app.MODE))
Folder = imports("suanpan.{}.arguments.Folder".format(app.MODE))
Data = imports("suanpan.{}.arguments.Data".format(app.MODE))
Csv = imports("suanpan.{}.arguments.Csv".format(app.MODE))
Npy = imports("suanpan.{}.arguments.Npy".format(app.MODE))
Visual = imports("suanpan.{}.arguments.Visual".format(app.MODE))
Model = imports("suanpan.{}.arguments.Model".format(app.MODE))
H5Model = imports("suanpan.{}.arguments.H5Model".format(app.MODE))
Checkpoint = imports("suanpan.{}.arguments.Checkpoint".format(app.MODE))
JsonModel = imports("suanpan.{}.arguments.JsonModel".format(app.MODE))

Table = imports("suanpan.{}.arguments.Table".format(app.MODE))
