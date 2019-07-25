# from letra._parser import extract_labels, validate_label
# from test.helpers import (
#     build_invalid_color_schema_error,
#     missing_name_schema_error,
#     stub_empty_template_file_contents,
#     stub_labels,
#     stub_template_file_contents,
#     stub_template_label_missing_name,
# )
# from pytest import raises


# def test_raises_error_template_label_invalid_color():
#     invalid_color = "zzz"
#     exp_err = build_invalid_color_schema_error(invalid_color)
#     with raises(ValueError) as err:
#         extract_labels({"labels": [{"color": invalid_color}]})
#     assert str(err.value) == exp_err


# def test_raises_error_template_label_missing_name():
#     with raises(ValueError) as err:
#         extract_labels({"labels": [{"description": "foo"}]})
#     assert str(err.value) == missing_name_schema_error


# def test_returns_labels_on_valid_input():
#     labels = extract_labels(stub_template_file_contents)
#     assert labels == stub_labels
