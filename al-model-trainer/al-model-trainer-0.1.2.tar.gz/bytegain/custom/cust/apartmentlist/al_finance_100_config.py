import bytegain.custom.cust.apartmentlist.al_xgb

config = {'table': 'apartmentlist.finance',
          'model_name': 'al_finance',
          'model_version': '1.0.0',
          'feature_json': 'al_finance_v1.0.0',
          'filter': 'al_finance_filter_100',
          'outcome_field': 'leased_at_property',
          'control_field': 'lsd_control',
          'control_weight': 1,
          'id_field': 'event_id',
          'interest_date_column': 'value_at',
          'start_date': '2017-01-01',
          'end_date': '2018-10-01',
          'random_seed': 91876,
          'max_rounds': 901,
          'max_depth': 2,
          'train_step_size': 0.3,
          'min_child_weight': 1000,
          'l2_norm': 200,
          'downsample': True}



prod_config = dict(config)
prod_config['downsample'] = False
