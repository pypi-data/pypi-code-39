from psycopg2 import pool
connection_pool = pool.SimpleConnectionPool(1,10,"dbname='alexandria' user='alexandria' host='db1-newnew.dolcera.net' password='pergola-uncross-linseed' port= '5434'")