import asyncio
import discord
import requests
from discord.ext import commands
import os
from random import randint
import json
client = commands.Bot(command_prefix='+', intents = discord.Intents(messages = True, guild_messages = True, members = True, guilds = True))
client.remove_command("help")
ids = []
@client.event
async def on_ready():
  print("Ready")
  with open('data.json', 'r') as dt:
   list = json.load(dt)
  for guild in client.guilds:
      for member in guild.members:
          for c in range(len(list["users"])):
              ids.append(list["users"][c]["id"])
          print(member, member.id)
          data = {
             "id": member.id,
             "bank": 500,
             "cash": 0,
             "inventory": [],
             "opened": [],
             "rob": 0
          }
          if data["id"] not in ids:
            with open('data.json', 'w') as dtm:
              list["users"].append(data)
              json.dump(list, dtm)
              print(list)
          else:
            print("OK")
  client.loop.create_task(payday())
  client.loop.create_task(robbing())
@client.event
async def on_member_join(member):
    print(member)
    data = {
        "id": member.id,
        "bank": 500,
        "cash": 0,
        "inventory": [],
        "opened": [],
        "rob": 0
    }
    with open('data.json', 'r+') as dt:
        list = json.load(dt)
        list["users"].append(data)
        dt.seek(0)
        json.dump(list, dt)
        print(list)

@client.command(aliases = ["bal", "balance", "money", "mon"])
async def user_bal(ctx, member: discord.Member = None):
    if member is None:
        with open('data.json', 'r+') as dt:
            list = json.load(dt)
            for i in list["users"]:
                if i["id"] != ctx.author.id:
                    pass
                else:
                    cash = i["cash"]
                    bank = i["bank"]
                    total = int(cash) + int(bank)
        embed = discord.Embed(
            color=discord.Color.green()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="cash:", value=f'{cash} :money_with_wings:')
        embed.add_field(name="bank:", value=f'{bank} :money_with_wings:')
        embed.add_field(name="total:", value=f'{total} :money_with_wings:')
        await ctx.send(embed=embed)
    else:
        with open('data.json', 'r+') as dt:
            list = json.load(dt)
            for i in list["users"]:
                if i["id"] != member.id:
                    pass
                else:
                    cash = i["cash"]
                    bank = i["bank"]
                    opened = i["inventory"]
                    total = int(cash) + int(bank)
        embed = discord.Embed(
            color=discord.Color.green()
        )
        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.add_field(name="cash:", value=cash)
        embed.add_field(name="bank:", value=bank)
        embed.add_field(name="total:", value=total)
        embed.add_field(name="inventory:", value=opened)
        await ctx.send(embed=embed)

