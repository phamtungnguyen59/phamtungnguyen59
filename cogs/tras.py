
from discord.ext import commands
from discord import app_commands
import discord,json,typing
from fakemodule import pydustry


class tras(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command()
    async def inforserver(self, ctx: discord.Interaction) -> None:
        """Hiển Thị Thông Tin Server"""
        embed = discord.Embed(title=f"{ctx.guild.name} Info", description="Thông Tin Máy Chủ", color=discord.Colour.random())
        embed.add_field(name='🆔Server ID', value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name='📆Ngày Tạo', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
        embed.add_field(name='👑Chủ Server', value=f"{ctx.guild.owner}", inline=True)
        embed.add_field(name='👥Thành Viên', value=f'{ctx.guild.member_count} Thành Viên', inline=True)
        embed.add_field(name='💬Kênh', value=f'{len(ctx.guild.text_channels)} text | {len(ctx.guild.voice_channels)} Voice', inline=True)
        embed.add_field(name='🌎Giới Thiệu', value=f'{ctx.guild.description}', inline=True)
        embed.set_thumbnail(url=ctx.guild.icon) 
        embed.set_footer(text="⭐⭐⭐⭐⭐ • Server Này Rất Bố Đời")    
        embed.set_author(name=f'{ctx.user.name}' ,icon_url=ctx.user.avatar.url)
        await ctx.response.send_message(embed=embed)

    @app_commands.command()
    async def ping(self, ctx: discord.Interaction) -> None:
        """Hiển Thị Tốc Độ Kết Nối với Bot"""
        ping1 = f"{str(round(self.client.latency * 1000))} ms"
        embed = discord.Embed(title = "**Pong!**", description = "**" + ping1 + "**", color = 0xafdafc)
        await ctx.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.describe(host='Địa Chỉ Máy Chủ',port="Cổng Máy Chủ")
    async def mindustry_ping_server(self, ctx: discord.Interaction,host:str,port:int=6567) -> None:
        """Hiển Thị THông Tin Server Mindustry"""
        a=pydustry.Server(host,port).get_status()
        embed = discord.Embed(title="Thông Tin Server Mindustry",description="")
        embed.set_author(name=f'{ctx.user.name}' ,icon_url=ctx.user.avatar.url)
        embed.set_footer(text="⭐⭐⭐⭐⭐ • Server Này Rất Bố Đời")
        embed.add_field(name=f"IP: {host}",value="",inline=False)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name=a.name,value="",inline=False)
        embed.add_field(name=f"Bản Đồ: {a.map}",value='',inline=False)
        embed.add_field(name=F'Đợt: {a.wave}',value='',inline=False)
        embed.add_field(name=f'Số Người Chơi: {a.players}',value='',inline=False)
        embed.add_field(name=f'Phiên Bản: {a.version}',value='',inline=False)
        embed.add_field(name=f'Ping: {a.ping}',value='',inline=False)
        embed.add_field(name=f'Thể loại: {a.vertype}',value='',inline=False)      
        await ctx.response.send_message(embed=embed)

    @app_commands.command()
    async def userinfo(self, ctx: discord.Interaction, *, user: typing.Optional[discord.Member] =None): 
        """Hiển Thị Thông Tin Thành Viên"""
        if user is None:
            user = ctx.user
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(title=f"Thông Tin Của {user.name}:", color=discord.Colour.random())
        em.set_image(url=user.avatar.url)
        em.add_field(name=f"Tên", value=f"{user.mention}", inline=True)
        em.add_field(name=f"Ngày Tham Gia Cộng Đồng Discord", value=f"{user.created_at.strftime(date_format)}", inline=True)
        em.add_field(name=f"Tham Gia Sẻver Vào Ngày", value=f"{user.joined_at.strftime(date_format)}", inline=True)
        em.set_footer(text='ID: ' + str(user.id))
        await ctx.response.send_message(embed=em)

    @app_commands.command(name="delete")
    async def delete(self,ctx: discord.Interaction, limit:int,member: typing.Optional[discord.Member] =None):
        """Xóa một số lượng Tin nhắn"""
        id=ctx.channel_id
        channel=self.client.get_channel(id)
        em=discord.Embed(description="",color=discord.Colour.random())
        if ctx.permissions.manage_messages == False:
            em.title="Bot Không có quyền thực hiện lệnh này!, vui lòng liên hệ Admin để cấp quyền cho bot."
            return ctx.response.send_message(embed=em,delete_after=3)
        aa=discord.Embed(title="Bắt đầu xóa tin nhắn!",description="",color=discord.Colour.random())
        msg = []
        if limit ==0:
            em.title="Vui lòng nhập số lượng tin nhắn cần để xóa!"
            return await channel.send(embed=em,delete_after=3)
        try:
            limit = int(limit)
        except:
            em.title="Vui lòng nhập số lượng tin nhắn cần để xóa!"
            return await channel.send(embed=em,delete_after=3)
        await ctx.response.send_message(embed=aa)

        if member ==None:
            await ctx.channel.purge(limit=limit)
            em.title=f"Đã xóa {limit} tin nhắn!"
            return await channel.send(embed=em,delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        em.title=f"Đã xóa {limit} tin nhắn của {member.mention}!"
        await channel.send(embed=em,delete_after=3)

    @app_commands.command()
    async def inforbot(self, ctx: discord.Interaction):
        """Hiển Thị Thông Tin Bot"""

        a=discord.ui.View()
        sup=discord.ui.Button(style=discord.ButtonStyle.link,url="https://discord.gg/SdxTxrYu8k",label="Hỗ Trợ")
        four=discord.ui.Button(style=discord.ButtonStyle.link,
                               url="https://www.youtube.com/channel/UCFINNqRcNcOAemuyKdBiDpA?sub_confirmation=1",
                               label="Four Gaming Studio")
        lin=discord.ui.Button(style=discord.ButtonStyle.link,url="https://github.com/FourGamingStudio/FGS_musicdiscord.py",label="Mã nguồn bot")
        a.clear_items()
        a.add_item(sup)
        a.add_item(four)
        a.add_item(lin)
        em=discord.Embed(title=f"Thông tin bot {self.client.user.name}",description="", color=discord.Colour.random())
        em.add_field(name=self.client.user.name,value=f"""Xin chào tôi là {self.client.user.name}. 
        - Tôi được sinh ra trong lúc thằng chủ tôi rảnh rỗi 😂.
        - Bot được phát triển bởi [JACK.VN](https://discord.gg/SdxTxrYu8k) - [Four Gaming Studio](https://www.youtube.com/channel/UCFINNqRcNcOAemuyKdBiDpA?sub_confirmation=1).
        - Bạn có thể sử dụng lệnh `/help` để biết thêm các lệnh mà bạn có thể tương tác với tôi.
        - [Bạn đang hỏi mã nguồn ở đâu? vâng nó ở đây](https://github.com/FourGamingStudio/FGS_musicdiscord.py)""") 
        await ctx.response.send_message(embed=em,view=a)
      
    
async def setup(bot):
    await bot.add_cog(tras(bot))
