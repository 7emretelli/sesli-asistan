# coding=utf-8
import speech_recognition as sr
import os
import time
import wikipedia
from gtts import gTTS
from selenium import webdriver

global browser


def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='tr')
    tts.save('audio.mp3')
    os.system('sudo afplay audio.mp3')


def recordAudio():  # Mikrofonu dinlemeden önce Recognizer(tanıyıcı)mızı tanımlıyoruz.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Seni dinliyorum")
        audio = r.listen(source)

    # Burada google'ın ses tanıma sistemini kullandık bu sistem internet gerektiriyor.
    data = ""

    try:
        data = r.recognize_google(audio, language='tr-tr')
        data = data.lower()

    except sr.UnknownValueError:

        print("Sesini duyamadım?")

    return data


def wiki():
    def arastirma(data):
        if data == "":
            speak("dediğini duyamadım, uyku moduna geçiyorum")
        else:
            def devam(wikis):
                data = recordAudio()
                print(data)
                if data == "":
                    speak("duyamadım... Senin için hangisini açmamı istersin?")
                    data = recordAudio()
                    print(data)
                    if data == "":
                        speak(
                            "dediğini duyamadım. Bir sonraki komutuna kadar uyku modunda kalacağım.")
                elif "hayır" in data:
                    def devam2():
                        data = recordAudio()
                        if "evet" in data:
                            wiki()
                        elif "hayır" in data:
                            speak("peki... Bekleme modundayım... hoşça kal")
                        else:
                            speak("dediğini anlayamadım tekrar söylermisin?")
                            devam2()
                    speak("Peki... Senin için yeni bir arama yapmamı istermisin?")
                    devam2()
                elif "birinci" in data:
                    bs = wikis
                    pg = wikipedia.page(bs[0])
                    print(pg.links[0]+"-"+pg.links[1])
                    speak(pg.title+" hakkındaki sayfayı hemen size açıyorum.")
                    link = pg.url
                    browser = webdriver.Chrome()
                    browser.get(link)

                elif "ikinci" in data:
                    bs = wikis
                    pg = wikipedia.page(bs[1])
                    print(pg.links[0]+"-"+pg.links[1])
                    speak(pg.title+" hakkındaki sayfayı hemen size açıyorum.")
                    link = pg.url
                    browser = webdriver.Chrome()
                    browser.get(link)
                elif "üçüncü" in data:
                    bs = wikis
                    pg = wikipedia.page(bs[2])
                    print(pg.links[0]+"-"+pg.links[1])
                    speak(pg.title+" hakkındaki sayfayı hemen size açıyorum.")
                    link = pg.url
                    browser = webdriver.Chrome()
                    browser.get(link)
                else:
                    speak("dediğini anlayamadım tekrar söylermisin?")
                    devam(a)

            wikipedia.set_lang("tr")
            a = wikipedia.search(data, results=3)
            if len(a) > 0:
                speak("işte bulduklarımdan birkaçı,"+a[0]+","+a[1]+","+a[2])
                devam(a)
            else:
                speak("Hiçbir şey bulamadım")

    speak("Bana anahtar kelimeleri söyle")
    data = recordAudio()
    print(data)

    arastirma(data)


def asistan(data):
    print(data)
    if "hey arix" in data:
        speak("evet, sizi dinliyorum")
    elif "merhaba" in data:
        mrb = "Merhaba"
        speak(mrb)
        speak("Nasıl yardımcı olabilirim?")
    elif "neler yapabilirsin" in data:
        ff = "işte yapabildiğim birkaç şey: müzik çal, hava durumu"
        speak(ff)
    elif "kendini kapat" in data:
        ff = "Hoşça Kal"
        speak(ff)
        exit()
    elif "çal" in data:
        speak("şarkının adı ne olsun?")
        data = recordAudio()
        # x = data.find("çal")
        # sarki = data[0:x]
        sarkilink = data.replace(" ", "+")
        browser = webdriver.Chrome()
        browser.get("https://www.youtube.com/results?search_query="+sarkilink)
        speak("İşte sizin için bulduğum bir kaç sonuç, hangisini açmamı istersiniz?")
        data = recordAudio()
        if "ilk" in data:
            bir = browser.find_element_by_xpath(
                "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a")
            bir.click()
        if "ikinci" in data:
            iki = browser.find_element_by_xpath(
                "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[2]/div[1]/div/div[1]/div/h3/a")
            iki.click()

    elif "sekmeyi kapat" in data:
        print("deniyorum")
        try:
            browser.close()
        except:
            return
    elif "beklemede kal" in data:
        speak("bekliyorum")
        while 1:
            data = recordAudio()
            if data == "":
                return
            else:
                break
    elif "hava durumu" in data:
        print("hemen bakıyorum")
        browser = webdriver.Chrome()
        browser.get(
            "https://www.google.com/search?q=hava+durumu&oq=hava+durumu")
        derece = browser.find_element_by_xpath(
            "//*[@id='wob_tm']").text
        hava = browser.find_element_by_xpath("//*[@id='wob_dc']").text
        speak("bugün " + derece+" derece, havanın durumu ise " + hava)
        time.sleep(3)
        browser.close()
    elif "bana yardım et" in data:
        speak("Ne gibi yardım istersin?")
        data = recordAudio()
        data2 = data
        while data2 == data:
            if "bilmem" in data:
                speak("tamam")
            break
    elif "araştır" in data:
        print(data)
        wiki()

    else:
        speak("Şuan ana menüdeyim ve ne dediğini anlamadım")


speak("Size nasıl yardım edebilirim?")
while 1:
    print("şuan while döngüsündeyim")
    data = recordAudio()
    if data == "":
        print("şuan datam boş")
        data = recordAudio()
    else:
        print("şuan asistana atadım")
        asistan(data)
