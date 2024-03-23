from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import cv2
import pytesseract
import os
from PIL import Image

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your image text removal bot. Send me an image with text, and I'll try to remove it for you.")

def text_handler(update, context):
    # Get the text message
    text = update.message.text

    # Handle the text message here
    context.bot.send_message(chat_id=update.effective_chat.id, text="I can only process images. Please send an image with text.")

def ocr(image_path, lang='eng'):
    # Open the image using PIL (Python Imaging Library)
    with Image.open(image_path) as img:
        # Perform OCR using pytesseract and specify the language
        text = pytesseract.image_to_string(img, lang=lang)

    return text

def image_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Received an image. Processing...")
    
    # Get the photo object from the update
    photo = update.message.photo[-1].get_file()

    # Download the photo
    photo_path = 'image.jpg'
    photo.download(photo_path)

    # Perform OCR on the image (default language is English)
    text = ocr(photo_path)

    # Add your message and link
    message = f"Detected Text: {text}\n\nContact Muhammad Sleem for assistance: https://mostaql.com/u/abdelrahman_am/portfolio"

    # Send the message with the extracted text and link back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True)

    # Cleanup: Delete the downloaded photo
    os.remove(photo_path)

def main():
    # Create an Updater for your bot
    updater = Updater("7090360842:AAFMZ9c1FkEsqwgiluCDEi3KjUthDyIuGj0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define your handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
