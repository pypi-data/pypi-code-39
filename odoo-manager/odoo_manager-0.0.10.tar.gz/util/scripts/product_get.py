import psycopg2

"""
Simple script to get fields from a database. Uncomment the one section below
to show the index vs. column names. I just piped the output to a csv for
later use.
"""

try:
    conn = psycopg2.connect("dbname='BHS_Production' user='odoo9e' host='localhost' password='youwish'")
except:
    print("Problems connecting to the database.")

cur = conn.cursor()
cur.execute("SELECT * FROM product_product")
rows = cur.fetchall()

# shows the columns of the query
# for i, item in enumerate(cur.description):
# 	print("%2d. %s" % (i, item))

print("id,description")

for row in rows:
    print("%d,%s" % (row[0], row[4]))
