from techTreeInfo import age_civs, techTreeDict, civ_score_dict

from twitchbot import (
    Arena,
    ARENA_DEFAULT_ENTRY_FEE,
    Command,
    Message,
    set_currency_name,
    get_currency_name,
    set_balance,
    get_balance,
    session,
    get_balance_from_msg,
    add_balance,
    cfg,
    InvalidArgumentsError,
    duel_expired,
    add_duel,
    accept_duel,
    subtract_balance,
    get_duel,
    add_balance_to_all,
    Balance,
    subtract_balance_from_all,
    get_nick,
    Config,
    CONFIG_FOLDER
)
import random, asyncio, aiohttp
import numpy as np

async def get_1v1_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start=1&count=10000') as r:
            r = await r.json(content_type=None)
            await session.close()
            return r

async def get_tg_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get('https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=4&start=1&count=10000') as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r

async def get_1v1_ew_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get('https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=13&start=1&count=10000') as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r

async def get_tg_ew_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get('https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=14&start=1&count=10000') as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r

async def get_1v1_dm_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get('https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=1&start=1&count=10000') as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r

async def get_tg_dm_player_json():
    """
    Helper function for pulling the top 10,000 AoE2 players' info.
    """
    async with aiohttp.ClientSession() as session2:
        async with session2.get('https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=1&start=1&count=10000') as r:
            r = await r.json(content_type=None)
            await session2.close()
            return r

@Command('rank', syntax='Optional: <"PlayerName">')
async def display_RM_rank(msg: Message, *args):
    response = await get_1v1_player_json()
    tg_response = await get_tg_player_json()
    rankings_1v1 = response['leaderboard']
    rankings_tg = tg_response['leaderboard']
    rank_1v1 = 'Not Found'
    rank_tg = 'Not Found'
    if len(args) == 0:
        for i in range(len(rankings_1v1)):
            if rankings_1v1[i]['name'] == 'BSHammer':
                rank_1v1 = rankings_1v1[i]['rating']
            if rankings_tg[i]['name'] == 'BSHammer':
                rank_tg = rankings_tg[i]['rating']
        response = f"RM BSHammer: 1v1: {rank_1v1}, TG: {rank_tg}"
    else:
        for i in range(len(rankings_1v1)):
            if rankings_1v1[i]['name'] == args[0]:
                rank_1v1 = rankings_1v1[i]['rating']
            if rankings_tg[i]['name'] == args[0]:
                rank_tg = rankings_tg[i]['rating']
        response = f"RM {args[0]}: 1v1: {rank_1v1}, TG: {rank_tg}"
    await msg.reply(response)

@Command('rankew', syntax='Optional: <"PlayerName">')
async def display_EW_rank(msg: Message, *args):
    response = await get_1v1_ew_player_json()
    tg_response = await get_tg_ew_player_json()
    rankings_1v1 = response['leaderboard']
    rankings_tg = tg_response['leaderboard']
    rank_1v1 = 'Not Found'
    rank_tg = 'Not Found'
    if len(args) == 0:
        for i in range(len(rankings_1v1)):
            if rankings_1v1[i]['name'] == 'BSHammer':
                rank_1v1 = rankings_1v1[i]['rating']
            if rankings_tg[i]['name'] == 'BSHammer':
                rank_tg = rankings_tg[i]['rating']
        response = f"EW BSHammer: 1v1: {rank_1v1}, TG: {rank_tg}"
    else:
        for i in range(len(rankings_1v1)):
            if rankings_1v1[i]['name'] == args[0]:
                rank_1v1 = rankings_1v1[i]['rating']
            if rankings_tg[i]['name'] == args[0]:
                rank_tg = rankings_tg[i]['rating']
        response = f"EW {args[0]}: 1v1: {rank_1v1}, TG: {rank_tg}"
    await msg.reply(response)


@Command('rankdm', syntax='Optional: <"PlayerName">')
async def display_DM_rank(msg: Message, *args):
    response = await get_1v1_dm_player_json()
    tg_response = await get_tg_dm_player_json()
    rankings_1v1 = response['leaderboard']
    rankings_tg = tg_response['leaderboard']
    rank_1v1 = 'Not Found'
    rank_tg = 'Not Found'
    if len(args) == 0:
        for i in range(len(rankings_1v1)):
            if rankings_1v1[i]['name'] == 'BSHammer':
                rank_1v1 = rankings_1v1[i]['rating']
            if rankings_tg[i]['name'] == 'BSHammer':
                rank_tg = rankings_tg[i]['rating']
        response = f"DM BSHammer: 1v1: {rank_1v1}, TG: {rank_tg}"
    else:
        for i in range(len(rankings_1v1)):
            if rankings_1v1[i]['name'] == args[0]:
                rank_1v1 = rankings_1v1[i]['rating']
            if rankings_tg[i]['name'] == args[0]:
                rank_tg = rankings_tg[i]['rating']
        response = f"DM {args[0]}: 1v1: {rank_1v1}, TG: {rank_tg}"
    await msg.reply(response)
