"""
Demonstration of using selenium to automate Odoo. This program does not
actually run any tests per se, but does run an automated action, starting
with choosing a database, logging in, then going through the process of
creating and saving a sales order.
"""

from selenium import webdriver
import time

from OdooTest import OdooSession

session = OdooSession()
session.ChooseDatabase("rothman")
session.Login("admin", "admin")

#
#  This shows how to create products, some with an initial inventory
#  adjustment and some without
#
for i in range(5):
    product_name = "Inventory %d" % i
    session.CreateProduct(product_name, initial=1000 * i)
    product_name = "No Inventory %d" % i
    session.CreateProduct(product_name)
