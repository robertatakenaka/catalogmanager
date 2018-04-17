import os
import json

from pyramid.response import Response
from pyramid.view import view_config
from cornice.resource import resource
import catalogmanager


@resource(collection_path='/articles', path='/articles/{id}', renderer='json')
class Article:

    def __init__(self, request, context=None):
        self.request = request
        self.context = context
        self.settings = request.registry.settings
        self.db_settings = {
            'db_host': self.settings.get('database_host'),
            'db_port': self.settings.get('database_port'),
            'username': self.settings.get('database_username'),
            'password': self.settings.get('database_password')
        }

    def put(self):
        try:
            file_field = self.request.POST.get('xml_file')
            content = file_field.file.read()
            size = len(content)
            xml_properties = {
                'filename': os.path.basename(file_field.filename),
                'content': content,
                'content_size': size,
            }
            catalogmanager.put_article(
                article_id=self.request.matchdict['id'],
                xml_properties=xml_properties,
                **self.db_settings
            )
        except catalogmanager.article_services.ArticleServicesException as e:
            return json.dumps({
                "error": "500",
                "message": "Article error"
            })

    def get(self):
        try:
            article_data = catalogmanager.get_article_data(
                article_id=self.request.matchdict['id'],
                **self.db_settings
            )
            return json.dumps(article_data)
        except catalogmanager.article_services.ArticleServicesException as e:
            return json.dumps({
                "error": "404",
                "message": "Article not found"
            })

    @view_config(route_name='get_article_xml')
    def get_article_xml(self):
        try:
            xml_file = catalogmanager.get_article_file(
                article_id=self.request.matchdict['id'],
                **self.db_settings
            )
            return Response(content_type='application/xml', body=xml_file)
        except catalogmanager.article_services.ArticleServicesException as e:
            return json.dumps({
                "error": "404",
                "message": "Article not found"
            })

    @view_config(route_name='get_asset_file')
    def get_asset_file(self):
        try:
            content_type, asset_file_content = catalogmanager.get_asset_file(
                article_id=self.request.matchdict['id'],
                asset_id=self.request.matchdict['asset_id'],
                **self.db_settings
            )
            return Response(
                content_type=content_type,
                body=asset_file_content
            )
        except catalogmanager.article_services.ArticleServicesException as e:
            return json.dumps({
                "error": "404",
                "message": "Asset not found"
            })
