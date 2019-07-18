import sqlite3 as sq

taxa_table_command = '''CREATE TABLE IF NOT EXISTS taxa (
    id integer PRIMARY KEY,
    name text,
    description text,
    species bit,
    status integer
);'''

description_table_command = '''CREATE TABLE IF NOT EXISTS descriptions (
    id integer PRIMARY KEY,
    taxon text,
    number integer,
    thesa text,
    thesa_num integer,
    thesa_taxon text,
    athesa text,
    athesa_num integer,
    athesa_taxon text,
    status integer
);'''

taxa_insertion = '''INSERT INTO taxa (name, description, species, status)
    VALUES(?, ?, ?, 0);
'''

selecting_0_taxa = '''SELECT id, name from taxa
                      WHERE status=?
                      LIMIT 1'''

edit_taxa_status = '''UPDATE taxa
                      SET status=?
                      WHERE id=?'''

edit_taxa_description = '''UPDATE taxa
                           SET description=?
                           WHERE id=?'''

edit_taxa_species = '''UPDATE taxa
                       SET species=?
                       WHERE id=?'''

vertex_insertion = '''INSERT INTO descriptions (taxon, number, status)
                      VALUES(?, ?, 0)'''


class Storage:
    def __init__(self, db_name):
        conn = sq.connect(db_name)
        self.cursor = conn.cursor()
        self.cursor.execute(taxa_table_command)
        self.cursor.execute(description_table_command)
        self.min_status = 0

    def update_taxa_status(self, id, status):
        self.cursor.execute(edit_taxa_status, (status, id))

    def update_taxa_description(self, id, description):
        self.cursor.execute(edit_taxa_description, (description, id))

    def update_taxa_species(self, id, species):
        self.cursor.execute(edit_taxa_species, (species, id))

    def push_taxa(self, name, description="", species=True):
        self.cursor.execute(taxa_insertion, (name, description, species))
        self.min_status = 0

    def push_vertex(self, taxon, number):
        self.cursor.execute(vertex_insertion, (taxon, number))

    def shift_taxa(self):
        self.cursor.execute(selecting_0_taxa, [self.min_status])
        try:
            id, name = self.cursor.fetchone()
            self.update_taxa_status(id, self.min_status + 1)

            return id, name
        except:
            self.min_status += 1
            return self.shift_taxa()

