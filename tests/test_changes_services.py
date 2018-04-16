from datetime import datetime

from unittest.mock import patch

import pytest

from catalog_persistence.databases import (
    InMemoryDBManager,
    DatabaseService,
    DocumentNotFound,
    ChangeType,
)
from catalog_persistence.models import RecordType
from catalogmanager.article_services import (
    ArticleServices,
    ArticleServicesException,
)
from catalogmanager.changes_services import (
    ChangesServices,
)
from catalogmanager.models.article_model import (
    Article,
)
from .conftest import (
    PKG_A,
)


def test_all_changes():

    date_start = str(datetime.utcnow().timestamp())

    xml_file_path, files = PKG_A[0], PKG_A[1:]

    changes_db_manager = InMemoryDBManager(database_name='changes')
    articles_db_manager = InMemoryDBManager(database_name='articles')

    article_services = ArticleServices(articles_db_manager, changes_db_manager)
    changes_services = ChangesServices(changes_db_manager)

    article_services.receive_xml_file('12345', xml_file_path)
    article_record = article_services.article_db_service.read('12345')
    results = changes_services.all_changes(date_start, date_end=None)

    print(results)
    assert len(results) == 1
    assert results[0].get('document_id') == article_record['document_id']
    assert results[0].get('document_type') == RecordType.ARTICLE.value
    assert results[0].get('type') == ChangeType.CREATE.value
    assert results[0].get('document_change_date') >= date_start


"""
    assert len(results) == 2
    assert results[0].get('document_id') == article_record['document_id']
    assert results[0].get('document_type') == RecordType.ARTICLE.value
    assert results[0].get('type') == ChangeType.CREATE.value
    assert results[0].get('document_change_date') >= date_start

    assert results[1].get('document_id') == article_record['document_id']
    assert results[1].get('document_type') == RecordType.ARTICLE.value
    assert results[1].get('type') == ChangeType.UPDATE.value
    assert results[1].get('document_change_date') > results[0].get('document_change_date')
"""
