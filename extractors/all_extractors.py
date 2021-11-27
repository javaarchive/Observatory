from .Multiextractor import MultiExtractor
from .BestBuyExtractor import BestBuyExtractor
from .WalmartExtractor import WalmartExtractor
extractors = [MultiExtractor,BestBuyExtractor,WalmartExtractor]

def create_instances():
    instances = []
    for extractor in extractors:
        instances.append(extractor())
    return instances