from io import BytesIO
import json
from collections import OrderedDict
from unittest.mock import patch

import webtest
from lxml import etree
import catalogmanager


def _get_file_property(filename, content, size):
    return {
        'filename': filename,
        'content': content,
        'content_size': size
    }


def test_http_get_home(testapp):
    result = testapp.get('/', status=200)
    assert result.status == '200 OK'
    assert result.body == b''


@patch.object(catalogmanager, 'get_article_data')
def test_http_get_article_calls_get_article_data(mocked_get_article_data,
                                                 db_settings,
                                                 testapp):
    article_id = 'ID123456'
    mocked_get_article_data.return_value = {"test": "123"}
    testapp.get('/articles/{}'.format(article_id))
    mocked_get_article_data.assert_called_once_with(
        article_id=article_id,
        **db_settings
    )


@patch.object(catalogmanager, 'get_article_data')
def test_http_get_article_not_found(mocked_get_article_data, testapp):
    article_id = 'ID123456'
    error_msg = 'Article {} not found'.format(article_id)
    mocked_get_article_data.side_effect = \
        catalogmanager.article_services.ArticleServicesException(
            message=error_msg
        )
    expected = {
        "error": "404",
        "message": error_msg
    }
    result = testapp.get('/articles/{}'.format(article_id))
    assert result.status == '200 OK'
    assert result.json == json.dumps(expected)


@patch.object(catalogmanager, 'get_article_data')
def test_http_get_article_succeeded(mocked_get_article_data, testapp):
    article_id = 'ID123456'
    expected = {
        "document_id": article_id,
        "document_type": "ART",
        "content": {
            'xml': "test.xml",
            'assets': ["img1.png", "img2.png", "img3.png"]
        },
    }
    mocked_get_article_data.return_value = expected
    result = testapp.get('/articles/{}'.format(article_id))
    assert result.status == '200 OK'
    assert result.json == json.dumps(expected)


@patch.object(catalogmanager, 'get_article_file')
def test_http_get_xml_file_calls_get_article_file(mocked_get_article_file,
                                                  db_settings,
                                                  testapp,
                                                  test_article_files):
    article_id = 'ID123456'
    with open(test_article_files[0], 'rb') as fb:
        xml_content = fb.read()
        mocked_get_article_file.return_value = xml_content
        testapp.get('/articles/{}/xml'.format(article_id))
        mocked_get_article_file.assert_called_once_with(
            article_id=article_id,
            **db_settings
        )


@patch.object(catalogmanager, 'get_article_file')
def test_http_get_xml_file_article_not_found(mocked_get_article_file, testapp):
    article_id = 'ID123456'
    error_msg = 'Article {} not found'.format(article_id)
    mocked_get_article_file.side_effect = \
        catalogmanager.article_services.ArticleServicesException(
            message=error_msg
        )
    expected = {
        "error": "404",
        "message": error_msg
    }
    result = testapp.get('/articles/{}/xml'.format(article_id))
    assert result.status == '200 OK'
    assert result.json == expected


@patch.object(catalogmanager, 'get_article_file')
def test_http_get_xml_file_not_found(mocked_get_article_file, testapp):
    article_id = 'ID123456'
    error_msg = 'Missing XML file {}'.format(article_id)
    mocked_get_article_file.side_effect = \
        catalogmanager.article_services.ArticleServicesException(
            message=error_msg
        )
    expected = {
        "error": "404",
        "message": error_msg
    }
    result = testapp.get('/articles/{}/xml'.format(article_id))
    assert result.status == '200 OK'
    assert result.json == expected


@patch.object(catalogmanager, 'get_article_file')
@patch.object(catalogmanager, 'get_article_data')
def test_http_get_xml_file_calls_get_article_data(mocked_get_article_data,
                                                  mocked_get_article_file,
                                                  db_settings,
                                                  testapp,
                                                  test_article_files):
    article_id = 'ID123456'
    with open(test_article_files[0], 'rb') as fb:
        xml_content = fb.read()
        mocked_get_article_file.return_value = xml_content
        testapp.get('/articles/{}/xml'.format(article_id))
        mocked_get_article_data.assert_called_once_with(
            article_id=article_id,
            **db_settings
        )


