# -*- coding: utf-8 -*-

PAGE_ACCESS_TOKEN = 'EAAIKeBZA61WUBAA8KbXzWBTYTIosqOPZCjcxkdhQnvthEj4LFuGyzGLCz6WgaKX2YhOLsPMYcaV6CqPlsOZBr6pLwgHUk4ZBhOjgxsvBVmJLZBuAe7IfP2RzAZB2nEsKz3AAoLlAsSZAwZBJIirNOJOCJizvZAIDZC5ZBrCgIX1LtXArXFdgb2upCj9O7MeFyVryb0ZD'
VERIFY_TOKEN = 'test1M453arkernk34sevfuweukCFCT76WfefbnscCTYDWjn76523cs'
# https://gentle-bastion-44090.herokuapp.com/ | https://git.heroku.com/gentle-bastion-44090.git

WEBHOOK_HOST = 'https://still-basin-56893.herokuapp.com'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

#WEBHOOK_SSL_CERT = './cert.pem'  # Путь к сертификату
#WEBHOOK_SSL_CHAIN = './fullchain.pem'  # Путь к сертификату
#WEBHOOK_SSL_PRIV = './privkey.pem'  # Путь к приватному ключу

GreetingMessageLine1 = 'Сәлеметсіз бе, Сізді Астана EXPO-2017 халықаралық көрмесінің анықтама қызмет бөлімінің автоматтандырылған ақпараттық жүйесі қарсы алуда.'
GreetingMessageLine2 = 'Здравствуйте, Вас приветствует бот-ассистент службы контакт центра международной выставки Астана EXPO-2017.'
GreetingMessageLine3 = 'Welcome to Astana EXPO-2017! You are talking to a bot-assistant of Contact Center EXPO-2017.'
GreetingMessageLine4 = 'При отправке заявки просим отправлять Ваши контактные данные (ФИО, номер телефона).'
GreetingMessageLine5 = 'Просим обратить внимание, что Обращение, по которому невозможно установить авторство, считается анонимным и не подлежит рассмотрению.'

GreetingMessageLine = GreetingMessageLine1 + '\n\n' + GreetingMessageLine2 + '\n\n' + GreetingMessageLine3 + '\n\n' + GreetingMessageLine4 + '\n\n' + GreetingMessageLine5


WelcomeMessageLine1 = 'Для использования сервиса нажмите на одну из следующих кнопок: «Создать обращение», «Другие услуги» (кнопки отображены в нижней части экрана).'
WelcomeMessageLine2 = 'Для полноценной работы сервиса требуется последняя версия приложения Facebook/Messenger.'

WelcomeMessageLineAll = WelcomeMessageLine1+'\n\n'+WelcomeMessageLine2

RequestMessageLine1 = 'Вы выбрали услугу для отправки Обращения.'
RequestMessageLine2 = 'Форма обращения состоит из двух этапов: отправка контактного номера телефона и обращения. Внимание, для возможности рассмотрения Вашего обращения просим отправлять достоверные контактные данные.'
RequestMessageLine3 = 'Введите Ваш номер телефона и нажмите на кнопку «Отправить».'
RequestMessageLine4 = 'Пожалуйста, оставьте обращение, нажмите на кнопку «Отправить» и дождитесь ответа.'

RequestMessageLineAll = RequestMessageLine1+'\n\n'+RequestMessageLine2+'\n\n'+RequestMessageLine3

OtherServicesLine1 = 'Для ознакомления с другими услугами нажмите на кнопку "Astana EXPO-2017"'

AddRequestMessageLine1 = 'Спасибо, Ваше обращение принято! Ожидайте ответа от менеджера по предоставленным Вами контактным данным. Благодарим за использование наших продуктов.'
AddRequestMessageLine2 = 'В случае возникновения вопросов, просим обращаться в Call center по номерам 1440 или 8800 080 2017.'

AddRequestMessageLineAll = AddRequestMessageLine1+'\n\n'+AddRequestMessageLine2

SendRertyMessageLine1 = 'Для регистрации обращения просим вести данные в текстовом формате.'
SendRertyMessageLine2 = 'Либо, для перехода в главное меню сервиса нажмите кнопку "Глaвнoе мeню".'

SendRertyMessageLineAll = SendRertyMessageLine1+'\n\n'+SendRertyMessageLine2

SendPhoneRertyMessageLine1 = 'Отправленный номер не прошел проверку по формату. Просим отправить номер телефона в формате: 8[Код города/Оператора][Номер телефона]. Пример: 87771234567.'
SendPhoneRertyMessageLineAll = SendPhoneRertyMessageLine1+'\n\n'+SendRertyMessageLine2

CreateAppeal = "Создать обращение"
OtherServices = "Другие услуги"
GoToMainMenu = "Главное меню"
GoToWebPage = "Astana EXPO-2017"
link = "https://expo2017astana.com/"
