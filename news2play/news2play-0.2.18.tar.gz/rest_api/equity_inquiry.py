from xml.etree import ElementTree
import requests
import csv

webUrl = 'https://fastquote.fidelity.com/service/quote/full?productid=iphone&app=AppleTV&quotetype=D&symbols='


def get_quote_text(company, symbol):
    stock_response = requests.get(webUrl + symbol)

    try:
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

            summary = f'{company} {up_down} {changed_percent} percent or {net_changed} dollars to {ask_price} dollars, ' \
                f'closed at {pre_close} dollars at last transaction day, ' \
                f'open at {open_price} today, ' \
                f'highest at {day_high} lowest at {day_low}, ' \
                f'with {volume} shares traded, {rating} market.'

            #print(summary)
            # example: Apple down 0.21 percent to 201.13 dollars, closed at 201.55 dollars at last transcation day, open at 203.17 today, highest at 204.49 lowest at 200.65, down for 3.63 dollars, with 1942 shares traded, it is Bullish equity.
            return summary
        else:
            return f"The equity {company} you try to inquirey dosn't exist, please try again."
    except Exception:
        return f"The equity {company} you try to inquirey dosn't exist, please try again."

def get_company_symbol(company):
    company_symbol = None
    with open('s&p_500_companies.csv', mode='r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if company in row[1]:
                company_symbol = row[0]
                break
            elif company in row[0]:
                 company_symbol = row[0]

    return company_symbol


def main():
    company_name = 'IBM'
    company_symbol = get_company_symbol(company_name)
    if (company_symbol == None):
        print('The equity ' + company_name + " you try to inquiry doesn't exist, please try again.")
    else:
        print(company_symbol)
        market_summary = get_quote_text(company_name, company_symbol)
        print(market_summary)


if __name__ == '__main__':
    main()
