import json


def get_vulnerabilities(json_data=None, dict_data=None):
    if json_data and not dict_data:
        dict_data = json.loads(json_data)
    return dict_data['metadata']['vulnerabilities']


def process(evaluation, args):
    info = ''
    if args.info_warning is not None:
        info += ';%d' % args.info_warning
        if args.info_critical is not None:
            info += ';%d' % args.info_critical
    low = ''
    if args.low_critical is not None:
        low += ';%d' % args.low_critical

    result = """<<<local>>>
P {args.service_name} INFO={evaluation[info]}{info}|LOW={evaluation[low]};{args.low_warning}{low}|MODERATE={evaluation[moderate]};{args.moderate_warning};{args.moderate_critical}|HIGH={evaluation[high]};{args.high_warning};{args.high_critical}|CRITICAL={evaluation[moderate]};{args.critical_warning};{args.critical_critical} See `npm audit` for more details.
""".format(args=args, evaluation=evaluation, info=info, low=low)
    return result
