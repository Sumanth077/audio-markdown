"""Test transcript_to_markdown."""
import pytest

from src.transcript_to_markdown import clean, transcript_to_markdown

MARKDOWN_TEST_CASES = [
    ("foo bar heading one bar", "foo bar \n# bar"),
    (
        "grocery list numbered list sandwiches finish item cheese sticks finish item fruit snacks finish element the end",
        "grocery list \n1. sandwiches \n2. cheese sticks \n3. fruit snacks \n\nthe end",
    ),
    (
        "grocery list bulleted list sandwiches finish item cheese sticks finish item fruit snacks finish element the end",
        "grocery list \n* sandwiches \n* cheese sticks \n* fruit snacks \n\nthe end",
    ),
    (
        "heading one This is the first heading heading two This is the second heading heading three This is the third "
        "heading heading four This is the fourth heading heading five This is the fifth heading heading six This is the "
        "sixth heading",
        "# This is the first heading \n## This is the second heading \n### This is the third heading \n#### This is the "
        "fourth heading \n##### This is the fifth heading \n###### This is the sixth heading",
    ),
    ("foo bar heading 3 bar", "foo bar \n### bar"),
    (
        "heading one This is a top level heading finish element this is normal text",
        "# This is a top level heading \n\nthis is normal text",
    ),
    ("foo, bar, heading, one, bar", "foo, bar, \n# bar"),
    (
        "Heading 1. Testing the SteamShabadi on Markdown Package. Here is a list of things we'd like to check, "
        "numbered lists with spur model, finish item, markdown extraction, finish item, webpage, finish element, "
        "the finish. Here is a list of things we don't care about, bolded list, misspellings, finish item, weird grammar, "
        "finish item, finish element, the end. And here are a list of headings, heading 1. This is the first heading, "
        "heading 2. This is the second heading, heading 3. This is the third heading, heading 4. This is the fourth "
        "heading, heading 5. This is the fifth heading, heading 6. This is the sixth heading. Thank you for listening to "
        "our test.",
        "# Testing the SteamShabadi on Markdown Package. Here is a list of things we'd like to check, \n1. with spur "
        "model, \n2. markdown extraction, \n3. webpage, \n\nthe finish. Here is a list of things we don't care about, "
        "bolded list, misspellings, weird grammar, \n\nthe end. And here are a list of headings, \n# This is the first "
        "heading, \n## This is the second heading, \n### This is the third heading, \n#### This is the fourth heading, "
        "\n##### This is the fifth heading, \n###### This is the sixth heading. Thank you for listening to our test.",
    ),
]


@pytest.mark.parametrize("input_text,output_text", MARKDOWN_TEST_CASES)
def test_transcript_to_markdown(input_text: str, output_text: str):
    """Test behavior."""
    result = transcript_to_markdown(input_text)
    print(f"\nINPUT\n{input_text}\n\nOUTPUT\n{result}")

    assert result == output_text


def test_clean():
    """Test behavior."""
    cleaned = clean("Flippity,")
    assert cleaned == "flippity"