@patch.object(catalogmanager, 'get_article_file')
@patch.object(catalogmanager, 'get_article_data')
@patch.object(catalogmanager, 'set_assets_public_url')
def test_http_get_xml_file_calls_set_assets_public_url_if_there_is_assets(
    mocked_set_assets_public_url,
    mocked_get_article_data,
    mocked_get_article_file,
    testapp,
    test_article_files
):
    article_id = 'ID123456'
    assets = [
        asset_file.name
        for asset_file in test_article_files[1:]
    ]
    mocked_get_article_data.return_value = {
        "document_id": article_id,
        "document_type": "ART",
        "content": {
            'xml': test_article_files[0],
            'assets': assets
        },
    }
    with open(test_article_files[0], 'rb') as fb:
        xml_content = fb.read()
        mocked_get_article_file.return_value = xml_content
        mocked_set_assets_public_url.return_value = xml_content
        testapp.get('/articles/{}/xml'.format(article_id))
        mocked_set_assets_public_url.assert_called_once_with(
            article_id=article_id,
            xml_content=xml_content,
            assets_filenames=assets,
            public_url='/articles/{}/{}'
        )


@patch.object(catalogmanager, 'get_article_file')
@patch.object(catalogmanager, 'get_article_data')
@patch.object(catalogmanager, 'set_assets_public_url')
def test_http_get_xml_file_doesnt_calls_set_assets_public_url_if_no_assets(
    mocked_set_assets_public_url,
    mocked_get_article_data,
    mocked_get_article_file,
    testapp,
    test_article_files
):
    article_id = 'ID123456'
    mocked_get_article_data.return_value = {
        "document_id": article_id,
        "document_type": "ART",
        "content": {
            'xml': "test.xml",
        },
    }
    assert not mocked_set_assets_public_url.called


@patch.object(catalogmanager, 'get_article_file')
@patch.object(catalogmanager, 'get_article_data')
def test_http_get_xml_file_succeeded(mocked_get_article_data,
                                     mocked_get_article_file,
                                     testapp,
                                     test_article_files,
                                     test_xml_file):
    article_id = 'ID123456'
    assets = [
        asset_file.name
        for asset_file in test_article_files[1:]
    ]
    expected_hrefs = [
        '/articles/{}/{}'.format(article_id, asset_file.name)
        for asset_file in test_article_files[1:]
    ]
    mocked_get_article_data.return_value = {
        "document_id": article_id,
        "document_type": "ART",
        "content": {
            'xml': test_article_files[0],
            'assets': assets
        },
    }
    mocked_get_article_file.return_value = test_xml_file.encode('utf-8')

    result = testapp.get('/articles/{}/xml'.format(article_id))
    assert result.status == '200 OK'
    assert result.content_type == 'application/xml'
    assert result.body is not None
    xml_tree = etree.parse(BytesIO(result.body))
    xpath = '{http://www.w3.org/1999/xlink}href'
    xml_nodes = [
        node.get(xpath)
        for node in xml_tree.findall('.//*[@{}]'.format(xpath))
    ]
    for expected_href in expected_hrefs:
        assert expected_href in xml_nodes


@patch.object(catalogmanager, 'put_article')
def test_http_article_calls_put_article(mocked_put_article,
                                        db_settings,
                                        testapp,
                                        test_xml_file):
    article_id = 'ID-post-article-123'
    params = OrderedDict([
        ('article_id', article_id),
        ("xml_file",
         webtest.forms.Upload("test_xml_file.xml",
                              test_xml_file.encode('utf-8')))
    ])
    testapp.put('/articles/{}'.format(article_id),
                params=params,
                content_type='multipart/form-data')
    mocked_put_article.assert_called_once_with(
        article_id=article_id,
        xml_properties=_get_file_property("test_xml_file.xml",
                                          test_xml_file.encode('utf-8'),
                                          len(test_xml_file)),
        assets_files=[],
        **db_settings
    )


