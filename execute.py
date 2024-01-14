from handler.extractor_handler import ExtractorHandler
from handler.template_handler import TemplateHandler


class Execute:
    def __init__(self):
        pass

    def run(self, url: str, template_string: str | None):
        template = TemplateHandler(url, template_string).handle()
        extractorHandler = ExtractorHandler(url, template)

        result = extractorHandler.handle()

        print("Execute: ", result)

        return result
