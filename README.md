# Setlist Survival

## Reproduce

## .env

```env
SETLIST_FM_API_KEY=

SPOTIFY_CLIENT_ID=
SPOTIFY_SECRET_KEY=
```

### Ingest data

Set up .env and config.yaml for configuration.

From the command line:

```bash
$ setlist-survival ingest --help

# Ingest all sources
$ setlist-survival ingest -o data/dir/

# Specify a specific source(s)
$ setlist-survival ingest -o data/dir/ -s spotify

# add run arguments
$ setlist-survival ingest -o /path/to/output/dir \
    -s setlists --arg "max_pages=10"
```
