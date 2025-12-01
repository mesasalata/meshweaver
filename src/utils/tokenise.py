from token_set import get_tokens_from_file


def tokenise(text: str, tokens_path: str = "tokens.txt") -> list[int]:
    """Tokenises selected text, turning it into a list of unsigned integers.
    Optionally configurable tokens file. Enter path relative to src/utils/tokenise.py."""

    token_set = get_tokens_from_file(tokens_path)
    tokens = []

    index = 0
    while index < len(text):
        for token in token_set:
            if token == text[index:(index + len(token))]:
                tokens.append(token)
                index += len(token) - 1 # - 1 because it will be + 1 below - spaghetti yay!
                break
        index += 1

    return tokens


def detokenise(tokens: list[int], tokens_path: str = "tokens.txt") -> str:
    """Detokenises a token list, turning it into a string. Currently, there is no concrete system for capitalising text.
    Optionally configurable tokens file. Enter path relative to src/utils/tokenise.py."""

    token_set = get_tokens_from_file(tokens_path)
    text = ""

    for token in tokens:
        text += token_set[token]

    return text
