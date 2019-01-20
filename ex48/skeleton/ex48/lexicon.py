class Lexicon(object):

    @classmethod
    def convert_number(self, s):
        try:
            return int(s)
        except ValueError:
            return None

    @classmethod
    def scan(self, s):
        directions = ['north', 'south', 'west', 'east', 'NORTH', 'SOUTH', 'WEST', 'EAST']
        verbs = ['go', 'kill', 'eat', 'stop', 'KILL']
        stops = ['the', 'in', 'of', 'at', 'from', 'it', 'FROM', 'to']
        nouns = ['bear', 'princess', 'Bear']

        result = []

        words = s.split()

        for word in words:
            if word in directions:
                result.append(('direction', word))
            elif word in verbs:
                result.append(('verb', word))
            elif word in stops:
                result.append(('stop', word))
            elif word in nouns:
                result.append(('noun', word))
            elif word.isdigit():
                result.append(('number', word))
            else:
                result.append(('error', word))

        return result
