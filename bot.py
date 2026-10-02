import os
import threading
import discord
from discord.ext import commands
from discord import app_commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()  

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Configuración de intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class ZyrexBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("¡Comandos de barra sincronizados correctamente!")

bot = ZyrexBot()

@bot.event
async def on_ready():
    print(f"¡Bot conectado como {bot.user}!")
    bot.add_view(VerificacionView())
    bot.add_view(TiendaView())
    bot.add_view(TerminosView())
    bot.add_view(PagosView())
    print("¡Vistas persistentes cargadas correctamente!")

# ==========================================
# 1. VERIFICACIÓN
# ==========================================
class VerificacionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verificarme", style=discord.ButtonStyle.green, emoji="✅", custom_id="verif_zyrex_v4")
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        rol = discord.utils.get(interaction.guild.roles, name="| unknown")

        if not rol:
            await interaction.followup.send("❌ Error: No encuentro el rol por su nombre en el servidor.", ephemeral=True)
            return

        if rol in interaction.user.roles:
            await interaction.followup.send("⚠️ ¡Ya estás verificado en Zyrex!", ephemeral=True)
        else:
            await interaction.user.add_roles(rol)
            await interaction.followup.send("🎉 ¡Te has verificado correctamente en Zyrex!", ephemeral=True)

@bot.tree.command(name="verificacion", description="Envía el panel de verificación de Zyrex")
async def verificacion(interaction: discord.Interaction):
    mensaje = (
        "✨ **Z Y R E X • V E R I F I C A C I Ó N** ✨\n"
        "--------------------------------------------------\n\n"
        "👏 ¡Bienvenido/a a la comunidad! Para tener acceso completo a todos los canales, completa tu acceso.\n\n"
        "📌 *Haz clic en el botón de abajo para verificar tu cuenta al instante.*"
    )
    await interaction.response.send_message(mensaje, view=VerificacionView()) 


# ==========================================
# 2. SISTEMA DE PAGOS (MERCADO PAGO)
# ==========================================
class CheckoutView(discord.ui.View):
    def __init__(self, link_pago: str):
        super().__init__(timeout=900)
        self.add_item(discord.ui.Button(label="Abrir Mercado Pago", url=link_pago, emoji="💳"))
        
        btn_verificar = discord.ui.Button(label="Ya pagué, verificar", style=discord.ButtonStyle.success, emoji="✅", custom_id="pago_ok_v4")
        btn_verificar.callback = self.verificar_callback
        self.add_item(btn_verificar)

    async def verificar_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "⏳ **Verificando pago...** En breve te dirán si el pago se hizo con éxito.", 
            ephemeral=True
        )

class PagosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Plan Básico ($15)", style=discord.ButtonStyle.success, emoji="💳", custom_id="plan_basico_v4")
    async def boton_basico(self, interaction: discord.Interaction, button: discord.ui.Button):
        link = "https://mpago.la/1mJDEKY"
        embed = discord.Embed(
            title="💳 Pagá con Mercado Pago",
            description="Hacé clic en **Abrir Mercado Pago** para completar tu pago de manera segura.\n\n*En breve te dirán si el pago se hizo con éxito.*",
            color=0x009EE3
        )
        embed.add_field(name="📦 Producto", value="Plan Básico × 1", inline=False)
        embed.add_field(name="💵 Total", value="$ 600,00 UYU", inline=False)
        embed.add_field(name="⏳ Estado", value="🟡 Esperando tu pago...", inline=False)
        
        view = CheckoutView(link)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Plan Personalizado ($35)", style=discord.ButtonStyle.primary, emoji="⚡", custom_id="plan_pers_v4")
    async def boton_personalizado(self, interaction: discord.Interaction, button: discord.ui.Button):
        link = "https://mpago.la/13E75Ct"
        embed = discord.Embed(
            title="💳 Pagá con Mercado Pago",
            description="Hacé clic en **Abrir Mercado Pago** para completar tu pago de manera segura.\n\n*En breve te dirán si el pago se hizo con éxito.*",
            color=0x009EE3
        )
        embed.add_field(name="📦 Producto", value="Plan Personalizado × 1", inline=False)
        embed.add_field(name="💵 Total", value="$ 1.400,00 UYU", inline=False)
        embed.add_field(name="⏳ Estado", value="🟡 Esperando tu pago...", inline=False)
        
        view = CheckoutView(link)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Full Custom ($50)", style=discord.ButtonStyle.danger, emoji="👑", custom_id="plan_full_v4")
    async def boton_full(self, interaction: discord.Interaction, button: discord.ui.Button):
        link = "https://mpago.la/1uPnuaK"
        embed = discord.Embed(
            title="💳 Pagá con Mercado Pago",
            description="Hacé clic en **Abrir Mercado Pago** para completar tu pago de manera segura.\n\n*En breve te dirán si el pago se hizo con éxito.*",
            color=0x009EE3
        )
        embed.add_field(name="📦 Producto", value="Full Custom × 1", inline=False)
        embed.add_field(name="💵 Total", value="$ 2.000,00 UYU", inline=False)
        embed.add_field(name="⏳ Estado", value="🟡 Esperando tu pago...", inline=False)
        
        view = CheckoutView(link)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# ==========================================
