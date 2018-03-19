import re
from .utils import Utils
from .logger import log


class Scrape(Utils):
    """scrape a single e-mail from PA One Call e-mail notification service
    for request serial number, type, and location data.
    """

    def __init__(self, text):
        log.info("PARSING MAIL...")

        self.data = {}
        self._scrape(text)

    def _scrape(self, text):

        # print(repr(text))

        parsed_data = {}

        # Serial Number and Mapped Type are always on one line.
        # if"Serial Number--" in line:
        result1 = re.search(
            r"\Serial\b.*?\bNumber\b--.*?\[(.*?)\]", text, re.DOTALL)
        # print("result1", result1)
        if result1:
            # log.info("Serial Number: {0}".format(result1.group(1)))
            parsed_data["serial_number"] = result1.group(1)

        # if"Mapped Type--" in line:
        result2 = re.search(
            r"\bMapped\b.*?\bType\b--.*?\[(.*?)\]", text, re.DOTALL)
        # print("result2", result2)
        if result2:
            # log.info("Mapped Type: {0}".format(result2.group(1)))
            parsed_data["type"] = result2.group(1)

        result3 = re.search(
            r"\bMapped\b.*?\bLat\/Lon\b--.*?\[(.*?)\]", text, re.DOTALL)
        # print("result3", result3)
        if result3:
            # log.info("Mapped Lat/Lon: {0}".format(result3.group(1)))
            coords = [
                [self.find_floats(coord) for coord in each_latlon.split("/")]
                # each_latlon.split("/")
                for each_latlon in result3.group(1).strip("[]").split(",")
            ]
            if coords:
                # put coordinate pairs in order and make polygon
                coords = [[pair[1], pair[0]] for pair in coords]
                coords.append(coords[0])
                # log.info("Polygon coords: {0}".format([coords]))
                parsed_data["coordinates"] = [coords]

        log.info("parsed data: {0}".format(parsed_data))

        self.data = parsed_data
        return parsed_data
