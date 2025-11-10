import subprocess


def main() -> None:
    subprocess.run(["isort", "."])
    subprocess.run(["black", "."])


if __name__ == "__main__":
    main()
