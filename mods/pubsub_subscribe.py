from twitchbot import PubSubTopics, Mod, get_pubsub
from dotenv import load_dotenv

load_dotenv()


# class PubSubSubscriberMod(Mod):
#     async def on_connected(self):
#         await get_pubsub().listen_to_channel('bshammer', [PubSubTopics.channel_points],
#                                              access_token=PUBSUB_OAUTH_CHANNELPOINTS)
#
#     # only needed in most cases for verifying a connection
#     # this can be removed once verified
#     # async def on_pubsub_received(self, raw: 'PubSubData'):
#     #     # this should print any errors received from twitch
#     #     print(raw.raw_data)
#
#     async def on_pubsub_custom_channel_point_reward(self, raw: 'PubSubData', data: 'PubSubPointRedemption'):
#         print(f'{data.user_display_name} has redeemed {data.reward_title}')