@client.command(aliases=["with", "withdraw", "WITH", "WITHDRAW"])
async def user_withdraw(ctx, value):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        for i in range(len(list["users"])):
            if list["users"][i]["id"] != ctx.author.id:
                pass
            else:
                print(i)
                cash = list["users"][i]["cash"]
                bank = list["users"][i]["bank"]
                if value == "all":
                    value = bank
                if int(value) <= bank and int(value) > 0:
                        value = int(value)
                        bank = bank - value
                        cash = cash + value
                        list["users"][i]["bank"] = bank
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)

                        embed = discord.Embed(color=discord.Color.green())
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        embed.add_field(name="Успешно! Теперь у тебя налички:", value=f'{cash} :money_with_wings:')
                        await ctx.send(embed=embed)
                else:

                    embed = discord.Embed(
                        color=discord.Color.red()
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Недостаточно средств:", value=f'{bank} :money_with_wings:')
                    await ctx.send(embed=embed)

@client.command(aliases=["dep", "deposit", "DEP", "DEPOSIT"])
async def user_deposit(ctx, value):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        for i in range(len(list["users"])):
            if list["users"][i]["id"] != ctx.author.id:
                pass
            else:
                print(i)
                cash = list["users"][i]["cash"]
                bank = list["users"][i]["bank"]
                if value == "all":
                    value = cash
                if int(value) <= cash and int(value) > 0:
                        value = int(value)
                        bank = bank + value
                        cash = cash - value

                        list["users"][i]["bank"] = bank
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)

                        embed = discord.Embed(color=discord.Color.green())
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        embed.add_field(name="Успешно! Теперь твой счет в банке:", value=f'{bank} :money_with_wings:')
                        await ctx.send(embed=embed)
                else:

                    embed = discord.Embed(
                        color=discord.Color.red()
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Недостаточно средств:", value=f'{cash} :money_with_wings:')
                    await ctx.send(embed=embed)

@client.command(aliases=["work", "WORK"])
async def user_work(ctx):
    num1 = randint(1, 1000)
    num2 = randint(1, 1000)
    num3 = randint(1, 10)
    num4 = randint(1, 10)
    ch = randint(1, 3)
    if ch == 1:
        answer = num1 + num2
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Сколько будет:", value=f" **{num1}** + **{num2}**")
        await ctx.send(embed=embed)
        print(answer)
        msg = await client.wait_for('message', check=check(ctx.author), timeout=None)
        if int(msg.content) == answer:
            pay = randint(33, 46)
            with open('data.json', 'r') as dt:
                list = json.load(dt)
                for i in range(len(list["users"])):
                    if list["users"][i]["id"] != ctx.author.id:
                        pass
                    else:
                        cash = list["users"][i]["cash"]
                        cash = cash + pay
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)
                            embed = discord.Embed(
                                color=discord.Color.green()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Верно! Вы получили",value=f'{pay} :money_with_wings:')
                            await ctx.send(embed=embed)
        else:
            pay = randint(33, 46)
            with open('data.json', 'r') as dt:
                list = json.load(dt)
                for i in range(len(list["users"])):
                    if list["users"][i]["id"] != ctx.author.id:
                        pass
                    else:
                        cash = list["users"][i]["cash"]
                        cash = cash - pay
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)
                            embed = discord.Embed(
                                color=discord.Color.red()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Ошибка! Вы были оштрафованы", value=f'{pay} :money_with_wings:')
                            await ctx.send(embed=embed)
    elif ch == 2:
        answer = num1 - num2
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Сколько будет:", value=f" **{num1}** - **{num2}**")
        await ctx.send(embed=embed)
        print(answer)
        msg = await client.wait_for('message', check=check(ctx.author), timeout=None)
        if int(msg.content) == answer:
            pay = randint(33, 46)
            with open('data.json', 'r') as dt:
                list = json.load(dt)
                for i in range(len(list["users"])):
                    if list["users"][i]["id"] != ctx.author.id:
                        pass
                    else:
                        cash = list["users"][i]["cash"]
                        cash = cash + pay
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)
                            embed = discord.Embed(
                                color=discord.Color.green()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Верно! Вы получили", value=f'{pay} :money_with_wings:')
                            await ctx.send(embed=embed)
        else:
            pay = randint(33, 46)
            with open('data.json', 'r') as dt:
                list = json.load(dt)
                for i in range(len(list["users"])):
                    if list["users"][i]["id"] != ctx.author.id:
                        pass
                    else:
                        cash = list["users"][i]["cash"]
                        cash = cash - pay
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)
                            embed = discord.Embed(
                                color=discord.Color.red()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Ошибка! Вы были оштрафованы", value=f'{pay} :money_with_wings:')
                            await ctx.send(embed=embed)
    else:
        answer = num3 * num4
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Сколько будет:", value=f" **{num4}** * **{num3}**")
        await ctx.send(embed=embed)
        print(answer)
        msg = await client.wait_for('message', check=check(ctx.author), timeout=None)
        if int(msg.content) == answer:
            pay = randint(33, 46)
            with open('data.json', 'r') as dt:
                list = json.load(dt)
                for i in range(len(list["users"])):
                    if list["users"][i]["id"] != ctx.author.id:
                        pass
                    else:
                        cash = list["users"][i]["cash"]
                        cash = cash + pay
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)
                            embed = discord.Embed(
                                color=discord.Color.green()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Верно! Вы получили", value=f'{pay} :money_with_wings:')
                            await ctx.send(embed=embed)
        else:
            pay = randint(33, 46)
            with open('data.json', 'r') as dt:
                list = json.load(dt)
                for i in range(len(list["users"])):
                    if list["users"][i]["id"] != ctx.author.id:
                        pass
                    else:
                        cash = list["users"][i]["cash"]
                        cash = cash - pay
                        list["users"][i]["cash"] = cash
                        with open('data.json', 'w') as dt:
                            json.dump(list, dt)
                            embed = discord.Embed(
                                color=discord.Color.red()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Ошибка! Вы были оштрафованы", value=f'{pay} :money_with_wings:')
                            await ctx.send(embed=embed)

@client.command(aliases=['pay', 'PAY'])
async def user_pay(ctx, member: discord.Member, amount):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        for i in range(len(list['users'])):
            if list['users'][i]['id'] == ctx.author.id:
                giver_cash = list['users'][i]['cash']
                if amount == 'all':
                    amount = giver_cash
                amount = int(amount)
                if amount > 0 and amount <= giver_cash:
                    giver_cash = giver_cash - amount
                    list['users'][i]['cash'] = giver_cash
                    for x in range(len(list['users'])):
                        if list['users'][x]['id'] == member.id:
                            getter_cash = list['users'][x]['cash']
                            getter_cash = getter_cash + amount
                            list['users'][x]['cash'] = getter_cash
                    with open('data.json', 'w') as dwt:
                        json.dump(list, dwt)
                        embed = discord.Embed(
                            color=discord.Color.green()
                        )
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        embed.add_field(name="Успешно!", value=f"Ты передал {amount} :money_with_wings: {member.display_name}")
                        await ctx.send(embed=embed)

@client.command(aliases=['shop', 'SHOP'])
async def user_shop(ctx):
    with open('shop.json', 'r') as dt:
        list = json.load(dt)
        embed = discord.Embed(
            color=discord.Color.blurple(),
            title='shop'
        )
        for i in range(len(list['items'])):
            embed.add_field(name=f'{list["items"][i]["name"]} - {list["items"][i]["price"]}:money_with_wings:', value=f'{list["items"][i]["decription"]}. В наличии: {list["items"][i]["quantity"]}.')
        await ctx.send(embed=embed)

@client.command(aliases=['buy', 'BUY'])
async def user_buy(ctx, item):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        for i in range(len(list["users"])):
            if list["users"][i]["id"] == ctx.author.id:
                cash = list["users"][i]["cash"]
                with open('shop.json', 'r') as sh:
                    shoplist = json.load(sh)
                    for x in range(len(shoplist["items"])):
                        print(shoplist["items"][x]["id"])
                        if shoplist["items"][x]["id"] == int(item):
                            if shoplist["items"][x]["price"] <= cash:
                                if shoplist["items"][x]["quantity"] != 0:
                                    list["users"][i]["inventory"].append(shoplist["items"][x]["id"])
                                    list["users"][i]["cash"] = cash - shoplist["items"][x]["price"]
                                    shoplist["items"][x]["quantity"] = shoplist["items"][x]["quantity"] - 1
                                    with open('data.json', 'w') as dt:
                                        json.dump(list, dt)
                                    with open('shop.json', 'w') as dt:
                                        json.dump(shoplist, dt)
                                    embed = discord.Embed(
                                        color=discord.Color.green()
                                    )
                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                    embed.add_field(name="Успешно! ты купил:", value=f"{shoplist['items'][x]['name']}")
                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(
                                        color=discord.Color.red()
                                    )
                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                    embed.add_field(name="Нет в наличии:", value=f"{shoplist['items'][x]['name']}")
                                    await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(
                                    color=discord.Color.red()
                                )
                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                embed.add_field(name="Недостаточно средств!", value=f"для покупки нужно: {shoplist['items'][x]['price']} :money_with_wings:")
                                await ctx.send(embed=embed)

@client.command(aliases=['inventory', 'inv', 'INV', 'INVENTORY'])
async def user_inventory(ctx):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        with open('shop.json', 'r') as sh:
            shoplist = json.load(sh)
            profit = 0
            for i in range(len(list["users"])):
                if list["users"][i]["id"] == ctx.author.id:
                    embed = discord.Embed(
                        color=discord.Color.green(),
                        title='Твой инвентарь:'
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    inventory = range(len(list["users"][i]["inventory"]))
                    for x in range(len(list["users"][i]["inventory"])):
                        for y in range(len(shoplist["items"])):
                            if list["users"][i]["inventory"][x] == shoplist["items"][y]["id"]:
                                profit = profit + shoplist["items"][y]["profit"]
                                embed.add_field(name=shoplist["items"][y]["name"], value=shoplist["items"][y]["decription"])
                    embed.add_field(name='Ваш часовой доход составляет:', value=profit)
                    await ctx.send(embed=embed)

@client.command(aliases=['coin', 'coinflip', 'COIN', 'COINFLIP'])
async def user_coinflip(ctx, bet, space):
  with open('data.json', 'r') as dt:
    list = json.load(dt)
    for i in range(len(list['users'])):
      if ctx.author.id == list['users'][i]['id']:
        if bet == 'all':
          bet = list['users'][i]['cash']
        space = int(space)
        bet = int(bet)
        if bet <= list['users'][i]['cash']:
          if space == randint(1, 2):
            list['users'][i]['cash'] = list['users'][i]['cash'] + bet
            with open('data.json', 'w') as dtj:
              json.dump(list, dtj)
              embed = discord.Embed(
                                        color=discord.Color.green()
                                    )
              embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
              embed.add_field(name="Победа", value=f"{bet}:money_with_wings:")
              await ctx.send(embed=embed)
          else:
            list['users'][i]['cash'] = list['users'][i]['cash'] - bet
            with open('data.json', 'w') as dtj:
              json.dump(list, dtj)
              embed = discord.Embed(
                                        color=discord.Color.red()
                                    )
              embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
              embed.add_field(name="Поражение", value=f"{bet}:money_with_wings:")
              await ctx.send(embed=embed)
        else:
          embed = discord.Embed(
                                        color=discord.Color.red()
                                    )
          embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
          embed.add_field(name="Недостаточно средств", value=f"{bet}:money_with_wings:")
          await ctx.send(embed=embed)

@client.command(aliases=['crypto', 'CRYPTO'])
async def user_crypto(ctx, crypto: str = None):
    if crypto == None:
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="BTC:", value=get_current_price('BTCUSDT'))
        embed.add_field(name="ETH:", value=get_current_price('ETHUSDT'))
        embed.add_field(name="BCH:", value=get_current_price('BCHUSDT'))
        embed.add_field(name="BNB:", value=get_current_price('BNBUSDT'))
        embed.add_field(name="ADA:", value=get_current_price('ADAUSDT'))
        embed.add_field(name="LUNA:", value=get_current_price('LUNAUSDT'))
        await ctx.send(embed=embed)
    else:
        currency = get_current_price(crypto.upper() + 'USDT')
        if currency == None:
            embed = discord.Embed(
                color=discord.Color.red()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"Такой валюты нет:", value=crypto)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.add_field(name=f"{crypto.upper()}:", value=currency)
            await ctx.send(embed=embed)

@client.command(aliases=['long', 'LONG'])
async def user_long(ctx, amount, laverage, symbol):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        for i in range(len(list["users"])):
            if list["users"][i]["id"] == ctx.author.id:
                if amount == 'all':
                    amount = list["users"][i]["cash"]
                if list["users"][i]["cash"] >= int(amount) and list["users"][i]["cash"] > 0:
                    id = len(list["users"][i]["opened"]) + 1
                    leverage = int(laverage)
                    if leverage > 0 and leverage <= 150:
                        amount = int(amount)
                        symbol = symbol.upper()
                        price = get_current_price(symbol + 'USDT')
                        if price != None:
                            list["users"][i]["cash"] = list["users"][i]["cash"] - amount
                            direction = 'long'
                            dict = {}
                            dict[id] = price, symbol, leverage, amount, direction
                            print(dict)
                            list["users"][i]["opened"].append(dict)
                            print(list["users"][i]["opened"])
                            with open('data.json', 'w') as jsf:
                                json.dump(list, jsf)
                                embed = discord.Embed(
                                    color=discord.Color.green()
                                )
                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                embed.add_field(name=f"Сделка открыта!", value=f"№ {id}\n валюта {symbol}\n кредитное плечо: {leverage}\n сумма: {amount}\n направление: {direction}\n цена открытия: {price}")
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                color=discord.Color.red()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name=f"Такой валюты нет!:",
                                            value=symbol)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            color=discord.Color.red()
                        )
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        embed.add_field(name=f"Кредитное плечо должно быть больше положительное и меньше 150",
                                        value=f"кредитное плечо: {leverage}")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color=discord.Color.red()
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    embed.add_field(name=f"Недостаточно средств!:",
                                    value=f"сумма: {amount}")
                    await ctx.send(embed=embed)

