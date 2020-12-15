def id_and_visit_from_filename(filename: str) -> str:
    import re
    pattern="SF([0-9]+)V([0-9]+)H.dcm"
    match = re.match(pattern, filename)
    return int(match.groups()[0]), int(match.groups()[1])
