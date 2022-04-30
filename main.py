import asyncio
import hashlib
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from telethon import functions, types, errors
from telethon.sync import TelegramClient
import config
import random
import json

token_now = requests.get('https://pastebin.com/raw/J7HtUwez').content
token = str(token_now).replace("b'", "").replace("'", "")

login = input('Введите токен: ')
if login == token:
    print('Вы авторизованы!\n\n')
    print('1. Поиск по номеру\n')
    print('2. Поиск по почте\n')
    print('3. Поиск по всем базам, любые данные')
    choice = input('Выберите: ')
    if choice == '1':
        def phone():
                phonse = input('Введите номер телефона: ')
                phonse = phonse.replace('+', '').replace('-', '').replace('(', '').replace(')',
                                                                                           '').replace(
                    ' ', '')
                phone = phonse[1:]

                SBnum = requests.get(f"https://fincalculator.ru/api/tel/{phonse}")
                datae = SBnum.json()
                # перенос номера -----------------------------
                urlMNP = f"https://xn----dtbofgvdd5ah.xn--p1ai/php/mnp.php?nomer={phonse}"
                mnpSiteSourc = requests.get(urlMNP).text.strip()
                mnp = mnpSiteSourc.replace('no',
                                           'Не переносился')  # Если ответ "no" то "Номер не переносился"
                # ОПРЕДЕЛЕНИЕ СТРАНЫ, РЕГИОНА И ОПЕРАТОРА ------------------------
                try:
                    countrys = datae["country"]
                    regions = datae["region"]
                    operators = datae["operator"]
                    if countrys != 'Россия':
                        fstep = f'📲 Номер телефона: {phonse}\n ├ Страна: {countrys}\n ├ Перенос номера: {mnp}\n └ Оператор: {regions}'
                    else:
                        fstep = f'📲 Номер телефона: {phonse}\n ├ Страна: {countrys}\n ├ Регион: {regions}\n ├ Перенос номера: {mnp}\n └ Оператор: {operators}'
                except:
                    countrys = 'Не опознано'
                    regions = 'Не опознано'
                    operators = 'Не опознано'

                SberURL = "https://securepayments.sberbank.ru/sbersafe/client/find?phone=" + phone

                headers = CaseInsensitiveDict()
                headers["Content-Length"] = "0"

                api_id = config.api_id
                api_hash = config.api_hash
                loop = asyncio.get_event_loop()

                respas = requests.post(SberURL, headers=headers).json()
                if 'error' not in respas:
                    sberrr = f'💳 Ответ на запрос по номеру от сбербанка: {respas}'
                else:
                    sberrr = ''

                try:
                    eqereq = phonse
                    email_login = (eqereq.split("@"))[0]
                    yandex = requests.get(f"https://yandex.ru/collections/api/users/{email_login}")
                    try:
                        yamail = phonse + '@yandex.ru'
                    except:
                        yamail = ''
                    yamailo = f', `{yamail}`'
                    yadata = yandex.json()
                    public_id = yadata['public_id']
                    display_name = yadata['display_name']
                    try:
                        yaname = f' ({display_name})'
                    except:
                        yaname = ''
                    try:
                        yandexx = f'\n㊗ Яндекс ID: {public_id}{yaname}'
                    except:
                        yandexx = f'\n㊗ Яндекс ID: {public_id}'
                except:
                    display_name = ''
                    public_id = ''
                    yandexx = ''
                    yamail = ''
                    yaname = display_name
                    if yandexx == '':
                        yamailo = ''

                # одноклассники
                session = requests.Session()
                session.get(
                    f'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong&st.email={phonse}')
                request = session.get(
                    f'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword')
                root_soup = BeautifulSoup(request.content, 'html.parser')
                soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
                if soup:
                    account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
                    masked_email = soup.find('button', {'data-l': 't,email'})
                    masked_phone = soup.find('button', {'data-l': 't,phone'})
                    if masked_phone:
                        masked_phone = masked_phone.find('div', {
                            'class': 'ext-registration_stub_small_header'}).get_text()
                    if masked_email:
                        masked_email = masked_email.find('div', {
                            'class': 'ext-registration_stub_small_header'}).get_text()
                        masked_email = f'Почта: `{masked_email}`,'
                    else:
                        masked_email = ''
                    if account_info:
                        masked_name = account_info.find('div',
                                                        {'class': 'ext-registration_username_header'})
                        if masked_name:
                            masked_name = masked_name.get_text()
                            account_info = account_info.findAll('div', {'class': 'lstp-t'})
                        if account_info:
                            profile_info = account_info[0].get_text()
                            profile_registred = account_info[1].get_text()
                        else:
                            profile_info = None
                            profile_registred = None
                    else:
                        pass
                try:
                    age = profile_info[:7].replace(',', '')
                    cityok = profile_info[8:].replace(',', '')
                    age = f''
                    cityok = f'{cityok}'
                    ok = f'\n🆗 Одноклассники: {masked_name} ({profile_info}, {masked_email} {profile_registred})'

                except:
                    ok = ''
                    cityok = ''
                    age = ''
                    masked_email = ''

                def address():
                    if regions == 'Москва и Московская область':
                        gorod = 'msk'
                    elif regions == 'Иркутская область':
                        gorod = 'irkutsk'
                    elif regions == 'Алтайский край':
                        gorod = 'barnaul'
                    elif regions == 'Пермский край':
                        gorod = 'ber'
                    elif regions == 'Брянская область':
                        gorod = 'bryansk'
                    elif regions == 'Волгоградская область':
                        gorod = 'volgograd'
                    elif regions == 'Воронежская область':
                        gorod = 'voronezh'
                    elif regions == 'Удмуртская республика':
                        gorod = 'votkinsk'
                    elif regions == 'Нижегородская область':
                        gorod = 'dzr'
                    elif regions == 'Ульяновская область':
                        gorod = 'ulsk'
                    elif regions == 'Воронежская область':
                        gorod = 'voronezh'
                    elif regions == 'Республика Марий Эл':
                        gorod = 'yola'
                    elif regions == 'Респубика Татарстан':
                        gorod = 'kazan'
                    elif regions == 'Кировская область':
                        gorod = 'kirov'
                    elif regions == 'Краснодарский край':
                        gorod = 'krd'
                    elif regions == 'Красноярский край':
                        gorod = 'krsk'
                    elif regions == 'Курганская область':
                        gorod = 'kurgan'
                    elif regions == 'Курская область':
                        gorod = 'kursk'
                    elif regions == 'Липецкая область':
                        gorod = 'lipetsk'
                    elif regions == 'Челябинская область':
                        gorod = 'chel'
                    elif regions == 'Тамбовская область':
                        gorod = 'mich'
                    elif regions == 'Новосибирская область':
                        gorod = 'nsk'
                    elif regions == 'Омская область':
                        gorod = 'omsk'
                    elif regions == 'Оренбургская область':
                        gorod = 'oren'
                    elif regions == 'Пензенская область':
                        gorod = 'penza'
                    elif regions == 'Ростовская область':
                        gorod = 'rostov'
                    elif regions == 'Рязанская область':
                        gorod = 'ryazan'
                    elif regions == 'Самарская область':
                        gorod = 'samara'
                    elif regions == 'Санкт-Петербург':
                        gorod = 'interzet'
                    elif regions == 'Саратовская область':
                        gorod = 'saratov'
                    elif regions == 'Воронежская область':
                        gorod = 'voronezh'
                    elif regions == 'Томская область':
                        gorod = 'tomsk'
                    elif regions == 'Тверская область':
                        gorod = 'tver'
                    elif regions == 'Тульская область':
                        gorod = 'tula'
                    elif regions == 'Тюменская область':
                        gorod = 'tmn'
                    elif regions == 'Республика Бурятия':
                        gorod = 'ulu'
                    elif regions == 'Республика Башкоторстан':
                        gorod = 'ufa'
                    elif regions == 'Республика Чувашия':
                        gorod = 'cheb'
                    elif regions == 'Ярославская область':
                        gorod = 'yar'
                    else:
                        gorod = "msk"
                    urldru = 'https://api-profile.domru.ru/v1/unauth/contract-asterisked?contact=' + phonse + '&amp;isActive=1'

                    headersd = CaseInsensitiveDict()
                    headersd["Host"] = "api-profile.domru.ru"
                    headersd["Domain"] = gorod

                    resp = requests.get(urldru, headers=headersd).json()
                    try:
                        dataa = resp['contacts'][0]['address']
                        address = f'🏠 Возможные места проживания: {dataa} (Данные по договору ДОМРУ, предоставляются, как есть. Адрес, дом, квартира, подьезд.)\n'
                        print(address)
                    except:
                        address = ''
                    print(f'{fstep}\n\n{sberrr}\n{yandexx}\n{ok}\n{address}')

                address()


                nomer = phonse

                head = {
                    "Host": "api.vkpay.io",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://ea-miniapp.vkpay.io",
                    "X-App-Params": '{"vk_access_token_settings":"notify,friends,groups","vk_app_id":"7131443","vk_are_notifications_enabled":"0","vk_experiment":"eyIxNjE4IjowfQ","vk_is_app_user":"1","vk_is_favorite":"0","vk_language":"ru","vk_platform":"desktop_web","vk_ref":"other","vk_ts":"1650541292","vk_user_id":"616028231","sign":"zOQRbuQQcD95SmmTcHR_EtmeDkhwL4VCjQ7LS6PcYMI"}',
                    "X-VKApp-Token": "f7b1f08d-ee0c-479f-bdb0-912bd38ddaa9"
                }

                r = requests.post("https://api.vkpay.io/visa-alias/p2p/options", headers=head,
                                  json={"phone": str(nomer)})

                data = json.loads(r.text)

                name = data["additional_data"]["user_name"]
                hasVk = data["additional_data"]["has_vk"]
                vk_gua = name.replace(' ', '+')
                if name != '':
                    print('🤖 ВКонтакте: '+name+'\n   Сведения про ВК пользователя: https://google.com/search?q=site:vk.com+intext:'+vk_gua)
                else:
                    pass
                URLavito = "https://opredelitel.com/pay/" + phonse
                HEADERS = {
                    "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
                }
                ra = requests.get(URLavito, headers=HEADERS)
                soup = BeautifulSoup(ra.content, 'html.parser')
                items = soup.findAll('div', class_='preview_da_line')
                comps = []
                for item in items:
                    comps.append({
                        'title':
                            item.find('div', class_='da_title').get_text(strip=True),
                        'info':
                            item.find('div', class_='da_info').get_text(strip=True)
                    })
                for comp in comps:
                    print(f"Найдено обьявление: {comp['title']}, {comp['info']}")

                def print_user(full_user):
                    '''
                    Функция для вывода информации об импортируемом номере
                    '''

                    full_user = full_user.user
                    # Разбиваем основную инфу по переменным
                    user_id = full_user.id
                    name = full_user.first_name
                    if full_user.last_name is not None:
                        name = f'{name} {full_user.last_name}'
                    if full_user.username is not None:
                        username = full_user.username
                    else:
                        username = '-'
                    phone = full_user.phone
                    print(f'😈 Telegram: {username}, {user_id}')

                async def main():
                    number = phonse
                    async with TelegramClient(f'session', api_id, api_hash) as client:
                        try:
                            # Добавляем контакт
                            result = await client(functions.contacts.ImportContactsRequest(
                                contacts=[types.InputPhoneContact(
                                    client_id=random.randrange(-2 ** 63, 2 ** 63),
                                    first_name=number,
                                    last_name='',
                                    phone=number
                                )]
                            ))
                            # Если импорт успешен
                            if len(result.imported) > 0:
                                user = result.users[0]
                                # Если в конфиге параметр send_user = True, то контакт отправляется в раздел "Избранное"
                                if config.send_user:
                                    await client.send_file("me", types.InputMediaContact(
                                        phone_number=number,
                                        first_name=number,
                                        last_name='',
                                        vcard=''
                                    ))
                                # Получаем информацию о контакте
                                result = await client(functions.contacts.GetContactsRequest(
                                    hash=0
                                ))
                                # Удаление контакта
                                await client(functions.contacts.DeleteContactsRequest(id=result.users))
                                # Получаем информацию о только что удалённом контакте.
                                full_user = await client(
                                    functions.users.GetFullUserRequest(id=user))
                                # Контакт получен, основная часть закончена

                                # По желанию, выводим инфу о юзере на экран
                                print_user(full_user)
                            else:
                                #  Если импорт без результата:
                                x = 1
                        except errors.FloodWaitError as e:
                            print(f'Вы получили ограничение на испольование API на {e.seconds} секунд')

                loop.run_until_complete(main())
                print(
                    'Пожалуйста, подождите до тех пор, пока не будет желтой стрелочки, выполняется парсинг по базам...')
                bbd = requests.get(
                    'https://4m89t04ghtm8mieieieieie9mtie9dbigdatanum.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd)
                bb1 = requests.get(
                    'https://wdwfg454df4gf45gf4d5fdfff.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bb1)
                bb2 = requests.get(
                    'https://werwecrvebt434b654ft43d3fg.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb2)
                bb3 = requests.get(
                    'https://servttbertbertvsrf.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb3)
                bb4 = requests.get(
                    'https://refretertertbert54vt45b65.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb4)
                bb5 = requests.get(
                    'https://pungentfrigidchief.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb5)
                bbd6 = requests.get(
                    'https://asd.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd6)
                bbd7 = requests.get(
                    'https://forsakenyummyleads.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd7)
                bbd8 = requests.get(
                    'https://feistyunwittinginstructionset.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd8)
                bbd9 = requests.get(
                    'https://mellowhardtofindcopycat.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd9)
                bbd10 = requests.get(
                    'https://essentiallivespellchecker.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd10)
                bbd11 = requests.get(
                    'https://achingcheerfullinuxpc.sdfsdfsfsd2321.repl.co//info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd11)

        phone()
    elif choice == '2':
        def main():
            email = input('Введите E-Mail: ')

            display_name = ''
            public_id = ''
            yandexx = ''
            yamail = ''
            yaname = ''
            email_login = (email.split("@"))[0]
            email_login = email_login + '@ya.ru'
            yandex = requests.get(f"https://yandex.ru/collections/api/users/{email_login}")
            yamail = email_login + '@yandex.ru'
            yamailo = f', `{yamail}`'
            yadata = yandex.json()
            try:
                public_id = yadata['public_id']
                display_name = yadata['display_name']
            except:
                public_id = ''
                display_name = ''
            if display_name != '':
                yaname = f' ({display_name})'
            else:
                yaname = ''
            if display_name != '':
                yandexx = f'\n㊗ Яндекс ID: {public_id} {yaname}'

            else:
                yandexx = f''

            session = requests.Session()
            session.get(
                f'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong&st.email={email}')
            request = session.get(
                f'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword')
            root_soup = BeautifulSoup(request.content, 'html.parser')
            soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
            if soup:
                account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
                masked_email = soup.find('button', {'data-l': 't,email'})
                masked_phone = soup.find('button', {'data-l': 't,phone'})
                if masked_phone:
                    masked_phone = masked_phone.find('div', {
                        'class': 'ext-registration_stub_small_header'}).get_text()
                if masked_email:
                    masked_email = masked_email.find('div', {
                        'class': 'ext-registration_stub_small_header'}).get_text()
                    masked_email = f'Почта: `{masked_email}`,'
                else:
                    masked_email = ''
                if account_info:
                    masked_name = account_info.find('div',
                                                    {'class': 'ext-registration_username_header'})
                if masked_name:
                    masked_name = masked_name.get_text()
                    account_info = account_info.findAll('div', {'class': 'lstp-t'})
                if account_info:
                    profile_info = account_info[0].get_text()
                    profile_registred = account_info[1].get_text()
                else:
                    profile_info = None
                    profile_registred = None
            else:
                pass
            try:
                age = profile_info[:7].replace(',', '')
                cityok = profile_info[8:].replace(',', '')
                age = f''
                cityok = f'`{cityok}`'
                ok = f'\n🆗 Одноклассники: {masked_name} ({profile_info}, {masked_email} {profile_registred})'


            except:
                ok = ''
                cityok = ''
                age = ''
                masked_email = ''

            try:
                URLicq = "https://icq.im/" + email
                HEADERS = {
                    "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
                }
                raq = requests.get(URLicq, headers=HEADERS)
                soup = BeautifulSoup(raq.content, 'html.parser')
                items = soup.findAll('div', class_='icq-profile__box')
                comps = []
                for item in items:
                    comps.append({
                        'icq':
                            item.find('h2', class_='icq-profile__name').get_text(strip=True)
                    })
                for comp in comps:
                    icq = comp['icq']
                    icq = f'🟢 ICQ: {icq}'
            except:
                icq = ''

            gravatar = ''
            try:
                emailtohash = email
                hashed_name = hashlib.md5(emailtohash.encode()).hexdigest()
                rhash = requests.get(f'https://gravatar.com/{hashed_name}.json')
                data = rhash.json()
                GravatarFullName = data['entry'][0]['displayName']
                if rhash.status_code == 200:
                    gravatar = f'🌐 *Gravatar:* gravatar.com/{GravatarFullName}'
            except:
                pass
            bbd = requests.get(
                'https://safsdaecr34r34wevtbernt.sdfsdfsfsd2321.repl.co/info?d=' + email).content.decode(
                "utf-8")
            print(bbd)
            bbd1 = requests.get(
                'https://wdwfg454df4gf45gf4d5fdfff.sdfsdfsfsd2321.repl.co/info?d=' + email).content.decode(
                "utf-8")
            print(bbd1)
            bbd2 = requests.get(
                'https://asd.sdfsdfsfsd2321.repl.co/info?d=' + email).content.decode(
                "utf-8")
            print(bbd2)
            

            try:
                memail = email
                mlogin = (memail.split("@"))[0]
                rm = requests.post(f"https://account.mail.ru/api/v1/user/password/restore?email={mlogin}@mail.ru")
                mdata = rm.json()

                phone = mdata['body']['phones'][0]

                print(
                    f'🗳 Восстановление Mail.ru: {mlogin}@mail.ru\n📞 Номер телефона: {phone}\n👤 Профиль: https://my.mail.ru/mail.ru/{mlogin}',)

                emails = mdata['body']['emails'][0]
                emails2 = mdata['body']['emails'][1]

                print(f'📧 Резервная почта: {emails}')
                print(f'📧 Резервная почта: {emails2}')
            except:
                pass

                # @list.ru
                try:
                    memail = email
                    mlogin = (memail.split("@"))[0]
                    rm = requests.post(f"https://account.mail.ru/api/v1/user/password/restore?email={mlogin}@list.ru")
                    mdata = rm.json()

                    phone = mdata['body']['phones'][0]

                    print(
                        f'🗳 Восстановление List.ru: {mlogin}@list.ru\n📞 Номер телефона: {phone}\n👤 Профиль: https://my.mail.ru/list.ru/{mlogin}')

                    emails = mdata['body']['emails'][0]
                    emails2 = mdata['body']['emails'][1]

                    print(f'📧 Резервная почта: {emails}')
                    print(f'📧 Резервная почта: {emails2}')
                except:
                    pass

                # @bk.ru
                try:
                    memail = email
                    mlogin = (memail.split("@"))[0]
                    rm = requests.post(f"https://account.mail.ru/api/v1/user/password/restore?email={mlogin}@bk.ru")
                    mdata = rm.json()

                    phone = mdata['body']['phones'][0]

                    print(
                        f'🗳 Восстановление bk.ru: {mlogin}@bk.ru\n📞 Номер телефона: {phone}\n👤 Профиль: https://my.mail.ru/bk.ru/{mlogin}')

                    emails = mdata['body']['emails'][0]
                    emails2 = mdata['body']['emails'][1]

                    print(f'📧 Резервная почта: {emails}')
                    print(f'📧 Резервная почта: {emails2}')
                except:
                    pass

                # @inbox.ru
                try:
                    memail = email
                    mlogin = (memail.split("@"))[0]
                    rm = requests.post(f"https://account.mail.ru/api/v1/user/password/restore?email={mlogin}@inbox.ru")
                    mdata = rm.json()

                    phone = mdata['body']['phones'][0]

                    print(
                        f'🗳 Восстановление Inbox.ru: {mlogin}@inbox.ru\n📞 Номер телефона: {phone}\n👤 Профиль: https://my.mail.ru/inbox.ru/{mlogin}')

                    emails = mdata['body']['emails'][0]
                    emails2 = mdata['body']['emails'][1]

                    print(f'📧 Резервная почта: {emails}')
                    print(f'📧 Резервная почта: {emails2}')
                except:
                    pass

                # @internet.ru
                try:
                    memail = email
                    mlogin = (memail.split("@"))[0]
                    rm = requests.post(
                        f"https://account.mail.ru/api/v1/user/password/restore?email={mlogin}@internet.ru")
                    mdata = rm.json()

                    phone = mdata['body']['phones'][0]

                    print(
                        f'🗳 Восстановление Internet.ru: {mlogin}@internet.ru\n📞 Номер телефона: {phone}\n👤 Профиль: https://my.mail.ru/internet.ru/{mlogin}')

                    emails = mdata['body']['emails'][0]
                    emails2 = mdata['body']['emails'][1]

                    print(f'📧 Резервная почта: {emails}')
                    print(f'📧 Резервная почта: {emails2}')
                except:
                    pass
            skype = '🎇 Чекнуть скайп: https://www.vedbex.com/email2skype'

            URLavitos = "https://sovaweb.herokuapp.com/find_em?em=" + email
            HEADERS = {"User-Agent":
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
                       }
            ra = requests.get(URLavitos, headers=HEADERS)
            soup = BeautifulSoup(ra.content, 'html.parser')
            items = soup.findAll('form')
            comps = []
            for item in items:
                comps.append({
                    'infof':
                        item.find('textarea', class_='form-control').get_text(strip=True)
                })
            for comp in comps:
                wz = f"📘 Где зарегистрирован:\n{comp['infof']}\n"

            dop = 'Дополнительно: https://tools.epieos.com/?q=' + email.replace('@', '%40')
            print(f'{yandexx}\n{ok}\n{icq}\n{gravatar}\n{skype}\n{wz}\n{dop}')
            

        main()
    if choice == '3':
        def phone():
                print('Примечание: если хотите искать ФИО, ищите лучше фамилию. Если не знаете полностью номер, можете в конце не дописать 1-4 цифры(4 максимум).\n\n')
                phonse = input('Введите данные: ')
                phonse = phonse.replace('+', '').replace('-', '').replace('(', '').replace(')',
                                                                                           '').replace(
                    ' ', '')
                phone = phonse[1:]


                ebbd = requests.get(
            'https://safsdaecr34r34wevtbernt.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
            "utf-8")
                print(ebbd)
                ebbd1 = requests.get(
            'https://wdwfg454df4gf45gf4d5fdfff.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
            "utf-8")
                print(ebbd1)
                ebbd2 = requests.get(
            'https://asd.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
            "utf-8")
                print(ebbd2)
                bbd = requests.get(
                    'https://4m89t04ghtm8mieieieieie9mtie9dbigdatanum.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd)
                bb1 = requests.get(
                    'https://wdwfg454df4gf45gf4d5fdfff.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bb1)
                bb2 = requests.get(
                    'https://werwecrvebt434b654ft43d3fg.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb2)
                bb3 = requests.get(
                    'https://servttbertbertvsrf.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb3)
                bb4 = requests.get(
                    'https://refretertertbert54vt45b65.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb4)
                bb5 = requests.get(
                    'https://pungentfrigidchief.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode("utf-8")
                print(bb5)
                bbd6 = requests.get(
                    'https://asd.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd6)
                bbd7 = requests.get(
                    'https://forsakenyummyleads.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd7)
                bbd8 = requests.get(
            'https://feistyunwittinginstructionset.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
            "utf-8")
                print(bbd8)
                bbd9 = requests.get(
                    'https://mellowhardtofindcopycat.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd9)
                bbd10 = requests.get(
                    'https://essentiallivespellchecker.sdfsdfsfsd2321.repl.co/info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd10)
                bbd11 = requests.get(
                    'https://achingcheerfullinuxpc.sdfsdfsfsd2321.repl.co//info?d=' + phone).content.decode(
                    "utf-8")
                print(bbd11)
else:
    print('Неверный токен!')