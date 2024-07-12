from gcal_meta import GcalEvent

def test_string_to_values_ok():
    description = 'a: val\nb: https://www.example.com'
    expect = [
        ("a", "val"),
        ("b", "https://www.example.com")
    ]
    res = GcalEvent._parse_description(description)
    assert res == expect


def test_mix_html_string_to_values_ok():
    description = 'a: val<br>b:\xa0<a href="http://www.example.com" target="_blank"><u>https://www.example.com</u></a>'
    expect = [
        ("a", "val"),
        ("b", "https://www.example.com")
    ]
    res = GcalEvent._parse_description(description)
    assert res == expect
