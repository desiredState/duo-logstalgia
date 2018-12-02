# Duo Logstalgia

### Usage 

```bash
docker run --rm \
    -e DUO_IKEY='<CHANGE_ME>' \
    -e DUO_SKEY='<CHANGE_ME>' \
    -e DUO_HOST='<CHANGE_ME>' \
    desiredstate/duo-logstalgia:latest | \
    tee /dev/tty | logstalgia -x -g "Duo Access Log,CODE=.*?,100" -
```
