
# DNS bulk updater for Cloudflare DNS

Simple search & replace of records across all zones.

**Note: pre-alpha/dev, work in progress!**

## Install
```sh
pip install -r requirements.txt
cfbulk --help
```

## Development

```sh
virtualenv venv
. venv/bin/activate
pip install --editable .

cfbulk --help
```