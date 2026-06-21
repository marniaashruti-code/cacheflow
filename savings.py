# Public AWS S3 standard storage price: ~$0.023 per GB per month
COST_PER_GB_MONTH = 0.023

# Published estimate: data centers use roughly 0.0065 kWh per GB stored per month
KWH_PER_GB_MONTH = 0.0065

def calculate_savings(bytes_saved):
    """Converts bytes saved into estimated $ and energy saved per month."""
    gb_saved = bytes_saved / (1024 ** 3)
    dollars_saved = gb_saved * COST_PER_GB_MONTH
    kwh_saved = gb_saved * KWH_PER_GB_MONTH
    return dollars_saved, kwh_saved