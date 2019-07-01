import bytegain.custom.cust.apartmentlist.leads_from_redshift as tfl
import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.custom.nn_tools.model_utils as model_utils
import bytegain.custom.nn_tools.xgb_classifier as xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.cust.apartmentlist.leads_filter_210 as lf
feature_file = 'bytegain/custom/cust/apartmentlist/features/al_2.1.0.json'
# features = tfl.run_feature_analysis(feature_file)

#rh, datasets = al_xgb.create_rh_and_dataset(feature_file, random_seed=2828712, filter = lf.filter, downsample_negative=True)
#classifier = xgb.XgbClassifier()
#classifier.train(datasets, max_rounds=301, max_depth=3, l2_norm=400, min_child_weight=200, train_step_size=0.2)
#features = classifier.feature_scores(rh)
#for feature in features:
#    print "%25s: %4.1f" % (feature[0], feature[1])
al_xgb.train_and_push(feature_file, 'al_lease_2.1.0', filter=lf.filter, random_seed=87371, max_rounds=601,
        max_depth=3, l2_norm=500, min_child_weight=1000, train_step_size = 0.2)

"""
train base rate: 0.898%
[0] eval-auc:0.615998   train-auc:0.620709
[100]   eval-auc:0.696227   train-auc:0.70627
[200]   eval-auc:0.701711   train-auc:0.714104
[300]   eval-auc:0.704001   train-auc:0.718934
[400]   eval-auc:0.705539   train-auc:0.722395
[500]   eval-auc:0.70628    train-auc:0.725357
[600]   eval-auc:0.707058   train-auc:0.727831
interest_state: 18.2
viewed_availability:  7.8
preferences_move_urgency:  6.6
move_in_delay:  5.1
preferences_beds_3:  4.0
commute_distance:  3.7
email_clicked:  3.6
distance:  3.6
total_units:  3.3
dwell_time:  3.1
distinct_ldp_views_count:  2.9
commute_mode:  2.8
interest_source_app:  2.8
et_experience:  2.7
preferences_beds_2:  2.4
budget_min:  2.2
has_phone_number:  2.0
registered_source_app:  2.0
preferences_lease_length:  1.9
preferred_available_units:  1.9
rental_id:  1.9
average_preferred_price:  1.8
metro_id:  1.8
budget_max:  1.6
positive_velocity_rate:  1.5
preferred_budget_deviation:  1.3
property_zip_code:  1.2
preferred_units:  1.2
median_preferred_price:  1.1
preferences_beds_0:  1.0
commute_minutes:  1.0
search_category:  1.0
preferences_beds_1:  0.8
Control AUC: 0.717
Positive rate in top 10 percent: 0.0260248447205
"""
