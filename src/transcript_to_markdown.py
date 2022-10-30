"""Convert raw text with prompts to Markdown format."""

import string


def fixed(value: str):
    """Fix input."""

    def heading_function(index: int) -> str:
        return value

    return heading_function


MARKDOWN_ELEMENTS = [
    # each element is a list of words that might be used in the transcript, plus the markdown heading prefix that will
    # be used, plus whether the prefix should carry over per-item until stopped.
    (["heading one", "heading 1"], fixed("#"), False),
    (["heading two", "heading 2"], fixed("##"), False),
    (["heading three", "heading 3"], fixed("###"), False),
    (["heading four", "heading 4"], fixed("####"), False),
    (["heading five", "heading 5"], fixed("#####"), False),
    (["heading six", "heading 6"], fixed("######"), False),
    (["bullet list", "bulleted list", "bulleted lists", "bullet lists"], fixed("*"), True),
    (
        ["number list", "numbered list", "numbered lists", "number lists"],
        lambda x: f"{x + 1}.",
        True,
    ),
    (["horizontal rule"], fixed("---\n"), False),
]

MARKDOWN_ELEMENTS_SPLIT = [
    (
        [text_possibility.split(" ") for text_possibility in text_possibilities],
        prefix_generator,
        carry_element,
    )
    for (text_possibilities, prefix_generator, carry_element) in MARKDOWN_ELEMENTS
]


def clean(token: str) -> str:
    """Remove punctuation and lower string."""
    result = token.lower()
    if result[-1] in string.punctuation:
        result = result[:-1]
    return result


def transcript_to_markdown(transcript: str) -> str:
    """Convert to markdown."""
    input_case_transcript_tokens = transcript.split(" ")
    lower_case_transcript_tokens = [clean(token) for token in input_case_transcript_tokens]

    output_tokens = []
    element_count = 0
    carried_element = None
    carried_newline = ""
    i = 0
    while i < len(lower_case_transcript_tokens):
        found_replacement = False
        for (text_possibilities, prefix_generator, carry_element) in MARKDOWN_ELEMENTS_SPLIT:
            for text_possibility in text_possibilities:
                if lower_case_transcript_tokens[i : i + len(text_possibility)] == text_possibility:
                    found_replacement = True
                    replacement_string = prefix_generator(element_count)
                    output_tokens.append(("\n" if i != 0 else "") + replacement_string)
                    i += len(text_possibility) - 1
                    carried_newline = ""
                    if carry_element:
                        carried_element = prefix_generator
                        element_count += 1
        if lower_case_transcript_tokens[i : i + 2] == ["finish", "element"]:
            carried_element = None
            element_count = 0
            carried_newline = "\n\n"
            found_replacement = True
            i += 1
        if lower_case_transcript_tokens[i : i + 2] == ["finish", "item"]:
            if carried_element is not None:
                output_tokens.append("\n" + carried_element(element_count))
            found_replacement = True
            i += 1
            element_count += 1
            carried_newline = ""

        if not found_replacement:
            output_tokens.append(carried_newline + input_case_transcript_tokens[i])
            carried_newline = ""
        i += 1
    return " ".join(output_tokens)
