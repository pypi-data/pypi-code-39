from bytegain.custom.cust.apartmentlist.feature_filter import FeatureFilter

EXCLUDED_FEATURES = [
    'opened_email',

    'email_opens_count',
    'email_clicks_count',
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
    # 'total_units',
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
    'preferences_baths',

    'avg_12mo_2bd_location_price',
    'relative_2bd_price',
    'total_ldp_views_count',
    'property_ldp_views_count',

    'property_lat',
    'property_lon',
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
    'model_version',
    'booked_tour',
    'browser_name',
    'clicked_call',
    'client_platforms',
    'conversation_reply_rate_1d',
    'days_since_active',
    'device_types',
    'downgraded_interest',
    'email_clicks_1w',
    'et_experience',
    'remarketing_visits_1w',
    'search_category',
    'sent_message',
    'traffic_source',
    'unsubscribed',
    'upgraded_interest',
    'user_sessions_count_1w',
    'lsd_control',
    'discard',
    'test_holdback',
    'interest_age_hours',
    'messages_count',
    'rental_id',
    'leased_at_property',
    'billable_lease_at_property',
    'pct_leases_imported'
]


NUMERICAL_FEATURES = [
    'preferences_lease_length',
    'preferences_move_urgency',
    'metro_price',
]

CATEGORY_FEATURES = [
    'preferences_location_id',
    'rental_id',
    'property_city_id'
]

BUCKET_FEATURES = [
    'registered_source_app',
    'search_category'
]

filter = FeatureFilter(EXCLUDED_FEATURES, NUMERICAL_FEATURES, CATEGORY_FEATURES, [])
model_version = "1.3.0"
config = {'table': 'apartmentlist.bytegain_leads_1h',
          'model_name': 'interest_created_1h',
          'model_version': model_version,
          'feature_json': 'interest_created_1h_v%s' % model_version,
          'filter': filter,
          'outcome_field': 'leased_at_property',
          'control_field': 'lsd_control',
           'positive_outcome_rate_field': 'pct_leases_imported',
          'control_weight': 3,
          'id_field': 'event_id',
          'interest_date_column': 'value_at',
          'start_date': '2017-01-01',
          'end_date': '2019-03-01',
          'random_seed': 91876,
          'max_rounds': 801,
          'max_depth': 3,
          'train_step_size': 0.25,
          'min_child_weight': 1800,
          'l2_norm': 100,
          'downsample': True}


prod_config = dict(config)
prod_config['downsample'] = False

