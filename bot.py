from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
import os

async def start(self):
    await super().start()
    me = await self.get_me()
    self.mention = me.mention
    self.username = me.username  
    self.uptime = Config.BOT_UPTIME     

    # Verifica se o suporte à web está ativado
    if Config.WEB_SUPPORT:
        app = web.AppRunner(web.Application(client_max_size=30000000))
        await app.setup()
        
        # Use a variável de ambiente PORT definida pelo Heroku
        port = os.environ.get('PORT', 8080)  # Fallback para 8080 se PORT não estiver definida
        await web.TCPSite(app, "0.0.0.0", port).start()

    print(f"\033[1;96m @{me.username} Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️\033[0m")

    # Envia mensagem para os administradores
    try:
        for admin_id in Config.ADMIN:
            await self.send_message(admin_id, f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
    except Exception as e:
        print(f"Erro ao enviar mensagem para os administradores: {e}")

    # Envia mensagem de log, se o canal de log estiver configurado
    if Config.LOG_CHANNEL:
        try:
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            message = (f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n"
                       f"📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n"
                       f"🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n"
                       f"🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")
            await self.send_message(Config.LOG_CHANNEL, message)
        except Exception as e:
            print(f"Erro ao enviar mensagem para o canal de log: {e}")
            print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")


Bot().run()
