
# DNS bulk updater for Cloudflare DNS

Simple search & replace of records across all zones.

**Note: pre-alpha/dev, work in progress!**

Currently only Cloudflare DNS is supported, other providers might be added in the future.

## Install
```sh
# install requirements (optional: run within virtualenv)
$ pip install -r requirements.txt

# copy example and make changes
$ cp config.example.yml config.yml

# run bulkdns
$ bulkdns --help
```

## Development

```sh
# create & activate virtualenv (recommended)
$ virtualenv venv
$ . venv/bin/activate

# install dependencies
$ pip install --editable .

# run bulkdns
$ bulkdns --help
```