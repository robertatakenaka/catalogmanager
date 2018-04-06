import os

from catalogmanager.models.article_model import (
    Article,
)
from catalogmanager.xml.xml_tree import (
    XMLTree,
)

from .test_article_files import(
    FIXTURE_DIR,
    get_files,
)


def test_article():
    xml_file_path = os.path.join(
        FIXTURE_DIR,
        '741a/0034-8910-rsp-S01518-87872016050006741.xml'
    )
    files = get_files(xml_file_path)
    article = Article('ID')
    article.xml_file = xml_file_path
    assets = article.update_asset_files(files)
    assets = [
        '0034-8910-rsp-S01518-87872016050006741-gf01.jpg',
        '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg'
    ]
    expected = {
        'assets': assets,
        'xml': '0034-8910-rsp-S01518-87872016050006741.xml',
    }
    assert article.xml_file.name == os.path.basename(xml_file_path)
    assert article.xml_tree.xml_error is None
    assert article.get_record_content() == expected
    assert article.xml_file.content == open(xml_file_path, 'rb').read()
    xml_from_file = XMLTree()
    xml_from_file.content = article.xml_file.content
    xml_from_tree = XMLTree()
    xml_from_tree.content = article.xml_tree.content
    assert xml_from_file.content == xml_from_tree.content


def test_missing_files_list():
    xml_file_path = os.path.join(
        FIXTURE_DIR,
        '741b/0034-8910-rsp-S01518-87872016050006741.xml'
    )
    files = get_files(xml_file_path)
    article = Article('ID')
    article.xml_file = xml_file_path

    assets = article.update_asset_files(files)

    assert len(article.assets) == 3
    assert sorted(article.assets.keys()) == sorted(
        [
            '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
            '0034-8910-rsp-S01518-87872016050006741-gf01.jpg',
            '0034-8910-rsp-S01518-87872016050006741-gf31.jpg',
        ]
    )
    assert article.unexpected_files_list == []
    assert article.missing_files_list == [
        '0034-8910-rsp-S01518-87872016050006741-gf31.jpg',
    ]


def test_unexpected_files_list():
    xml_file_path = os.path.join(
        FIXTURE_DIR,
        '741c/0034-8910-rsp-S01518-87872016050006741.xml'
    )
    files = get_files(xml_file_path)
    article = Article('ID')
    article.xml_file = xml_file_path
    assets = article.update_asset_files(files)

    assert len(article.assets) == 2
    assert sorted(article.assets.keys()) == sorted(
        [
            '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
            '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'
        ]
    )
    assert article.unexpected_files_list == [
        os.path.join(
            FIXTURE_DIR,
            '741c/fig.jpg'
        )
    ]
    assert article.missing_files_list == []


def test_update_href():
    xml_file_path = os.path.join(
        FIXTURE_DIR,
        '741a/0034-8910-rsp-S01518-87872016050006741.xml'
    )
    files = get_files(xml_file_path)
    article = Article('ID')
    article.xml_file = xml_file_path
    assets = article.update_asset_files(files)
    content = article.xml_tree.content
    asset = article.assets.get(
        '0034-8910-rsp-S01518-87872016050006741-gf01.jpg')
    asset.href = 'novo href'
    items = [
        item
        for name, item in article.assets.items()
        if name == '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'
    ]

    assert len(items) == 1
    assert items[0].href == 'novo href'
    assert items[0].name == '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'

    assert not article.xml_tree.content == content
