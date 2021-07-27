from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import requests
import json
import aiohttp
import pathlib
import time
import database
import os
import youtube_dl


ostrich = Client("theostrich",
        bot_token=os.getenv("TOKEN"),
       api_id=os.getenv("API_ID"),
        api_hash=os.getenv("API_HASH"))

@ostrich.on_message(filters.command(["start"]))
async def start(client, message):
    try:
        await message.reply_text(
        text=f"**Hello {message.chat.first_name} 👋 !"
             "\n\nAre you feeling slow download speed? Don't worry. I can generate high-speed download links and store those files for you. "
             "\n\nCheck help to find out more about how to use me.**",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("HELP", callback_data="getHelp"),
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )
    except:
        await message.reply_text(
            text=f"**Hi 👋 !"
                 "\n\nAre you feeling slow download speed? Don't worry. I can generate high-speed download links and store those files for you."
                 "\n\nCheck help to find out more about how to use me.**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("HELP", callback_data="getHelp"),
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    database.scrape(message)

@ostrich.on_message(filters.command(["help"]))
async def assist(client, message):

    await message.reply_text(
        text=f"**Hi {message.chat.first_name}."
                 "\nHere is a detailed guide on using me."
                 "\n\nYou might have faced slow download speed while downloading telegram files."
                 "\n\nForward me any telegram file, and I will generate you a high-speed download link."
                 "\n\nFor further information and guidance, contact my developers at my support group.**",
                  disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/ostrichdiscussion"),
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )


@ostrich.on_message(filters.command(["utube"]))
async def utube(client, message):
    ydl = youtube_dl.YoutubeDL()
    try:
        url = message.command[1]
        try:
            result = ydl.extract_info(url, download=False)
            await message.reply_text(f"**Click this to download your file:**\n\n{result['url']}",reply_markup=InlineKeyboardMarkup([
                              [InlineKeyboardButton(text="OPEN IN BROWSER", url =f'{result["url"]}')]
                          ])
                          ,disable_web_page_preview=True, parse_mode=None)
        except:
            with youtube_dl.YoutubeDL(dict(forceurl=True)) as ydl:
                r = ydl.extract_info(url, download=False)
                media_url = r['formats'][-1]['url']
                print(media_url)
                await message.reply_text(f"Click this to download your file:\n\n{media_url}",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="OPEN IN BROWSER", url=f'{media_url}')]
                                   ])
                                   , disable_web_page_preview=True, parse_mode=None)
    except:
        await message.reply_text('**Provide me some URL to get direct link\n\nEg:**\n\t\t`/utube https://www.youtube.com/watch?v=h6fcK_fRYaI`')


@ostrich.on_message(filters.private & (filters.document | filters.video))
async def download(client, message):
    media = message
    filetype = media.document or media.video

    freelimit = 500000000
    filesize = filetype.file_size
    if filesize < freelimit:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="CONTINUE", callback_data="download")],
            [InlineKeyboardButton(text="CANCEL", callback_data="close")]
                    ])
        await message.reply_text("**Are you sure you want to continue?**", quote=True, reply_markup=keyboard)
    else:
        try:
            user = await client.get_chat_member('theostrich', message.chat.id)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(text="CONTINUE", callback_data="download")],
                [InlineKeyboardButton(text="CANCEL", callback_data="close")]
            ])
            await message.reply_text("**Are you sure you want to continue?**", quote=True, reply_markup=keyboard)
        except UserNotParticipant:
            await message.reply_text(
                text="**Due to limited resource, files greater than 500mb require channel membership.**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="Join theostrich", url=f"https://t.me/theostrich")]
              ])
            )


