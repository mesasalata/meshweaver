from token_set import seed_tokens_to_file


if __name__ == "__main__":
    # "long.txt" is the full text of Jane Eyre: >1MB in size.
    with open("datasets/long.txt", "r") as test_sample_text_file:
        sample_text = test_sample_text_file.read()

    # Put 1024 most common tokens into tokens.txt
    seed_tokens_to_file("tokens.txt", sample_text, False, 1024) # Switch to True if too slow
