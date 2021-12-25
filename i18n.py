ar_iq = {
    "about": "هذا البوت يسهل للطلاب الوصول الى جدولهم بسهولة او هم بحاجة الى تبليغ يومي بجدولهم😀\n\n",
    "technologies": "*Python* : باكيند, ومدري شلون اترجمها بالعربي بس المهم فد شي ديجيب الداتا من موقع الجدول مال "
                    "جامعة وتحول HTML وايضا البوت الدتستعملة\n\n"
                    "*Node-Express* : دنحول الداتا الى صورة\n\n"
                    "*Vuejs* : بالفيو دنسوي مثل موقع فوك موقع الجدول بس نخلي واحد يوصلة عن طريق روابط واسهل استعمالة",
    "how_does_it_work": "بختصار بالبايثون دجيب الداتا من موقع الجامعة دحولها HTML"
                        "بعدين ددزها للنود دتحول ولو ندز الصورة بالبوت لو ندزها بالموقع مالتنا",
    "credits": "@no6_sha الموقع وال HTML \n@MAtheerS الحبشكلات البقية",

}
en_us = {
    "about": "We have created this bot to send you your schedule, Obviously😀",
    "technologies": "*Python* : Backend, Web scrapper and Websocket for telegram bot\n\n"
                    "*Node-Express* : Rendering Html to image\n\n"
                    "*Vuejs* : a better wrapper for main website make it Queryful Searchable\n\n",
    "how_does_it_work": "After you tell the *schedule* you need python scrape the data from "
                        "techno website (uotcs.edupage.org/timetable)",
    "credits": "@no6_sha @MAtheerS",
}

languages = {
    "en": en_us,
    "ar": ar_iq,
}


def translate(lang: str, key: str):
    try:
        return languages[lang][key]
    except KeyError:
        return en_us[key]
