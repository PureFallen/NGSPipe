# NGSPipe
Low effort Python script to post PSO2NGS log messages to a Discord webhook.

Depends on [NGSLogPrep](https://github.com/PureFallen/NGSLogPrep).

The code has literally been thrown together and patched several times over the last few years and as such is definitely a mess. It was never intended to be state of the art or performant, or I probably would have used something other than Python code for it. It just _works_, and that was good enough for me during that time.

Core functionality happens in `NGSPipe.py`. The file `Killswitch.py` provides a very naive solution quickly deleting all Discord webhooks used in case of emergency to user that lacks experience with the use of REST APIs.

## Known Problems

A lot.

The program is implemented as a decentralized approach to remove me (or just about anyone) as a single point of failure. However, there is no synchronization between all users, which easily leads to duplicate messages if multiple people run it for the same chats and webhooks.
Speaking of webhooks, they are stored and distributed via a `config.toml` file, to easily update parts of the bot functionality without having to distribute a new executable each time. This obviously violates several security policies and implies that the person running the script **must be fully trusted**, as they have full access to the webhook and thus the ability to do serious damage to the Discord server. The same goes for the `ID.toml`, which naively identifies a single user in case of emergency, but could easily be modified by a malicious user.
Generally said, the source code is here for auditing reasons and you are probably better off making your own. You have been warned.

## License

The source code is licensed under [The Unlicense](https://unlicense.org/). This means that the source code is contributed to the Public Domain and you can do with it whatever you want.
