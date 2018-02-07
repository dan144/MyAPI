# MyAPI

This repo will contain an API built using Flask to provide
a number of in-home services. The first planned tooling is
a way to track the progress I make reading books, and some
method of compiling progress and historical stats to basic
reports.

A service will be built to allow the API to persist on any
always-on host (e.g. a Raspberry Pi).

## API

GET `/`

A basic homepage

GET `/report`

Displays a table of all recorded page history with their
timestamps

POST `/log`

Requires a JSON payload with `date` and `page` to add data
to the page history

## Files

`install.sh` is a temporary script to "install" files into
/opt/MyAPI/

`run.sh` is a temporary script to "install" files and then
stop, reload, and start `myapi.service`

`test_log.py` is a script to test the fuctionality of POST
calls to the endpoing `/log`
