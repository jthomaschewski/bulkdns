from schema import And, Optional, Schema
from .adapters import ADAPTERS

replace_schema = {
    'from': str,
    'to': str,
    Optional('ttl'): And(int, lambda n: n >= 120),
}

config_schema = Schema({
    'provider': lambda p: p in ADAPTERS.keys(),
    'auth': {
        Optional('cloudflare'): {
            Optional('token'): str,
            Optional('email'): str,
            Optional('certtoken'): str,
            Optional('debug'): bool,
        },
    },
    'replace': {
        Optional('a'): [replace_schema],
        Optional('aaaa'): [replace_schema],
        Optional('cname'): [replace_schema],
    }
})
