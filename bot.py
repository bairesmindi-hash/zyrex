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



bot.run(os.getenv("DISCORD_TOKEN"))