@patch.object(catalogmanager, 'put_article')
def test_http_article_calls_put_article_service_error(mocked_put_article,
                                                      testapp,
                                                      test_xml_file):
    article_id = 'ID-post-article-123'
    mocked_put_article.side_effect = \
        catalogmanager.article_services.ArticleServicesException(
            message='Missing XML file {}'.format(article_id)
        )
    expected = {
        "error": "500",
        "message": "Article error"
    }
    params = OrderedDict([
        ('article_id', article_id),
        ("xml_file",
         webtest.forms.Upload("test_xml_file.xml",
                              test_xml_file.encode('utf-8')))
    ])
    result = testapp.put('/articles/{}'.format(article_id),
                         params=params,
                         content_type='multipart/form-data')
    assert result.status == '200 OK'
    assert result.json == json.dumps(expected)


@patch.object(catalogmanager, 'put_article')
def test_http_article_put_article_succeeded(mocked_put_article,
                                            testapp,
                                            test_xml_file):
    article_id = 'ID-post-article-123'
    params = OrderedDict([
        ('article_id', article_id),
        ("xml_file",
         webtest.forms.Upload("test_xml_file.xml",
                              test_xml_file.encode('utf-8')))
    ])
    result = testapp.put('/articles/{}'.format(article_id),
                         params=params,
                         content_type='multipart/form-data')
    assert result.status == '200 OK'


@patch.object(catalogmanager, 'put_article')
def test_http_article_put_article_with_assets(mocked_put_article,
                                              db_settings,
                                              testapp,
                                              test_xml_file,
                                              test_article_files):
    article_id = 'ID-post-article-123'
    expected_assets_properties = []
    assets_field = []
    for article_file in test_article_files[1:]:
        with open(article_file, 'rb') as fb:
            file_content = fb.read()
            expected_assets_properties.append(
                _get_file_property(article_file.name,
                                   file_content,
                                   article_file.lstat().st_size),
            )
        assets_field.append(
            ('asset_field', article_file.name, file_content)
        )
    params = OrderedDict([
        ('article_id', article_id),
        ("xml_file",
         webtest.forms.Upload("test_xml_file.xml",
                              test_xml_file.encode('utf-8')))
    ])
    result = testapp.put('/articles/{}'.format(article_id),
                         params=params,
                         upload_files=assets_field,
                         content_type='multipart/form-data')
    assert result.status == '200 OK'
    mocked_put_article.assert_called_once_with(
        article_id=article_id,
        xml_properties=_get_file_property("test_xml_file.xml",
                                          test_xml_file.encode('utf-8'),
                                          len(test_xml_file)),
        assets_files=expected_assets_properties,
        **db_settings
    )


@patch.object(catalogmanager, 'get_asset_file')
def test_http_get_asset_file_calls_get_asset_file(mocked_get_asset_file,
                                                  db_settings,
                                                  testapp):

    article_id = 'ID123456'
    asset_id = 'ID123456'
    mocked_get_asset_file.return_value = '', b'123456Test'
    testapp.get('/articles/{}/{}'.format(article_id, asset_id))
    mocked_get_asset_file.assert_called_once_with(
        article_id=article_id,
        asset_id=asset_id,
        **db_settings
    )


@patch.object(catalogmanager, 'get_asset_file')
def test_http_get_asset_file_not_found(mocked_get_asset_file,
                                       testapp):
    article_id = 'ID123456'
    asset_id = 'a.jpg'
    error_msg = 'Asset {} (Article {}) not found'.format(asset_id, article_id)
    mocked_get_asset_file.side_effect = \
        catalogmanager.article_services.ArticleServicesException(
            message=error_msg
        )
    expected = {
        "error": "404",
        "message": error_msg
    }
    result = testapp.get('/articles/{}/{}'.format(article_id, asset_id))
    assert result.status == '200 OK'
    assert result.json == expected


@patch.object(catalogmanager, 'get_asset_file')
def test_http_get_asset_file_succeeded(mocked_get_asset_file,
                                       testapp,
                                       test_xml_file):
    article_id = 'ID123456'
    asset_id = 'a.jpg'
    expected = 'text/xml', test_xml_file.encode('utf-8')
    mocked_get_asset_file.return_value = expected
    result = testapp.get('/articles/{}/{}'.format(article_id, asset_id))
    assert result.status == '200 OK'
    assert result.body == expected[1]
    assert result.content_type == expected[0]
