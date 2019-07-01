from bytegain.custom.cust.apartmentlist.feature_filter import FeatureFilter
EXCLUDED_FEATURES = [
    # 'search_category',
    # 'viewed_availability',
    #'clicked_email',
    'opened_email',
    # 'preferences_lease_length',
    # 'preferences_move_urgency',

    'email_opens_count',
    'email_clicks_count',
    # 'median_matching_price',
    'matching_units',
    'all_price',
    'availability_views',
    'commute_congestion',
    'preferences_amenities',
    'preferences_beds',
    'score',
    'interest_id',
    'leased_at_notified_property',
    'matched_user',
    'commute_lat',
    'commute_lon',
    'source_app',
    # median_matching_price replaced by median_preferred_price
    'median_matching_price',
    'photo_gallery_views',
    # Prev interests excluded because it's hard to compute at runtime
    'prev_interests',
    'consent_call_consent',
    'consent_email_consent',
    'preferences_contracts',
    'renter_phone_area_code',
    'renter_phone_exchange',
    'interest_created_at',
    'total_units',
    'matched_interest',
    'user_id',

    'preferences_wants_dishwasher',
    'preferences_most_important_feature',
    'preferences_wants_on_site_laundry',
    'preferences_wants_gym',
    'preferences_wants_in_unit_laundry',
    'preferences_wants_dog_friendly',
    'preferences_wants_pool',
    'preferences_wants_air_conditioning',
    'preferences_wants_parking',
    'preferences_cotenant',
    'preferences_cosigner',
    #'avg_12mo_2bd_location_price',
    'relative_2bd_price',

    # 'preferences_baths',
    # 'preferences_beds_0',
    # 'preferences_beds_1',
    #'preferences_beds_2',
    # 'preferences_beds_3',
    # 'has_phone_number',
    # 'email_clicked',
    # 'commute_mode',
    # 'registered_source_app',
    'property_lat_round',
    'property_lon_round',
    # 'relative_positive_velocity_rate',
    'property_to_total_velocity_rate',
    'positive_interest_velocity',
    'total_interest_velocity',
    'model',
    'version',
    'score',
    'prediction',
    'month',
]

NUMERICAL_FEATURES = [
    'preferences_lease_length',
    'preferences_move_urgency',
    'metro_price',

]

CATEGORY_FEATURES = [
    'preferences_location_id',
    'rental_id',
]

BUCKET_FEATURES = [
    'registered_source_app',
    'search_category'
]

filter = FeatureFilter(EXCLUDED_FEATURES, NUMERICAL_FEATURES, CATEGORY_FEATURES, [])
filter2 = FeatureFilter(EXCLUDED_FEATURES + ['event_count', 'ios_event_count'], NUMERICAL_FEATURES, CATEGORY_FEATURES, [])
