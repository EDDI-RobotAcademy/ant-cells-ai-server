from collections import Counter


class NounFrequencyService:
    MIN_NOUN_LENGTH = 2

    @staticmethod
    def count_frequencies(nouns: list[str]) -> list[tuple[str, int]]:
        """명사 리스트를 받아 빈도수 기준 내림차순 정렬된 (명사, 빈도수) 튜플 리스트를 반환한다."""
        filtered = [n for n in nouns if len(n) >= NounFrequencyService.MIN_NOUN_LENGTH]
        counter = Counter(filtered)
        return counter.most_common()
