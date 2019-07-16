spark_format = "org.elasticsearch.spark.sql"
es_nodes = "node"
es_user = "user"
es_password = "password"


elastic_spark_sql_write_options = {
    "es.mapping.date.rich": "true",
    "es.index.auto.create": "true",
    "es.net.ssl.protocol": "true",
    "es.nodes.wan.only": "true",
    "es.field.read.empty.as.null": "yes",
    # "es.resource": "",  # Maybe we'll get it from environment at some point
    # "es.net.http.auth.user": "",
    # "es.net.http.auth.pass": "",
    # "es.nodes": "",
}


def make_sql_write_elastic_options(user_options):
    """make a new dict to use for elastic write options"""
    options = {}
    for key in elastic_spark_sql_write_options:
        options[key] = elastic_spark_sql_write_options[key]

    for key in user_options:
        options[key] = user_options[key]

    return options