# 3. CENTRO DE ATENCIÓN (3 BOTONES: TICKET, SOPORTE, COMPRA)
# ==========================================
class TiendaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 1. BOTÓN TICKET GENERAL
    @discord.ui.button(label="Ticket", style=discord.ButtonStyle.secondary, emoji="🎫", custom_id="btn_ticket_v4")
    async def boton_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        member = interaction.user
        rol_staff = guild.get_role(1554703303223287899)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        if rol_staff:
            overwrites[rol_staff] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        ticket_channel = await guild.create_text_channel(
            name=f"🎫-ticket-{member.name}",
            overwrites=overwrites,
            topic=f"Ticket general de {member.name}"
        )

        mencion_staff = rol_staff.mention if rol_staff else "@Staff"
        await ticket_channel.send(
            f"¡Hola {member.mention}! {mencion_staff}\n"
            f"🎫 Has abierto un **Ticket** general. ¿En qué podemos ayudarte?"
        )
        await interaction.followup.send(f"✅ ¡Tu ticket ha sido creado! Dirígete a {ticket_channel.mention}", ephemeral=True)

    # 2. BOTÓN SOPORTE
    @discord.ui.button(label="Soporte", style=discord.ButtonStyle.primary, emoji="🛠️", custom_id="btn_soporte_v4")
    async def boton_soporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        member = interaction.user
        rol_staff = guild.get_role(1554703303223287899)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        if rol_staff:
            overwrites[rol_staff] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        ticket_channel = await guild.create_text_channel(
            name=f"🛠️-soporte-{member.name}",
            overwrites=overwrites,
            topic=f"Ticket de soporte de {member.name}"
        )

        mencion_staff = rol_staff.mention if rol_staff else "@Staff"
        await ticket_channel.send(
            f"¡Hola {member.mention}! {mencion_staff}\n"
            f"🛠️ Has abierto un ticket de **Soporte**. Cuéntanos cuál es tu problema detalladamente."
        )
        await interaction.followup.send(f"✅ ¡Tu ticket ha sido creado! Dirígete a {ticket_channel.mention}", ephemeral=True)

    # 3. BOTÓN COMPRA (ABRE CANAL Y MANDA EL PANEL DE PAGOS ADENTRO)
    @discord.ui.button(label="Compra", style=discord.ButtonStyle.success, emoji="🛒", custom_id="btn_compra_v4")
    async def boton_compra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        member = interaction.user
        rol_staff = guild.get_role(1554703303223287899)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
        }

        if rol_staff:
            overwrites[rol_staff] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        ticket_channel = await guild.create_text_channel(
            name=f"🛒-compra-{member.name}",
            overwrites=overwrites,
            topic=f"Ticket de compra de {member.name}"
        )

        mencion_staff = rol_staff.mention if rol_staff else "@Staff"
        
        embed_compra = discord.Embed(
            title="💳 Zyrex Store • Panel de Compra",
            description=(
                "Selecciona el plan que deseas adquirir haciendo clic en su botón correspondiente abajo para pagar con **Mercado Pago**.\n\n"
                "🔹 **Plan Básico ($15)** — $600 UYU\n"
                "🔹 **Plan Personalizado ($35)** — $1.400 UYU\n"
                "🔹 **Full Custom ($50)** — $2.000 UYU"
            ),
            color=discord.Color.from_rgb(0, 158, 227)
        )
        embed_compra.set_footer(text="Zyrex Store | Pagos Seguros con Mercado Pago")

        await ticket_channel.send(
            f"¡Hola {member.mention}! {mencion_staff}\n"
            f"🛒 Has abierto un ticket de **Compra**. Elegí tu plan para pagar:",
            embed=embed_compra,
            view=PagosView()
        )
        await interaction.followup.send(f"✅ ¡Tu ticket de compra ha sido creado! Dirígete a {ticket_channel.mention}", ephemeral=True)

@bot.tree.command(name="tienda", description="Envía el panel principal de atención y tienda de Zyrex")
@app_commands.checks.has_permissions(administrator=True)
async def tienda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Zyrex • Centro de atención y Tienda",
        description="¿Cómo podemos ayudarte?\nSelecciona la opción que prefieras para abrir tu ticket al instante con nuestro equipo.",
        color=discord.Color.dark_embed()
    )
    embed.add_field(name="🎫 Ticket", value="Consultas generales.", inline=True)
    embed.add_field(name="🛠 Soporte", value="Ayuda técnica o de servicios.", inline=True)
    embed.add_field(name="🛒 Compra", value="Ver planes y realizar pagos.", inline=True)
    
    await interaction.response.send_message(embed=embed, view=TiendaView())


