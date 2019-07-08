#!/usr/bin/env python3
import boto3
import argparse
import time

SLA_ZONE_ID = "SLA_ZONE_ID"
PERSONAL_ONE = "Z1XY6GIMZ8S0NH"

### Todo : make -d flag actually work from cli, 
## cleanup and get_obj etc
class DNSEntry:
    """
    Wraps AWS's Route 53 DNS service to either insert a record, or to pull a record from a given domain.
    """
    sla_zone_id = PERSONAL_ONE

    def __init__(self, name_entry=None, value_entry=None, target_domain_id=None):
        self.subdomain = name_entry  # type: str
        self.value_entry = value_entry  # type: str
        self.target_zone_id = self.sla_zone_id
        if target_domain_id is not None: self.target_zone_id = target_domain_id  # type: str
        self.client = boto3.client("route53")
        self.root_domain_name = self.client.get_hosted_zone(Id=self.target_zone_id)["HostedZone"]["Name"]

    def driver(self) -> boto3.client:
        """
        :return: instantiated Amazon Route53
        """
        return self.client

    def verify(self, entry_name):
        """ Check whether or not an entry was succesfully added. """
        for entry in self.pull_records():
            if entry_name in entry["Name"]:
                ret = entry["Type"], entry["Name"], entry["ResourceRecords"][0]["Value"]
                print(ret)
                return ret

    def pull_records(self) -> boto3.resource:
        """
        Return either the entire hosted zones JSON object or hosted_zones[sla-ptt.com.]
        :param key: root domain
        :return: boto3 json object.
        """
        return self.client.list_resource_record_sets(HostedZoneId=self.target_zone_id)["ResourceRecordSets"]

    def set_record(self, record_type="A", name: "name  column" = None, value: "value column" = None,
                   ttl: int = 60) -> boto3.resource:
        """
        Insert a record into the AWS Route53 records. Be very_very_careful!
        :param record_type: A, CNAME, TXT, NS, MX
        :param name: Name column, ie, subdomain
        :param value: Value column: ie, IP address, txt entry, etc
        :return:
        """
        if name is None: name = self.subdomain
        if value is None: value = self.value_entry
        print("Inserting:     {}   {}   {}   [domain: {}]".format(record_type, name, value, self.root_domain_name))
        for i in range(0, 5):
            print("{}\r".format(5 - i), end="", flush=True)
            time.sleep(1)
        response = self.client.change_resource_record_sets(
            HostedZoneId=self.target_zone_id,
            ChangeBatch={

                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": name + "." + self.root_domain_name,
                            "Type": record_type,
                            "TTL": ttl,
                            "ResourceRecords": [{"Value": value}]
                        }
                    }]
            }
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("-OK- : [{}] {}.{}".format(record_type, name, self.root_domain_name))
        else:
            print("FAIL -- " + response["ResponseMetadata"]["HTTPStatusCode"])
        return response

    def records(self):
        """
        :return: iterable by domains
        """
        rec = self.pull_records()
        return [self.verify(record["Name"]) for record in rec]


class R53Args(DNSEntry):

    def __init__(self):
        """
        version 2 - removed the pull function. Accepts arguments like one would find in a zonefile.

        """
        self.parser = argparse.ArgumentParser()
        self.cliargs = self._do_parse_args()
        super().__init__(self.cliargs.name_column, self.cliargs.value_column,
                         self.cliargs.domain if self.cliargs.domain else None)
        self.set_record(self.cliargs.record_type)

    def _do_parse_args(self):
        """
        Get the command line args.
        should look like: ./route53.py A new_deployment 10.9.5.180
        does:
        A record, name: new_deployment.sla-ptt.com, value: 10.9.5.18
        :return:
        """

        self.parser.add_argument(
            "record_type",
            help="Type of record to insert.",

        )
        self.parser.add_argument(
            "name_column",
            help="Name column of the DNS entry.",

        )

        self.parser.add_argument(
            "value_column",
            help="Value column of the DNS entry.",

        )

        self.parser.add_argument(
            "-d", "--domain",
            help="Root domain - if other than sla-ptt.com"
        )

        a = self.parser.parse_args()

        return a


if __name__ == "__main__":
    R53Args()
