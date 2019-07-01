import bytegain.custom.cust.apartmentlist.al_xgb

config = {'table': 'apartmentlist.bytegain_leads_1h',
          'model_name': 'interest_created_1h',
          'model_version': '1.1.0',
          'feature_json': 'interest_created_1h_v1.1.0',
          'filter': 'interest_created_1h_filter_110',
          'outcome_field': 'leased_at_property',
          'control_field': 'lsd_control',
          'control_weight': 3,
          'id_field': 'event_id',
          'interest_date_column': 'value_at',
          'start_date': '2017-01-01',
          'end_date': '2018-07-01',
          'random_seed': 91876,
          'max_rounds': 801,
          'max_depth': 3,
          'train_step_size': 0.25,
          'min_child_weight': 1800,
          'l2_norm': 100,
          'downsample': True}



prod_config = dict(config)
prod_config['downsample'] = False