@client.command(aliases=['short', 'SHORT'])
async def user_short(ctx, amount, laverage, symbol):
    with open('data.json', 'r') as dt:
        list = json.load(dt)
        for i in range(len(list["users"])):
            if list["users"][i]["id"] == ctx.author.id:
                if amount == 'all':
                    amount = list["users"][i]["cash"]
                if list["users"][i]["cash"] >= int(amount) and list["users"][i]["cash"] > 0:
                    id = len(list["users"][i]["opened"]) + 1
                    leverage = int(laverage)
                    if leverage > 0 and leverage <= 150:
                        amount = int(amount)
                        symbol = symbol.upper()
                        price = get_current_price(symbol + 'USDT')
                        if price != None:
                            list["users"][i]["cash"] = list["users"][i]["cash"] - amount
                            direction = 'short'
                            dict = {}
                            dict[id] = price, symbol, leverage, amount, direction
                            print(dict)
                            list["users"][i]["opened"].append(dict)
                            print(list["users"][i]["opened"])
                            with open('data.json', 'w') as jsf:
                                json.dump(list, jsf)
                                embed = discord.Embed(
                                    color=discord.Color.green()
                                )
                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                embed.add_field(name=f"Сделка открыта!", value=f"№ {id}\n валюта {symbol}\n кредитное плечо: {leverage}\n сумма: {amount}\n направление: {direction}\n цена открытия: {price}")
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                color=discord.Color.red()
                            )
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name=f"Такой валюты нет!:",
                                            value=symbol)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            color=discord.Color.red()
                        )
                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        embed.add_field(name=f"Кредитное плечо должно быть больше положительное и меньше 150",
                                        value=f"кредитное плечо: {leverage}")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color=discord.Color.red()
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    embed.add_field(name=f"Недостаточно средств!:",
                                    value=f"сумма: {amount}")
                    await ctx.send(embed=embed)

