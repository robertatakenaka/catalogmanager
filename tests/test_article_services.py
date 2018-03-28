import os

from catalog_persistence.databases import (
    InMemoryDBManager,
)
from catalog_persistence.models import (
    RecordType,
)

from catalogmanager.article_services import(
    ArticleServices,
)


def get_article(filename):
    path = os.path.dirname(filename)
    files = [path + '/' + item for item in os.listdir(path) if not item.endswith('.xml')]
    xml_filename = filename
    return (xml_filename, files)


def test_receive_article():

    xml_filename = '/Users/roberta.takenaka/github.com/scieloorg/catalogmanager/packages/0034-8910-rsp-S01518-87872016050006741/0034-8910-rsp-S01518-87872016050006741.xml'
    xml_filename, files = get_article(xml_filename)

    changes_db_manager = InMemoryDBManager({'database_name': 'changes'})
    articles_db_manager = InMemoryDBManager({'database_name': 'articles'})

    article_services = ArticleServices(articles_db_manager, changes_db_manager)

    expected = {}
    got = article_services.receive_article('ID', xml_filename, files)
    assert expected == got
