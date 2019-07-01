config = {'table': 'apartmentlist.notified',
          'model_name': 'notified',
          'model_version': '1.2.1',
          'feature_json': 'notified_v1.2.1',
          'filter': 'notified_filter_121',
          'outcome_field': 'leased_at_property',
          'control_field': 'lsd_control',
          'control_weight': 3,
          'id_field': 'event_id',
          'interest_date_column': 'value_at',
          'start_date': '2017-01-01',
          'end_date': '2018-11-22',
          'random_seed': 91876,
          'max_rounds': 1001,
          'max_depth': 3,
          'train_step_size': 0.25,
          'min_child_weight': 1100,
          'l2_norm': 150,
          'downsample': True}



prod_config = dict(config)
prod_config['downsample'] = False