@client.command(aliases=['deals', 'DEALS'])
async def user_deals(ctx):
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                embed = discord.Embed(
                    color=discord.Color.blue(),
                    title='Твои сделки:'
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                for x in range(len(list1["users"][i]["opened"])):
                    for m in list1['users'][i]['opened'][x]:
                        embed.add_field(name=f"сделка No. {list(list1['users'][i]['opened'][x].keys())[0]}", value=f'валюта: {list1["users"][i]["opened"][x][m][1]}\nкредитное плечо: {list1["users"][i]["opened"][x][m][2]}\nсумма: {list1["users"][i]["opened"][x][m][3]}\nнаправление: {list1["users"][i]["opened"][x][m][4]}\nцена открытия: {list1["users"][i]["opened"][x][m][0]}')
                await ctx.send(embed=embed)

@client.command(aliases=['close', 'CLOSE'])
async def user_close(ctx, num):
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                for x in range(len(list1["users"][i]["opened"])):
                    if list(list1['users'][i]['opened'][x].keys())[0] == num:
                        for m in list1['users'][i]['opened'][x]:
                            openprice = list1["users"][i]["opened"][x][m][0]
                            symbol = list1["users"][i]["opened"][x][m][1]
                            leverage = list1["users"][i]["opened"][x][m][2]
                            amount = list1["users"][i]["opened"][x][m][3]
                            direction = list1["users"][i]["opened"][x][m][4]
                            usdbal = list1['users'][i]['cash']
                            curprice = get_current_price(symbol + 'USDT')
                            openprice = float(openprice)
                            leverage = int(leverage)
                            amount = int(amount)
                            usdbal = int(usdbal)
                            curprice = float(curprice)
                            if direction == 'short':
                                profit = curprice / openprice * 100 - 100
                                profit = profit * leverage
                                profit = profit / 100
                                profit = profit * -1
                                list1['users'][i]['cash'] = round(amount * profit + amount + usdbal)
                                list1['users'][i]['opened'].remove(list1['users'][i]['opened'][x])
                                with open('data.json', 'w') as obj:
                                    json.dump(list1, obj)
                                    embed = discord.Embed(
                                        color=discord.Color.green()
                                    )
                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                    embed.add_field(name=f"Сделка закрыта!:",
                                                    value=f"валюта: {symbol}\n кредитное плечо: {leverage}\n сумма: {amount}\n направление: {direction}\n цена открытия: {openprice}\n цена закрытия: {curprice}")
                                    await ctx.send(embed=embed)
                            else:
                                profit = curprice / openprice * 100 - 100
                                profit = profit * leverage
                                profit = profit / 100
                                list1['users'][i]['cash'] = round(amount * profit + amount + usdbal)
                                list1['users'][i]['opened'].remove(list1['users'][i]['opened'][x])
                                with open('data.json', 'w') as obj:
                                    json.dump(list1, obj)
                                    embed = discord.Embed(
                                        color=discord.Color.green()
                                    )
                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                    embed.add_field(name=f"Сделка закрыта!:",
                                                    value=f"валюта: {symbol}\n кредитное плечо: {leverage}\n сумма: {amount}\n направление: {direction}\n цена открытия: {openprice}\n цена закрытия: {curprice}")
                                    await ctx.send(embed=embed)

@client.command(aliases=['help', 'HELP'])
async def user_help(ctx):
    embed = discord.Embed(
        color=discord.Color.blue()
    )
    embed.add_field(name=f"+bal - показывает ваш баланс",
                    value=f"+bal\n +bal @user")
    embed.add_field(name=f"+with - снятие денег из банковского счета",
                    value=f"+with [сумма]")
    embed.add_field(name=f"+dep - пополнение банковского счета",
                    value=f"+dep [сумма]")
    embed.add_field(name=f"+work - работа",
                    value=f"+work")
    embed.add_field(name=f"+pay - перечисление денег другому пользователю",
                    value=f"+pay @user [сумма]")
    embed.add_field(name=f"+shop - показывает список доступных товаров",
                    value=f"+shop")
    embed.add_field(name=f"+buy - покупка имущества",
                    value=f"+buy [id предмета]")
    embed.add_field(name=f"+inv - показывает ваш инвентарь",
                    value=f"+inv")
    embed.add_field(name=f"+coin - игра в монетку",
                    value=f"+coin [сумма] [1|2]")
    embed.add_field(name=f"+crypto - показывает стоимость криптовалют",
                    value=f"+crypto\n +crypto [монета]")
    embed.add_field(name=f"+long - открытие сделки в лонг",
                    value=f"+long [сумма] [кредитное плечо] [монета]")
    embed.add_field(name=f"+short - открытие сделки в шорт",
                    value=f"+short [сумма] [кредитное плечо] [монета]")
    embed.add_field(name=f"+deals - показывает открытые сделки",
                    value=f"+deals")
    embed.add_field(name=f"+close - закрытие сделки",
                    value=f"+close [id сделки]")
    embed.add_field(name=f"+help - показывает это сообщение",
                    value=f"+help")
    embed.add_field(name=f"+rob - ограбление пользователя",
                    value=f"+rob @user")
    embed.add_field(name=f"+give - передача предмета другому пользователю",
                    value=f"+give @user [id предмета]")
    await ctx.send(embed=embed)

@client.command(aliases=['darkshop', 'DARKSHOP'])
async def user_darkshop(ctx):
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                if 12 in list1["users"][i]["inventory"]:
                    with open('shop.json', 'r') as dt:
                        list = json.load(dt)
                        embed = discord.Embed(
                            color=discord.Color.blurple(),
                            title='Darknet shop'
                        )
                        for i in range(len(list['dark'])):
                            embed.add_field(
                                name=f'{list["dark"][i]["name"]} - {list["dark"][i]["price"]}:money_with_wings:',
                                value=f'{list["dark"][i]["decription"]}. В наличии: {list["dark"][i]["quantity"]}.')
                        await ctx.send(embed=embed)

@client.command(aliases=['darkbuy', 'DARKBUY'])
async def user_darkbuy(ctx, item):
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                if 12 in list1["users"][i]["inventory"]:
                    with open('data.json', 'r') as dt:
                        list = json.load(dt)
                        for i in range(len(list["users"])):
                            if list["users"][i]["id"] == ctx.author.id:
                                cash = list["users"][i]["cash"]
                                with open('shop.json', 'r') as sh:
                                    shoplist = json.load(sh)
                                    for x in range(len(shoplist["dark"])):
                                        print(shoplist["dark"][x]["id"])
                                        if shoplist["dark"][x]["id"] == int(item):
                                            if shoplist["dark"][x]["price"] <= cash:
                                                if shoplist["dark"][x]["quantity"] != 0:
                                                    list["users"][i]["inventory"].append(shoplist["dark"][x]["id"])
                                                    list["users"][i]["cash"] = cash - shoplist["dark"][x]["price"]
                                                    shoplist["dark"][x]["quantity"] = shoplist["dark"][x][
                                                                                           "quantity"] - 1
                                                    with open('data.json', 'w') as dt:
                                                        json.dump(list, dt)
                                                    with open('shop.json', 'w') as dt:
                                                        json.dump(shoplist, dt)
                                                    embed = discord.Embed(
                                                        color=discord.Color.green()
                                                    )
                                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                                    embed.add_field(name="Успешно! ты купил:",
                                                                    value=f"{shoplist['dark'][x]['name']}")
                                                    await ctx.send(embed=embed)
                                                else:
                                                    embed = discord.Embed(
                                                        color=discord.Color.red()
                                                    )
                                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                                    embed.add_field(name="Нет в наличии:",
                                                                    value=f"{shoplist['dark'][x]['name']}")
                                                    await ctx.send(embed=embed)
                                            else:
                                                embed = discord.Embed(
                                                    color=discord.Color.red()
                                                )
                                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                                embed.add_field(name="Недостаточно средств!",
                                                                value=f"для покупки нужно: {shoplist['dark'][x]['price']} :money_with_wings:")
                                                await ctx.send(embed=embed)

@client.command(aliases=['darkinv', 'DARKINV'])
async def user_darkinv(ctx):
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                if 12 in list1["users"][i]["inventory"]:
                    with open('data.json', 'r') as dt:
                        list = json.load(dt)
                        with open('shop.json', 'r') as sh:
                            shoplist = json.load(sh)
                            profit = 0
                            for i in range(len(list["users"])):
                                if list["users"][i]["id"] == ctx.author.id:
                                    embed = discord.Embed(
                                        color=discord.Color.green(),
                                        title='Твой инвентарь:'
                                    )
                                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                    inventory = range(len(list["users"][i]["inventory"]))
                                    for x in range(len(list["users"][i]["inventory"])):
                                        for y in range(len(shoplist["dark"])):
                                            if list["users"][i]["inventory"][x] == shoplist["dark"][y]["id"]:
                                                profit = profit + shoplist["dark"][y]["profit"]
                                                embed.add_field(name=shoplist["dark"][y]["name"],
                                                                value=shoplist["dark"][y]["decription"])
                                    embed.add_field(name='Ваш часовой доход составляет:', value=profit)
                                    await ctx.send(embed=embed)

@client.command(aliases=['rob', 'ROB'])
async def user_rob(ctx, member: discord.Member):
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                for x in range(len(list1["users"])):
                    if list1["users"][x]["id"] == member.id:
                        giver_cash = list1["users"][x]["cash"]
                        robber_cash = list1["users"][i]["cash"]
                        if giver_cash != 0:
                            if list1["users"][i]["rob"] == 0:
                                robbed = randint(1, giver_cash)
                                chance = randint(1, 10)
                                if chance == 1 or chance == 2:
                                    list1["users"][x]["cash"] = giver_cash - robbed
                                    list1["users"][i]["cash"] = robber_cash + robbed
                                    list1["users"][i]["rob"] = 3600
                                    with open('data.json', 'w') as jsf:
                                        json.dump(list1, jsf)
                                        embed = discord.Embed(
                                            color=discord.Color.green()
                                        )
                                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                        embed.add_field(name="Успешно!",
                                                        value=f"Ты украл {robbed} :money_with_wings: у {member.display_name}")
                                        await ctx.send(embed=embed)
                                else:
                                    a = randint(1, 700)
                                    list1["users"][i]["cash"] = robber_cash - a
                                    list1["users"][i]["rob"] = 3600
                                    with open('data.json', 'w') as jsf:
                                        json.dump(list1, jsf)
                                        embed = discord.Embed(
                                            color=discord.Color.red()
                                        )
                                        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                        embed.add_field(name="Неудача!",
                                                        value=f"Ты попытался украсть :money_with_wings: у {member.display_name} но тебя поймали! Ты был оштрафован на {a} :money_with_wings:")
                                        await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(
                                    color=discord.Color.red()
                                )
                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                embed.add_field(name="Ты не можешь украсть сейчас!",
                                                value=f"Подожди еще {list1['users'][i]['rob']} секунд")
                                await ctx.send(embed=embed)
                        else:
                            list1["users"][i]["rob"] = 3600
                            with open('data.json', 'w') as jsf:
                                json.dump(list1, jsf)
                                embed = discord.Embed(
                                    color=discord.Color.red()
                                )
                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                embed.add_field(name="Неудача!",
                                                value=f"У {member.display_name} 0 :money_with_wings:")
                                await ctx.send(embed=embed)

@client.command(aliases=['give', 'GIVE'])
async def user_give(ctx, member: discord.Member, item):
    item = int(item)
    with open('data.json', 'r') as dt:
        list1 = json.load(dt)
        for i in range(len(list1["users"])):
            if list1["users"][i]["id"] == ctx.author.id:
                for x in range(len(list1["users"])):
                    if list1["users"][x]["id"] == member.id:
                        if item in list1["users"][i]["inventory"]:
                            list1["users"][x]["inventory"].append(item)
                            list1["users"][i]["inventory"].remove(item)
                            with open('data.json', 'w') as jsf:
                                json.dump(list1, jsf)
                                embed = discord.Embed(color=discord.Color.green())
                                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                                embed.add_field(name="Успешно!", value=f"Ты передал {item} {member.display_name}")
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(color=discord.Color.red())
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="У тебя нет этого предмета!", value=f"{item}")
                            await ctx.send(embed=embed)

