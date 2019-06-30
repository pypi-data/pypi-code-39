from smoacks.ApiClientBase import ApiClientBase

class RoadmapItem (ApiClientBase):
    _id_fields = 'roadmap_item_id'
    _api_path = 'rs/roadmap_items'
    _ro_fields = {'roadmap_item_id', 'record_created', 'record_updated'}

    def __init__(self, **kwargs):
        self.roadmap_item_id = kwargs['roadmap_item_id'] if 'roadmap_item_id' in kwargs else None
        self.roadmap_id = kwargs['roadmap_id'] if 'roadmap_id' in kwargs else None
        self.commit_status = kwargs['commit_status'] if 'commit_status' in kwargs else None
        self.execution_status = kwargs['execution_status'] if 'execution_status' in kwargs else None
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.short_name = kwargs['short_name'] if 'short_name' in kwargs else None
        self.code_name = kwargs['code_name'] if 'code_name' in kwargs else None
        self.description = kwargs['description'] if 'description' in kwargs else None
        self.commit_date = kwargs['commit_date'] if 'commit_date' in kwargs else None
        self.target_date = kwargs['target_date'] if 'target_date' in kwargs else None
        self.release_date = kwargs['release_date'] if 'release_date' in kwargs else None
        self.record_created = kwargs['record_created'] if 'record_created' in kwargs else None
        self.record_updated = kwargs['record_updated'] if 'record_updated' in kwargs else None

    def get_ids(self):
        return [self.roadmap_item_id]