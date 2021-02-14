from schema import And, Optional, Schema

replace_schema = {
    'from': str,
    'to': str,
    Optional('ttl'): And(int, lambda n: n >= 120),
}

config_schema = Schema({
    'auth': {'token': str},
    'replace': {
        Optional('a'): [replace_schema],
        Optional('aaaa'): [replace_schema],
        Optional('cname'): [replace_schema],
    }
})
