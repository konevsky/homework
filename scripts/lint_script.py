import subprocess


def main():
    subprocess.run(["black", "--check", "."])
    subprocess.run(["isort", "--check-only", "."])
    subprocess.run(["flake8"])
    subprocess.run(["mypy", "."])


if __name__ == "__main__":
    main()
