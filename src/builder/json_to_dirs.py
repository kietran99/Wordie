import json
import os
from typing import Callable

class ValidationError:
    def __init__(self, what:str, err_data) -> None:
        self.what = what
        self.err_data = err_data

def make_item_groups(root_dir_path:str, data:dict, item_processor:Callable[[list[dict], str], None]) -> None:
    groups:list[list[dict]] = zip(*[items for items in data.values()])
    for i, group in enumerate(groups):
        dir_path:str = f'{root_dir_path}\\{i:02d}'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        item_processor(group, dir_path)

def validate_json(data: dict, n_categories_expected:int, item_validator:Callable[[dict], bool]) -> [ValidationError | None]:
    n_categories:int = len(data)
    if n_categories != n_categories_expected:
        return ValidationError('Category size mismatch', n_categories)
    
    item_sizes:list[int] = [len(value) for value in data.values()]
    sample_size:int = item_sizes[0]
    has_same_size:bool = all(size == sample_size for size in item_sizes)
    if not has_same_size:
        return ValidationError('Item size mismatch', item_sizes)
    
    invalid_items:list[dict] = [item for category in data.values() for item in category if not item_validator(item)]
    if len(invalid_items) > 0:
        return ValidationError('Invalid item(s)', invalid_items)

    return None

def parse_json(path: str) -> dict:
    with open(path, 'r') as file_json:
        out_json:dict = json.load(file_json)
        return out_json