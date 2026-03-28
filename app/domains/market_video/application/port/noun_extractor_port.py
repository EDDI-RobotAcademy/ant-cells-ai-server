from abc import ABC, abstractmethod


class NounExtractorPort(ABC):
    @abstractmethod
    def extract_nouns(self, texts: list[str]) -> list[str]:
        """텍스트 목록에서 명사 리스트를 추출한다."""
        pass
