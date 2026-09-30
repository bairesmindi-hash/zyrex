import os
import discord
from discord.ext import commands
from discord import app_commands

# Configuración de intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class ZyrexBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincroniza los comandos de barra con Discord para que aparezcan al escribir "/"
        await self.tree.sync()
        print("¡Comandos de barra (Slash Commands) sincronizados correctamente!")

bot = ZyrexBot()

@bot.event
async def on_ready():
    print(f"¡Bot conectado como {bot.user}!")
    bot.add_view(VerificacionView())
    bot.add_view(TicketsView())
    print("¡Vistas persistentes cargadas correctamente!")



class VerificacionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verificarme", style=discord.ButtonStyle.green, emoji="✅", custom_id="verificacion_btn")
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        # Buscamos el rol directamente por su nombre exacto
        rol = discord.utils.get(interaction.guild.roles, name="| unknown")

        if not rol:
            await interaction.followup.send("❌ Error: No encuentro el rol por su nombre. Revisá que esté bien escrito en el código.", ephemeral=True)
            return

        if rol in interaction.user.roles:
            await interaction.followup.send("⚠️ ¡Ya estás verificado en Zyrex!", ephemeral=True)
        else:
            await interaction.user.add_roles(rol)
            await interaction.followup.send("🎉 ¡Te has verificado correctamente en Zyrex!", ephemeral=True)

# --- COMANDO DE BARRA ÚNICO ---
@bot.tree.command(name="verificacion", description="Envía el panel de verificación de Zyrex")
async def verificacion(interaction: discord.Interaction):
    mensaje = (
        "✨ **Z Y R E X • V E R I F I C A C I Ó N** ✨\n"
        "--------------------------------------------------\n\n"
        "👏 ¡Bienvenido/a a la comunidad! Para tener acceso completo a todos los canales y desbloquear la experiencia, por favor completa tu acceso.\n\n"
        "📌 *Haz clic en el botón de abajo para verificar tu cuenta al instante.*"
    )
    await interaction.response.send_message(mensaje, view=VerificacionView()) 


# --- VISTA PARA EL CENTRO DE ATENCIÓN / TICKETS ---
class TicketsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Compra", style=discord.ButtonStyle.success, emoji="🛒", custom_id="persistent_view:compra")
    async def boton_compra(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

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
        await ticket_channel.send(
            f"¡Hola {member.mention}! {mencion_staff}\n"
            f"🛒 Has abierto un ticket de **Compra**. Un vendedor te atenderá pronto."
        )
        await interaction.followup.send(f"✅ ¡Tu ticket ha sido creado! Dirígete a {ticket_channel.mention}", ephemeral=True)

    @discord.ui.button(label="Soporte", style=discord.ButtonStyle.primary, emoji="🛠️", custom_id="persistent_view:soporte")
    async def boton_soporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

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


    
  

# Comando de barra para enviar el panel de Tickets: /soporte
@bot.tree.command(name="soporte", description="Envía el centro de atención y tickets de Zyrex (Solo administradores)")
@app_commands.checks.has_permissions(administrator=True)
async def soporte(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Zyrex • Centro de atención",
        description="¿Cómo podemos ayudarte?\nSelecciona la opción que mejor describe tu consulta. Nuestro equipo te atenderá lo antes posible.",
        color=discord.Color.dark_embed()
    )
    embed.add_field(name="🛒 Compras", value="Productos, pagos y pedidos.", inline=True)
    embed.add_field(name="🛠️ Soporte", value="Ayuda con productos o servicios.", inline=True)
    embed.add_field(name="💻 HWID Reset", value="Solicita el restablecimiento de HWID.", inline=True)
    
    await interaction.response.send_message("Panel de soporte creado con éxito.", ephemeral=True)
    await interaction.channel.send(embed=embed, view=TicketsView())

class TerminosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Español", style=discord.ButtonStyle.primary, emoji="🇪🇸")
    async def espanol_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Has seleccionado el idioma **Español**. ¡Gracias por leer los términos y condiciones de Zyrex!", 
            ephemeral=True
        )

    @discord.ui.button(label="English", style=discord.ButtonStyle.secondary, emoji="🇺🇸")
    async def english_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "You have selected **English**. Thank you for reading Zyrex's terms and conditions!", 
            ephemeral=True
        )
class TerminosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Español", style=discord.ButtonStyle.primary, emoji="🇪🇸")
    async def espanol_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🇪🇸 **Términos y Condiciones (Español)**\n"
            "Nuestros Términos y Condiciones establecen tus responsabilidades y derechos como miembro de **Zyrex Store**. "
            "Al participar en esta comunidad, aceptás respetar las normas establecidas para garantizar un entorno seguro y confiable para todos los usuarios.", 
            ephemeral=True
        )

    @discord.ui.button(label="English", style=discord.ButtonStyle.secondary, emoji="🇺🇸")
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






LOG_CHANNEL_ID = 1554704852272291900  

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

    # Cambio de Apodo
    if before.nick != after.nick:
        embed = discord.Embed(
            title="✏️ Apodo Cambiado",
            description=f"A **{after.mention}** se le cambió el apodo.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Antes", value=str(before.nick), inline=True)
        embed.add_field(name="Después", value=str(after.nick), inline=True)
        await channel.send(embed=embed)

    # Roles
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


# ==========================================
# SISTEMA DE LOGS - BLOQUE 2: MENSAJES
# ==========================================

# 1. Mensaje Eliminado
@bot.event
async def on_message_delete(message):
    # Ignorar mensajes de bots para no saturar el canal de logs
    if message.author.bot:
        return

    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="🗑️ Mensaje Eliminado",
            description=f"**Canal:** {message.channel.mention}\n**Autor:** {message.author.mention}",
            color=discord.Color.orange()
        )
        # Si el mensaje tenía texto, lo mostramos
        if message.content:
            # Cortamos el texto si es muy largo para que no rompa el embed
            content = message.content[:1024]
            embed.add_field(name="Contenido", value=content, inline=False)
            
        embed.set_footer(text=f"ID de Usuario: {message.author.id}")
        await channel.send(embed=embed)

# 2. Mensaje Editado
@bot.event
async def on_message_edit(before, after):
    # Ignorar bots y mensajes cuyo contenido no haya cambiado (ej: embeds que cargan tarde)
    if before.author.bot or before.content == after.content:
        return

    channel = bot.get_channel(1554704852272291900)
    if channel:
        embed = discord.Embed(
            title="✏️ Mensaje Editado",
            description=f"**Canal:** {before.channel.mention}\n**Autor:** {before.author.mention} [Ir al mensaje]({after.jump_url})",
            color=discord.Color.gold()
        )
        
        # Limitar la longitud por si el mensaje es muy largo
        old_content = before.content[:1024] if before.content else "*Sin texto (posible embed o imagen)*"
        new_content = after.content[:1024] if after.content else "*Sin texto (posible embed o imagen)*"

        embed.add_field(name="Antes", value=old_content, inline=False)
        embed.add_field(name="Después", value=new_content, inline=False)
        embed.set_footer(text=f"ID de Usuario: {before.author.id}")
        
        await channel.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)