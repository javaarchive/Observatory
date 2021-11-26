from .Multiextractor import MultiExtractor
from .BestBuyExtractor import BestBuyExtractor
extractors = [MultiExtractor,BestBuyExtractor]

def create_instances():
    instances = []
    for extractor in extractors:
        instances.append(extractor())
    return instances