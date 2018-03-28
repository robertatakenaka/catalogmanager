# coding=utf-8
import os

from ..xml.article_xml_tree import ArticleXMLTree


class Asset:

    def __init__(self, asset_node, _filename=None):
        self._filename = None
        self.asset_node = asset_node
        self.filename = _filename
        self.asset_name = asset_node.href

    @property
    def filename(self):
        return self._filename

    @property
    def file_content(self):
        if os.path.isfile(self.filename):
            return open(self.filename)

    @filename.setter
    def filename(self, _filename):
        if _filename is not None and os.path.isfile(_filename):
            self._filename = _filename

    def get_record_content(self):
        record_content = {}
        record_content['name'] = self.asset_name
        record_content['href'] = self.href
        return record_content

    @property
    def href(self):
        if self.asset_node is not None:
            return self.asset_node.href

    @href.setter
    def href(self, value):
        if self.asset_node is not None:
            self.asset_node.href = value


class Article:

    def __init__(self, xml=None, files=None):
        self.id = None
        self.xml_tree = xml
        self.files = {os.path.basename(f): f for f in files}
        self._assets = {name: Asset(node, self.files.get(name)) for name, node in self.xml_tree.asset_nodes.items()}

    @property
    def xml_tree(self):
        return self._xml_tree

    @xml_tree.setter
    def xml_tree(self, xml):
        self._xml_tree = ArticleXMLTree(xml)

    def get_record_content(self):
        record_content = {}
        record_content['xml'] = self.xml_tree.basename
        record_content['assets'] = [asset.get_record_content() for asset in self.assets.values()]
        return record_content

    @property
    def assets(self):
        return self._assets

    @property
    def missing_asset_files(self):
        _missing_asset_files = []
        if self.xml_tree.asset_nodes is not None:
            _missing_asset_files = [item for item in self.assets.keys() if item not in self.files.keys()]
        return _missing_asset_files

    @property
    def unexpected_asset_files(self):
        _unexpected_asset_files = []
        if self.files is not None:
            _unexpected_asset_files = [item for item in self.files.keys() if item not in self.assets.keys()]
        return _unexpected_asset_files
