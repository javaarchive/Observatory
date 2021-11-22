from .Multiextractor import MultiExtractor
extractors = [MultiExtractor]

def create_instances():
    instances = []
    for extractor in extractors:
        instances.append(extractor())
    return instances