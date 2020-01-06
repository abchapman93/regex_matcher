import re

class RegexMatcher:

    def __init__(self, vocab):
        self.vocab = vocab
        self._patterns = {}

    def add(self, match_id, patterns, on_match=None):
        if on_match is not None:
            raise NotImplementedError()
        if match_id not in self.vocab:
            self.vocab.strings.add(match_id)
        self._patterns.setdefault(self.vocab.strings[match_id], [])
        for pattern in patterns:
            self._patterns[self.vocab.strings[match_id]].append(re.compile(pattern))

    def get(self, key):
        return self._patterns.get(self.vocab.strings[key], [])

    def __call__(self, doc):
        matches = []
        for (match_id, patterns) in self._patterns.items():
            for pattern in patterns:
                re_matches = pattern.finditer(doc.text)
                for match in re_matches:
                    span = doc.char_span(match.start(), match.end())
                    matches.append((match_id, span.start, span.end))
        return matches