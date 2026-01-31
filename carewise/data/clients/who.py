"""WHO API Client"""

import requests
from config.settings import WHO_URL


# WHO GHO Indicator Mapping
WHO_INDICATOR_MAP = {
    "diabetes": "NCD_GLUC_04",
    "tuberculosis": "MDG_0000000020",
    "malaria": "MALARIA_EST_DEATHS",
    "hiv": "HIV_0000000026",
    "covid": "COVID19",
    "covid-19": "COVID19",
    "obesity": "NCD_BMI_30C",
    "hypertension": "NCD_HYP_PREVALENCE_A",
    "life expectancy": "WHOSIS_000001",
    "maternal mortality": "MDG_0000000026"
}


def get_who_indicator(topic):
    """Map health topic to WHO indicator code"""
    return WHO_INDICATOR_MAP.get(topic.lower())


def query_who(topic, limit=20):
    """Query WHO Global Health Observatory"""
    indicator = get_who_indicator(topic)
    
    if not indicator:
        print(f"ℹ️ WHO: No indicator mapping for '{topic}'")
        return []
    
    url = WHO_URL + indicator
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        data = res.json().get("value", [])

        results = [
            {
                "source": "WHO",
                "indicator": indicator,
                "topic": topic,
                "country": item.get("SpatialDim"),
                "year": item.get("TimeDim"),
                "value": item.get("NumericValue")
            }
            for item in data[:limit]
        ]
        
        return results
    except Exception as e:
        print(f"WHO API error: {e}")
        return []
