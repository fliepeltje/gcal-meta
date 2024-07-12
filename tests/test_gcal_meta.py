from dataclasses import dataclass
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

def test_multiple_entries_to_list_ok():
    description = "a: value a\na: value b\na: value c"
    expect = [
        ("a", "value a"),
        ("a", "value b"),
        ("a", "value c"),
    ]
    res = GcalEvent._parse_description(description)
    assert res == expect

def test_cast_to_cls_ok():
    @dataclass
    class A:
        a: str
    values = [("a", "a")]
    res = GcalEvent._cast_values_to_type(values=values, clas=A)
    assert isinstance(res, A)
    assert res.a == "a"

def test_cast_to_cls_with_optional_value_and_str_ok():
    @dataclass
    class A:
        a: str | None
    values = [("a", "a")]
    res = GcalEvent._cast_values_to_type(values=values, clas=A)
    assert isinstance(res, A)
    assert res.a == "a"

def test_cast_to_cls_with_optional_value_no_value_ok():
    @dataclass
    class A:
        a: str | None
    values = []
    res = GcalEvent._cast_values_to_type(values=values, clas=A)
    assert isinstance(res, A)
    assert res.a == None

def test_cast_to_cls_with_list():
    @dataclass
    class A:
        a: list[str]

    values = [("a", "a"), ("a", "b")]
    res = GcalEvent._cast_values_to_type(values=values, clas=A)
    assert isinstance(res, A)
    assert res.a == ["a", "b"]

def test_parse_event_to_gcal_meta_event_ok():
    @dataclass
    class A:
        a: str
        b: str
        c: str | None

    @dataclass
    class Event:
        description: str

    ev = Event(description='a: val\nb: https://www.example.com')
    gcal = GcalEvent.from_event(A, ev)
    assert isinstance(gcal, GcalEvent)
    assert gcal.meta.a == "val"
    assert gcal.meta.b == "https://www.example.com"
    assert gcal.meta.c is None