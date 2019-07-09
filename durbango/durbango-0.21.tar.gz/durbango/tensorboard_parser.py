from collections import defaultdict
import pandas as pd

def is_interesting_tag(tag):
    if 'val' in tag or 'train' in tag:
        return True
    else:
        return False


def _find_modal_len(metrics: dict) -> int:
    return pd.Series({k: len(v) for k, v in metrics.items()}).value_counts().index[0]


def parse_tf_events_file(p1):
    import tensorflow as tf
    metrics = defaultdict(list)
    for e in tf.train.summary_iterator(str(p1)):
        for v in e.summary.value:

            if isinstance(v.simple_value, float) and is_interesting_tag(v.tag):
                metrics[v.tag].append(v.simple_value)
            if v.tag == 'loss' or v.tag == 'accuracy':
                print(v.simple_value)
    n_epochs = _find_modal_len(metrics)
    metrics_df = pd.DataFrame({k: v for k,v in metrics.items() if len(v) == n_epochs})
    return metrics_df
