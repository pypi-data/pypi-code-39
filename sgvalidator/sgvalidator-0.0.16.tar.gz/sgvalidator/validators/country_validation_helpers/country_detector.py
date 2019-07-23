import re
import us
from ..validator_utils import ValidatorUtils


class CountryDetector:
    US_COUNTRY_CODE = "US"
    CA_COUNTRY_CODE = "CA"

    CANADA_STATE_VARIATIONS = {'ab', 'alberta', 'bc', 'british columbia', 'mb', 'manitoba', 'nb', 'new brunswick', 'nl',
                               'newfoundland and labrador', 'nt', 'northwest territories', 'ns', 'nova scotia', 'nu',
                               'nunavut', 'on', 'ontario', 'pe', 'prince edward island', 'qc', 'quebec', 'sk',
                               'saskatchewan', 'yt', 'yukon'}

    US_COUNTRY_CODE_VARIATIONS = {"us", "usa", "united states", "united states of america"}
    CA_COUNTRY_CODE_VARIATIONS = {"ca", "can", "canada"}

    @staticmethod
    def detect(row):
        state = row["state"]
        zipcode = row["zip"]
        country = row["country_code"]
        inferredCountryCode = CountryDetector.inferCountryCode(country)
        if inferredCountryCode == CountryDetector.US_COUNTRY_CODE or CountryDetector.isUsZip(
                zipcode) or CountryDetector.isUsState(state):
            return CountryDetector.US_COUNTRY_CODE
        elif inferredCountryCode == CountryDetector.CA_COUNTRY_CODE or CountryDetector.isCaZip(
                zipcode) or CountryDetector.isCaState(state):
            return CountryDetector.CA_COUNTRY_CODE
        else:
            return None

    @staticmethod
    def inferCountryCode(raw_country):
        if ValidatorUtils.is_blank(raw_country):
            return None

        normalized = raw_country.strip().lower()
        if normalized in CountryDetector.US_COUNTRY_CODE_VARIATIONS:
            return CountryDetector.US_COUNTRY_CODE
        elif normalized in CountryDetector.CA_COUNTRY_CODE_VARIATIONS:
            return CountryDetector.CA_COUNTRY_CODE
        return None

    @staticmethod
    def isUsZip(zipcode):
        if ValidatorUtils.is_blank(zipcode):
            return False

        cleaned_zip = str(zipcode).strip()
        firstpart = cleaned_zip.split("-")[0]
        if len(firstpart) == 5 and ValidatorUtils.is_number(firstpart):
            return True
        else:
            return False

    @staticmethod
    def isUsState(state):
        if ValidatorUtils.is_blank(state):
            return False

        cleanedState = state.strip().lower()
        return bool(us.states.lookup(cleanedState))

    @staticmethod
    def isCaZip(zipcode):
        pattern = re.compile("^[ABCEGHJ-NPRSTVXY][0-9][ABCEGHJ-NPRSTV-Z] [0-9][ABCEGHJ-NPRSTV-Z][0-9]$")
        return ValidatorUtils.is_not_blank(zipcode) and pattern.match(zipcode)

    @staticmethod
    def isCaState(state):
        if ValidatorUtils.is_blank(state):
            return False

        cleanedState = state.strip().lower()
        return cleanedState in CountryDetector.CANADA_STATE_VARIATIONS
