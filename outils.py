import flag
import pycountry
from pycountry.db import Country


def get_country_flag_emoji(country:Country):
    if country:
        flags=""
        try:
            countries = country.split(",")
            for country in countries:
                country_obj = pycountry.countries.search_fuzzy(country)[0]
                country_code = country_obj.alpha_2
                flags += flag.flag(country_code)
            return flags
        except Exception:
            return ""
    else:
        return ""