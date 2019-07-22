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
            previous_close = quote.find('PREVIOUS_CLOSE').text
            pre_close_price = quote.find('PREV_CLOSE_PRICE').text
            open_price = quote.find('OPEN_PRICE').text
            day_high = quote.find('DAY_HIGH').text
            day_low = quote.find('DAY_LOW').text
            net_changed = float(quote.find('NETCHG_TODAY').text)
            rating = quote.find('EQUITY_SUMMARY_RATING').text  # very bearish/bearish/neutral/bullish/very bullish
            # score = quote.find('EQUITY_SUMMARY_SCORE').text #0.1 ~ 1.0/1.1 ~ 3.0/3.1 ~ 7.0/7.1 ~ 9.0/9.1 ~ 10.0
            volume = quote.find('VOLUME').text  # total number of shares traded on one side of the transaction
            changed_percent = round(float(net_changed) / float(previous_close) * 100, 2)
            # Philly-Semis up 2.5% to start the week (unbeliveable)
            if changed_percent > 0:
                up_down = 'up'
            else:
                up_down = 'down'
                changed_percent = 0 - changed_percent
                net_changed = 0 - net_changed

            #summary = f'{company} {up_down} {changed_percent} percent or {net_changed} dollars to {ask_price} dollars, ' \
            #    f'closed at {pre_close} dollars at last transaction day, ' \
            #    f'open at {open_price} today, ' \
            #    f'highest at {day_high} lowest at {day_low}, ' \
            #    f'with {volume} shares traded, {rating} market.'

            summary = f'{company} closed at {previous_close} yesterday, open at {open_price} today, now {up_down} {net_changed} or' \
                f' {changed_percent} percent to {pre_close_price}, highest at {day_high}, lowest at {day_low}, with {volume} shares traded, {rating} market.' \

            #print(summary)
            # example: Apple down 0.21 percent to 201.13 dollars, closed at 201.55 dollars at last transcation day, open at 203.17 today, highest at 204.49 lowest at 200.65, down for 3.63 dollars, with 1942 shares traded, it is Bullish equity.
            return summary
        else:
            return f"Sorry, the stock {company} you try to inquirey dosn't exist, please try again."
    except Exception as e:
        print(e)
        return f"Sorry, the stock {company} you try to inquirey dosn't exist, please try again."

def get_company_symbol(company):
    company_symbol = ''
    company_name = ''
    with open('CompleteCompanyList.csv', mode='r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if company in row[1]:
                company_symbol = row[0]
                company_name = row[1]
                break
            elif company in row[0]:
                company_symbol = row[0]
                company_name = row[1]
                break

    return company_name, company_symbol


def main():
    company_name = 'Columbia Sportswear' # Facebook Apple IBM  Lockheed Boeing Alibaba
    company_name, company_symbol = get_company_symbol(company_name)
    if (company_symbol == ''):
        print('Sorry, the stock ' + company_name + " you try to inquiry doesn't exist, please try again.")
    else:
        print(company_symbol)
        market_summary = get_quote_text(company_name, company_symbol)
        print(market_summary)


if __name__ == '__main__':
    main()

#COLB Columbia Banking System, Inc. closed at 36.39 yesterday, open at 35.84 today, now up 0.27 or 0.74 percent to 36.39, highest at 36.45, lowest at 35.84, with 0 shares traded, Bearish market.
#CLBK Columbia Financial, Inc. closed at 15.35 yesterday, open at 15.29 today, now up 0.03 or 0.2 percent to 15.35, highest at 15.37, lowest at 15.25, with 0 shares traded, Very Bearish market.
#COLM Columbia Sportswear Company closed at 100.38 yesterday, open at 101.63 today, now down 1.39 or 1.38 percent to 100.38, highest at 101.88, lowest at 100.03, with 0 shares traded, Neutral market.
