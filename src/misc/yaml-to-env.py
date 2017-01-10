#!/usr/bin/env python

import yaml
import pipes

# Merge data structures
def merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        d = dict(a)
        d.update({k: merge(a.get(k, None), b[k]) for k in b})
        return d

    if isinstance(a, list) and isinstance(b, list):
        return [merge(x, y) for x, y in itertools.izip_longest(a, b)]

    return a if b is None else b

# Read config file, keep env
def readFileKeepEnv(filename):
    f = open("config.yml", "r")
    out = ""
    for line in f:
        if "#env" in line:
            out += line + "\n"
    return out

# Load config files
config = yaml.load(readFileKeepEnv("config.yml"))
config_priv = yaml.load(readFileKeepEnv("config-private.yml"))
config = merge(config, config_priv)

print config

# Export as env vars
# TODO generalise to nested dict
envFile = ""
for k, v in config.items():
    k = pipes.quote(k)
    v = pipes.quote(v)
    envFile += "%s=%s\n" % (k, v)
open(".env", "w").write(envFile)
