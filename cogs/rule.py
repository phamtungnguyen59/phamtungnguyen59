
from discord.ext import commands
from discord import app_commands
import discord,json
class rule(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ruleevn={
    1: "1. Không toxic, bắt nạt người khác.",
    2: "2. Không spam, làm phiền người khác.",
    3: "3. Không NSFW, nội dung phản cảm, bạo lực.",
    4: "4. Sử dụng các kênh, lệnh đúng cách.",
    5: "5. Không tương tác với người người phá luật, thay vào đó hãy báo cáo họ.",
    6: "6. Không nói về các vấn đề chính trị, tôn giáo, phân biệt chủng tộc, phân biệt giới tính.",
    7: "7. Không mention(đề cập) các vai trò một cách bừa bãi.",
    8: "8. Không quảng cáo, spam link nếu chưa có sự cho phép của admin"
}
      
    @app_commands.command()
    @app_commands.describe(number='Số Thứ Tự Luật')
    async def rulevn(self, ctx: discord.Interaction,number:int=0):
        """Hiển Thị Luật Lệ"""
        em= discord.Embed(title="Luật Lệ",description="", color=discord.Colour.random())
        if number !=0:
            em.add_field(name=self.ruleevn[number],value="",inline=False)
        if number==0:
            for i in self.ruleevn:
                em.add_field(name=self.ruleevn[i],value="",inline=False)
        em.add_field(name="Các hành vi phá hoại, không tuân thủ luật tùy mức độ thì sẽ bị xử phạt chính đáng.",value="",inline=False)
        em.set_footer(text="-  -  -  Đội NGũ ADMIN XIN CHÂN THÀNH CẢM ƠN  -  -  -")
        em.set_thumbnail(url=ctx.guild.icon)
        em.set_author(icon_url=ctx.user.avatar.url,name=f"{ctx.user.name} | {ctx.guild.name}")
        await ctx.response.send_message(embed=em)
async def setup(bot):
    await bot.add_cog(rule(bot))
