import asyncio
from discord.ext import commands 
import time, discord,json


class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        url = f'https://www.google.com/search?q={query}'
        self.add_item(discord.ui.Button(label='Click Here', url=url))

class mes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="test")
    async def test(self,ctx):
        """Kiểm tra tốc độ kết nối với bot"""
        await ctx.message.add_reaction('✅')
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`",delete_after=25)
        print(f'Ping {int(ping)}ms')

    @commands.command()
    async def clear(self,ctx, limit=100, member: discord.Member=None):
        await ctx.message.delete()
        msg = []
        try:
            limit = int(limit)
        except:
            return await ctx.send("Please pass in an integer as limit",delete_after=3)
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)

    @commands.command()
    async def google(self,ctx: commands.Context, *, query: str):
        """Returns a google link for a query"""
        await ctx.send(f'Google Result for: `{query}`', view=Google(query),delete_after=60)
    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Returns a google link for a query"""
        await ctx.message.delete()


    
    @commands.Cog.listener("on_member_join")
    async def on_member_join(self,member):
        await member.send(f'Chào mùng {member.name} đến với **{member.guild.name}, nhớ đọc #luật trước khi bị ban nhé**.')
        #verifiedRole = discord.utils.get(member.guild.roles, id = 1011324831297450005)
        #await member.add_roles(verifiedRole)

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self,member):
        await member.send('''Ơ tại sao bạn lại rời sever thế?.
Đây là link sever discord nếu bạn suy nghĩ lại.
https://discord.gg/4nEVbnXgcy''')
        #channel = self.bot.get_channel(wellcome_channel_id)
        #await self.get_channel(channel).send(f"{member.name} has joined")

    
    @commands.command(pass_context=True,aliases=['in'])
    async def invite(self,ctx,user=0,age=0):
        link = await ctx.channel.create_invite(max_age = age, max_uses = user)
        if age == 0:
            age='Không bao giờ hết hạn.'
        if user == 0:
            user='sử dụng vô hạn.'
        em = discord.Embed(title=f"Tham gia Discord {ctx.guild.name} Ngay Bây Giờ!", url=link, description=f"**{ctx.guild.member_count} Thành Viên Đã** [**Tham Gia**]({link})\n\n**Liên kết với kênh {ctx.channel.mention} đã được tạo.**\nSố người dùng tối đa: **{user}**\nThời Gian tối đa: **{age}**", color=0x303037)       
        em.set_footer(text=f"Made by {ctx.guild.name}. \nTin nhắn này sẽ bị xóa sau 60s")
        em.set_thumbnail(url=ctx.guild.icon)
        em.set_author(name="LỜI MỜI THAM GIA")
        await ctx.send(f"> {link}", embed=em,delete_after=60)


    @commands.command(name="lock",aliases=['lc','lk'])
    @commands.has_permissions(manage_channels=True)
    async def lock(self,ctx,channel:discord.TextChannel = None):
        """Đóng kênh chat"""
        if channel ==None:
            channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send(f'{channel} lock.',delete_after=10)
        except Exception:
            await ctx.send(f"Bot không có đủ quyền để unlock bố ơi!!!!!",delete_after=5)
            
    @commands.command(name='unlock',aliases=['un'])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self,ctx,channel:discord.TextChannel = None):
        """Mở khóa kênh chat"""
        if channel ==None:
            channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await ctx.send(f'{channel} unlock.',delete_after=10)
        except Exception:
            await ctx.send(f"Bot không có đủ quyền để unlock bố ơi!!!!!",delete_after=5)
        


async def setup(bot):
    await bot.add_cog(mes(bot))
