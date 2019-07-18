#!/usr/bin/env python3

import unittest
import os
import pprint

from sitelogparser.common.sitelog import SiteLogParser



class TestSitelogParser(unittest.TestCase):

    def setUp(self):
        sitelog_file = os.path.join(os.path.dirname(__file__), "AMST_20190705.txt")
        self.parser = SiteLogParser(sitelog_file)
        self.sitelog_data = self.parser.get_data()

    def test_antennas(self):
        self.assertEqual(len(self.sitelog_data["sitelog"]["gnss_antennas"]["list"]), 6)

    def test_receivers(self):
        self.assertEqual(len(self.sitelog_data["sitelog"]["gnss_receivers"]["list"]), 20)

    def test_apos_sis(self):
        d = self.sitelog_data["sitelog"]
        site = {
            "name": d["site_identification"]["site_name"],
            "four_letter_code": d["site_identification"]["four_character_id"],
            "ip_address": "0.0.0.0",
            "monument": {
                "antennas": [],
                "domes_number": d["site_identification"]["iers_domes_number"],
                "station": {
                    "four_letter_code": d["site_identification"]["four_character_id"],
                    "receivers": [],                        
                }
            }
        }
        for obj in d["gnss_antennas"]["list"]:
            site["monument"]["antennas"].append({
                "valid_from": obj["gnss_antenna"]["date_installed"],
                "valid_until": obj["gnss_antenna"]["date_removed"],
                "antenna_typ": str(obj["gnss_antenna"]["antenna_type"][:-4]).strip(),
                "antenna_snr": obj["gnss_antenna"]["serial_number"],
                "radome_typ": obj["gnss_antenna"]["antenna_radome_type"],
                "radome_snr": obj["gnss_antenna"]["radome_serial_number"],
            })
        for obj in d["gnss_receivers"]["list"]:
            site["monument"]["station"]["receivers"].append({
                "valid_from": obj["gnss_receiver"]["date_installed"],
                "valid_until": obj["gnss_receiver"]["date_removed"],
                "firmware": obj["gnss_receiver"]["firmware_version"],
                "receiver_typ": obj["gnss_receiver"]["receiver_type"],
                "receiver_snr": obj["gnss_receiver"]["serial_number"],
            })


if __name__ == '__main__':
    unittest.main()



