import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.custom.nn_tools.xgb_classifier as xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.cust.apartmentlist.leads_filter_180 as lf
def train_model(downsample, rh = None, datasets=None):
    feature_file = 'features/al_2.0.0.json'
    #features = tfl.run_feature_analysis(feature_file)
    if datasets == None:
        rh, datasets = al_xgb.create_rh_and_dataset(feature_file, random_seed=2828799, filter = lf.filter, downsample_negative=downsample)
    classifier = xgb.XgbClassifier()
    classifier.train(datasets, max_rounds=1001, max_depth=2, l2_norm=500, min_child_weight=100, train_step_size=0.2, subsample=0.7)
    features = classifier.feature_scores(rh)
    for feature in features:
         print "%25s: %4.1f" % (feature[0], feature[1])
    control_results = classifier.get_sorted_results(datasets.test)
    auc_plot.compute_auc(control_results)
    control_results = classifier.get_sorted_results(datasets.get_test_control())
    auc_plot.compute_auc(control_results)
    print("Control AUC: %5.3f" % auc_plot.compute_auc(control_results))
    return rh, datasets,classifier

def push_model():
    feature_file = 'features/al_2.0.0.json'
    al_xgb.train_and_push(feature_file, 'al_lease_2.0.0.t2', filter=lf.filter, random_seed=87371, max_rounds=1201,
                          max_depth=2, l2_norm=500, min_child_weight=110, train_step_size = 0.2, subsample=0.7)

push_model()

