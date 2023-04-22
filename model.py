from typing import List
from typing import Any
from dataclasses import dataclass, asdict
import json

@dataclass
class Dataset:
    label: str
    data: List[int]
    borderColor: str
    fill: bool
        
@dataclass
class Data:
    labels: List[str]
    datasets:List[Dataset]
    
@dataclass        
class Graph:
    type: str
    data: Data