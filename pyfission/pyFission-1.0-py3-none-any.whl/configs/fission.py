"""
fission_src Structure:
:key = dwh_cred_shortname
:value = dict
    :key = database
    :value = list of dicts
        :key = tablename
        :value = dict
            :key = (mandatory) primary_key (pk), replication_key (rk), (optional) method (full/incremental)
            :value = list of fieldnames


fission_dest Structure:
:key = dwh_cred_shortname
:value = dict
    :key = dwh_cred_shortname serving as source
    :value = destination schemaname/datasetname
"""

fission_src = {
}

fission_dest = {
}
