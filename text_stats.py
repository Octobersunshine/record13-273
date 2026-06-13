import re
from collections import Counter
from dataclasses import dataclass, asdict
import json


@dataclass
class TextStats:
    char_count: int
    word_count: int
    sentence_count: int
    top5_words: list[tuple[str, int]]


def analyze(text: str) -> TextStats:
    char_count = len(text)

    words = re.findall(r"[A-Za-z\u4e00-\u9fff]+(?:'[A-Za-z]+)*", text)
    word_count = len(words)

    sentences = re.split(r'[.!?。！？]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)

    lowered = [w.lower() for w in words]
    counter = Counter(lowered)
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
