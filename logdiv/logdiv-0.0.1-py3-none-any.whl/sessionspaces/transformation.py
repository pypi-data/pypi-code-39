import time as timelib
import numpy as np
from sklearn.preprocessing import StandardScaler

def log_normalization(session_data, session_features, lognorm_dimensions):
    """
    Calculate log of selected features
    """
    session_data = session_data.copy(deep=True)
    for d in lognorm_dimensions:
        # shift to avoid log(0) + log_normalization
        session_data[d] = (session_data[d]+1).apply(lambda x: np.log(x))
    return session_data[session_features];

def normalization(session_data, session_features):
    """
    Normalize sessions features using StandardScaler from sklearn package
    """
    scaler = StandardScaler()
    session_data[session_features] = session_data[session_features].astype(np.float64)
    session_data[session_features] = scaler.fit_transform(session_data[session_features])
    return session_data[session_features];

def weight(session_data_clustering,session_data, session_features):
    """
    Weighting selected session features
    """
    cv = {}
    cv_tot = 0
    w = {}
    for d in session_features:
        cv[d] = np.sqrt(session_data_clustering[d].var()) / session_data_clustering[d].mean()
        cv_tot = cv_tot + cv[d]
    for d in session_features:
        w[d] = cv[d] / cv_tot
    for d in session_features:
        session_data[d] = np.sqrt(np.abs(w[d])) * session_data[d]
    return session_data[session_features];

def session_transformation(session_data_clustering, session_features, lognorm_dimensions, verbose = False):
    """
    Normalize and Weight selected session features. Return session_data
    """
    if verbose == True:
        start_time_tot = timelib.time()
        print("\n   * Session features transformation : log normalization of selected features, normalization and weighting ...")
        
    # log normalzation of selected features
    session_data_transformed = log_normalization(session_data_clustering, session_features, lognorm_dimensions)
    # normalization
    session_data_transformed = normalization(session_data_transformed,session_features)
    # weighting
    session_data_transformed = weight(session_data_clustering, session_data_transformed,session_features)

    if verbose == True:
        print("     Session features transformed in %.1f seconds."%(timelib.time() - start_time_tot))

    return session_data_transformed;
