import discum

# Replace 'your_token_here' with your actual account token
TOKEN = "your_token_here"

# Replace 'your_user_id_here' with your actual user ID
YOUR_USER_ID = "your_user_id_here"

# Function to read trigger sentences from a text file
def read_trigger_sentences(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file.readlines()]

# Load trigger sentences from the file
TRIGGER_SENTENCES = read_trigger_sentences('trigger_sentences.txt')

# Create a discum client
bot = discum.Client(token=TOKEN, log=False)

@bot.gateway.command
def on_message(resp):
    if resp.event.message:
        message = resp.parsed.auto()
        author_id = message['author']['id']
        channel_id = message['channel_id']
        guild_id = message.get('guild_id')  # None if DM, present if in a server

        # Check if the message is a DM and not from yourself
        if guild_id is None and author_id != YOUR_USER_ID:
            # Check if the message contains any of the trigger sentences
            message_content = message['content'].lower()
            if any(trigger in message_content for trigger in TRIGGER_SENTENCES):
                try:
                    # Send a warning message
                    bot.sendMessage(channel_id, f"<@{author_id}>, try faster next time, last word.")
                    # Attempt to block the user
                    bot.blockUser(author_id)
                    print(f"Blocked user: {author_id}")
                except Exception as e:
                    print(f"Failed to block user: {author_id}. Error: {e}")

bot.gateway.run(auto_reconnect=True)
