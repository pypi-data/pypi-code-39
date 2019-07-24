from typing import List, Optional

from cortex_common.types import Profile
from cortex_common.utils import unique_id, utc_timestamp
from cortex_profiles.synthesize.attributes import AttributeProvider
from cortex_profiles.synthesize.base import BaseProviderWithDependencies
from cortex_profiles.synthesize.tenant import TenantProvider


class ProfileProvider(BaseProviderWithDependencies):

    def __init__(self, *args, **kwargs):
        super(ProfileProvider, self).__init__(*args, **kwargs)

    def dependencies(self) -> List[type]:
        return [
            TenantProvider,
            AttributeProvider
        ]

    def profile(self, profileId:Optional[str]=None, max_attributes:int=3) -> Profile:
        return Profile(
            profileId=self.fake.profileId() if not profileId else profileId,
            createdAt=utc_timestamp(),
            profileSchema="cortex/synthetic-schema",
            attributes = self.fake.attributes(limit=self.fake.random.randint(1, max_attributes))
        )
