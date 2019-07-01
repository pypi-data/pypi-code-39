import logging
import random

from bytegain.zap.prediction_instance import PredictionInstance

DAY = 24 * 3600


class RentInstanceGenerator(object):
    def __init__(self):
        self._random = random.Random()
        self._random.seed(123456)
        self._predict_mode = False
        self._path = None
        self._bucketer = None

        self._use_days = 21
        self._blackout_days = 7
        self._signup_limit_days = 120

    def config(self, driver_input, instance_generator_config, instance_config, session_generator_data, input_sessions):
        """
        Need this function to create buckets. It is called from bytegain.zap.sessions_to_instances.make_instances
        """
        self._predict_mode = driver_input.command == 'predict'
        self._path = session_generator_data['redshift_training_data']
        assert self._path

        self._bucketer = self.get_bucketer(n_numerical_buckets=instance_config.get('n_numerical_buckets', 10))
        self._bucketer.construct_buckets()

        # Set the number of buckets generated by the bucketer. instance_config gets updated all the way
        # back up to the driver.
        instance_config['extra_features'] = self._bucketer.total_length
        instance_config['extra_features_map'] = self._bucketer.feature_map
        assert instance_config['extra_features'] > 0

    def get_bucketer(self, n_numerical_buckets):
        """
        Use schemas to construct buckets for features.

        :return:
        """
        from bytegain.custom.model_data.schema_from_TableInfo import get_schema
        from bytegain.custom.model_data.bucket_features import FeatureBucketerNonLinear as bucketer
        from bytegain.custom.cust.apartmentlist.excluded_features import EXCLUDED_FEATURES

        # Try to find pickled TableInfo file
        schemas = get_schema(self._path, {'features': '/ml_notified_training_set/'})
        # We need only schema for features
        if schemas:
            return bucketer(EXCLUDED_FEATURES, schemas['features'], n_numerical_buckets=n_numerical_buckets)
        else:
            return None
        # import pickle
        # file_features = open('bytegain/cust/apartmentlist/data/2days_median_fix/2days_median_fix/lead_scoring_lead_scoring_set_with_model/lead_scoring.lead_scoring_set_with_model..pickle')
        # schema_features = pickle.load(file_features)
        # if schema_features:
        #     return bucketer(excluded_features, schema_features)
        # else:
        #     return None

    def get_instances(self, rows):
        """
        Generate instances based on only 'extra_label': if there is no 'extra_label' - it is a negative sample.
        Make one instance per user.

        `events_to_sessions` attaches a label and features to the last event in the click stream

        :param rows:
        :return: instance
        """
        if len(rows) < 1:
            return []

        from bytegain.beam.beam_util import get_counter
        from bytegain.zap.abstract_instance_generator import timestamp_to_epoch, get_timestamp
        import random

        # Create instances only at the following events
        instance_events = {'page', 'screen', 'compass'}

        # Find the first and last page events to use
        first_page_event = None
        last_page_to_use = None
        for row_i, row in enumerate(rows):
            if row.get('type') in instance_events:
                if first_page_event is None:
                    last_page_to_use = first_page_event = row_i
                else:
                    # Save last page event before blackout
                    if timestamp_to_epoch(get_timestamp(row)) - timestamp_to_epoch(
                            get_timestamp(rows[first_page_event])) <= self._use_days * DAY:
                        last_page_to_use = row_i

        last_page_to_use_time = timestamp_to_epoch(get_timestamp(rows[last_page_to_use]))

        # Make instances only if all following criteria are met
        make_instances = True

        label_time = None
        extra_features = {}

        for row_i, row in enumerate(rows):
            if row.get('type') == 'acappella_lease':
                get_counter('instance', 'acappella_lease_found').inc()
                label_time = timestamp_to_epoch(get_timestamp(row))
                if label_time:
                    # Consider only users who sign-up no longer than 120 days since their last before blackout visit
                    sign_up_limit = self._signup_limit_days * DAY
                    if label_time - last_page_to_use_time > sign_up_limit:
                        get_counter('drop_session', 'signed_120_days_later').inc()
                        make_instances = False

                    # There should be AT LEAST 'self._blackout_days' days from the user's last event to a lease
                    blackout = self._blackout_days * DAY
                    if label_time - last_page_to_use_time < blackout:
                        get_counter('drop_session', 'events_within_blackout').inc()
                        make_instances = False

                    # Use only the earliest acappella lease
                    break

        # Use only first 'self._use_days' days of data if in a training mode
        if not self._predict_mode:
            if last_page_to_use:
                get_counter('events', 'session_truncated').inc()
                rows = rows[:last_page_to_use]

        # Make label
        label = True if label_time else False

        if self._predict_mode and label:
            make_instances = False
            get_counter('drop_user', 'user_converged').inc()

        instances = []
        # If some criteria haven't met don't construct instances
        if not make_instances:
            get_counter('instance_generator', 'no_instances').inc()
            return instances

        # Now make one instance per user

        # Make sure the number of feature buckets is the same
        default_buckets = [0] * self._bucketer.total_length

        # Find the latest features
        extra_features_buckets = default_buckets
        for row_i in xrange(len(rows) - 1, -1, -1):
            if rows[row_i].get('type') == 'features':
                get_counter('instance', 'features_found').inc()
                extra_features = rows[row_i]
                # Bucket features or use 'default_buckets'
                extra_features_buckets = self._bucketer.sample_to_vec(extra_features)
                break

        if len(extra_features) > 0 and random.randint(0, 100) == 73:
            logging.info("Features: %s, buckets: %s" % (extra_features, extra_features_buckets))

        instances.append(PredictionInstance(0, len(rows), label, predict_index=None, final_dwell=None,
                                            future_data=None, extra_features=extra_features_buckets))
        return instances
