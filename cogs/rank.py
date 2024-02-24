import asyncio,discord,math,random,json,typing
from discord.ext import commands
from discord import app_commands
from fakemodule import pic
import requests
from io import BytesIO
from numerize import numerize
from PIL import Image,ImageDraw,ImageFont
async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['exp'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
            users[str(server.id)][str(user.id)]['custom'] ={}
            users[str(server.id)][str(user.id)]['custom']['back']='https://cdn.discordapp.com/attachments/1010412857541799997/1065528346068402186/dfdf.png'
            users[str(server.id)][str(user.id)]['rank'] = 0
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['exp'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
            users[str(server.id)][str(user.id)]['custom'] ={}
            users[str(server.id)][str(user.id)]['custom']['back']='https://cdn.discordapp.com/attachments/1010412857541799997/1065528346068402186/dfdf.png'
            users[str(server.id)][str(user.id)]['rank'] = 0
async def updaterank(users,id):
    leaderboard = {}
    total=[]
    x=len(users[str(id)])      
    for user in list(users[str(id)]):
        name = int(user)
        total_amt = users[str(id)][str(user)]['exp']
        leaderboard[total_amt] = name
        total.append(total_amt)
        total = sorted(total,reverse=True)
    index = 1
    for amt in total:
        sid = leaderboard[amt]
        users[str(id)][str(sid)]['rank'] = index
        if index == x:
            break
        else:
            index += 1


async def add_experience(users, user):
  users[str(user.guild.id)][str(user.author.id)]['exp'] += random.randint(1,3)

async def level_up(users, user):
    exp = users[str(user.guild.id)][str(user.id)]['exp']
    users[str(user.guild.id)][str(user.id)]['level'] =exp//100
class rankup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if not message.author.bot:
            with open('jsonfile/rank.json','r') as expp:
                users = json.load(expp)
            await update_data(users, message.author,message.guild)
            await add_experience(users, message)
            await level_up(users, message.author)
            await updaterank(users,message.guild.id)
            with open('jsonfile/rank.json','w') as expp:
                json.dump(users, expp,indent=4)
    @app_commands.command()
    @app_commands.describe(member="Thành viên trong server")
    async def rank(self, ctx: discord.Interaction,*, member:  typing.Optional[discord.Member]=None):
        '''Hiển thị cấp độ và xếp hạng của mình hoặc thành viên trong server này.'''
        await ctx.response.defer()
        with open('jsonfile/rank.json', 'r') as f:
            users = json.load(f)
        server=ctx.guild.id
        if member == None:
            id = ctx.user.id
            us=ctx.user
        else:
            if member.bot:
                em = discord.Embed(title = f'Thành viên này là một người máy!',description="Một người máy thì không thể có rank.",color=discord.Colour.random())
                await ctx.response.send_message(embed=em)
                return
            id = member.id
            us=member
        avatar=us.display_avatar.url
        name=us.name
        try:
            lvl=users[str(server)][str(id)]['level']
            exp=users[str(server)][str(id)]['exp']
            rank=users[str(server)][str(id)]['rank']
            maxelv=100
            back=users[str(server)][str(id)]['custom']['back']
            image = pic.pic(name,avatar,rank,lvl,exp% 100,maxelv,back)
            await ctx.followup.send(file=discord.File(image, filename="rank.png"))
        except:
            em = discord.Embed(title = f'Thành viên này chưa có rank!',description="Thành viên này chưa có rank vì không tương tác.",color=discord.Colour.random())
            await ctx.followup.send(embed=em)
    @app_commands.command()
    @app_commands.describe(back_url="link hình ảnh")
    async def editbackrank(self, ctx: discord.Interaction,*,back_url:str):
        '''Thay đổi hình nền thẻ cấp độ và xếp hạng.'''
        with open('jsonfile/rank.json','r') as expp:
            users = json.load(expp)
        users[str(ctx.guild_id)][str(ctx.user.id)]['custom']['back']=back_url
        with open('jsonfile/rank.json','w') as expp:
                json.dump(users, expp,indent=4)
        response = requests.get(back_url)
        back = Image.open(BytesIO(response.content))
        image = BytesIO()
        back.save(image, 'PNG')
        image.seek(0)
        em = discord.Embed(title = f'Đã chỉnh sửa ảnh nền thành:',color=discord.Colour.random())
        em.set_image(url=back_url)
        await ctx.response.send_message(embed=em)
    @app_commands.command()
    async def top5rank(self, ctx: discord.Interaction):
        """Hiển thị top 5 thành viên có mức xếp hạng cao nhất."""
        with open('jsonfile/rank.json', 'r') as f:
            users = json.load(f)
        x=5
        leaderboard = {}
        total=[]
        
        for user in list(users[str(ctx.guild.id)]):
            name = int(user)
            total_amt = users[str(ctx.guild.id)][str(user)]['exp']
            leaderboard[total_amt] = name
            total.append(total_amt)

        total = sorted(total,reverse=True)
        
        em = discord.Embed(
            title = f'Top {x} Người có level cao nhất trong {ctx.guild.name}',
            description = ''
        ,color=discord.Colour.random())
        index = 1
        for amt in total:
            id = leaderboard[amt]
            lvl=users[str(ctx.guild.id)][str(id)]['level']
            maxelv=(lvl+1)*100
            namee = await self.client.fetch_user(int(id))           
            member = namee.name
            em.add_field(name = f'{index}: {member}', value = f'LEVEL: ``{lvl}``\nEXP: ``{numerize.numerize(int(amt))}``/``{numerize.numerize(int(maxelv))}``', inline=False)
            if index == x:
                break
            else:
                index += 1       
        await ctx.response.send_message(embed=em)

async def setup(bot):
    await bot.add_cog(rankup(bot))

