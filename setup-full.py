from src.utils.token_set import seed_tokens_to_file
from src.utils.logger import log


# Only run from setup-full.sh
if __name__ == "__main__":
    token_file_path = "../../src/utils/tokens.txt"

    log(f"Seeding tokens to {token_file_path.split("/")[-1]}...", "info")

    # "long.txt" is the full text of Jane Eyre: >1MB in size.
    with open("../../datasets/long.txt", "r") as test_sample_text_file:
        sample_text = test_sample_text_file.read()

    # Put 1024 most common tokens into tokens.txt
    seed_tokens_to_file(token_file_path, sample_text=sample_text, fast=False, token_count=1024) # Switch to True if too slow

    log(f"Tokens seeded to {token_file_path.split("/")[-1]}.", "info")
