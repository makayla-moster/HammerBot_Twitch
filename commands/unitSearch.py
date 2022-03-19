from techTreeInfo import age_civs, techTreeDict, civ_score_dict, unitList

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
import random
import numpy as np

@Command('unit', syntax='!unit <letter(s)>')
async def cmd_civ_info(msg: Message, *args):
    if len(args) == 0:
        message = "Search for a Unit with !unit <letter>. Example: !unit a"
    elif len(args) < 5:
        if len(args) == 4:
            arg1 = args[0].lower() + " " + args[1].lower() + " " + args[2].lower() + " " + args[3].lower()
        elif len(args) == 3:
            arg1 = args[0].lower() + " " + args[1].lower() + " " + args[2].lower()
        elif len(args) == 2:
            arg1 = args[0].lower() + " " + args[1].lower()
        else:
            arg1 = args[0].lower()

        tempDict = {}
        for key in unitList:
            if key.lower().startswith(arg1.lower()):
                tempDict[key] = unitList[key]
        if len(tempDict) == 0:
            message = f"There are no '{arg1.upper()}' Units"
        elif len(tempDict) > 10:
            message =f"There are too many '{arg1.upper()}' Units. Please refine your search."
        else:
            message = ""
            count = 0
            for key in tempDict:
                if count < len(tempDict) - 1:
                    message += key + ", "
                    count += 1
                else:
                    message += key
    await msg.reply(message)
