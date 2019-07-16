server = "server-name"
username = "user-name"
password = "passwd"
driver = "jdbc-driver"


load_jdbc_options = {
    "header": "true",
    "encrypt": "false",
    "nullValue": "0",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
}


def make_load_sql_table_options(user_options):
    options = {}
    for key in load_jdbc_options:
        options[key] = load_jdbc_options[key]
    for key in user_options:
        options[key] = user_options[key]
    return options
