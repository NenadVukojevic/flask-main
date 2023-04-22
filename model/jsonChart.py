from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Dataset:
    label: str
    backgroundColor: List[str]
    data: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        _label = str(obj.get("label"))
        _backgroundColor = [.from_dict(y) for y in obj.get("backgroundColor")]
        _data = [.from_dict(y) for y in obj.get("data")]
        return Dataset(_label, _backgroundColor, _data)
        return Data(_labels, _datasets)
    
@dataclass
class Data:
    labels: List[str]
    datasets: List[Dataset]

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        _labels = [.from_dict(y) for y in obj.get("labels")]
        _datasets = [Dataset.from_dict(y) for y in obj.get("datasets")]


@dataclass
class Legend:
    display: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Legend':
        _display = 
        return Legend(_display)

@dataclass
class Title:
    display: bool
    text: str

    @staticmethod
    def from_dict(obj: Any) -> 'Title':
        _display = 
        _text = str(obj.get("text"))
        return Title(_display, _text)
    
@dataclass
class Options:
    legend: Legend
    title: Title

    @staticmethod
    def from_dict(obj: Any) -> 'Options':
        _legend = Legend.from_dict(obj.get("legend"))
        _title = Title.from_dict(obj.get("title"))
        return Options(_legend, _title)

@dataclass
class Root:
    type: str
    data: Data
    options: Options

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _type = str(obj.get("type"))
        _data = Data.from_dict(obj.get("data"))
        _options = Options.from_dict(obj.get("options"))
        return Root(_type, _data, _options)


# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
