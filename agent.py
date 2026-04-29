from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def main():
    print("DivineSide Client Discovery Agent — ready.")


if __name__ == "__main__":
    main()
