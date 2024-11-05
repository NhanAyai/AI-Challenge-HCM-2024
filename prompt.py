from nltk.tokenize import sent_tokenize

# nltk.download('punkt_tab')


class Prompt():
    def __init__(self,
                 text: str = " ") -> None:
        self.text: str = text

    def tokenize(self) -> list[str]:
        return sent_tokenize(self.text)
