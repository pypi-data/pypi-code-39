from rest_framework.response import Response

def stream_view(self, request, pk=None):
    options_fields = ['limit', 'offset', 'id_gt', 'id_gte', 'id_lt', 'id_lte', 'offset', 'ranking', 'enrich']
    extra_args = {}
    for field in options_fields:
        value = request.GET.get(field, None)
        if value is not None:
            extra_args[field] = value
            if field == 'enrich':
                true_values = ['true', 'True', 't', '1', 1]
                if value in true_values:
                    extra_args[field] = True
                else:
                    extra_args[field] = False

    stream = self.get_object().get_feed(**extra_args)
    return Response(stream)

def streamactivity_view(self, request, pk=None):

    feed = self.get_object().get_feed(**{"limit": 100, "enrich": False})

    activities = feed.get('results', [])
    action_breakdown = {}
    timeseries = { "total": {} }
    to_time = None
    from_time = None

    if activities:
        to_time = activities[0].get('time')
        from_time = activities[len(activities) - 1].get('time')

        for activity in activities:
            object_type = activity.get('object').split(":")[1]
            verb = activity.get('verb')
            key = "{}:{}".format(object_type, verb)
            count = action_breakdown.get(key, 0)
            action_breakdown[key] = (count + 1)

            day = activity.get('time').date().isoformat()
            count = timeseries.get("total").get(day, 0)
            key_count = timeseries.get(key, {}).get(day, 0)

            timeseries["total"][day] = (count + 1)
            if not (key in timeseries):
                timeseries[key] = {}
            timeseries[key][day] = (key_count + 1)


    return Response({
        "period": {
            "from": from_time,
            "to": to_time
        },
        "count": len(activities),
        # stacked timeseries:
        "timeseries": timeseries,
        "radial": action_breakdown
    })