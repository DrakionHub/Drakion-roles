import discord
from discord.ext import commands
from discord.ui import View, Button
import os

TOKEN = os.getenv("TOKEN_CARGOS") 

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs dos cargos fornecidos
ROLES_CONFIG = {
    "script": 1483435965669310566,
    "giveaway": 1483436471452172360,
    "drop": 1483436850176725153,
    "blox_news": 1483437342923423876
}

class CargoButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction: discord.Interaction, role_id: int):
        role = interaction.guild.get_role(role_id)
        if not role:
            return await interaction.response.send_message("Erro: Cargo não encontrado.", ephemeral=True)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"❌ Você removeu: **{role.name}**", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Você recebeu: **{role.name}**", ephemeral=True)

    # Todos os estilos alterados para 'danger' (vermelho)
    # Labels ajustados com espaços para tentar equalizar o tamanho visual
    
    @discord.ui.button(label="Script Updates  ", style=discord.ButtonStyle.danger, custom_id="btn_script")
    async def script_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role(interaction, ROLES_CONFIG["script"])

    @discord.ui.button(label="Giveaway        ", style=discord.ButtonStyle.danger, custom_id="btn_giveaway")
    async def giveaway_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role(interaction, ROLES_CONFIG["giveaway"])

    @discord.ui.button(label="Drop            ", style=discord.ButtonStyle.danger, custom_id="btn_drop")
    async def drop_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role(interaction, ROLES_CONFIG["drop"])

    @discord.ui.button(label="Blox Fruits News", style=discord.ButtonStyle.danger, custom_id="btn_blox")
    async def blox_button(self, interaction: discord.Interaction, button: Button):
        await self.toggle_role(interaction, ROLES_CONFIG["blox_news"])

@bot.tree.command(name="setup_cargos", description="Envia o painel de cargos vermelhos")
async def setup_cargos(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Sem permissão.", ephemeral=True)

    embed = discord.Embed(
        title="🐉 Drakion | Auto-Cargos",
        description="Escolha as notificações que deseja receber clicando nos botões abaixo.",
        color=0xff0000 # Cor da barra lateral da embed também em vermelho
    )
    
    await interaction.channel.send(embed=embed, view=CargoButtons())
    await interaction.response.send_message("Painel enviado!", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(CargoButtons())
    await bot.tree.sync()
    print(f"Bot de Cargos Vermelhos Online!")

bot.run(TOKEN)
