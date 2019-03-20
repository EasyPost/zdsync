*zdsync* is a command-line utility for syncing Zendesk environments.

## Dependencies

 - Python 3.5+
 - [`zenpy`](https://github.com/facetoe/zenpy)

## Usage

If you install with `python setup.py install` or through pip, this should drop a program named `zdsync` into your PYTHONHOME. Otherwise, you can use `PYTHONPATH=. python -m zdsync.cli` to get the same effect.

There are four required environment variables:

 * `SANDBOX_SUBDOMAIN` - The subdomain of your sandbox environment, e.g. `mycompany1552085434`.
 * `SANDBOX_TOKEN` - An oauth token with _read/write_ access to the sandbox environment.
 * `PRODUCTION_SUBDOMAIN` - The subdomain of your production environment, e.g. `mycompany`.
 * `PRODUCTION_TOKEN` - An oauth token with _read only_ access to the production environment.

There are five supported objects for syncing:

 * `--brands`
 * `--groups`
 * `--ticket-fields`
 * `--ticket-forms`
 * `--macros`

It its recommended to sync in this order since there are object dependencies as you progress through the list. If you pass all the flags at once it will sync in this order.

Just passing an object flag will print out the status of the environments,

```
$ zdsync --macros

The following Macros only exist in the sandbox:


The following Macros only exist in production:


The following Macros are different between environments:
Take it!                                                Downgrade and inform                                    Close and redirect to topics                            Customer not responding

There are 257 other Macros that are the same between environments.
```

In order to actually execute the sync you must pass the `--execute` flag,

```
$ zdsync --macros --execute
```

## License

This tool is licensed under the ISC License, the text of which is available at [LICENSE.txt](LICENSE.txt).
