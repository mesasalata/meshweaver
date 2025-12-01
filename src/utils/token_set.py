# import time # Profiling
from src.utils.logger import log
from rich.progress import Progress


## Constants
# Maximum number of tokens generated.
default_token_count = 1024
# Maximum token length
max_expr_length = 8
# Minimum token length
min_expr_length = 2
# Number of repeats necessary for a token to be added to the set
token_repeat_margin = 3
# Scaling power for length of a word to the value the word provides
scaling_pow = 3

## DATA regarding different variable settings:
# For all below: max_expr_length = 8, token_repeat_margin = 3, text = datasets/long.txt, fast = False, token_count = 1024
# min_expr_length = 2, scaling_pow = 1: 58% replacement
# min_expr_length = 3, scaling_pow = 1: 79% replacement
# min_expr_length = 4, scaling_pow = 1: 69% replacement (no min_expr_length > 4 because it would be worse)
# min_expr_length = 2, scaling_pow = 2: 86% replacement
# min_expr_length = 3, scaling_pow = 2: 80% replacement (no min_expr_length > 3 because it would be worse)
# min_expr_length = 2, scaling_pow = 3: 87% replacement (no min_expr_length > 2 because it would be worse) # CHOSEN
# min_expr_length = 2, scaling_pow = 4: 87% replacement (no min_expr_length > 2 because it would be worse)

# Replace Unicode and complicated characters with simpler characters, in order to get more optimised tokens
# Note: Add more replacements
replacements = {
    "”": "\"",
    "“": "\"",
    "’": "\'"
}
# Note: Remove all names from long.txt


