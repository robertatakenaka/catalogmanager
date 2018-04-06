import os

from catalog_persistence.databases import (
    InMemoryDBManager,
)

from catalogmanager.article_services import(
    ArticleServices,
)

from catalogmanager.models.article_model import(
    Article,
)

from .test_article_files import(
    FIXTURE_DIR,
    get_files,
)


def test_receive_xml_file():

    xml_file_path = os.path.join(
        FIXTURE_DIR,
        '741b/0034-8910-rsp-S01518-87872016050006741.xml'
    )
    files = get_files(xml_file_path)
    article = Article('ID')
    article.xml_file = xml_file_path
    assets = article.update_asset_files(files)

    changes_db_manager = InMemoryDBManager(database_name='changes')
    articles_db_manager = InMemoryDBManager(database_name='articles')

    article_services = ArticleServices(articles_db_manager, changes_db_manager)

    article_content = {
        'xml': '0034-8910-rsp-S01518-87872016050006741.xml',
        'assets': [
            '0034-8910-rsp-S01518-87872016050006741-gf01.jpg',
            '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
        ]
    }

    expected = {
        'attachments': [
            '0034-8910-rsp-S01518-87872016050006741.xml',
            '0034-8910-rsp-S01518-87872016050006741-gf01.jpg',
            '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
        ],
        'content': article_content,
        'document_type': 'ART',
        'document_id': 'ID',
    }

    article = article_services.receive_xml_file('ID', xml_file_path)


def test_receive_package():

    xml_file_path = os.path.join(
        FIXTURE_DIR,
        '741a/0034-8910-rsp-S01518-87872016050006741.xml'
    )
    files = get_files(xml_file_path)
    article = Article('ID')
    article.xml_file = xml_file_path
    assets = article.update_asset_files(files)

    changes_db_manager = InMemoryDBManager(database_name='changes')
    articles_db_manager = InMemoryDBManager(database_name='articles')

    article_services = ArticleServices(articles_db_manager, changes_db_manager)

    unexpected, missing = article_services.receive_package(
        'ID', xml_file_path, files)
    assert unexpected == []
    assert missing == []
