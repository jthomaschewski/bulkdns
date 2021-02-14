from .cloudflare_adapter import CloudFlareAdapter
from .dummy_adapter import DummyAdapter
from .base_adapter import BaseAdapter


ADAPTERS = {
    'cloudflare': CloudFlareAdapter,
    'dummy': DummyAdapter,
}
