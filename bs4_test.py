from models import TagContent
from modules.download import NewsDownloader
from modules.extractors import (
    AuthorsExtractor,
    BaseExtractor,
    SubtitleExtractor,
    TitleExtractor,
)
from modules.extractors.metadata.copyright import CopyrightExtractor
from modules.extractors.metadata.datetime import DatetimeExtractor
from modules.extractors.metadata.keywords import KeywordsExtractor
from modules.extractors.metadata.site_name import SiteNameExtractor
from modules.extractors.metadata.url import UrlExtractor
from modules.parser import Parser

urls: list[str] = [
    "https://www.wsj.com/articles/youtube-promotes-nfl-sunday-ticket-in-las-vegas-spheres-first-paid-ad-15c6b40a",
    "https://g1.globo.com/pop-arte/cinema/noticia/2023/09/01/taylor-swift-anuncia-lancamento-do-filme-the-eras-tour-experiencia-mais-significativa-e-eletrizante-da-vida.ghtml",
    "https://www.nytimes.com/2023/09/01/business/college-admissions-essay-ai-chatbots.html",
    "https://www.repubblica.it/cronaca/2023/09/02/news/sicurezza_sul_lavoro_norme_responsabilita-413006339/?ref=RHLF-BG-I413009319-P3-S1-T1",
    "https://www1.folha.uol.com.br/poder/2023/09/pf-cita-pagamentos-a-empresa-de-fachada-e-ministro-de-lula-tem-bens-bloqueados.shtml",
    "https://time.com/6309815/floridas-broken-home-insurance-market-is-creating-a-hurricane-tax/",
    "https://edition.cnn.com/2023/09/04/football/rubiales-complaints-intl/index.html",
    "https://www.cnnbrasil.com.br/politica/na-reta-final-cpmi-do-8-1-tem-mais-convocados-que-sessoes-para-depoimentos/",
    "https://www.poder360.com.br/poderdata/ativista-e-anti-bolsonaro-supremo-melhora-avaliacao-em-2023/",
    "https://www.bbc.com/portuguese/articles/cg3ll7zre1go",
    "https://www.bbc.com/news/world-africa-66765493",
    "https://www.foxnews.com/politics/new-mexico-republican-legislators-call-dem-gov-grishams-impeachment-gun-order-rogue",
    "https://www.reuters.com/world/africa/magnitude-7-earthquake-strikes-morocco-gfz-2023-09-08/",
]

url = "https://edition.cnn.com/2023/09/04/football/rubiales-complaints-intl/index.html"


def exec(url: str):
    html = NewsDownloader().download(url)

    def print_result(tags: list[TagContent]):
        for tag in tags:
            print(tag)

    def extract(extractor: BaseExtractor):
        tags: list[TagContent] = extractor.extract()
        print_result(tags)
        return tags[0]

    parser = Parser(html).parse()

    # extract(MetaTagExtractor(parser))
    # extract(OpenGraphExtractor(parser))
    title = extract(TitleExtractor(parser))
    subtitle = extract(SubtitleExtractor(parser, title))
    extract(AuthorsExtractor(parser, title, subtitle))
    extract(DatetimeExtractor(parser, title, subtitle))
    extract(UrlExtractor(parser))
    copyright = extract(CopyrightExtractor(parser))
    extract(SiteNameExtractor(parser, copyright))
    extract(KeywordsExtractor(parser))

    print()


for url in urls:
    exec(url)
