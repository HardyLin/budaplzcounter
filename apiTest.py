from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import asyncio

APP_ID = '45c2yhxzp8cr8m3p9g9eiuqvqf0ukf'
APP_SECRET = 'ztg5d71akqjrgrqazgl74rrmrsdz7r'
async def on_ready():
    twitch = await Twitch(APP_ID, APP_SECRET)

    target_scope = [AuthScope.BITS_READ]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    # this will open your default browser and prompt you with the twitch verification website
    token, refresh_token = await auth.authenticate()
    # add User authentication
    await twitch.set_user_authentication(token, target_scope, refresh_token)

asyncio.run(on_ready())