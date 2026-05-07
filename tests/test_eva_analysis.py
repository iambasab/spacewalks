import pytest
from eva_data_analysis import text_to_duration, calculate_crew_size

def test_text_to_duration_float():
    '''
    Test that the function returns expected ground truth values for typical
    durations with a non-zero minute component
    '''
    assert text_to_duration("10:20") == pytest.approx(10.3333333)


def test_text_to_duration_integer():
    '''
    Test that the function returns expected ground truth values for typical
    whole hour durations
    '''
    assert text_to_duration("10:00") == 10


@pytest.mark.parametrize("input_value, expected_result", [
    ("Valentina Tereshkova;", 1),
    ("Judith Resnik; Sally Ride;", 2)
])
def test_calculate_crew_size(input_value, expected_result):
    """
    Test that it returns ground truth values for typical crew values
    """
    actual_result = calculate_crew_size(input_value)
    assert actual_result == expected_result


def test_calculate_crew_size_edge_cases():
    '''
    Test it returns expected values for edge cases where crew is an empty string
    '''
    actual_result=calculate_crew_size("")
    assert actual_result is None
