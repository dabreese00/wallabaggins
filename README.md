# Wallabaggins

This is a -- *shiiiiire* ---

-- *baaaaagginsssss* ---

Sorry this is a piece of code that connects to your wallabag instance from the command line.

I mean it's a wallabag command line client.

Install it with `pip`, then run:

```
wallabaggins -h
```

You will be prompted for your Wallabag login info and API key, or you can make a config file to store it.

The config file would look like:

```
serverurl=https://my.wallabag.site
username=myuser
client=myapiclientid
```

## Obligatory security note

You could also include `password` (your Wallabag password) and `secret` (the API client secret) in the config file, but you may not like the risk of storing your secrets in a plain text file.  For now, your alternatives are:

1. You can set the environment variables `WBGINS_PASSWORD` and `WBGINS_SECRET`.
2. If you have a desktop keyring compatible with Freedesktop.org's [Secret Service](https://specifications.freedesktop.org/secret-service/latest/index.html), then wallabaggins will offer to store these secrets in your keyring for you, and should load them automatically next time you run a command.
3. If neither of those works for you, you can keep entering them at the prompt every time.

## Some other facts

It's based on work from https://github.com/Nepochal/wallabag-cli/.

It's licensed under MIT license.

It's completely incomplete.

Come on, Sam.
