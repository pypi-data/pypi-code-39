mysql_to_bigquery = {
    #        'string'
    'char': 'string',
    'character': 'string',
    'varchar': 'string',
    'tinytext': 'string',
    'text': 'string',
    'mediumtext': 'string',
    'longtext': 'string',
    'enum': 'string',
    'blob': 'string',
    #        'integer'
    'tinyint': 'integer',
    'smallint': 'integer',
    'mediumint': 'integer',
    'integer': 'integer',
    'int': 'integer',
    'bigint': 'integer',
    #        'float/numeric'
    'float': 'numeric',
    'double': 'numeric',
    'real': 'numeric',
    'decimal': 'numeric',
    'fixed': 'numeric',
    'dec': 'numeric',
    'numeric': 'numeric',
    # date
    'date': 'date',
    #        'timestamp'
    'datetime': 'datetime',
    'timestamp': 'timestamp',
    'time': 'string',
    #        'boolean'
    'bit': 'boolean',
    'bool': 'boolean',
    'boolean': 'boolean',
}
rs_to_bigquery = {
    #        'string'
    'text': 'string',
    'character varying': 'string',
    'character': 'string',
    'char': 'string',
    'varchar': 'string',
    'time': 'string',
    #        'integer'
    'bigint': 'integer',
    'smallint': 'integer',
    'integer': 'integer',
    #        'numeric'
    'numeric': 'numeric',
    'double precision': 'numeric',
    'real': 'numeric',
    # date
    'date': 'date',
    #        'timestamp'
    'timestamp without time zone': 'datetime',
    'timestamp': 'datetime',
    'timestamp with time zone': 'timestamp',
    'timestampz': 'timestamp',
    #        'boolean'
    'boolean': 'boolean',
    # different
    'jsonb': 'string',
    'uuid': 'string',
}
mssql_to_bigquery = {
    # strings
    'varchar': 'string',

    # numeric
    'decimal': 'numeric',

}

bigquery_to_mysql = {
    'string': 'varchar',
    'date': 'date',
    'numeric': 'double',
    'float': 'double',
    'integer': 'int',
    'datetime': 'datetime',
    'timestamp': 'timestamp',
    'boolean': 'bool',
}
