import pytest
import os

from catalogmanager.models import article_model


def get_files():
    xml_filename = './packages/0034-8910-rsp-S01518-87872016050006741/0034-8910-rsp-S01518-87872016050006741.xml'
    files = [item for item in os.listdir('./packages/0034-8910-rsp-S01518-87872016050006741/') if not item.endswith('.xml')]
    return (xml_filename, files)


def create_article(xml_filename, files):
    return article_model.Article(xml_filename, files)


def test_article():
    xml_filename, files = get_files()
    article = create_article(xml_filename, files)
    assert article.basename == os.path.basename(xml_filename)
    assert article.filename == xml_filename
    assert article.article_xml_tree.xml_tree.xml_error == None
    assert type(article.content) == type('')


def test_link_files_to_assets():
    xml_filename, files = get_files()
    article = create_article(xml_filename, files)

    article.link_files_to_assets()
    assert len(article.assets) == 2
    assert sorted(article.assets.keys()) == sorted(
        ['0034-8910-rsp-S01518-87872016050006741-gf01-pt.jpg',
        '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'])
    assert article.unlinked_assets == []
    assert article.unlinked_files == []


def test_update_href():
    xml_filename, files = get_files()
    article = create_article(xml_filename, files)
    content = article.content
    article.link_files_to_assets()
    asset = article.assets.get('0034-8910-rsp-S01518-87872016050006741-gf01.jpg')
    asset.update_href('novo href')
    items = [item for name, item in article.assets.items() if name == '0034-8910-rsp-S01518-87872016050006741-gf01.jpg']
    assert len(items) == 1
    assert items[0].href == 'novo href'
    assert items[0].original_href == '0034-8910-rsp-S01518-87872016050006741-gf01.jpg'

    assert not article.content == content
