from schema import And, Optional, Schema
from .adapters import ADAPTERS
from ipaddress import ip_address, IPv4Address, IPv6Address


def is_ipv4(s): return isinstance(ip_address(s), IPv4Address)


def is_ipv6(s): return isinstance(ip_address(s), IPv6Address)


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
        Optional('a'): [{**replace_schema, 'from': is_ipv4, 'to': is_ipv4}],
        Optional('aaaa'): [{**replace_schema, 'from': is_ipv6, 'to': is_ipv6}],
        Optional('cname'): [replace_schema],
    }
})
