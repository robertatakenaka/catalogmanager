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














""""
        change_record = {
            'change_id': uuid4().hex,
            'document_id': document_record['document_id'],
            'document_type': document_record['document_type'],
            'type': change_type.value,
            'created_date': str(datetime.utcnow().timestamp()),
        }
        if attachment_id:
            change_record.update({'attachment_id': attachment_id})
        self.changes_db_manager.create(
            change_record['change_id'],
            change_record
        )
        return change_record['change_id']

"""