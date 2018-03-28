# coding=utf-8

from catalog_persistence.models import (
        get_record,
        RecordType,
    )
from catalog_persistence.databases import (
        DatabaseService,
    )
from .data_services import DataServices
from .models.article_model import Article


Record = get_record


class ArticleServices:

    def __init__(self, articles_db_manager, changes_db_manager):
        self.article_data_services = DataServices('articles')
        self.article_db_service = DatabaseService(
            articles_db_manager, changes_db_manager)

    def receive_article(self, id, xml, files):
        article = Article(xml, files)
        article.id = id
        article_record = Record(
            document_id=article.id,
            content=article.get_record_content(),
            document_type=RecordType.ARTICLE)

        self.article_db_service.register(
            article.id, article_record)

        self.article_db_service.put_attachment(
                document_id=article.id,
                filename=article.xml_tree.basename,
                content=article.xml_tree.content
            )

        if article.assets is not None:
            for name, asset in article.assets.items():
                self.article_db_service.put_attachment(
                        document_id=article.id,
                        filename=asset.asset_name,
                        content=asset.file_content
                    )
        return self.article_db_service.read(article.id)
