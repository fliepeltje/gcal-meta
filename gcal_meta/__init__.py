from bs4 import BeautifulSoup
from dataclasses import dataclass

from ics import Calendar, Event

from typing import Type, TypeVar

T = TypeVar("T")
Values = list[tuple[str, str]]

@dataclass
class GcalEvent:
    event: Event
    meta: T | None


    @staticmethod
    def _parse_description(description: str) -> Values:
        values = []
        if "<" in description and ">" in description:
            description = description.replace("\xa0", "").strip()
            elements = BeautifulSoup(description, "html.parser").findAll(text=True)
            string = " ".join(elements)
            pairs = string.split(": ")
            i_list: list[str] = []
            for idx, val in enumerate(pairs, start=1):
                if idx % 2 == 0:
                    v, _, k = val.rpartition(" ")
                    i_list.append(v)
                    i_list.append(k)
                else:
                    i_list.append(val)
            kv_pairs = [(i_list[i], i_list[i+1]) for i in range(0, len(i_list), 2)]
            return kv_pairs
        for line in description.strip().split("\n"):
            key, _, value = line.strip().partition(":")
            values.append((key.strip(), value.strip()))
        return values
