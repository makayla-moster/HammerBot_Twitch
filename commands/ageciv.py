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
import random
import numpy as np

@Command('civ', syntax='<civ name>')
async def cmd_civ_info(msg: Message, *args):
    if len(args) != 1:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_civ_info)
    try:
        civName = args[0].lower()
    except InvalidArgumentsError:
        raise InvalidArgumentsError(reason='missing required arguments or check civ spelling', cmd=cmd_civ_info)
    if civName in age_civs:
        await msg.reply(f"https://aoe2techtree.net/#{civName}")
    else:
        raise InvalidArgumentsError(reason='missing required arguments or check civ spelling', cmd=cmd_civ_info)


@Command('randomciv', syntax='<optional number less than 15>')
async def cmd_random_civ(msg: Message, *args):
    response = ''
    if (len(args) == 1) and (args[0].isnumeric() == True) and (1 <= int(args[0]) <= 15):
        for i in range(int(args[0])):
            if i == 0:
                response = random.choice(age_civs).title()
            else:
                response += ", " + random.choice(age_civs).title()
    elif (len(args) == 0):
        response = random.choice(age_civs).title()
    else:
        raise InvalidArgumentsError(reason='check argument input', cmd=cmd_random_civ)

    await msg.reply(response)


@Command('teamciv', syntax='<optional integer number from 2-4>')
async def cmd_team_random_civ(msg: Message, *args):
    def random_civ_position(position, amount, uniform_size, b1):
        # position: flank = 0, pocket = 1
        b0_values = [flankavg, pocketavg]
        result = []
        for i in range(amount):
            random_civs = []
            for i in range(uniform_size):
                random_civs.append(age_civs[random.randint(0, 38)].title())

            total_score = 0
            for item in random_civs:
                total_score += civ_score_dict[item][position]

            weights = []
            b0 = (-b0_values[position]+0)*b1

            for item in random_civs:
                p = 1/ (1 + np.exp( -(b0 + b1*civ_score_dict[item][position]) ))
                weights.append(p)
            result.append(random.choices(random_civs, weights, k = 1)[0])

        return result

    if (len(args) == 0):
        user_arg = 2
    elif (len(args) == 1) and (args[0].isnumeric() == True) and (1 < int(args[0]) < 5):
        user_arg = int(args[0])
    else:
        raise InvalidArgumentsError(reason='check argument input', cmd=cmd_civ_info)
    try:
        flanksum = 0
        pocketsum = 0
        for item in civ_score_dict:
            flanksum += civ_score_dict[item][0]
            pocketsum += civ_score_dict[item][1]
        flankavg = flanksum/39
        pocketavg = pocketsum/39

        if (user_arg == None) or user_arg == 2:
            response = f"{random_civ_position(0, 1, 5, 2)[0]}, {random_civ_position(1, 1, 5, 2)[0]}"
        elif user_arg == 3:
            response = f"Flanks: {', '.join(random_civ_position(0, 2, 5, 2))} || Pocket: {random_civ_position(1, 1, 5, 2)[0]}"
        else:
            response = f"Flanks: {', '.join(random_civ_position(0, 2, 5, 2))} || Pockets: {', '.join(random_civ_position(1, 2, 5, 2))}"
        await msg.reply(response)
    except InvalidArgumentsError:
        raise InvalidArgumentsError(reason='check argument input', cmd=cmd_civ_info)


@Command('whichciv', syntax='<tech1> or <tech1+tech2+...> or <techNamePart1 techNamePart2 ...>')
async def cmd_which_civ(msg:Message, *args):
    if (len(args) == 5):
        arg1 = args[0].title() + " " + args[1].title() + " " + args[2].title() + " " + args[3].title() + " " + args[4].title()
        try:
            response = techTreeDict[arg1]
        except InvalidArgumentsError:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
        response.sort()
    elif (len(args) == 4):
        arg1 = args[0].title() + " " + args[1].title() + " " + args[2].title() + " " + args[3].title()
        try:
            response = techTreeDict[arg1]
        except InvalidArgumentsError:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
        response.sort()
    elif (len(args) == 3):
        arg1 = args[0].title() + " " + args[1].title() + " " + args[2].title()
        try:
            response = techTreeDict[arg1]
        except InvalidArgumentsError:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
        response.sort()
    elif (len(args) == 2):
        arg1 = args[0].title() + " " + args[1].title()
        try:
            response = techTreeDict[arg1]
        except InvalidArgumentsError:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
        response.sort()
    elif (len(args) == 1) and ('+' in args[0]):
        arg1 = args[0].split("+")
        try:
            for i in range(len(arg1)-1):
                tech = arg1[int(i)]
                tech2 = arg1[int(i+1)]
                if i == 0:
                    list1 = techTreeDict[tech.title()]
                    list2 = techTreeDict[tech2.title()]
                else:
                    list1 = list3
                    list2 = techTreeDict[tech2.title()]
                list3 = set(list1).intersection(list2)
            response = list3
        except InvalidArgumentsError:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
        response = sorted(response)
    elif (len(args) == 1):
        try:
            response = techTreeDict[args[0].title()]
        except InvalidArgumentsError:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
        response.sort()
    else:
        raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_which_civ)
    await msg.reply(", ".join(response))

@Command('does', syntax='<civName techName> or <civName1+civName2 techName> or <civName(s) techNamePart1 techNamePart2>')
async def cmd_does(msg: Message, *args):
    if len(args) > 0:
        if args[0].lower() in age_civs:
            if len(args) == 5:
                arg2 = args[1].title() + " " + args[2].title() + " " + args[3].title() + " " + args[4].title()
            elif len(args) == 4:
                arg2 = args[1].title() + " " + args[2].title() + " " + args[3].title()
            elif len(args) == 3:
                arg2 = args[1].title() + " " + args[2].title()
            elif len(args) == 2:
                arg2 = args[1].title()

            bool = args[0].title() in techTreeDict[arg2.title()]

            if bool:
                response = args[0].title() + " have " + arg2.title()
            elif not bool:
                response = args[0].title() + "do not have" + arg2.title()
            else:
                response = "Error!"

        elif '+' in args[0]:
            arg1 = args[0].split("+")

            if len(args) == 5:
                arg2 = args[1].title() + " " + args[2].title() + " " + args[3].title() + " " + args[4].title()
            elif len(args) == 4:
                arg2 = args[1].title() + " " + args[2].title() + " " + args[3].title()
            elif len(args) == 3:
                arg2 = args[1].title() + " " + args[2].title()
            elif len(args) == 2:
                arg2 = args[1].title()

            if len(arg1) > 0:
                for i in range(len(arg1)):
                    if arg1[i].lower() in age_civs:
                        bool = arg1[i].title() in techTreeDict[arg2.title()]
                        if bool:
                            if i == 0:
                                response = arg1[i].title() + " have " + arg2.title()
                            else:
                                response += ", " + arg1[i].title() + " have " + arg2.title()
                        elif not bool:
                            if i == 0:
                                response = arg1[0].title() + " do not have " + arg2.title()
                            else:
                                response += ", " + arg1[i].title() + " do not have " + arg2.title()
                        else:
                            response = f"Error!"
        else:
            raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_does)
    else:
        raise InvalidArgumentsError(reason='check argument input or spelling', cmd=cmd_does)

    await msg.reply(response)





# @Command('gg', syntax='<civ name>')
# async def cmd_gg(msg: Message, *args):
#     await msg.reply(f"bshammGG bshammGG bshammGG")
