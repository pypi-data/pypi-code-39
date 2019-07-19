import asyncio
from pyppeteer import launch


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('file://C:/Users/Sean/OneDrive/Projects/ADA/north_c9/scripts/report.html')
    await page.pdf({'path': 'example.pdf'})
    #await page.screenshot({'path': 'example.pdf'})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
