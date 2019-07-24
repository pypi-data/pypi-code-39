from typing import List, Optional, Any

from cortex_common.types import Dimension, NumericAttributeValue, PercentileAttributeValue, \
    PercentageAttributeValue, TotalAttributeValue, \
    DimensionalAttributeValue, StringAttributeValue, DecimalAttributeValue, IntegerAttributeValue, \
    BooleanAttributeValue, ListAttributeValue, WeightedAttributeValue, EntityAttributeValue
from cortex_common.utils import unique_id, str_or_context
from cortex_profiles.synthesize.base import BaseProviderWithDependencies
from cortex_profiles.synthesize.defaults import PROFILE_TYPES
from cortex_profiles.synthesize.tenant import TenantProvider

__all__ = [
    "AttributeValueProvider",
]


class AttributeValueProvider(BaseProviderWithDependencies):

    # def __init__(self, *args, **kwargs):
    #     super(AttributeValueProvider, self).__init__(*args, **kwargs)
    #     self.fake = args[0]

    def dependencies(self) -> List[type]:
        return [
            TenantProvider
        ]

    def dimensional_value(self, max_dimensions=7) -> DimensionalAttributeValue:
        dimensions = [
            Dimension(
                dimensionId=unique_id(),
                dimensionValue=self.total_value()
            )
            for x in self.fake.range(0, max_dimensions)
        ]
        return DimensionalAttributeValue(
            value=dimensions,
            contextOfDimension = str_or_context(StringAttributeValue),
            contextOfDimensionValue = str_or_context(TotalAttributeValue)
        )

    def string_value(self) -> StringAttributeValue:
        return StringAttributeValue(value=self.fake.color_name())

    def integer_value(self) -> IntegerAttributeValue:
        return IntegerAttributeValue(value=self.fake.random.randint(0, 100))

    def decimal_value(self) -> DecimalAttributeValue:
        return DecimalAttributeValue(value=self.fake.random.randint(0, 100) / 0.1)

    def boolean_value(self) -> BooleanAttributeValue:
        return BooleanAttributeValue(value=self.fake.random.choice([True, False]))

    def list_value(self) -> ListAttributeValue:
        return ListAttributeValue(
            value=self.fake.random_subset_of_list(
                list(set(list(
                    map(lambda x: x(), [self.fake.color_name]*10)
                )))
            )
        )

    def percentile_value(self) -> PercentileAttributeValue:
        return PercentileAttributeValue(value=min(self.fake.random.randint(0, 100) * 0.98, 100))

    def percentage_value(self) -> PercentageAttributeValue:
        return PercentageAttributeValue(value=min(self.fake.random.randint(0, 100) * 0.98, 100))

    def total_value(self) -> TotalAttributeValue:
        return TotalAttributeValue(value=self.numeric_value().value)

    def numeric_value(self) -> NumericAttributeValue:
        return NumericAttributeValue(value=self.fake.random.choice([int, float])(self.fake.random.randint(0,100) * 0.123))

    def weighted_value(self, value:Optional[Any]=None) -> WeightedAttributeValue:
        return WeightedAttributeValue(
            value=value if value is not None else self.fake.company(),
            weight=self.fake.random.randint(0, 100) / 100.00
        )

    def entity_value(self, value:Optional[Any]=None) -> EntityAttributeValue:
        return EntityAttributeValue(
            value=value if value is not None else {
                "company": self.fake.company(),
                "employees": self.fake.random.randint(1,1000*1000)
            }
        )

    def profile_type_value(self) -> ListAttributeValue:
        return ListAttributeValue(
            value=self.fake.random_subset_of_list([PROFILE_TYPES])
        )

    def attribute_value(self):
        return self.fake.random.choice([
            self.dimensional_value,
            self.numeric_value,
            self.percentage_value,
            self.percentile_value,
            self.total_value,
            self.profile_type_value
            # self.counter_value,
            # self.relationship_value,
            # self.average_value,
            # self.object_value,
        ])()

    # def object_value(self) -> ObjectAttributeValue:
    #     return ObjectAttributeValue(value=dict(zip(["favorite_color"], [self.fake.color_name()])))
    #
    # def primitive_value(self) -> PrimitiveAttributeValue:
    #     return PrimitiveAttributeValue(
    #         value=self.fake.random.choice([
    #             self.string_value,
    #             self.boolean_value,
    #             self.integer_value,
    #             self.decimal_value,
    #         ])().value
    #     )
    #
    # def average_value(self) -> AverageAttributeValue:
    #     return AverageAttributeValue(value=self.fake.random.randint(0, 1000) * 0.98)
    #
    # def concept_value(self) -> ConceptAttributeValue:
    #     return ConceptAttributeValue(
    #         value=unique_id()
    #     )

    # def counter_value(self) -> CounterAttributeValue:
    #     return CounterAttributeValue(value=self.fake.random.randint(0, 2500))

    # def relationship_value(self) -> RelationshipAttributeValue:
    #     return RelationshipAttributeValue(
    #         value=unique_id(),
    #         relatedConceptType=self.fake.random.choice(list(CONTEXTS.keys())),
    #         relationshipType="cortex/likes",
    #         relationshipTitle="Likes",
    #         relatedConceptTitle=self.fake.company(),
    #         relationshipProperties={}
    #     )
