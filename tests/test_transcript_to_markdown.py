import pytest
from src.transcript_to_markdown import transcript_to_markdown

MARKDOWN_TEST_CASES = [
    ("foo bar heading one bar", "foo bar \n# bar"),
    ("grocery list numbered list sandwiches end item cheese sticks end item fruit snacks end element the end", "grocery list \n1. sandwiches \n2. cheese sticks \n3. fruit snacks \nthe end"),
    ("grocery list bulleted list sandwiches end item cheese sticks end item fruit snacks end element the end", "grocery list \n* sandwiches \n* cheese sticks \n* fruit snacks \nthe end"),
    ("heading one This is the first heading heading two This is the second heading heading three This is the third heading heading four This is the fourth heading heading five This is the fifth heading heading six This is the sixth heading",
     "# This is the first heading \n## This is the second heading \n### This is the third heading \n#### This is the fourth heading \n##### This is the fifth heading \n###### This is the sixth heading"),
    ("foo bar heading 3 bar", "foo bar \n### bar"),
    ("heading one This is a top level heading end element this is normal text", "# This is a top level heading \nthis is normal text")
]

@pytest.mark.parametrize("input_text,output_text", MARKDOWN_TEST_CASES)
def test_transcript_to_markdown(input_text: str, output_text: str):
    result = transcript_to_markdown(input_text)
    print(f"\nINPUT\n{input_text}\n\nOUTPUT\n{result}")

    assert result == output_text