def seed_tokens(sample_text: str, fast: bool = False, token_count: int = default_token_count, silent: bool = False) -> list[str]:
    """Seeds a token set with latin characters. Sloppy function as of right now."""

    char_tokens = [] # Lower priority of use. Recommended that all tokens only contain characters from this set.
    expr_tokens = [] # Expressions composed of multiple characters. Higher priority of use.

    # Add all default characters (most ASCII characters)
    for letter in "abcdefghijklmnopqrstuvwxyz":
        char_tokens.append(letter)
    for digit in "1234567890":
        char_tokens.append(digit)
    for symbol in " ,<.>/?;:\'@#~]}[{=+-_)(*&^%$£\"\n\\|`":
        char_tokens.append(symbol)

    # Get token limit and copy sample text
    remaining_token_count = token_count - len(char_tokens)
    remaining_text = sample_text.lower()

    # Replace Unicode and complicated characters with simpler characters, in order to get more optimised tokens
    for key in replacements.keys():
        remaining_text = remaining_text.replace(key, replacements[key])

    # Get lowercase because capital letters decrease token optimisation
    # Also split text into lines so that the algorithm is easier to work with
    remaining_texts = remaining_text.split("\n")

    # total_calc_time = 0.0 # Profiling
    # total_repl_time = 0.0 # Profiling
    single_chars_left = 0 # Logging

    # Logging
    progress = Progress()
    progress.start()
    generation_progress = progress.add_task("Generating tokens...", total=len(sample_text), start=False)

    if not silent:
        log(f"Generating up to {remaining_token_count} tokens with text \"{remaining_text[:30].replace('\n', ' ')}{"(...)" * int(len(remaining_text) > 30)}\" (length {len(sample_text)}).")
        log(f"Token length range {min_expr_length} to {max_expr_length}, token repeat margin {token_repeat_margin}, length scaling power {scaling_pow}.")
        if fast:
            log("Fast mode on.")

    # Break if reached token limit
    while len(expr_tokens) < remaining_token_count:
        # Profiling
        # start_time = time.process_time()

        # Frequency calculation of all tokens
        frequencies = {}

        for remaining_text in remaining_texts:
            for token_length in range(max_expr_length, (min_expr_length - 1), -1):
                if len(remaining_text) < token_length:
                    continue

                for index in range(0, len(remaining_text) - token_length + 1):
                    expr = remaining_text[index:(index + token_length)]

                    if expr in frequencies:
                        frequencies[expr] += 1
                    else:
                        frequencies[expr] = 1

        # Sort most important tokens
        tokenising_effects = {key: frequencies[key] * pow(len(key), scaling_pow) for key in frequencies.keys()} # Get effects of removing tokens
        token_candidates = sorted(tokenising_effects.keys(), key=tokenising_effects.get) # Sort these effects
        most_effect = ""

        if fast and not silent:
            log("(Fast mode) Token effect calculation complete.")
            log("(Fast mode) Starting token replacement.")

        # Profiling
        # calc_time = time.process_time() - start_time
        # total_calc_time += calc_time
        # start_time = time.process_time()

        # Hella janky:
        # Slow (not fast): Recalculates frequencies for every token
        # Fast: Calculates frequencies once and gets all tokens if fast
        # Also break if reached token limit or no more token candidates left
        while len(expr_tokens) < remaining_token_count and token_candidates:
            # Get most important token
            most_effect = token_candidates.pop(-1)

            # Break if token is not repeated (not worth it)
            if frequencies[most_effect] == 1:
                break
            expr_tokens.append(most_effect)

            # Remove token from the remaining text
            new_remaining_texts = []
            for remaining_text in remaining_texts:
                if len(remaining_text) >= min_expr_length: # Small optimisation: texts smaller than min_expr_length have no replacements left
                    if len(remaining_text) >= len(most_effect): # Another small optimisation: texts smaller than replacement do not contain the replacement
                        new_remaining_texts += remaining_text.split(most_effect)
                    else:
                        new_remaining_texts.append(remaining_text)
                else:
                    single_chars_left += len(remaining_text) # Logging
            remaining_texts = new_remaining_texts

            # Logging
            progress.start_task(generation_progress)
            progress.update(generation_progress, advance=int(tokenising_effects[most_effect] / pow(len(most_effect), scaling_pow - 1)))

            # Calculate frequencies again if on slow mode
            if not fast:
                break

        # Break if nothing left to do
        if frequencies[most_effect] == 1:
            break

        # Profiling
        # repl_time = time.process_time() - start_time
        # total_repl_time += repl_time
        # print(f"Added token: \"{most_effect}\" with effect {int(tokenising_effects[most_effect] / pow(len(most_effect), scaling_pow - 1))} (scaling {pow(len(most_effect), scaling_pow)})")
        # print(f"Token counting time:    {str(calc_time)[:10]} seconds (total {str(total_calc_time)[:10]} seconds)")
        # print(f"Token replacement time: {str(repl_time)[:10]} seconds (total {str(total_repl_time)[:10]} seconds)")
        # print()

    # Logging
    total = 0
    for remaining_text in remaining_texts:
        total += len(remaining_text)

    progress.update(generation_progress, advance=len(sample_text))
    progress.stop()

    if not silent:
        log("Token generation complete.")
        log(f"Initial:  {len(sample_text)}")
        log(f"Leftover: {' ' * (len(str(len(sample_text))) - len(str(total + single_chars_left)))}{total + single_chars_left}")
        log(f"Reduction ratio: {round(100 - 100 * (total + single_chars_left) / len(sample_text))}%")
        log(f"{default_token_count - remaining_token_count + len(expr_tokens)} tokens generated.")

    # Add with expr_tokens before char_tokens because they have a higher priority
    return expr_tokens + char_tokens


def seed_tokens_to_file(path: str, *args, **kwargs) -> list[str]:
    """Writes a token set to a file path, generating the token set if necessary."""

    if not "tokens" in kwargs:
        # Seed tokens if no tokens provided
        tokens = seed_tokens(*args, **kwargs)
    else:
        tokens = kwargs["tokens"]

    # Write
    with open(path, 'w') as file:
        for token in tokens:
            file.write(token + "\n") # I know, complicated reading, but it's definitely possible (I will do it)

    return tokens


def get_tokens_from_file(path: str) -> list[str]:
    """Gets a token set from a .txt file."""

    tokens = []

    # Open file
    with open(path, 'r') as file:
        # Loop over all lines until the penultimate one (the last line is blank)
        lines = file.readlines()
        for line in lines[:-1]:
            # Newline characters are not allowed in tokens, so the only token with a newline is the newline token
            if len(line) == 1:
                if "\n" not in tokens:
                    tokens.append("\n")
            else:
                # Otherwise the line is a token - remove the last character because it is a newline
                tokens.append(line[:-1])

    return tokens
