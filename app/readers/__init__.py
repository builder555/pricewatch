from pathlib import Path
import importlib
from typing import Protocol

class PriceExtractor(Protocol):
    def __call__(self, url: str) -> float:
        ...

class SiteNotSupported(Exception):
    def __init__(self, site: str):
        super().__init__(f'Site {site} is not supported yet.')

class Modules:
    def __init__(self):
        self.modules = []
        current_dir = Path(__file__).parent
        module_files = Path(current_dir).rglob('*.py')
        for module_file in module_files:
            module_name = module_file.stem
            if module_name == '__init__':
                continue
            module = importlib.import_module(f'.{module_name}', __package__)
            if hasattr(module, 'SITE'):
                self.modules.append(module)
    def __getitem__(self, key):
        for m in self.modules:
            if m.SITE in key:
                return m

def get_price_extractor(site: str) -> PriceExtractor:
    module = Modules()[site]
    if module is None:
        raise SiteNotSupported(site)
    return module.get_price

def get_price(url: str) -> float:
    kind = url.split('/')[2]
    extract_price = get_price_extractor(kind)
    return extract_price(url)

def get_item_price_with_retries(url: str, max_retires: int = 10) -> float:
    retries = max_retires
    exception = Exception('error')
    while retries > 0:
        try:
            price = get_price(url)
            break
        except SiteNotSupported:
            raise
        except Exception as e:
            exception = e
            retries -= 1
    else:
        raise exception
    return price
