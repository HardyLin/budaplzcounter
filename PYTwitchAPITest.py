# from twitchAPI.twitch import Twitch
# from twitchAPI.helper import first
# import asyncio

# async def twitch_example():
#     # initialize the twitch instance, this will by default also create a app authentication for you
#     twitch = await Twitch('45c2yhxzp8cr8m3p9g9eiuqvqf0ukf', 'ztg5d71akqjrgrqazgl74rrmrsdz7r')
#     # call the API for the data of your twitch user
#     # this returns a async generator that can be used to iterate over all results
#     # but we are just interested in the first result
#     # using the first helper makes this easy.
#     user = await first(twitch.get_users(logins='ycc3741'))
#     # print the ID of your user or do whatever else you want with it
#     print(user.id)

# '45c2yhxzp8cr8m3p9g9eiuqvqf0ukf', 'ztg5d71akqjrgrqazgl74rrmrsdz7r'

from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.eventsub import EventSub
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import asyncio

TARGET_USERNAME = 'awaler0215'
EVENTSUB_URL = 'https://127.0.0.1:5000/webhook'
APP_ID = '45c2yhxzp8cr8m3p9g9eiuqvqf0ukf'
APP_SECRET = 'ztg5d71akqjrgrqazgl74rrmrsdz7r'
TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS]


async def on_follow(data: dict):
    # our event happend, lets do things with the data we got!
    print(data)


async def eventsub_example():
    # create the api instance and get the ID of the target user
    twitch = await Twitch(APP_ID, APP_SECRET)
    user = await first(twitch.get_users(logins=TARGET_USERNAME))

    # the user has to authenticate once using the bot with our intended scope.
    # since we do not need the resulting token after this authentication, we just discard the result we get from authenticate()
    # Please read up the UserAuthenticator documentation to get a full view of how this process works
    auth = UserAuthenticator(twitch, TARGET_SCOPES)
    await auth.authenticate()

    # basic setup, will run on port 8080 and a reverse proxy takes care of the https and certificate
    event_sub = EventSub(EVENTSUB_URL, APP_ID, 8080, twitch)

    # unsubscribe from all old events that might still be there
    # this will ensure we have a clean slate
    await event_sub.unsubscribe_all()
    # start the eventsub client
    event_sub.start()
    # subscribing to the desired eventsub hook for our user
    # the given function (in this example on_follow) will be called every time this event is triggered
    # the broadcaster is a moderator in their own channel by default so specifying both as the same works in this example
    await event_sub.listen_channel_follow_v2(user.id, user.id, on_follow)

    # eventsub will run in its own process
    # so lets just wait for user input before shutting it all down again
    try:
        input('press Enter to shut down...')
    finally:
        # stopping both eventsub as well as gracefully closing the connection to the API
        await event_sub.stop()
        await twitch.close()
    print('done')


# lets run our example
loop = asyncio.get_event_loop()
loop.run_until_complete(eventsub_example())