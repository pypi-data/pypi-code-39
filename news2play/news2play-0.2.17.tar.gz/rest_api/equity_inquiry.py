from xml.etree import ElementTree

import requests

webUrl = 'https://fastquote.fidelity.com/service/quote/full?productid=iphone&app=AppleTV&quotetype=D&symbols='


def get_quote_text(company, symbol):
    stock_response = requests.get(webUrl + symbol)

    if stock_response.status_code == 200:
        quote_tree = ElementTree.fromstring(stock_response.content)
        quote = quote_tree[1][2]
        ask_price = quote.find('ASK_PRICE').text
        pre_close = quote.find('PREVIOUS_CLOSE').text
        open_price = quote.find('OPEN_PRICE').text
        day_high = quote.find('DAY_HIGH').text
        day_low = quote.find('DAY_LOW').text
        net_changed = quote.find('NETCHG_TODAY').text
        rating = quote.find('EQUITY_SUMMARY_RATING').text  # very bearish/bearish/neutral/bullish/very bullish
        # score = quote.find('EQUITY_SUMMARY_SCORE').text #0.1 ~ 1.0/1.1 ~ 3.0/3.1 ~ 7.0/7.1 ~ 9.0/9.1 ~ 10.0
        volume = quote.find('VOLUME').text  # total number of shares traded on one side of the transaction
        changed_percent = round((float(ask_price) - float(pre_close)) / float(pre_close) * 100, 2)
        # print (chged_percent)

        # Philly-Semis up 2.5% to start the week (unbeliveable)
        if changed_percent > 0:
            up_down = 'up'
        else:
            up_down = 'down'
            changed_percent = 0 - changed_percent

        # summary = company + ' ' + up_down + ' ' + str(changed_percent) + ' percent to ' + str(
        #     ask_price) + ' dollars, closed at '
        # summary += str(pre_close) + ' dollars at last transcation day, open at ' + str(
        #     open_price) + ' today, highest at '
        # summary += str(day_high) + ' lowest at ' + str(day_low) + ', ' + up_down + ' for ' + str(
        #     net_changed) + ' dollars, with '
        # summary += str(volume) + ' shares traded, it is ' + rating + ' equity.'

        summary = f'{company} {up_down} {changed_percent} percent to {ask_price} dollars, ' \
            f'closed at {pre_close} dollars at last transaction day, ' \
            f'open at {open_price} today, ' \
            f'highest at {day_high} lowest at {day_low}, ' \
            f'{up_down} for {net_changed} dollars, ' \
            f'with {volume} shares traded, it is {rating} equity.'

        print(summary)
        # example: Apple down 0.21 percent to 201.13 dollars, closed at 201.55 dollars at last transcation day, open at 203.17 today, highest at 204.49 lowest at 200.65, down for 3.63 dollars, with 1942 shares traded, it is Bullish equity.


def main():
    get_quote_text('Apple', 'AAPL')


if __name__ == '__main__':
    main()
