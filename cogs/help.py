import asyncio
from discord.ext import commands 
from discord import app_commands
import time, discord,math

class MyView(discord.ui.View): 
    def __init__(self,em,server):
        super().__init__(timeout=None)
        self.em=em
        self.count_numepage={}
        self.count_numepage[server]=0
        self.maxpage=len(em)
        self.back2.disabled =True
        self.back.disabled =True
        self.back.style=discord.ButtonStyle.grey
        self.back2.style=discord.ButtonStyle.grey
        self.count.label=f"0/{len(em)-1}"
    async def button_update(self,server):
        text=f"{self.count_numepage[server]}/{self.maxpage-1}"
        self.count.label=text
        if self.count_numepage[server]==0:
            self.back2.disabled =True
            self.back.disabled =True
            self.back.style=discord.ButtonStyle.grey
            self.back2.style=discord.ButtonStyle.grey
        else:
            self.back2.disabled =False
            self.back.disabled =False
            self.back.style=discord.ButtonStyle.green
            self.back2.style=discord.ButtonStyle.green
        if self.count_numepage[server]==self.maxpage-1:
            self.go2.disabled =True
            self.go.disabled =True
            self.go.style=discord.ButtonStyle.grey
            self.go2.style=discord.ButtonStyle.grey
        else:
            self.go2.disabled =False
            self.go.disabled =False
            self.go.style=discord.ButtonStyle.green
            self.go2.style=discord.ButtonStyle.green

    @discord.ui.button( style=discord.ButtonStyle.primary, emoji="⏪")
    async def back2(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        embedd = self.em
        if self.count_numepage[server] ==0:
            await interaction.response.send_message('Đang ở trang đầu!!!',ephemeral=True)  
            return
        self.count_numepage[server]=0
        await self.button_update(server)
        await interaction.response.edit_message(embed=embedd[0].set_footer(text="Trang: 0"),view=self)
    @discord.ui.button( style=discord.ButtonStyle.primary, emoji="⬅️")
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        embedd = self.em     
        if self.count_numepage[server] ==0:
            await interaction.response.send_message('Đang ở trang đầu!!!',ephemeral=True)  
            return
        self.count_numepage[server]-=1
        await self.button_update(server)
        count=self.count_numepage[server]
        await interaction.response.edit_message(embed=embedd[count].set_footer(text=f"Trang: {count}"),view=self)
    @discord.ui.button(style=discord.ButtonStyle.red)
    async def count(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message('Đã Hủy')
        await ctx.channel.purge(limit=2)
        self.stop()

    @discord.ui.button( style=discord.ButtonStyle.primary, emoji="➡️")
    async def go(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        embedd = self.em
        if self.count_numepage[server] ==self.maxpage-1:
            await interaction.response.send_message('Đang ở trang cuối!!!',ephemeral=True)  
            return
        self.count_numepage[server]+=1
        count=self.count_numepage[server]
        await self.button_update(server)
        await interaction.response.edit_message(embed=embedd[count].set_footer(text=f"Trang: {count}"),view=self)

    @discord.ui.button( style=discord.ButtonStyle.primary, emoji="⏩")
    async def go2(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        embedd = self.em
        maxpagee=self.maxpage-1
        if self.count_numepage[server] ==maxpagee:
            await interaction.response.send_message('Đang ở trang cuối!!!',ephemeral=True)  
            return
        self.count_numepage[server]=maxpagee
        await self.button_update(server)

        await interaction.response.edit_message(embed=embedd[maxpagee].set_footer(text=f"Trang: {maxpagee}"),view=self)
class help_2(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="help")
    async def help(self, ctx: discord.Interaction,) -> None:
        """Xem Lệnh Của Bot"""
        commands = self.client.tree.walk_commands()
        listcom=[]
        for command in commands:
            listcom.append({
                "name":command.name,
                "dis":command.description,
                "parameters":command.parameters
            })
        k=7
        a=0
        embeds=[]
        for i in range(math.ceil(len(listcom)/k)):
            aa=listcom[a:k]
            a=k
            k+=7
            em=discord.Embed(title="Danh Sách Lệnh:",description="",color=discord.Colour.random())
            for abc in aa:
                namet=""
                namet+=f"/{abc['name']}"
                if len(abc["parameters"]) != 0:
                    for i in abc['parameters']:
                        namet+=f" `{i.name}`"
                em.add_field(name=namet,value=abc["dis"],inline=False)
            embeds.append(em)
        server= ctx.guild_id
        await ctx.response.send_message(embed=embeds[0].set_footer(text="Trang: 0"), view=MyView(embeds,server))


async def setup(bot):
    await bot.add_cog(help_2(bot))