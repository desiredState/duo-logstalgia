# Duo Logstalgia

### Usage 

```bash
#!/usr/bin/env bash

docker build -t duo-logstalgia:latest . && \
docker run --rm \
    -e DUO_IKEY='<CHANGE_ME>' \
    -e DUO_SKEY='<CHANGE_ME>' \
    -e DUO_HOST='<CHANGE_ME>' \
    duo-logstalgia:latest | logstalgia --sync

```
