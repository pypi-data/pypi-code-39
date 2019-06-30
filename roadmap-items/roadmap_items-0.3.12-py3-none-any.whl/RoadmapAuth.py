from smoacks.ApiClientBase import ApiClientBase

class RoadmapAuth (ApiClientBase):
    _id_fields = {'roadmap_id', 'group_id'}
    _api_path = 'rs/roadmap_auths'
    _ro_fields = {'record_created', 'record_updated'}

    def __init__(self, **kwargs):
        self.roadmap_id = kwargs['roadmap_id'] if 'roadmap_id' in kwargs else None
        self.group_id = kwargs['group_id'] if 'group_id' in kwargs else None
        self.role = kwargs['role'] if 'role' in kwargs else None
        self.record_created = kwargs['record_created'] if 'record_created' in kwargs else None
        self.record_updated = kwargs['record_updated'] if 'record_updated' in kwargs else None

    def get_ids(self):
        return [self.roadmap_id, self.group_id]