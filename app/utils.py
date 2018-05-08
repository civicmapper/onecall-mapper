import re
from .logger import log

# --------------------------------------------
# UTILITIES


class Utils(object):

    def list_of_seq_unique_by_key(self, seq, key):
        # make sure spec'd key exists in provided records first
        seq = [x for x in seq if key in x.keys()]
        # create a list of unique keys from the records provided
        if seq:
            seen = set()
            seen_add = seen.add
            return [x for x in seq if x[key] not in seen and not seen_add(x[key])]
        else:
            return []

    def find_floats(self, string, lower=-180, upper=180):
        '''This will do its best to get a postive or negative float from a string
        that might contain other things.
        '''
        try:
            n = float(string)
            # make sure its in range
            if (upper >= n >= lower):
                return n
            else:
                return None
        except ValueError:
            # print(string)
            # optional - in front
            numexp1 = re.compile(r'[-]?\d[\d,]*[\.]?[\d{2}]*')
            numbers = numexp1.findall(string)
            # if the result has multiples, that mean something caused a split.
            if len(numbers) > 0:
                cleaned = [numbers[0]]
                # there may be decimals after the split, so we want to get numbers and decimals
                numexp2 = re.compile(r'[^\d.]+')
                for i in numbers[1:]:
                    cleaned.append(numexp2.sub('', i))
                # print(cleaned)
                # replace the contents of numbers with a single cleaned-up string
                numbers = ["".join(cleaned)]
                # print(numbers)
                try:
                    # finally, replace any commas acting as decimal points
                    n = float(numbers[0].replace(',', ''))
                    # make sure its in range
                    if (upper >= n >= lower):
                        return n
                    else:
                        return None
                except ValueError:
                    return None
            else:
                return None
        return None
