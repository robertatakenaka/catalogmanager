import os

from catalogmanager.models.article_model import (
    Article,
)


def get_article(filename):
    path = os.path.dirname(filename)
    files = [item for item in os.listdir(path) if not item.endswith('.xml')]
    xml_filename = filename
    return Article(xml_filename, files)


def test_article():
    xml_filename = './packages/0034-8910-rsp-S01518-87872016050006741/0034-8910-rsp-S01518-87872016050006741.xml'
    article = get_article(xml_filename)
    article.id = 'ID'

    assets = []
    assets.append({'name': '0034-8910-rsp-S01518-87872016050006741-gf01.jpg', 'attachment_id': 'boy.jpg'})
    assets.append({'name': '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg', 'attachment_id': '0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg'})
    expected = {
        'assets': assets,
        'xml': '0034-8910-rsp-S01518-87872016050006741.xml',
        }
    assert article.xml_tree.basename == os.path.basename(xml_filename)
    assert article.xml_tree.filename == xml_filename
    assert article.xml_tree.xml_error == None
    assert type(article.xml_tree.content) == type('')
    assert article.get_record_content() == expected


def test_unexpected_asset_files():
    xml_filename = './packages/741b/0034-8910-rsp-S01518-87872016050006741.xml'
    article = get_article(xml_filename)

    assert len(article.assets) == 3
    assert sorted(article.assets.keys()) == sorted(
        ['0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
        '0034-8910-rsp-S01518-87872016050006741-gf01.jpg',
        '0034-8910-rsp-S01518-87872016050006741-gf31.jpg',
        ])
    assert article.unexpected_asset_files == []
    assert article.missing_asset_files == ['0034-8910-rsp-S01518-87872016050006741-gf31.jpg']


def test_missing_asset_files():
    xml_filename = './packages/741c/0034-8910-rsp-S01518-87872016050006741.xml'
    article = get_article(xml_filename)

    assert len(article.assets) == 2
    assert sorted(article.assets.keys()) == sorted(
        ['0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
        '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'])
    assert article.unexpected_asset_files == ['fig.jpg']
    assert article.missing_asset_files == []


def test_update_href():
    xml_filename = './packages/0034-8910-rsp-S01518-87872016050006741/0034-8910-rsp-S01518-87872016050006741.xml'
    article = get_article(xml_filename)
    content = article.xml_tree.content
    asset = article.assets.get('0034-8910-rsp-S01518-87872016050006741-gf01.jpg')
    asset.href = 'novo href'
    items = [item for name, item in article.assets.items() if name == '0034-8910-rsp-S01518-87872016050006741-gf01.jpg']
    assert len(items) == 1
    assert items[0].href == 'novo href'
    assert items[0].asset_name == '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'

    assert not article.xml_tree.content == content
