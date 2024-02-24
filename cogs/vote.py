from discord.ext import commands 
from discord import app_commands
import discord,json
from fakemodule import pic
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Chấp Nhận!', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Đang tải!', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Hủy!', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Đang tải!', ephemeral=True)
        self.value = False
        self.stop()
class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self,server,title,description):
        super().__init__(timeout=None)
        self.title=title
        self.description=description
        with open('jsonfile/vote.json', 'r') as exppp:
            userss = json.load(exppp)
        self.answer1.label=userss[str(server)]['answer1']['Name']
        self.answer2.label=userss[str(server)]['answer2']['Name']
        if userss[str(server)]['answer3']['Name'] != None:
            self.answer3.label=userss[str(server)]['answer3']['Name']
        else: self.remove_item(self.answer3)
        if userss[str(server)]['answer3']['Name'] != None:
            self.answer4.label=userss[str(server)]['answer4']['Name']
        else: self.remove_item(self.answer4)
        if userss[str(server)]['answer3']['Name'] != None:
            self.answer5.label=userss[str(server)]['answer5']['Name']
        else: self.remove_item(self.answer5)
    @discord.ui.button( style=discord.ButtonStyle.green)
    async def answer1(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        server= interaction.guild_id
        user= interaction.user.id
        
        with open('jsonfile/vote.json', 'r') as exppp:
            userss = json.load(exppp)
        Name=userss[str(server)]['answer1']['Name']
        if str(user) in userss[str(server)]['answer1']:
            await interaction.response.send_message(f'Bạn đã bỏ phiếu cho {Name} rồi!',ephemeral=True)  
            return
        text=f"Bạn đã bỏ phiếu cho {Name} ở <#{interaction.channel.id}>."
        for i in userss[str(server)]:
            if str(user) in userss[str(server)][i]:
                del userss[str(server)][i][str(user)]
                Name1=userss[str(server)][i]['Name']
                userss[str(server)][i]['T']-=1
                text=f"Bạn đã thay đổi phiếu bầu từ {Name1} sang {Name} ở <#{interaction.channel.id}>."
        userss[str(server)]['answer1'][str(user)]={}
        userss[str(server)]['answer1']['T']+=1
        with open('jsonfile/vote.json','w') as expp:
            json.dump(userss, expp,indent=4)

        image=pic.votepic(str(server))
        embed = discord.Embed(title=self.title,description=self.description, color=discord.Colour.random())
        file = discord.File(image, filename="vote.png")
        embed.set_image(url="attachment://vote.png")
        await interaction.response.edit_message(embed=embed,attachments=[file],view=self)
        await interaction.user.send(text,delete_after=15,) 
    @discord.ui.button( style=discord.ButtonStyle.green)# Create a button with the label "😎 Click me!" with color Blurple
    async def answer2(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        user= interaction.user.id
        
        with open('jsonfile/vote.json', 'r') as exppp:
            userss = json.load(exppp)
        Name=userss[str(server)]['answer2']['Name']
        if str(user) in userss[str(server)]['answer2']:
            await interaction.response.send_message(f'Bạn đã bỏ phiếu cho {Name} rồi!',ephemeral=True)  
            return
        text=f"Bạn đã bỏ phiếu cho {Name} ở <#{interaction.channel.id}>."
        for i in userss[str(server)]:
            if str(user) in userss[str(server)][i]:
                del userss[str(server)][i][str(user)]
                Name1=userss[str(server)][i]['Name']
                userss[str(server)][i]['T']-=1
                text=f"Bạn đã thay đổi phiếu bầu từ {Name1} sang {Name} ở <#{interaction.channel.id}>."
        userss[str(server)]['answer2'][str(user)]={}
        userss[str(server)]['answer2']['T']+=1
        with open('jsonfile/vote.json','w') as expp:
            json.dump(userss, expp,indent=4)

        image=pic.votepic(str(server))
        embed = discord.Embed(title=self.title,description=self.description, color=discord.Colour.random())
        file = discord.File(image, filename="vote.png")
        embed.set_image(url="attachment://vote.png")
        await interaction.response.edit_message(embed=embed,attachments=[file],view=self)
        await interaction.user.send(text,delete_after=15,)
    @discord.ui.button( style=discord.ButtonStyle.green)# Create a button with the label "😎 Click me!" with color Blurple
    async def answer3(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        user= interaction.user.id
        
        with open('jsonfile/vote.json', 'r') as exppp:
            userss = json.load(exppp)
        Name=userss[str(server)]['answer3']['Name']
        if str(user) in userss[str(server)]['answer3']:
            await interaction.response.send_message(f'Bạn đã bỏ phiếu cho {Name} rồi!',ephemeral=True)  
            return
        text=f"Bạn đã bỏ phiếu cho {Name} ở <#{interaction.channel.id}>."
        for i in userss[str(server)]:
            if str(user) in userss[str(server)][i]:
                del userss[str(server)][i][str(user)]
                Name1=userss[str(server)][i]['Name']
                userss[str(server)][i]['T']-=1
                text=f"Bạn đã thay đổi phiếu bầu từ {Name1} sang {Name} ở <#{interaction.channel.id}>."
        userss[str(server)]['answer3'][str(user)]={}
        userss[str(server)]['answer3']['T']+=1
        with open('jsonfile/vote.json','w') as expp:
            json.dump(userss, expp,indent=4)

        image=pic.votepic(str(server))
        embed = discord.Embed(title=self.title,description=self.description, color=discord.Colour.random())
        file = discord.File(image, filename="vote.png")
        embed.set_image(url="attachment://vote.png")
        await interaction.response.edit_message(embed=embed,attachments=[file],view=self)
        await interaction.user.send(text,delete_after=15,)
    @discord.ui.button( style=discord.ButtonStyle.green)# Create a button with the label "😎 Click me!" with color Blurple
    async def answer4(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        user= interaction.user.id
        
        with open('jsonfile/vote.json', 'r') as exppp:
            userss = json.load(exppp)
        Name=userss[str(server)]['answer4']['Name']
        if str(user) in userss[str(server)]['answer1']:
            await interaction.response.send_message(f'Bạn đã bỏ phiếu cho {Name} rồi!',ephemeral=True)  
            return
        text=f"Bạn đã bỏ phiếu cho {Name} ở <#{interaction.channel.id}>."
        for i in userss[str(server)]:
            if str(user) in userss[str(server)][i]:
                del userss[str(server)][i][str(user)]
                Name1=userss[str(server)][i]['Name']
                userss[str(server)][i]['T']-=1
                text=f"Bạn đã thay đổi phiếu bầu từ {Name1} sang {Name} ở <#{interaction.channel.id}>."
        userss[str(server)]['answer4'][str(user)]={}
        userss[str(server)]['answer4']['T']+=1
        with open('jsonfile/vote.json','w') as expp:
            json.dump(userss, expp,indent=4)

        image=pic.votepic(str(server))
        embed = discord.Embed(title=self.title,description=self.description, color=discord.Colour.random())
        file = discord.File(image, filename="vote.png")
        embed.set_image(url="attachment://vote.png")
        await interaction.response.edit_message(embed=embed,attachments=[file],view=self)
        await interaction.user.send(text,delete_after=15,) 
    @discord.ui.button( style=discord.ButtonStyle.green)# Create a button with the label "😎 Click me!" with color Blurple
    async def answer5(self, interaction: discord.Interaction, button: discord.ui.Button):
        server= interaction.guild_id
        user= interaction.user.id
        
        with open('jsonfile/vote.json', 'r') as exppp:
            userss = json.load(exppp)
        Name=userss[str(server)]['answer5']['Name']
        if str(user) in userss[str(server)]['answer1']:
            await interaction.response.send_message(f'Bạn đã bỏ phiếu cho {Name} rồi!',ephemeral=True)  
            return
        text=f"Bạn đã bỏ phiếu cho {Name} ở <#{interaction.channel.id}>."
        for i in userss[str(server)]:
            if str(user) in userss[str(server)][i]:
                del userss[str(server)][i][str(user)]
                Name1=userss[str(server)][i]['Name']
                userss[str(server)][i]['T']-=1
                text=f"Bạn đã thay đổi phiếu bầu từ {Name1} sang {Name} ở <#{interaction.channel.id}>."
        userss[str(server)]['answer5'][str(user)]={}
        userss[str(server)]['answer5']['T']+=1
        with open('jsonfile/vote.json','w') as expp:
            json.dump(userss, expp,indent=4)

        image=pic.votepic(str(server))
        embed = discord.Embed(title=self.title,description=self.description, color=discord.Colour.random())
        file = discord.File(image, filename="vote.png")
        embed.set_image(url="attachment://vote.png")
        await interaction.response.edit_message(embed=embed,attachments=[file],view=self)
        await interaction.user.send(text,delete_after=15,)
    @discord.ui.button( style=discord.ButtonStyle.red,label="Kết Thúc!")# Create a button with the label "😎 Click me!" with color Blurple
    async def end(self, ctx: discord.Interaction, button: discord.ui.Button):
        rolelist=['Admin']
        if any(role.name in rolelist  for role  in ctx.user.roles):
            view = Confirm()
            await ctx.response.send_message('Bạn có chắc là Kết thúc cuộc bình chọn này không?', view=view,ephemeral=True) 
            await view.wait()
            if view.value is None:
                await ctx.user.send('Hết thời gian! Tiếp tục cuộc bình chọn!')
            elif view.value:
                await ctx.user.send('Chấp nhận kết thúc cuộc bình chọn!')
                server= ctx.guild_id
                image=pic.votepic(str(server))
                embed = discord.Embed(title=self.title,description=self.description, color=discord.Colour.random())
                file = discord.File(image, filename="vote.png")
                embed.set_image(url="attachment://vote.png")
                await ctx.followup.send(f'@everyone, Admin {ctx.user.mention} đã kết thúc cuộc bỏ phiếu!\nSau đây là kết quả cuộc bỏ phiếu:',embed=embed,file=file,view=self)
                a=await ctx.channel.fetch_message(ctx.message.id)
                await a.delete()
                self.stop()
            else:
                await ctx.user.send('Hủy kết thúc cuộc bình chọn!')
            
        else:
            await ctx.response.send_message("Bạn không có quyền thực hiện lênh này!") 
    @discord.ui.button( style=discord.ButtonStyle.red,label="Hủy!")# Create a button with the label "😎 Click me!" with color Blurple
    async def Cancel(self, ctx: discord.Interaction, button: discord.ui.Button):
        rolelist=['Admin']
        if any(role.name in rolelist  for role  in ctx.user.roles):
            view = Confirm()
            await ctx.response.send_message('Bạn có chắc là xóa cuộc bình chọn này không?', view=view,ephemeral=True) 
            await view.wait()
            if view.value is None:
                await ctx.user.send('Hết thời gian! Tiếp tục cuộc bình chọn!')
            elif view.value:
                await ctx.user.send('Chấp nhận xóa cuộc bình chọn!')
                a=await ctx.channel.fetch_message(ctx.message.id)
                await a.delete()
                self.stop()
            else:
                await ctx.user.send('Hủy xóa cuộc bình chọn!')
        else:
            await ctx.response.send_message("Bạn không có quyền thực hiện lênh này!")
class vote(commands.Cog):
    def __init__(self, client):
        self.client = client
    @app_commands.command()
    async def vote(self, ctx: discord.Interaction,
                   title:str,
                   answer1:str,answer2:str,
                   answer3:str=None,answer4:str=None,answer5:str=None,description:str=None,):
        rolelist=['Admin']
        if any(role.name in rolelist  for role  in ctx.user.roles):
            await ctx.response.defer()
            with open('jsonfile/vote.json', 'r') as f:
                userss = json.load(f)
            server = ctx.guild.id
            userss[str(server)] = {}
            userss[str(server)]['answer1']={}
            userss[str(server)]['answer1']['T']=0
            userss[str(server)]['answer1']['Name']=answer1
            userss[str(server)]['answer2']={}
            userss[str(server)]['answer2']['T']=0
            userss[str(server)]['answer2']['Name']=answer2
            userss[str(server)]['answer3']={}
            userss[str(server)]['answer3']['T']=0
            userss[str(server)]['answer3']['Name']=answer3
            userss[str(server)]['answer4']={}
            userss[str(server)]['answer4']['T']=0
            userss[str(server)]['answer4']['Name']=answer4
            userss[str(server)]['answer5']={}
            userss[str(server)]['answer5']['T']=0
            userss[str(server)]['answer5']['Name']=answer5
            with open('jsonfile/vote.json','w') as expp:
                json.dump(userss, expp,indent=4)
            image=pic.votepic(str(server))
            embed = discord.Embed(title=title,description=description, color=discord.Colour.random())
            file = discord.File(image, filename="vote.png")
            embed.set_image(url="attachment://vote.png")
            four=discord.ui.Button(style=discord.ButtonStyle.link,
                               url="https://www.youtube.com/channel/UCFINNqRcNcOAemuyKdBiDpA?sub_confirmation=1",
                               label="Four Gaming Studio")
            
            await ctx.followup.send(f'@everyone, Admin {ctx.user.mention} đã Bắt đầu cuộc bỏ phiếu!',embed=embed,file=file,view=MyView(server,title,description).add_item(four))
        else:
            await ctx.response.send_message("Bạn không có quyền thực hiện lênh này!")  
async def setup(bot):
    await bot.add_cog(vote(bot))