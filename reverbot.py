import telebot
from PIL import Image
from io import BytesIO

# Initialize the bot
bot = telebot.TeleBot("6527203137:AAEXo71tynBBv9dI_IUaWwL0x9oYTXxMIB4")

@bot.message_handler(commands=['start'])
def handle_start(message):
    usage_message = ("Welcome to the Flip Bot!\n\n"
                     "You can use the /left command to flip images, stickers, or text. "
                     "Just reply to a text, image, or sticker message with /left to see the magic! "
                     "If you reply to an image or sticker, it will be flipped horizontally. "
                     "If you reply to a text message, the text will be reversed.")
    bot.reply_to(message, usage_message)

@bot.message_handler(commands=['left'])
def handle_flip(message):
    replied_to_message = message.reply_to_message
    if replied_to_message:
        if replied_to_message.photo:
            # Handle incoming photos
            file_id = replied_to_message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Load the image
            image = Image.open(BytesIO(downloaded_file))

            # Flip the image
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

            # Save the flipped image to a BytesIO object
            flipped_image_buffer = BytesIO()
            flipped_image.save(flipped_image_buffer, format='PNG')
            flipped_image_buffer.seek(0)

            # Send the flipped image
            bot.send_photo(message.chat.id, flipped_image_buffer)
        elif replied_to_message.sticker:
            # Handle incoming stickers
            file_id = replied_to_message.sticker.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Load the sticker image
            sticker_image = Image.open(BytesIO(downloaded_file))

            # Flip the sticker image
            flipped_sticker_image = sticker_image.transpose(Image.FLIP_LEFT_RIGHT)

            # Save the flipped sticker image to a BytesIO object
            flipped_sticker_buffer = BytesIO()
            flipped_sticker_image.save(flipped_sticker_buffer, format='PNG')
            flipped_sticker_buffer.seek(0)

            # Send the flipped sticker as a photo (stickers cannot be sent directly)
            bot.send_photo(message.chat.id, flipped_sticker_buffer)
        elif replied_to_message.text:
            # Handle incoming text messages
            flipped_text = replied_to_message.text[::-1]  # Reverse the text
            bot.reply_to(message, flipped_text)
    else:
        bot.reply_to(message, "Please reply to a text, image, or sticker message to flip.")

# Start the bot
bot.polling()
