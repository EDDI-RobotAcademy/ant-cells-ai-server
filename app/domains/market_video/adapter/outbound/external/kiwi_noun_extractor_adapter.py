from kiwipiepy import Kiwi

from app.domains.market_video.application.port.noun_extractor_port import NounExtractorPort

_kiwi = Kiwi()

NOUN_TAGS = {"NNG", "NNP"}


class KiwiNounExtractorAdapter(NounExtractorPort):
    def extract_nouns(self, texts: list[str]) -> list[str]:
        nouns = []
        for text in texts:
            if not text:
                continue
            tokens = _kiwi.tokenize(text)
            for token in tokens:
                if token.tag in NOUN_TAGS:
                    nouns.append(token.form)
        return nouns
