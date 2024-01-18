from multi_rake import Rake

from modules.generator.BaseGenerator import BaseGenerator


class KeywordsGenerator(BaseGenerator[list[str]]):
    def __init__(self, text: str, language_code: str = "en"):
        self.text = text
        self._language_code = language_code

    def generate(self) -> list[str]:
        rake = Rake(language_code=self._language_code)
        keywords = rake.apply(self.text)
        return [str(keyword[0]) for keyword in keywords[:10]]
