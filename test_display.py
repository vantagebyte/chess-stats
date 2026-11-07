from display import format_hour, format_time_control

def test_format_hour():
    assert format_hour('0') == '12am'
    assert format_hour('9') == '9am'
    assert format_hour('12') == '12pm'
    assert format_hour('16') == '4pm'

def test_format_time_control():
    assert format_time_control('180') == '3 min'
    assert format_time_control('180+2') == '3+2'
    assert format_time_control('1/259200') == '3 days'
    assert format_time_control('-') == 'unknown'