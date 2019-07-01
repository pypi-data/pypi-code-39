from bytegain.custom.model_data.schema_from_TableInfo import get_schema
from bytegain.custom.model_data.bucket_features import FeatureBucketerNonLinear as bucketer
from bytegain.custom.cust.apartmentlist.excluded_features import EXCLUDED_FEATURES


def bucketer_test(path='/home/yuri/devel/custom/'):
    schemas = get_schema(path, {'features': 'ml_notified_training_set/'})
    b = bucketer(EXCLUDED_FEATURES, schemas['features'], n_numerical_buckets=5)
    b.construct_buckets()
    map_sorted = sorted(b._feature_map.iteritems(), key=lambda (k,v): (v, k))
    for i in xrange(len(map_sorted)):
        print map_sorted[i][1]
    return map_sorted


sample = {"budget_min":"630","dwell_time":"149","commute_minutes":"","user_id":"236156686",
          "interest_state":"strong_interest","viewed_availability":"t","registered_source_partner":"apartment_list",
          "interest_source_app":"MobileApartmentList","property_lat":"39.974504",
          "preferred_budget_deviation":"1.04046242","preferred_available_units":"45","label":"f",
          "positive_velocity_rate":"0.53508771929824561","preferred_units":"75","search_category":"Email",
          "registered_source_app":"MobileApartmentList","budget_max":"900",
          "preferences_move_urgency":"0.80000000000000004","timestamp":"2017-01-11 06:00:14.914","move_in_delay":"-123",
          "metro_id":"747240","preferences_lease_length":"12","commute_distance":"","commute_mode":"",
          "preferences_baths":"","property_lon":"-86.080742","distance":"2.861052221994","rental_id":"p10663",
          "interest_source_partner":"apartment_list","median_preferred_price":"865.0","preferences_beds_2":"f",
          "preferences_beds_3":"f","preferences_beds_0":"f","preferences_beds_1":"t","property_zip_code":"46033",
          "email_clicked":"t","average_preferred_price":"904","has_phone_number":"t","data_updated_at":"2017-10-18 23:58:33"}
bucketer_test()

