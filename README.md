# aiogram-alert-bot

~~A telegram Aiogram bot for pinning messages about air alert in Ukraine~~

That was (and still kinda is) my first aiogram bot. It was made for purely as a part of my coding journey (and, of course, fun). Even the name of the repo is outadated because it does much more (unfortunately) than just sending alert messages.

> [!WARNING]
> **SHIT CODE WARNING.** There isn't one good decision implemented there, *beileve me*. With that said, *please*, don't base any of your projects on this one, for your own mental sake.

The main reason that repo was not private is that I didn't know about deployment keys and github actions when I started, that's how bad everything was :skull:.

Now I keep it public because I don't feel ashamed!! And also because there indeed are some useful parts of code that I can give as an example *(:warning: it still doesn't mean that you should look through that project seeking something good!!)*

## What this bot can do

- automatically pin a video that warns about and air alarm and unpin it as soon as air raid is over (using alerts_in_ua API)

- `/help`: send a list of available commands
- `/faq`: send a FAQ article
- `/vahta`: send a watchmen's schedule
- `/donate`: send  donation details
- `/bunt` and `/rusoriz`: send corresponding stickers
- greet a new chat member
- `/weather_now` and `/weather_today`: show current weather and a forecast for a day
- `/concert`: send a random audio with some music
- `/svyato`: send a list of today's holidays
- `/svitlo` and `/svitlo2`: send electicity schedule for today
- `/next_svitlo` and `/next_svitlo2`: send electicity schedule for tomorrow

## What can an admin of this bot do

- update the watchmen's schedule using commands
- send messages to the chat and pin them on behalf of the bot

## What's wrong with the bot??

Ohh, you should have asked what's right with it. Firstly, a lot of things are hardcoded (like location for weather and alerts), so even if you decide to use this bot in your chat (please *don't*) - you would need to hardcode it as well. Oh! And alert's logic is based on `while True`, which is...... not great. A lot of unnecessary files, logic is flawed, not optimized etc etc.. 

## Conclusion

![im-cringe-but-im-free](https://i.kym-cdn.com/entries/icons/original/000/047/915/thumb-cringe.png)
