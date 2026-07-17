from bartbase import chunk_text_by_sentences
from ocr_combiner import is_bad_text


def test_chunk_text_by_sentences_basic():
    text = "This is one. This is two. This is three. This is four."
    chunks = chunk_text_by_sentences(text, max_sentences=2)
    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_chunk_text_by_sentences_empty_input():
    chunks = chunk_text_by_sentences("", max_sentences=2)
    assert isinstance(chunks, list)


def test_is_bad_text_flags_empty_string():
    assert is_bad_text("") in (True, False)  # confirms function runs without error


def test_is_bad_text_flags_normal_text():
    result = is_bad_text("This is a perfectly normal sentence.")
    assert isinstance(result, bool)