# ==========================================
# 4. TÉRMINOS Y CONDICIONES
# ==========================================
class TerminosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Español", style=discord.ButtonStyle.primary, emoji="🇪🇸", custom_id="term_es_v4")
    async def espanol_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🇪🇸 **Términos y Condiciones (Español)**\n"
            "Nuestros Términos y Condiciones establecen tus responsabilidades y derechos como miembro de **Zyrex Store**. "
            "Al participar en esta comunidad, aceptás respetar las normas establecidas para garantizar un entorno seguro y confiable para todos los usuarios.", 
            ephemeral=True
        )

    @discord.ui.button(label="English", style=discord.ButtonStyle.secondary, emoji="🇺🇸", custom_id="term_en_v4")
    async def english_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🇺🇸 **Terms and Conditions (English)**\n"
            "Our Terms and Conditions set out your responsibilities and rights as a member of **Zyrex Store**. "
            "By participating in this community, you agree to follow the established rules to ensure a safe and trustworthy environment for all users.", 
            ephemeral=True
        )

@bot.tree.command(name="terminos", description="Muestra el panel de Términos y Condiciones de Zyrex")
@app_commands.checks.has_permissions(administrator=True)
async def terminos(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Términos y Condiciones — Zyrex Store",
        description=(
            "🇪🇸 **Español**\n"
            "Nuestros Términos y Condiciones establecen tus responsabilidades y derechos como miembro de **Zyrex Store**. "
            "Al participar en esta comunidad, aceptás respetar las normas establecidas para garantizar un entorno seguro y confiable para todos los usuarios.\n\n"
            "🇺🇸 **English**\n"
            "Our Terms and Conditions set out your responsibilities and rights as a member of **Zyrex Store**. "
            "By participating in this community, you agree to follow the established rules to ensure a safe and trustworthy environment for all users."
        ),
        color=discord.Color.from_rgb(40, 40, 40)
    )
    if bot.user.avatar:
        embed.set_thumbnail(url=bot.user.avatar.url)
        
    embed.set_footer(text="Zyrex Store | Términos y Condiciones")
    
    view = TerminosView()
    await interaction.response.send_message(embed=embed, view=view)


# ==========================================
# 5. SISTEMA DE LOGS
# ==========================================
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="📥 Miembro Unido",
            description=f"{member.mention} (`{member.name}`) ha entrado al servidor.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="📤 Miembro Salió",
            description=f"**{member.name}** ha abandonado el servidor.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    channel = bot.get_channel(1554704852272291900)
    if not channel:
        return

    if before.nick != after.nick:
        embed = discord.Embed(
            title="✏️ Apodo Cambiado",
            description=f"A **{after.mention}** se le cambió el apodo.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Antes", value=str(before.nick), inline=True)
        embed.add_field(name="Después", value=str(after.nick), inline=True)
        await channel.send(embed=embed)

    if before.roles != after.roles:
        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]
        
        if added_roles:
            roles_str = ", ".join([role.mention for role in added_roles])
            embed = discord.Embed(
                title="🟢 Rol Asignado",
                description=f"A **{after.mention}** se le dio el rol: {roles_str}",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)
            
        if removed_roles:
            roles_str = ", ".join([role.mention for role in removed_roles])
            embed = discord.Embed(
                title="🔴 Rol Removido",
                description=f"A **{after.mention}** se le quitó el rol: {roles_str}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="🔨 Miembro Baneado",
            description=f"**{user.name}** ha sido baneado del servidor.",
            color=discord.Color.dark_red()
        )
        await channel.send(embed=embed)

@bot.event
async def on_member_unban(guild, user):
    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="🔓 Miembro Desbaneado",
            description=f"**{user.name}** ha sido desbaneado.",
            color=discord.Color.teal()
        )
        await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="🗑 Mensaje Eliminado",
            description=f"**Canal:** {message.channel.mention}\n**Autor:** {message.author.mention}",
            color=discord.Color.orange()
        )
        if message.content:
            content = message.content[:1024]
            embed.add_field(name="Contenido", value=content, inline=False)
            
        embed.set_footer(text=f"ID de Usuario: {message.author.id}")
        await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content:
        return

    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="✏️️ Mensaje Editado",
            description=f"**Canal:** {before.channel.mention}\n**Autor:** {before.author.mention} [Ir al mensaje]({after.jump_url})",
            color=discord.Color.gold()
        )
        
        old_content = before.content[:1024] if before.content else "*Sin texto*"
        new_content = after.content[:1024] if after.content else "*Sin texto*"

        embed.add_field(name="Antes", value=old_content, inline=False)
        embed.add_field(name="Después", value=new_content, inline=False)
        embed.set_footer(text=f"ID de Usuario: {before.author.id}")
        
        await channel.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)