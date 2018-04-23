# coding = utf-8


class ChangesServices:

    def __init__(self, changes_db_manager):
        self.changes_db_manager = changes_db_manager

    def all_changes(self, date_start, date_end=None):
        selector = {}
        selector['document_change_date'] = (date_start, date_end)
        fields = [
            'document_change_date',
            'change_id',
            'type',
            'document_id',
            'document_type',
        ]
        sort = [{'document_change_date': 'asc'}]
        return self.changes_db_manager.find(selector, fields, sort)
