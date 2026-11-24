"""Build the inputs of step 7 of Supplement 1: the ten cases, the twenty pairs in a seeded order, and their key.

Usage: python3 -I s7_pairs.py OUT_FOLDER
Writes OUT_FOLDER/CASES.md (the ten cases as the parties see them), OUT_FOLDER/PAIRS.tsv (twenty pairs of a case and an
answer, in the order given by the seed 20261123, without labels) and OUT_FOLDER/key/KEY.tsv (which answer of each pair
is the known one; withheld from the parties).
"""
import csv
import os
import random
import sys

SEED = 20261123
OWN = 'It must be recorded: by a line of its own, or as a dependency of a recorded package.'
MUST = 'It must be recorded.'
NEED_NOT = 'It need not be recorded.'
CASES = [
    (1, 'Shared content or capability', 'A font, a translation or a theme shared by many programs.', OWN, NEED_NOT),
    (2, 'Lookup tables', 'Terminal descriptions and character tables.', OWN, NEED_NOT),
    (3, 'A package containing only dependencies',
     'An installed package that has no files of its own and only requires other packages.', MUST, NEED_NOT),
    (4, 'Support for absent hardware', 'Firmware for a device that is absent and boot files for another hypervisor.',
     MUST, NEED_NOT),
    (5, 'An object that the system recreates',
     'An object that, after it is removed, the system restores from another object.',
     'It needs no line of its own.', 'It must be recorded by a line of its own.'),
    (6, 'A system service setting', 'A setting of a system service.', MUST, NEED_NOT),
    (7, 'A compiled copy of code', 'A compiled copy of code that a program recreates itself.',
     'It must be recorded: it is covered by the line of the original package.', NEED_NOT),
    (8, 'A history that its program executes as code', 'A history file of a program that the program executes as code.',
     'It must be recorded: by a line of its own.', NEED_NOT),
    (9, 'A record that a service was enabled in the past',
     'A record that a service was enabled at some time in the past.',
     NEED_NOT, 'It must be recorded by a line of its own.'),
    (10, 'A browser extension', 'A browser extension that a person installed.', MUST, NEED_NOT),
]


def main(out):
    os.makedirs(os.path.join(out, 'key'), exist_ok=True)
    with open(os.path.join(out, 'CASES.md'), 'w', encoding='utf-8') as handle:
        handle.write('# Ten cases\n\nEach case is an object on a computer. Nothing here says what the object is in the '
                     'terms of the definition.\n\n')
        for number, title, description, _right, _wrong in CASES:
            handle.write(f'{number}. **{title}.** {description}\n')
    pairs = []
    for number, _title, _description, right, wrong in CASES:
        pairs.append((number, right, 'known'))
        pairs.append((number, wrong, 'opposite'))
    random.Random(SEED).shuffle(pairs)
    with open(os.path.join(out, 'PAIRS.tsv'), 'w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t', lineterminator='\n')
        writer.writerow(['pair', 'case', 'answer'])
        for index, (number, answer, _label) in enumerate(pairs, 1):
            writer.writerow([index, number, answer])
    with open(os.path.join(out, 'key', 'KEY.tsv'), 'w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t', lineterminator='\n')
        writer.writerow(['pair', 'case', 'label'])
        for index, (number, _answer, label) in enumerate(pairs, 1):
            writer.writerow([index, number, label])
    print('cases:', len(CASES), 'pairs:', len(pairs))


if __name__ == '__main__':
    main(sys.argv[1])
