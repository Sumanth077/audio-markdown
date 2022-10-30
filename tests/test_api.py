"""Test transcript_to_markdown."""
import pytest

from steamship import Steamship

from src.api import ChineseTokenizer

TEST_STRING = "美国中期选举很重要。选民投票选举的范围包括众议院的所有席位、参议院的三分之一席位，以及数以千计的州的立法机构和行政领导职位。"


def test_clean():
    """Test behavior."""
    client = Steamship(profile="staging")
    tokenizer = ChineseTokenizer(client)
    response = tokenizer.tokenize_string(TEST_STRING)
    print(response)