# cs244b-web-caching
## To run the proxy server
SSH to your myth server or other server machine that you want to use. Update the `host` and `port` configuration of the `master` key in data.json.

Then run

```
python3 proxy.py
```


## To run the cache server
SSH to each cache machine that you want to use. Make sure that the `host` and `port`
configuration of the `master` key in data.json matches the master server. Make
sure that the `cachePort` key in data.json is the same in the master server and 
the cache server.

Then run

```
python3 cache.py
```

Final design paper:
https://www.scs.stanford.edu/22sp-cs244b/projects/Web%20Caching%20with%20Consistent%20Hashing.pdf
