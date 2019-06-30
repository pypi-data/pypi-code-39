from smoacks.ApiClientBase import ApiClientBase
from roadmap_items.RoadmapAuth import RoadmapAuth

class Roadmap (ApiClientBase):
    _id_fields = 'roadmap_id'
    _api_path = 'rs/roadmaps'
    _ro_fields = {'roadmap_id', 'record_created', 'record_updated'}

    def __init__(self, **kwargs):
        self.roadmap_id = kwargs['roadmap_id'] if 'roadmap_id' in kwargs else None
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.record_created = kwargs['record_created'] if 'record_created' in kwargs else None
        self.record_updated = kwargs['record_updated'] if 'record_updated' in kwargs else None
        self._authorizations = []
        if 'authorizations' in kwargs:
            for auth in kwargs['authorizations']:
                self._authorizations.append(RoadmapAuth(**auth))

    def toJSON(self, deep=False):
        result = super().toJSON(deep)
        if deep:
            result['authorizations'] = []
            for child in self._authorizations:
                result['authorizations'].append(child.toJSON(parent_id=self._id_fields[0]))
        return result

    def add_auth(self, role, group_id):
        self._authorizations.append(RoadmapAuth(role=role, group_id=group_id))


    def get_ids(self):
        return [self.roadmap_id]