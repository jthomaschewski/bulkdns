
# DNS bulk updater for Cloudflare DNS

Simple search & replace of records across all zones.

**Note: pre-alpha/dev, work in progress!**

Currently only Cloudflare DNS is supported, other providers might be added in the future.

## Install
```sh
pip install -r requirements.txt
bulkdns --help
```

## Development

```sh
virtualenv venv
. venv/bin/activate
pip install --editable .

bulkdns --help
```