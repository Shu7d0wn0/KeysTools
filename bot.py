import discord
import requests
import logging

logging.basicConfig(level=logging.INFO)  # Configurer le journal de base

TOKEN = '(token discord)'  # Remplacez par le token de votre bot Discord
NGROK_URL = '(ngrok id)'
API_URL = f'{NGROK_URL}/generate_key'
LIST_KEYS_URL = f'{NGROK_URL}/list_keys'
DELETE_KEY_URL = f'{NGROK_URL}/delete_key'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    logging.info(f'Received message: {message.content}')  # Journaliser le message reçu

    # Commande pour générer une clé
    if message.content.startswith('!generate_key'):
        try:
            _, duration = message.content.split(maxsplit=1)
        except ValueError:
            duration = None

        logging.info(f'Generating key with duration: {duration}')  # Journaliser la durée de la clé

        response = requests.post(API_URL, json={'duration': duration})
        if response.status_code == 200:
            data = response.json()
            key = data.get('key')
            expiration_date = data.get('expiration_date')
            if expiration_date and expiration_date != "No expiration":
                await message.channel.send(f'Voici votre clé d\'accès pour SH7: {key} (valable jusqu\'au {expiration_date})')
            else:
                await message.channel.send(f'Voici votre clé d\'accès pour SH7: {key} (valable à vie)')
        else:
            await message.channel.send('Erreur lors de la génération de la clé.')

    # Commande pour voir toutes les clés
    elif message.content.startswith('!list_keys'):
        logging.info('Listing all keys')  # Journaliser la commande list_keys
        response = requests.get(LIST_KEYS_URL)
        if response.status_code == 200:
            keys = response.json().get('keys', [])
            if keys:
                keys_list = '\n'.join([f"Key: {key['key']} (Expires: {key['expiration_date']})" for key in keys])
                await message.channel.send(f'Voici toutes les clés d\'accès:\n{keys_list}')
            else:
                await message.channel.send('Aucune clé trouvée.')
        else:
            await message.channel.send('Erreur lors de la récupération des clés.')

    # Commande pour supprimer une clé
    elif message.content.startswith('!delete_key'):
        try:
            _, key_to_delete = message.content.split(maxsplit=1)
        except ValueError:
            await message.channel.send('Veuillez fournir la clé à supprimer.')
            return

        logging.info(f'Deleting key: {key_to_delete}')  # Journaliser la clé à supprimer

        response = requests.post(DELETE_KEY_URL, json={'key': key_to_delete})
        if response.status_code == 200:
            await message.channel.send(f'Clé {key_to_delete} supprimée.')
        else:
            await message.channel.send('Erreur lors de la suppression de la clé.')

client.run(TOKEN)
