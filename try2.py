import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import cv2
import pytesseract

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable GPU acceleration for Pytesseract (if available)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your image text removal bot. Send me an image with text, and I'll try to extract it for you.")

def text_handler(update, context):
    """Handle non-image messages and inform the user to send an image."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="I can only process images. Please send an image with text.")

def image_handler(update, context):
    """Extract text from the received image and send it back to the user."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Received an image. Processing...")

    # Get the photo object from the update
    photo = update.message.photo[-1].get_file()

    # Download the photo
    photo_path = 'image.jpg'
    try:
        photo.download(photo_path)
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error occurred while processing the image. Please try again.")
        return

    # Read the image using OpenCV
    image = cv2.imread(photo_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Tesseract for OCR
    try:
        text = pytesseract.image_to_string(gray)
    except Exception as e:
        logger.error(f"Error running OCR: {e}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error occurred while processing the image. Please try again.")
    else:
        # Send the extracted text back to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Detected Text: {text}")

    # Cleanup: Delete the downloaded photo
    os.remove(photo_path)

def main():
    """Start the bot."""
    # Create an Updater for your bot
    updater = Updater("7090360842:AAFMZ9c1FkEsqwgiluCDEi3KjUthDyIuGj0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define your handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()