import re
from collections import Counter
from dataclasses import dataclass, asdict
import json


DEFAULT_STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "can", "could", "may", "might", "must", "ought", "this",
    "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them", "my", "your", "his", "its", "our",
    "their", "what", "which", "who", "whom", "how", "when", "where", "why",
    "yes", "no", "not", "no", "so", "very", "just", "also", "too", "quite",
    "than", "then", "once", "here", "there", "as", "because",
})


@dataclass
class TextStats:
    char_count: int
    word_count: int
    sentence_count: int
    top5_words: list[tuple[str, int]]


def analyze(
    text: str,
    stop_words: set | frozenset | None = DEFAULT_STOP_WORDS,
    filter_stopwords: bool = True,
) -> TextStats:
    char_count = len(text)

    cleaned = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    words = [w for w in cleaned.split() if w]
    lowered = [w.lower() for w in words]

    if filter_stopwords and stop_words is not None:
        filtered_lowered = [w for w in lowered if w not in stop_words]
    else:
        filtered_lowered = lowered

    word_count = len(filtered_lowered)

    sentences = re.split(r'[.!?。！？]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)

    counter = Counter(filtered_lowered)
    top5_words = counter.most_common(5)

    return TextStats(
        char_count=char_count,
        word_count=word_count,
        sentence_count=sentence_count,
        top5_words=top5_words,
    )


if __name__ == "__main__":
    sample = (
        "The quick brown fox jumps over the lazy dog. "
        "The dog barked. The fox ran away quickly! "
        "Was the fox fast? Yes, the fox was very fast."
    )
    stats = analyze(sample)
    print(json.dumps(asdict(stats), ensure_ascii=False, indent=2))
