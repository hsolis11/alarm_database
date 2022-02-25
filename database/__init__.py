import sqlite3
from sqlite3 import Error

from database.alarms import Alarms
from database.equipment import Vendors, EqpModels, EqpModules
from database.users import Users


def create_connection(db_file):
    """ Create a database connection to a SQLite database
        Specified by db_file
        :param db_file: database file
        :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statment
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(conn, sql):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


create_vendors = """CREATE TABLE IF NOT EXISTS vendors(
                        id integer PRIMARY KEY,
                        vendor text NOT NULL UNIQUE)"""

create_models = """CREATE TABLE IF NOT EXISTS eqp_models(
                        id integer PRIMARY KEY,
                        model text NOT NULL,
                        vendor integer NOT NULL,
                        FOREIGN KEY(vendor) REFERENCES vendors (id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE)"""

create_modules = """CREATE TABLE IF NOT EXISTS eqp_modules(
                        id integer PRIMARY KEY,
                        module text NOT NULL,
                        eqp_model integer NOT NULL,
                        FOREIGN KEY(eqp_model) REFERENCES eqp_models (id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE)"""

create_alarms = """CREATE TABLE IF NOT EXISTS alarms(
                        id integer PRIMARY KEY,
                        eqp_module integer NOT NULL,
                        alarm_id text NOT NULL,
                        title text NOT NULL,
                        message text NOT NULL,
                        cause text NOT NULL,
                        response NOT NULL,
                        FOREIGN KEY(eqp_module) REFERENCES eqp_modules (id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE)"""

create_ordered_parts = """CREATE TABLE IF NOT EXISTS ordered_parts(
                            id integer PRIMARY KEY,
                            q_number text NOT NULL,
                            vendor_pn text NOT NULL,
                            description text NOT NULL)"""

create_parts_common = """CREATE TABLE IF NOT EXISTS alarm_parts_common(
                            idalarms integer NOT NULL,
                            idordered_parts integer NOT NULL,
                            FOREIGN KEY(idalarms) REFERENCES alarms (id)
                            ON UPDATE CASCADE 
                            ON DELETE CASCADE
                            FOREIGN KEY(idordered_parts) REFERENCES ordered_parts (id)
                            ON UPDATE CASCADE 
                            ON DELETE CASCADE )"""

create_user = """CREATE TABLE IF NOT EXISTS users(
                        id integer PRIMARY KEY,
                        tech_id text NOT NULL UNIQUE,
                        f_name text NOT NULL,
                        l_name text NOT NULL,
                        password text NOT NULL,
                        created_date DEFAULT CURRENT_TIMESTAMP)"""

create_entries = """CREATE TABLE IF NOT EXISTS entries(
                        id integer PRIMARY KEY,
                        date DEFAULT CURRENT_TIMESTAMP,
                        iduser integer NOT NULL DEFAULT 0,
                        entry text NOT NULL,
                        idalarm integer NOT NULL,
                        FOREIGN KEY(iduser) REFERENCES users (id)
                        ON UPDATE CASCADE 
                        ON DELETE SET DEFAULT 
                        FOREIGN KEY (idalarm) REFERENCES alarms (id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE)"""

create_equipment_view = """CREATE VIEW equipment
                            AS
                            SELECT vendor, eqp_models.model, eqp_modules.module
                            FROM vendors
                            INNER JOIN eqp_models ON eqp_models.vendor = vendors.id
                            INNER JOIN eqp_modules ON eqp_modules.eqp_model = eqp_models.id"""

insert_vendors = """INSERT INTO
                    vendors(vendor)
                    VALUES('SEMES'), ('TEL')"""

insert_techs = """INSERT INTO users(tech_id, f_name, l_name, password)
                  VALUES('80111', 'john', 'doe', '$2b$12$KVDJUpweAmwF4wIqXXqXN.xQQ7J/4N/ExU.WGAhB9GkNFekx9N5n6'),
                        ('80112', 'bob', 'jones', '$2b$12$KVDJUpweAmwF4wIqXXqXN.xQQ7J/4N/ExU.WGAhB9GkNFekx9N5n6')"""

insert_eqp_models = """INSERT INTO eqp_models(vendor, model)
                        VALUES(1, 'KSPIN'), (1, 'LOZIX'), (2, 'ACT 12'), (2, 'LITHIUS'), 
                                (2, 'LITHIUS PRO'), (2, 'LITHIUS PRO V'), (2, 'LITHIUS PRO Z')"""

insert_eqp_modules = """INSERT INTO eqp_modules(eqp_model, module)
                        VALUES(1, 'SC'), (1, 'FUST'), (1, 'SCP'), (1, 'HP'), (1, 'TR'), (1, 'INDX'), (1, 'UPB'), (1, 'DNB'),
                        (2, 'COT'), (2, 'LP'), (2, 'CP'), (2, 'HP'), (2, 'TR'), (2, 'INDX'), (2, 'UPB'), (2, 'DNB'),
                        (3, 'PCT'), (3, 'LP'), (3, 'CP'), (3, 'HCH'), (3, 'PRA'), (3, 'CRA'), (3, 'TR'),
                        (4, 'COT'), (4, 'LP'), (4, 'CP'), (4, 'CPHP'), (4, 'PRA'), (4, 'CRA'), (4, 'DEV'), (4, 'WEE'),
                        (5, 'COT'), (5, 'LP'), (5, 'CP'), (5, 'CPHP'), (5, 'PRA'), (5, 'CRA'), (5, 'DEV'), (5, 'WEE'),
                        (6, 'COT'), (6, 'LP'), (6, 'CP'), (6, 'CPHP'), (6, 'PRA'), (6, 'CRA'), (6, 'DEV'), (6, 'WEE'),
                        (7, 'COT'), (7, 'LP'), (7, 'CP'), (7, 'CPHP'), (7, 'PRA'), (7, 'CRA'), (7, 'DEV'), (7, 'WEE')"""

insert_alarms = """INSERT INTO alarms(eqp_module, alarm_id, title, message, cause, response)
                    VALUES(1, '1234', 'Spin errors on SC1', 'Spin step counter is off', 'Driver malfunction', 'Replace spin driver'),
                    (2, '1234', 'FUST open error', 'FUST did not meet open time limit of 5sec', 'Sensor malfunction', 'Replace faulty open sensor'),
                    (3, '1234', 'SCP temp error', 'SCP failed to reach 23c temp', 'temp sensor malfunction', 'replace SCP'),
                    (4, '1234', 'HP temp error', 'HP failed to reach 400c temp', 'heating element has failed', 'replace HP controller'),
                    (5, '1234', 'TR2 fork 1 mishandle ', 'Object from fork 1 lost in transit', 'detection sensor malfunction', 'replace detection sensor'),
                    (6, '1234', 'INDX fork 2 mishandle ', 'Object from fork 1 lost in transit', 'detection sensor malfunction', 'replace detection sensor'),
                    (7, '1234', 'UPB movement errors', 'failed to reach final position', 'driver error', 'replace failing driver'),
                    (8, '1234', 'DNB movement errors', 'failed to reach final position', 'driver error', 'replace failing driver')"""

insert_entries = """INSERT INTO entries(`iduser`, `entry`, `idalarm`)
                    VALUES(1, "Attempted to replace faulty driver and error returned.", 1),
                            (1, "replaced the controller and alarm returned", 1),
                            (2, "replaced wiring harness from driver to the SC controller and alarm recovered.", 1)"""

insert_parts = """INSERT INTO ordered_parts(q_number, vendor_pn, `description`)
                    VALUES('q001-1234', 'NT123-GB123', 'spin driver'),
                            ('q002-1222', 'TR123-LM', 'spin controller'),
                            ('q001-1311', 'NT122-1131', 'wire harness')"""

insert_parts_common = """INSERT INTO alarm_parts_common(idalarms, idordered_parts)
                            VALUES(1, 1),
                                    (1, 2),
                                    (1, 3)"""



def main():
    conn = create_connection("test.db")
    create_table(conn, create_vendors)
    create_table(conn, create_models)
    create_table(conn, create_modules)
    create_table(conn, create_alarms)
    create_table(conn, create_user)
    create_table(conn, create_ordered_parts)
    create_table(conn, create_parts_common)
    create_table(conn, create_entries)
    create_table(conn, create_equipment_view)

    insert_data(conn, insert_vendors)
    insert_data(conn, insert_eqp_models)
    insert_data(conn, insert_eqp_modules)
    insert_data(conn, insert_alarms)
    insert_data(conn, insert_techs)
    insert_data(conn, insert_parts)
    insert_data(conn, insert_parts_common)
    insert_data(conn, insert_entries)

if __name__ == '__main__':
    main()
