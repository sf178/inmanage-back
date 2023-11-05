import asyncio

# from pypasser import reCaptchaV3
from pyppeteer import launch
from .parser import format_response
from pyvirtualdisplay import Display

# receipt_info = {
#     'fn': '7281440500914241', # 9960440301535337
#     'fd': '27803', # 91550
#     'fp': '4253735630', # 2287615490
#     'sum': '1998,00', # 2144,00
#     'n': '1',
#     't': '2023-10-25T20:44'
# }

# recaptcha_response = reCaptchaV3(
#         "https://www.google.com/recaptcha/api2/reload?k=6Le5J3UeAAAAAMzc-SgmYzXK8xXV0AtOcdDXOdL5"
#         )
# print(recaptcha_response)
async def main(receipt_info):
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    try:
        # browser = await launch(headless=False)
        browser = await launch(headless=False, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
        page = await browser.newPage()  # Открытие новой вкладки
        await page.goto('https://proverkacheka.ru/requisites-form')  # Переход на веб-страницу

        # Определение обработчиков запросов и ответов
        async def handle_request(req):
            print(f'Request: {req.url}')
            if 'api2/' in req.url:
                body = await req.text()
                print(f'Request body: {body}')

        async def handle_response(res):
            # print(f'Response: {res.url}')
            if 'api2/' in res.url:
                body = await res.text()
                print(f'Response body: {body}')
            if 'api/receipt' in res.url:  # Предполагая, что ответ, который вам нужен, имеет эту часть URL.
                body = await res.text()
                try:
                    parsed = format_response(body)
                    return parsed
                except Exception as e:
                    print(e)

        page.on('request', handle_request)
        page.on('response', lambda res: asyncio.ensure_future(handle_response(res)))

        # Заполнение и отправка формы
        await page.type('input[name=fn]', receipt_info['fn'])
        await page.type('input[name=fd]', receipt_info['fd'])
        await page.type('input[name=fp]', receipt_info['fp'])
        await page.type('input[name=total]', receipt_info['sum'])
        # datetime_value = receipt_info['t']
        datetime_selector = 'input[name=datetime]'

        try:
            # await page.type('input[name=datetime]', '25.10.202300T20:44')
            # await page.evaluate('''() => {
            #     const input = document.querySelector('input[name=datetime]');
            #     input.focus();
            #     input.value = datetime_value;
            #     input.blur();
            #     input.dispatchEvent(new Event('change', { bubbles: true }));
            # }''')
            # await page.focus('input[name=datetime]')

            date, time = receipt_info['t'].split('T')
            year, month, day = date.split('-')
            hour, minutes = time.split(':')
            # Ввод даты
            await page.type(datetime_selector, day)
            await asyncio.sleep(0.5)  # Добавьте задержку

            await page.type(datetime_selector , month)
            await asyncio.sleep(0.5)  # Добавьте задержку

            await page.type(datetime_selector, year)
            await page.focus('input[name=datetime]')

            # Имитация нажатия клавиши "ShiftRight" дважды
            await page.keyboard.press('ArrowRight')
            await asyncio.sleep(0.5)  # Добавьте задержку

            # await page.keyboard.press('ArrowRight')
            # await asyncio.sleep(0.5)  # Добавьте задержку

            # Ввод времени
            await page.type(datetime_selector, hour)
            await asyncio.sleep(0.5)
            await page.type(datetime_selector, minutes)

        except Exception as e:
            print(e)
        # await page.evaluate('''() => {
        #     const input = document.querySelector('input[name=datetime]');
        #     input.value = '2023-10-25T20:44';
        #     input.dispatchEvent(new Event('change', { bubbles: true }));
        # }''')
        # await asyncio.sleep(1)
        await page.type('input[name=type]', '1')

        # await page.click('#mui-component-select-type')

        # await page.waitForSelector('li[data-value="1"]')
        # await page.click('li[data-value="1"]')
        await page.click('button[type=submit]')

        # Ждите, пока не будет готов ответ от сервера (может потребоваться более сложная логика)
        await asyncio.sleep(1000)

        await browser.close()  # Закрытие браузера

    finally:
    # Остановите виртуальный дисплей в конце выполнения вашего кода
        display.stop()


