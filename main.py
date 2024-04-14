import platform, json

import aiohttp, logging
import asyncio, datetime

''' Logging'''
logger = logging.getLogger('simple')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

file_logger = logging.FileHandler('app.log')
file_logger.setLevel(logging.WARNING)
file_logger.setFormatter(formatter)

logger.addHandler(file_logger)


async def choose_date():
    while True:
        days = int(input("Enter date: "))
        try:
            if days<=10:
                date_period = []
                for i in range(days):
                    period =  datetime.datetime.today()- datetime.timedelta(i)
                    date = datetime.datetime.strftime(period, '%d.%m.%Y')
                    date_period.append(date)
                print(date_period)
                return date_period
            else:
                print('It\'s too long period to find')
        except Exception as e:
            print(f'\nIt\'s a something wrong: {e}\n')
async def rate_input():
    rate = str(input("Enter some rate: \n")).upper()
    return rate

async def formatted_json(result=dict, rate = 'USD'):
    try:
        with open('info.json', 'r+') as f:
            info = json.load(f)
    
        for k, z in result.items():
                if 'date' in k:
                    date_key = z
                if "exchangeRate" in k:
                    list_info:list = z
                    # print(list_info) # значенння-список по ключу "exchangeRate"
                    for dic in list_info:
                        # print(dic) # перший словник
                        for i, v in dic.items(): #ітерація по словнику
                            # print(i) # перший ключ
                            if 'currency' in i and v == rate:
                                info[date_key] = {}
                                order = await ordering(dic)
                                if rate in info[date_key]:
                                    info[date_key][rate] = order
                                else: 
                                    info[date_key]={rate : order}
                                with open('info.json', 'w+') as f:
                                    json.dump(info, f, indent=2)
                                return f
                            elif v == rate:
                                info[date_key] = {}
                                order = await ordering(dic)
                                if rate in info[date_key]:
                                    info[date_key][rate] = order
                                else: 
                                    info[date_key]={rate : order}
                                with open('info.json', 'w+') as f:
                                    json.dump(info, f, indent=2)
                                return f
    except KeyError:
        logger.warning('Simple key error// or not?')
    except KeyboardInterrupt:
        logger.warning('I can\'t wait to go out')
    except Exception as e:
        logger.warning(f'I don\'t excpexted this problem: {e}')
        
                        
async def ordering(dic:dict):
# формат виводу курсу валют
    order = {}
    for i, v in dic.items():
            order['sale'] = dic['saleRate']
            order['purshase'] = dic['purchaseRate']
    return order                                

async def main(d,rate):
    async with aiohttp.ClientSession() as session:
        params = {
            'date' : f'{d}'
        }
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates', params = params) as response:
            try:
                if response.status == 200:
                    print("Status:\n", response.status)
                    print("Content-type:", response.headers['content-type'])
                    result = await response.json()
                    fine = await formatted_json(result, rate)
                    return fine
                else:
                    print("Status:", response.status)
                    print('Error connection')
            except ConnectionError:
                logger.error('Connection error was expected')
            except Exception as e:
                logger.error(f'The error is {e}')


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    date =  asyncio.run(choose_date())
    rate = asyncio.run(rate_input() )

    if date==1:
        r = asyncio.run(main(date, rate))
    else:
        for da in date:
            r = asyncio.run(main(da, rate))
        with open('info.json') as f:
                print(f.read())
        