async def anonfiles(client, message):

      media = message.reply_to_message
      msg = await client.send_message(chat_id=message.chat.id, text='**Downloading your file to my server...**',reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton(text="Check Progress", callback_data="progress_msg")]
                                    ]))
      c_time = time.time()
      try:
        download_location = await client.download_media(message = media,progress=progress_func,
        progress_args=(
            "**Downloading your file to server...**",
            msg,
            c_time))
      except:
          msg.edit_text('Retrying Download, Please wait')
          download_location = await client.download_media(message=media)

      await msg.edit_text(text='Getting you a fast URL...')
      try:
        async with aiohttp.ClientSession() as session:
            files = {
                'file': open(download_location, 'rb')
            }
            request = await session.post("https://api.anonfiles.com/upload", data=files)
      except:
          msg.edit_text(text='Something went wrong. Contact my developers @theostrich')
      json_response = await request.json()
      download_url = json_response["data"]["file"]["url"]["full"]
      await msg.edit_text(text = f'**Click this to download your file:**\n\n{download_url}',
                          reply_markup=InlineKeyboardMarkup([
                              [InlineKeyboardButton(text="OPEN IN BROWSER", url =f'{download_url}')]
                          ])
                          ,disable_web_page_preview=True)

      os.remove(download_location)




@ostrich.on_message(filters.command(["about"]))
async def aboutTheBot(client, message):
    """Log Errors caused by Updates."""

    keyboard = [
        [
            InlineKeyboardButton("➰Channel",
                                          url="t.me/theostrich"),
            InlineKeyboardButton("👥Support Group", url="t.me/ostrichdiscussion"),
        ],
        [InlineKeyboardButton("🔖Add Me In Group", url="https://t.me/iconrailsBot?startgroup=new")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text("<b>Hello! I am Graken.</b>"
                              "\nI can generate high-speed download links."
                              "\n\n<b>About Me :</b>"
                              "\n\n  - <b>Name</b>        : Graken"
                              "\n\n  - <b>Creator</b>      : @theostrich"
                              "\n\n  - <b>Language</b>  : Python 3"
                              "\n\n  - <b>Library</b>       : <a href=\"https://docs.pyrogram.org/\">Pyrogram</a>"
                              "\n\nIf you enjoy using me and want to help me survive, contribute  my developers with the /donate command - my creator will be very grateful! It doesn't have to be much - every little would help us! Thanks for reading :)",
                             reply_markup=reply_markup, disable_web_page_preview=True)

@ostrich.on_message(filters.command(["donate"]))
async def donate(client, message):
    keyboard = [
        [
            InlineKeyboardButton("Contribute",
                                          url="https://github.com/theostrich"),
            InlineKeyboardButton("Paypal Us",url="https://paypal.me/donateostrich"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("Thank you for your wish to contribute. I hope you enjoyed using our services. Make a small donation/contribute to let this project alive." , reply_markup=reply_markup)

@ostrich.on_callback_query()
async def cb_handler(client, query):
    if query.data == "download":
        await query.answer()
        await query.message.delete()
        await anonfiles(client, query.message)
    elif query.data == "progress_msg":

        try:
            msg = "Progress Details...\n\nCompleted : {current}\nTotal Size : {total}\nSpeed : {speed}\nProgress : {progress:.2f}%\nETA: {eta}"
            await query.answer(
                msg.format(
                    **PRGRS[f"{query.message.chat.id}_{query.message.message_id}"]
                ),
                show_alert=True
            )

        except:
            await query.answer(
                "Processing your file...",
                show_alert=True
            )


    elif query.data == "close":
        await query.message.delete()
        await query.answer(
        "Process Cancelled..."
    )
    elif query.data == "getHelp":
        await query.answer()
        await query.message.edit_text(
            text=f"**Hi {query.message.chat.first_name}."
                 "\nHere is a detailed guide on using me."
                 "\n\nYou might have faced slow download speed while downloading telegram files."
                 "\n\nForward me any telegram file, and I will generate you a high-speed download link."
                 "\n\nFor further information and guidance, contact my developers at my support group.**",
                  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/ostrichdiscussion"),
                ]
            ]
        ),
        disable_web_page_preview=True
        )
        return


PRGRS = {}

async def progress_func(
        current,
        total,
        ud_type,
        message,
        start
):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        af = total / speed
        elapsed_time = round(af) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        eta =  TimeFormatter(milliseconds=time_to_completion)
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        PRGRS[f"{message.chat.id}_{message.message_id}"] = {
            "current": humanbytes(current),
            "total": humanbytes(total),
            "speed": humanbytes(speed),
            "progress": percentage,
            "eta": eta
        }


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

ostrich.run()