def get_price(symbol, prices):
    for price in prices:
        if symbol == price['symbol']:
            return price['price']
def get_current_price(symbol):
    prices = requests.get('https://api.binance.com/api/v3/ticker/price').json()
    return get_price(symbol, prices)
def check(author):
    def inner_check(messege):
        if messege.author != author:
            return False
        try:
            int(messege.content)
            return True
        except ValueError:
            return False
    return inner_check
async def payday():
    while True:
        with open('data.json', 'r') as dt:
            list = json.load(dt)
            for i in range(len(list["users"])):
                bank = list["users"][i]["bank"]
                bank = int(bank) + randint(40, 60)
                list["users"][i]["bank"] = bank
                for x in range(len(list["users"][i]["inventory"])):
                    if list["users"][i]["inventory"][x] == 1:
                        bank = bank + 50
                    elif list["users"][i]["inventory"][x] == 2:
                        bank = bank + 160
                    elif list["users"][i]["inventory"][x] == 3:
                        bank = bank + 310
                    elif list["users"][i]["inventory"][x] == 4:
                        bank = bank + 700
                    elif list["users"][i]["inventory"][x] == 5:
                        bank = bank + 290
                    elif list["users"][i]["inventory"][x] == 6:
                        bank = bank + 300
                    elif list["users"][i]["inventory"][x] == 7:
                        bank =bank + 300
                    elif list["users"][i]["inventory"][x] == 8:
                        bank = bank + 300
                    elif list["users"][i]["inventory"][x] == 9:
                        bank = bank + 200
                        bank = round(bank)
                    elif list["users"][i]["inventory"][x] == 10:
                        bank = bank + 400
                        bank = round(bank)
                    elif list["users"][i]["inventory"][x] == 11:
                        bank = bank + 200
                        bank = round(bank)
                list["users"][i]["bank"] = bank
                with open('data.json', 'w') as dt:
                    json.dump(list, dt)

        await asyncio.sleep(3600)
async def robbing():
    while True:
        with open('data.json', 'r') as dt:
            list = json.load(dt)
            for i in range(len(list["users"])):
                if list["users"][i]["rob"] != 0:
                    list["users"][i]["rob"] = list["users"][i]["rob"] - 1
                    with open('data.json', 'w') as dt:
                        json.dump(list, dt)
        await asyncio.sleep(1)
client.run('')