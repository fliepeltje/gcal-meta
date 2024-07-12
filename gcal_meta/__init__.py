from bs4 import BeautifulSoup
from dataclasses import dataclass

from types import UnionType
from typing import Type, TypeVar, Protocol

T = TypeVar("T")
Values = list[tuple[str, str]]

class Event(Protocol):
    description: str

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

    @staticmethod
    def _cast_values_to_type(clas: Type[T], values: Values) -> T:
        create_args = {}
        annotations = clas.__annotations__
        for key, val_type in annotations.items():
            if isinstance(val_type, UnionType) and type(None) in val_type.__args__:
                create_args[key] = None
            elif hasattr(val_type, "sort"):
                create_args[key] = []
        for key, val in values:
            val_type = annotations[key]
            if isinstance(val_type, UnionType):
                for union_type in [x for x in val_type.__args__]:
                    try:
                        create_args[key] = union_type(val)
                        break
                    except:
                        continue
            elif key in create_args and isinstance(create_args[key], list):
                create_args[key].append(val)
            else:
                create_args[key] = val_type(val)
        return clas(**create_args)
    
    @classmethod
    def from_event(cls, t: Type[T], event: Event) -> "GcalEvent":
        values = cls._parse_description(event.description)
        meta = cls._cast_values_to_type(t, values)
        return GcalEvent(event=Event, meta=meta)