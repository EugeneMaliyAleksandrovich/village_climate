from collectors.climate_collector import ClimateStationCollector
from config import Config

collector = ClimateStationCollector(Config.STATION_URL)
collector.collect()