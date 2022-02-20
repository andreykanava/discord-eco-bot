import asyncio

import discord
import uaclient.entitlements
from discord.ext import commands
import os
from random import randint
import json
client = commands.Bot(command_prefix='+', intents = discord.Intents(messages = True, guild_messages = True, members = True, guilds = True))
client.remove_command("help")

@client.event
async def on_ready():
  print("Ready")
  for guild in client.guilds:
      for member in guild.members:
          print(member, member.id)
          data = {
              "id": member.id,
              "bank": 500,
              "cash": 0,
              "inventory": [],
          }
          with open('data.json', 'r+') as dt:
              list = json.load(dt)
              if data not in list["users"]:
                  list["users"].append(data)
                  dt.seek(0)
                  json.dump(list, dt)
                  print(list)
              else:
                  print("OK")
  client.loop.create_task(payday())
@client.event
async def on_member_join(member):
    print(member)
    data = {
        "id": member.id,
        "bank": 500,
        "cash": 0,
        "inventory": [],
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

@client.command(aliases=['give', 'GIVE'])
async def user_give(ctx, member: discord.Member, amount):
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
            embed.add_field(name=f'{list["items"][i]["name"]}', value=f'{list["items"][i]["decription"]} Цена: {list["items"][i]["price"]}:money_with_wings:. В наличии: {list["items"][i]["quantity"]}.')
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
                                embed.add_field(name=shoplist["items"][y]["name"], value=shoplist["items"][y]["decription"])
                    await ctx.send(embed=embed)


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
                        bank = bank + bank * 8
                    elif list["users"][i]["inventory"][x] == 10:
                        bank = bank + bank * 14
                    elif list["users"][i]["inventory"][x] == 11:
                        bank = bank + bank * 19
                list["users"][i]["bank"] = bank
                with open('data.json', 'w') as dt:
                    json.dump(list, dt)

        await asyncio.sleep(3600)
client.run('OTMwNTQ2MTM5MjI3MzYxMzIw.Yd3coA.ChkoFlV4Uv-tLAswaA0H9mu4kHk')