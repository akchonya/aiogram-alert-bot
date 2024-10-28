from aiogram import F, Bot, Router, html
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
import aiohttp


async def fetch_terminal_state(terminal_id):
    url = f"https://ls.bilantek.com/api/terminalstate/{terminal_id}"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Connection": "keep-alive",
        "Origin": "https://lcapp.bilantek.com",
        "Referer": "https://lcapp.bilantek.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TenantCode": "lcapp_bilantek",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()  #

router = Router()


@router.message(Command("laundry"))
async def laundry_handler(message: Message):
    first = await fetch_terminal_state(743)
    second = await fetch_terminal_state(744)
    
    def format_wm_info(wm_data):
        wm_info = []
        for wm in wm_data['WMs']:
            number_display = "сушарка" if wm['Number'] == 8 else wm['Number']
            
            if wm['IsActive'] is False and wm['ProgramState'] is not None:
                left_symbol = wm['ProgramState']['LeftSymbol']
                right_symbol = wm['ProgramState']['RightSymbol']
                if left_symbol == "2" and right_symbol == "H":
                    wm_info.append(f"🔴 {html.bold(number_display)}: тимчасово не працює")
                else:
                    wm_info.append(f"🟢 {html.bold(number_display)}: вільна")
            elif wm['ProgramState'] is None or (wm['ProgramState']['LeftSymbol'] in ["", "\u0000"] and wm['ProgramState']['RightSymbol'] in ["", "\u0000"]):
                wm_info.append(f"🟢 {html.bold(number_display)}: вільна")
            else:
                left_symbol = wm['ProgramState']['LeftSymbol']
                right_symbol = wm['ProgramState']['RightSymbol']
                if left_symbol == "2" and right_symbol == "H":
                    wm_info.append(f"⌛ {html.bold(number_display)}: більше 2 годин")
                else:
                    wm_info.append(
                        f"⌛ {html.bold(number_display)}: {left_symbol}{right_symbol} хв."
                    )
        return "\n".join(wm_info)
    
    first_info = format_wm_info(first)
    second_info = format_wm_info(second)
    
    await message.answer(f"🧺 {html.bold('пралки:')}\n\n{html.link(html.bold('коридор:'), 'https://lcapp.bilantek.com/?tcn=743')}\n{first_info}\n\n{html.link(html.bold('умивальники:'), 'https://lcapp.bilantek.com/?tcn=744')}\n{second_info}\n\n👁‍🗨 {html.italic('автор ідеї:')} @clar1keth", disable_web_page_preview=True)
    
