import argparse
import datetime
import os.path
import re
import sys
import time
from pathlib import Path
from shutil import copy
from urllib import error
from urllib import parse
from urllib import request

YEAR = 2024

INPUT_FILENAME = 'input.txt'
TEMPLATE_DIR = Path('day00')
TEMPLATE_FILENAME = 'part.py'
TEMPLATE_FILEPATH = TEMPLATE_DIR / TEMPLATE_FILENAME
PART1_FILENAME = 'part1.py'
PART2_FILENAME = 'part2.py'
HERE = os.path.dirname(os.path.abspath(__file__))

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '.token'),
) as f:
    CONTENTS = f.read()
USER_AGENT = 'bugra-yilmaz, hi Eric!'

TOO_QUICK = re.compile('You gave an answer too recently.*to wait.')
WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


def get_input(day: int) -> str:
    url = f"https://adventofcode.com/{YEAR}/day/{day}/input"
    req = request.Request(
        url, headers={'Cookie': CONTENTS, 'User-Agent': USER_AGENT},
    )
    return request.urlopen(req).read().decode()


def make_files(day: int, string: str) -> None:
    folder = Path(f"day{day:02d}")
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / INPUT_FILENAME, 'w') as f:
        f.write(string)
    os.chmod(folder / INPUT_FILENAME, 0o400)
    copy(TEMPLATE_FILEPATH, folder / PART1_FILENAME)
    copy(TEMPLATE_FILEPATH, folder / PART2_FILENAME)


def get_todays_puzzle() -> int:
    day = datetime.date.today().day

    for i in range(5):
        try:
            s = get_input(day)
        except error.URLError as e:
            print(f"zzz: not ready yet: {e}")
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit('timed out after attempting many times')

    make_files(day, s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print('...')
    else:
        print(lines[0][:80])
        print('...')

    return 0


def _post_answer(day: int, part: int, answer: int) -> str:
    params = parse.urlencode({'level': part, 'answer': answer})
    req = request.Request(
        f"https://adventofcode.com/{YEAR}/day/{day}/answer",
        method='POST',
        data=params.encode(),
        headers={'Cookie': CONTENTS, 'User-Agent': USER_AGENT},
    )
    resp = request.urlopen(req)

    return resp.read().decode()


def submit_todays_answer() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', type=int, required=True)
    args = parser.parse_args()

    day = datetime.date.today().day
    answer = int(sys.stdin.read())

    print(f"answer: {answer}")

    contents = _post_answer(day, args.part, answer)

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f"\033[41m{error_match[0]}\033[m")
            return 1

    if RIGHT in contents:
        print(f"\033[42m{RIGHT}\033[m")
        return 0
    else:
        # unexpected output?
        print(contents)
        return 1
