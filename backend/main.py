import os
from pathlib import Path


def run_profiling():
    current_dir = Path(__file__).parent.resolve()
    run_file = current_dir / 'profile/profile.py'
    os.system(f'python {run_file}')


def main() -> None:
    print("Hello World!")


if __name__ == "__main__":
    main()