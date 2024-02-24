import discord,json,math,re,requests,yt_dlp,datetime,time
from pytube import *
from discord.ext import commands,tasks
from discord import app_commands
from asyncio import run_coroutine_threadsafe
from numerize import numerize
from fakemodule import ytb
from discord import SyncWebhook
yt_dlp.utils.bug_reports_message = lambda: ''
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
        if self.count_numepage[server]==self.maxpage-1:
            self.go2.disabled =True
            self.go.disabled =True
            self.go.style=discord.ButtonStyle.grey
            self.go2.style=discord.ButtonStyle.grey

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
        await ctx.response.send_message('Đã Hủy',delete_after=3)
        await ctx.message.delete()
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



class music(commands.Cog):
    def __init__(self,bot):
        self.bot =bot
        self.votesk={}
        self.is_playing = {}
        self.is_paused={}
        self.music_queue={}
        self.queueIndex ={}
        self.vieww=discord.ui.View()
        self.ytdl_format_options ={ 'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'logtostderr': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto'}
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)
        self.vc = {}
    def parse_duration(self,duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} Ngày'.format(days))
        if hours > 0:
            duration.append('{} Giờ'.format(hours))
        if minutes > 0:
            duration.append('{} Phút'.format(minutes))
        if seconds > 0:
            duration.append('{} Giây'.format(seconds))

        return ' '.join(duration)
    def time_public(self,time):
        pip= datetime.datetime.strptime(time, "%d:%m:%Y")  
        a = datetime.datetime.now()
        c = a - pip
        d, h, m = c.days, c.seconds // 3600, c.seconds // 60 % 60
        if m==0:
            pu=('{} Giây Trước'.format(c))
        if h==0:
            pu=('{} Phút Trước'.format(m))
        if d==0:
            pu=('{} Giờ Trước'.format(h))
        if d>=1:
            pu=('{} Ngày Trước'.format(d))
            if d%7==0:
                t=d//7
                pu=('{} Tuần Trước'.format(t))
        if d>=30:
            w=d//30
            if w>=12:
                y=w//12
                pu=('{} Năm Trước'.format(y))
            else:
                pu=('{} Tháng Trước'.format(w))
        return(pu)
    # @tasks.loop(seconds=1)
    # async def checkforvideos(self):
    #     with open("jsonfile/youtubedata.json", "r") as f:
    #         data=json.load(f)
    #     for youtube_channel in data:
    #         channel = f"https://www.youtube.com/channel/{youtube_channel}"
    #         html = requests.get(channel+"/videos").text
    #         latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    #         if str(data[youtube_channel]["latest_video_url"]) != latest_video_url:
    #             data[str(youtube_channel)]['latest_video_url'] = latest_video_url
    #             with open("jsonfile/youtubedata.json", "w") as f:
    #                 json.dump(data, f,indent=4)
    #             song = self.search_link(latest_video_url)
    #             embed = self.creat_embed(song,"add",discord.utils.get(self.bot.get_all_members(), id=664052500571226112))
    #             SyncWebhook.send(embed=embed)
    def search_link(self,search):
        inf = self.ytdl.extract_info(search, download=False)
        return inf
    def creat_embed(self,data,why,user):
        uploader = data.get('uploader')
        uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        upload_date = self.time_public(date[6:8] + ':' + date[4:6] + ':' + date[0:4])
        title = data.get('title')
        thumbnail = data.get('thumbnail')
        duration = self.parse_duration(int(data.get('duration')))
        view_count = data.get('view_count')
        like_count = data.get('like_count')
        sup_count = data.get('channel_follower_count')
        webpage_url = data.get('webpage_url')
        avatar = user.avatar.url
        embed = discord.Embed(color=discord.Colour.random())
        if why == "add":
            embed.title="Thêm vào danh sách phát:"
        elif why == "remove":
            embed.title="Đã xóa bài hát:"
        elif why == "now":
            embed.title="Đang chơi:"
        elif why == "loop":
            embed.title="Lặp bài hát:"
        else:
            embed.title= why
        embed.description=f"[{title}]({webpage_url})"
        embed.add_field(name="Kênh Youtube",value=f"[{uploader}]({uploader_url})",inline=True)
        embed.add_field(name="Lượt Đăng Ký",value=numerize.numerize(int(sup_count)),inline=True)
        embed.add_field(name="Ngày Xuất Bản",value=upload_date,inline=True)
        embed.add_field(name="Thời Lượng",value=duration,inline=True)
        embed.add_field(name="Lượt Xem",value=numerize.numerize(int(view_count)),inline=True)
        if like_count !=None:
            embed.add_field(name="Lượt Like",value=numerize.numerize(int(like_count)),inline=True)
        embed.set_image(url=thumbnail)
        embed.set_footer(text=f'Bài hát được thêm bởi: {str(user.name)}', icon_url=avatar)
        return embed
    def clearlist(self,ctx):
        id =int(ctx.guild.id)
        self.music_queue[id]=[]
    def messem(self,ctx,why):
        if why == "pnotvoice":
            why = "Bạn Cần phải ở trong phong voice mới được thực hiện lệnh này!"
        if why == "notlist":
            why = "Cần ít nhất một bài hát trong hàng chờ mới sử dụng được lệnh này!"
        if why == "bnotvoice":
            why = "Bot không ở trong phòng voice!"
        embed = discord.Embed(title=why,description='', color=discord.Colour.random())
        embed.set_footer(text=f'Người sử dụng lệnh: {str(ctx.user)}', icon_url=ctx.user.avatar.url)
        return embed
    @commands.Cog.listener()
    async def on_ready(self):
        print("setup")
        await self.bot.tree.sync()

        for guild in self.bot.guilds:
            id =int(guild.id)
            self.music_queue[id]=[]
            self.vc[id]=None
            self.votesk[id]=[]
            self.is_paused[id]=False
            self.is_playing[id]=False
        print("done")
        # self.checkforvideos.start()
    async def on_voice_state_update(self, member, before, after):
        id = int(member.guild.id)

        if member.id != self.bot.user.id and before.channel != None and after.channel != before.channel:
            remainingChannelMembers = before.channel.members
            if len(remainingChannelMembers) == 1 and remainingChannelMembers[0].id == self.bot.user.id:
                await self.vc[id].disconnect()
                self.is_playing[id] = False
                self.is_paused[id] = False
                self.vc[id].stop()
                self.vc[id]=None
                await before.channel.send("im out")
                self.clearlist(member)
                return
        #if member.id != self.bot.user.id and before.channel == None and after.channel != before.channel:
        #    remainingChannelMembers = after.channel.members
        #    if len(remainingChannelMembers) >= 1 :
        #        if self.vc[id]==None:
        #            self.vc[id]=await after.channel.connect()
        #            return
    async def join_vc(self,ctx,channel):
        id = int(ctx.guild.id)
        if id in self.bot.voice_clients:
            self.vc[id]=discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            return 
        elif self.vc[id]==None: 
            self.vc[id]=await channel.connect()
            if self.vc[id]==None:
                await ctx.send("Không thể kết nối tới voice")
                return
        else:
            await self.vc[id].move_to(channel)
            
    def play_next(self, ctx):
        channel = self.bot.get_channel(ctx.channel_id)
        id = int(ctx.guild.id)
        self.music_queue[id].pop(0)
        if self.music_queue[id] !=[] and len(self.music_queue[id]) != 0:
            song = self.music_queue[id][0][0]
            ctxx = self.music_queue[id][0][1]
            message = self.creat_embed(song,"now",ctxx)
            coro = ctx.followup.send(embed=message)
            fut = run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except:
                pass
            self.is_playing[id] = True
            self.is_paused[id] = False
            self.vc[id].play(discord.FFmpegPCMAudio(song['url'],before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), after=lambda e: self.play_next(ctx))
        else:
            self.is_playing[id] = False
            self.vc[id].stop()
            em= discord.Embed(title="Tất cả bài hát trong danh sách đã được phát hết",description="",color=discord.Colour.random())
            coro =  channel.send(embed=em)
            fut = run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except:
                pass
    async def play_music(self,ctx,channel):
        id = int(ctx.guild.id)
        self.is_playing[id] = True
        self.is_paused[id] = False
        if self.vc[id]==None or not self.vc[id].is_connected():
            await self.join_vc(ctx, channel)
        song = self.music_queue[id][0][0]
        ctxx = self.music_queue[id][0][1]
        message = self.creat_embed(song,"now",ctxx)
        await ctx.followup.send(embed=message)
        self.vc[id].play(discord.FFmpegPCMAudio(song['url'],before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), after=lambda r: self.play_next(ctx))
    @app_commands.command(name="play")
    @app_commands.describe(url="Chơi nhạc trên youtube hoặc spotyfi!")
    async def play(self,  ctx: discord.Interaction,*,url:str) -> None:
        """Chơi nhạc trên youtube hoặc spotyfi!"""
        search = "".join(url)
        await ctx.response.defer()
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.followup.send(embed=self.messem(ctx,"pnotvoice"))
            return
        
        userChannel = ctx.user.voice.channel

        if "/playlist/" in search or '/album/' in search:
            if "/playlist/" in search:
                idl=ytb.getidspo(search)
                a=ytb.playlist(idl)
            if '/album/' in search:
                idl=ytb.getidspo(search)
                a=ytb.ambum(idl)
            for i in a:
                b = ytb.songbyid(i)
                search=f"{b['name']} lyrics - {b['artists']}"
                song = self.search_link(search)
                self.music_queue[id].append([song,ctx.user])
                if self.is_playing[id] == False:
                    await self.play_music(ctx,userChannel)
                else:
                    message = self.creat_embed(song,"add",ctx.user)
                    await ctx.followup.send(embed=message)
                   
            return
                
        elif "list=" in search :
            playlist = self.search_link(ytb.get_playlist_id(search))
            if playlist ==None:
                await ctx.followup.send(embed=self.messem(ctx,"Danh sách phát không tồn tại hoặc đăng ở chế độ riêng tư."))
                return
            if "entries" not in playlist:
                await ctx.followup.send(embed=self.messem(ctx,"Bot không thể phát nhạc từ danh kết hợp của youtube."))
                return
            
            for song in playlist['entries']:
                self.music_queue[id].append([song,ctx.user])
                if self.is_playing[id] == False:
                    await self.play_music(ctx,userChannel)
                else:
                    message = self.creat_embed(song,"add",ctx.user)
                    await ctx.followup.send(embed=message)
            return
        
        elif "/track/" in search:
            idl=ytb.getidspo(search)
            a = ytb.songbyid(idl)
            search=f"{a['name']} - {a['artists']}"
        song = self.search_link(search)
        if any(c in search for c in ('https://', 'http://')):
            pass
        else:
            song = (self.search_link(search))['entries'][0]
        self.music_queue[id].append([song,ctx.user])
        if self.is_playing[id] == False:
            await self.play_music(ctx,userChannel)
        else:
            message = self.creat_embed(song,"add",ctx.user)
            await ctx.followup.send(embed=message)

    @app_commands.command(name="join")
    async def join(self, ctx: discord.Interaction) -> None:
        """Tham Gia Kênh Voice"""
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.response.send_message(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            userChannel = ctx.user.voice.channel
            await self.join_vc(ctx, userChannel)
            await ctx.response.send_message(embed=self.messem(ctx,f'Bot đã tham gia phòng voice {userChannel}'))

    @app_commands.command(name="leave")
    async def leave(self, ctx: discord.Interaction) -> None:
        """Rời Phòng Voice"""
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.response.send_message(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.response.send_message(embed=self.messem(ctx,"bnotvoice"))
            return
        id = int(ctx.guild.id)
        self.is_playing[id] = False
        self.is_paused[id] = False
        self.clearlist(ctx)
        if self.vc[id] != None:
            await ctx.response.send_message("Bot đã rời phòng voice")
            await self.vc[id].disconnect()
            self.vc[id] = None
    @app_commands.command(name="clear")
    async def clear(self, ctx: discord.Interaction) -> None:
        """Xóa Tất Cả Bài Hát Có Trong Danh Sách"""
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.response.send_message(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.music_queue[id] != []:
            self.clearlist(ctx)
            self.is_playing[id] = False
            self.is_paused[id] = False
            self.vc[id].stop()
            await ctx.response.send_message(embed=self.messem(ctx,"Tất cả bài hát có trong danh sách đã được xóa."))
    @app_commands.command(name="skip")
    async def skip(self, ctx: discord.Interaction) -> None:
        """Bỏ Qua Bài Hát Đang Phát"""
        await ctx.response.defer()
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.followup.send(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.followup.send(embed=self.messem(ctx,"bnotvoice"))
            return
        if len(self.music_queue[id]) -1 <=0:
            await ctx.followup.send(embed=self.messem(ctx,"notlist"))
            return
        voter = ctx.user.id
        votesk=self.votesk[id]
        voice=self.vc[id]
        total=len(votesk)
        rolelist=['Admin']
        if any(role in ctx.user.roles for role  in rolelist) or voter==664052500571226112:
            votesk.clear()
            self.vc[id].pause()
            self.vc[id].stop()
            song = self.music_queue[id][0][0]
            ctxx = self.music_queue[id][0][1]
            message = self.creat_embed(song,"Đã bỏ qua bài hát với quyền admin:",ctxx)
            await ctx.followup.send(embed=message)
            return
        max=len(voice.channel.members)-1
        if total >= max//2:
            votesk.clear()
            self.vc[id].pause()
            self.vc[id].stop()
            song = self.music_queue[id][0][0]
            ctxx = self.music_queue[id][0][1]
            message = self.creat_embed(song,"Đã bỏ qua bài hát:",ctxx)
            await ctx.followup.send(embed=message)
            return
        elif voter not in votesk:
            votesk.append(voter)
            voice=self.vc[id]
            total=len(votesk)
            max=len(voice.channel.members)-1

            if total >= max//2:
                votesk.clear()
                self.vc[id].pause()
                self.vc[id].stop()
                song = self.music_queue[id][0][0]
                ctxx = self.music_queue[id][0][1]
                message = self.creat_embed(song,"Đã bỏ qua bài hát:",ctxx)
                await ctx.followup.send(embed=message)
                return
            else:
                await ctx.followup.send(embed=self.messem(ctx,'Số Phiếu Đã Được Cập Nhật **{}/{}**'.format(total,max//2)))
                return

        else:
            await ctx.followup.send(embed=self.messem(ctx,'Bạn Đã Bỏ Phiếu rồi.'))
            return
            

    @app_commands.command(name="remove")
    async def remove(self, ctx: discord.Interaction, number: int) -> None:
        """Xóa Bài Hát Trong Danh Sách Hàng Đợi"""
        await ctx.response.defer()
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.followup.send(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.followup.send(embed=self.messem(ctx,"bnotvoice"))
            return
        if len(self.music_queue[id]) -1 <=0:
            await ctx.followup.send(embed=self.messem(ctx,"notlist"))
            return
        
        if number ==None:
            await ctx.followup.send(embed=self.messem(ctx,"Thiếu số thứ tự bài hát trong hàng chờ!"))
            return
        
        if self.music_queue[id] != []:
            song = self.music_queue[id].pop(number)
            ctxx = self.music_queue[id][0][1]
            message = self.creat_embed(song[0],"remove",ctxx)
            await ctx.followup.send(embed=message)

        if self.music_queue[id] == []:
            # clear queue and stop playing
            if self.vc[id] != None and self.is_playing[id]:
                self.is_playing[id] = False
                self.is_paused[id] = False
                self.vc[id].stop()

    @app_commands.command(name="pause")
    async def pause(self, ctx: discord.Interaction) -> None:
        """Dừng Phát Bài Hát Đang Phát"""
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.response.send_message(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.response.send_message(embed=self.messem(ctx,"bnotvoice"))
            return
        if self.is_playing[id]:
            await ctx.response.send_message(embed=self.messem(ctx,"Tạm dừng phát nhạc!"))
            self.is_playing[id] = False
            self.is_paused[id] = True
            self.vc[id].pause()
            
    @app_commands.command(name="resume",)
    async def resume(self, ctx: discord.Interaction) -> None:
        """Phát Bài Hát Đang Dừng"""
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.response.send_message(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.response.send_message(embed=self.messem(ctx,"bnotvoice"))
            return
        if self.is_paused[id]:
            await ctx.response.send_message(embed=self.messem(ctx,"Tiếp tục phát nhạc!"))
            self.is_playing[id] = True
            self.is_paused[id] = False
            self.vc[id].resume()
    @app_commands.command(name="volume")
    async def volume(self, ctx: discord.Interaction, volume: int)-> None:
        """Thay Đổi Âm Lượng"""
        id = int(ctx.guild.id)
        if ctx.user.voice == None:
            await ctx.response.send_message(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.response.send_message(embed=self.messem(ctx,"bnotvoice"))
            return
        ctx.voice_client.source.volume = volume // 100
        await ctx.send(f"Changed volume to {volume}%")


    @app_commands.command(name="now")
    async def now(self, ctx: discord.Interaction) -> None:
        """Hiển Thị Bài Hát Đang Phát Và Bài Hát Tiếp Theo"""
        id = int(ctx.guild.id)
        await ctx.response.defer()
        if ctx.user.voice == None:
            await ctx.followup.send(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.followup.send(embed=self.messem(ctx,"bnotvoice"))
            return
        if self.music_queue[id]==[]:
            await ctx.followup.send(embed=self.messem(ctx,"notlist"))
            return
        queue = discord.Embed(title="Bài hát hiện tại và kế tiếp!",description='',color=discord.Colour.random())
        queue.add_field(name="Đang phát:",value=f"[{self.music_queue[id][0][0]['title']}]({self.music_queue[id][0][0]['webpage_url']})",inline=False)
        if len(self.music_queue[id])>=2:
            queue.add_field(name="Kết tiếp:",value=f"[{self.music_queue[id][1][0]['title']}]({self.music_queue[id][1][0]['webpage_url']})",inline=False)
        await ctx.followup.send(embed=queue)

    @app_commands.command(name="list")
    async def list(self, ctx: discord.Interaction) -> None:
        """Hiển Thị Danh Sách Phát Bài Hát"""
        id = int(ctx.guild.id)
        await ctx.response.defer()
        if ctx.user.voice == None:
            await ctx.followup.send(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.followup.send(embed=self.messem(ctx,"bnotvoice"))
            return
        if self.music_queue[id]==[]:
            await ctx.followup.send(embed=self.messem(ctx,"notlist"))
            return
        server= ctx.guild_id
        id = int(ctx.guild.id)
        end=10
        firt=0
        index=0
        embeds=[]
        cc=len(self.music_queue[id])/end
        if cc==0:
            cc=1
        for i in range(math.ceil(cc)):
            aa=self.music_queue[id]
            song=aa[firt:end]
            firt=end
            end+=10
            embed=discord.Embed(title="Danh Sách 10 Bài Hát", color=discord.Colour.random())
            txt=""
            for abc in song:
                txt+= f"{index} | [{abc[0]['title']}]({abc[0]['webpage_url']})\n"
                index+=1
            embed.description=txt
            embeds.append(embed)
        await ctx.followup.send(embed=embeds[0].set_footer(text="Trang: 0"), view=MyView(embeds,server))

    @app_commands.command(name='loop')
    async def loop(self, ctx: discord.Interaction) -> None:
        """Lặp Bài Hát Đang Phát."""
        id = int(ctx.guild.id)
        await ctx.response.defer()
        if ctx.user.voice == None:
            await ctx.followup.send(embed=self.messem(ctx,"pnotvoice"))
            return
        if self.vc[id] == None:
            await ctx.followup.send(embed=self.messem(ctx,"bnotvoice"))
            return
        if self.music_queue[id]==[]:
            await ctx.followup.send(embed=self.messem(ctx,"notlist"))
            return
        
        song =self.music_queue[id][0]
        self.music_queue[id].insert(1,song)
        ctxx = self.music_queue[id][0][1]
        message = self.creat_embed(song[0],"loop",ctxx)
        await ctx.followup.send(embed=message)

    @app_commands.command(name="postvideo")
    @app_commands.describe(video_url="Link Video Trên Youtube!")
    async def postvideo(self, ctx: discord.Interaction,*,video_url:str=None) -> None:
        """Hiển Thị Thông Tin Video"""
        rolelist=['Admin',"Youtuber"]
        if any(role.name in rolelist  for role  in ctx.user.roles):
            try:
                with open('data.json','r') as expp:
                    users = json.load(expp)
                id= users[str(ctx.guild.id)]
            except:
                return await ctx.response.send_message(embed=self.messem(ctx,"Bạn chưa đặt kênh đăng video để thực hiện lênh này!"))
            if video_url==None:
                return await ctx.response.send_message("url không được để trống!")
            if  video_url:
                song = self.search_link(video_url)
                embed = self.creat_embed(song,"add",ctx.user)
                a=discord.ui.View()
                channell=discord.ui.Button(style=discord.ButtonStyle.link,url=song['uploader_url'],label=song['uploader'])
                videol=discord.ui.Button(style=discord.ButtonStyle.link,url=song['uploader_url'],label="VIDEO")
                a.add_item(channell)
                a.add_item(videol)
                channel = self.bot.get_channel(id)
                try:
                    await channel.send(embed=embed,view=a)
                    await ctx.response.send_message(f"Đã đăng video lên kênh {channel.mention}")
                except:
                    await ctx.response.send_message(f"Bot không có quyền nhắn vào kênh {channel.mention}")
        else:
            await ctx.response.send_message(embed=self.messem(ctx,"Bạn không có quyền thực hiện lênh này!"))
    @app_commands.command(name="setpostchannel")
    @app_commands.describe(channel="Kênh Bạn Muốn Đặt Làm Nơi Đăng Video!")
    async def setpostchannel(self, ctx: discord.Interaction,channel:discord.TextChannel):
        """Đặt Làm Nơi Đăng Video!"""
        rolelist=['Admin',"Youtuber"]
        if any(role.name in rolelist  for role  in ctx.user.roles):
            with open('data.json','r') as expp:
                users = json.load(expp)
            users[str(ctx.guild.id)]=channel.id
            with open('data.json','w') as expp:
                json.dump(users, expp,indent=4)
            await ctx.response.send_message(f"Đã đặt kênh {channel.mention} làm kênh đăng video!")
        else:
            await ctx.response.send_message(embed=self.messem(ctx,"Bạn không có quyền thực hiện lênh này!"))
    # @app_commands.command(name="add_thong_bao_youtube")
    # @app_commands.describe(webhook="webhook url",channel_url="Link kênh youtube")
    # async def add_thong_bao_youtube(self, ctx: discord.Interaction,webhook:str, channel_url: str):
    #     """Thông báo tới Kênh discord khi có video mới!"""
    #     rolelist=['Admin',"Youtuber"]
    #     if any(role.name in rolelist  for role  in ctx.user.roles):
    #         with open("jsonfile/youtubedata.json", "r") as f:
    #             data = json.load(f)
    #         if '/@' in channel_url:
    #             r = requests.get(channel_url, allow_redirects=True)
    #             channel_id=(re.search(r'(?<=<link rel="canonical" href="https:\/\/www\.youtube\.com\/channel\/)(-?\w+)*(?=">)', r.text).group(0)) 
    #         else:
    #             youtube = ytb.youtube_authenticate()
    #             channel_id = ytb.get_channel_id_by_url(youtube, channel_url)
    #         data[str(channel_id)]={}
    #         data[str(channel_id)]["latest_video_url"]="none"
    #         data[str(channel_id)]["webhook"]=f"{webhook}"
    #         with open("jsonfile/youtubedata.json", "w") as f:
    #             json.dump(data, f,indent=4)
    #         await ctx.response.send_message(embed=self.messem(ctx,"Đã thêm!"))
    #     else:
    #         await ctx.response.send_message(embed=self.messem(ctx,"Bạn không có quyền thực hiện lênh này!"))
    # @app_commands.command(name="remove_thong_bao_youtube")
    # @app_commands.describe(channel_url="Link kênh youtube")
    # async def remove_thong_bao_youtube(self, ctx: discord.Interaction,channel_url: str):
    #     """Xóa Thông báo Youtube"""
    #     rolelist=['Admin',"Youtuber"]
    #     if any(role.name in rolelist  for role  in ctx.user.roles):
    #         with open("jsonfile/youtubedata.json", "r") as f:
    #             data = json.load(f)
    #         if '/@' in channel_url:
    #             r = requests.get(channel_url, allow_redirects=True)
    #             channel_id=(re.search(r'(?<=<link rel="canonical" href="https:\/\/www\.youtube\.com\/channel\/)(-?\w+)*(?=">)', r.text).group(0)) 
    #         else:
    #             youtube = ytb.youtube_authenticate()
    #             channel_id = ytb.get_channel_id_by_url(youtube, channel_url)
    #         data[str(channel_id)]={}
    #         del data[str(channel_id)]
    #         with open("jsonfile/youtubedata.json", "w") as f:
    #             json.dump(data, f,indent=4)
    #         await ctx.response.send_message(embed=self.messem(ctx,"Đã Xóa!"))
    #     else:
    #         await ctx.response.send_message(embed=self.messem(ctx,"Bạn không có quyền thực hiện lênh này!"))
    # @app_commands.command(name="list_thong_bao_youtube")
    # async def list_thong_bao_youtube(self, ctx: discord.Interaction):
    #     """Hiển thị danh sách các kênh thông báo youtube."""
    #     rolelist=['Admin',"Youtuber"]
    #     if any(role.name in rolelist  for role  in ctx.user.roles):
    #         with open("jsonfile/youtubedata.json", "r") as f:
    #             data = json.load(f)
    #         youtube = ytb.youtube_authenticate()
    #         e= discord.Embed(title="Danh sách thông báo youtube", color=discord.Colour.random(),description="")
    #         for i in data:
    #             response = ytb.get_channel_details(youtube, id=i)
    #             snippet = response["items"][0]["snippet"]
    #             channel_title = snippet["title"]
    #             channel_url=f"https://www.youtube.com/channel/{i}"
    #             e.description+=f'[{channel_title}]({channel_url})\n'
    #         await ctx.response.send_message(embed=e)
    #     else:
    #         await ctx.response.send_message(embed=self.messem(ctx,"Bạn không có quyền thực hiện lênh này!"))
async def setup(bot):
    await bot.add_cog(music(bot))
