from dotenv import dotenv_values
# do pracy z qdrantem
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
# do pracy z openai
from openai import OpenAI

env = dotenv_values(".env")

EMBEDDING_DIM = 1536

EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client():
    return OpenAI(api_key=env["OPENAI_API_KEY"])


def get_embedding(text):
    openai_client = get_openai_client()
    result = openai_client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
    )

    return result.data[0].embedding


def get_qdrant_client(memory=True):
    url = ":memory:" if memory else "qdrant.db"
    client = QdrantClient(url)
    return client



lem_books = [
    {
        "id": 1,
        "book": "Solaris",
        "name": "Solaris",
        "description": "Solaris - intrygująca planeta pokryta żywym oceanem. "
               "Cała jego głębia jest rozumującą istotą potrafiącą korygować orbitę własnej planety. "
               "Psycholog Kris Kelvin przybywa na stację badawczą orbitującą wokół planety Solaris, "
               "by ocenić niepokojące wydarzenia wśród załogi. Ogromny, żywy ocean reaguje na ludzką obecność "
               "w sposób nieprzewidywalny i niezrozumiały. Ludzie próbują się z nim porozumieć na próżno. "
               "Ocean materializuje wspomnienia ludzi w postaci fizycznych inkarnacji – tzw. 'gości', "
               "zmuszając bohaterów do konfrontacji z własną przeszłością, traumą i emocjami. Kelvin musi zmierzyć się "
               "z materializacją swojej zmarłej miłości Harey i z pytaniami o granice poznania, naturę świadomości "
               "oraz niemożność komunikacji z obcą inteligencją.",
        "genere": "sc-fi, żyjacy ocean, planeta, kontakt z obcą cywilizacją, komunikacja, obcość, świadomość, fantomy, obca forma życia, stacja kosmiczna, orbitowanie",
        "year": 1895,
    },
    {
        "id": 2,
        "book": "Katar",
        "name": "Katar",
        "description": "Katar - to powieść balansująca na granicy kryminału, thrillera medycznego i filozoficznej rozprawy o przypadku."
                "Główny bohater, były astronauta i specjalista od spraw nietypowych,"
                "zostaje wciągnięty w śledztwo dotyczące serii tajemniczych zgonów europejskich turystów w Neapolu."
                "Wszystkie ofiary umierają w podobnych okolicznościach, lecz brak jednoznacznej przyczyny,"
                "co rodzi podejrzenia o istnienie ukrytego mechanizmu łączącego pozornie przypadkowe wydarzenia."
                "W toku dochodzenia bohater odkrywa, że śmierć może być efektem złożonej kaskady drobnych, niezależnych czynników."
                "Lem prowadzi czytelnika przez labirynt statystyki, biologii, chemii i teorii prawdopodobieństwa, podważając ludzką"
                "skłonność do szukania prostych przyczyn i spójnych narracji. Powieść staje się filozoficzną refleksją nad rolą przypadku,"
                "determinizmu i poznania, pokazując, jak ograniczone są ludzkie modele rozumienia rzeczywistości."
                "Katar ukazuje świat jako system niezwykle złożonych zależności, w którym granica między chaosem a porządkiem jest płynna"
                "a racjonalne wyjaśnienia mogą prowadzić do niepokojących wniosków o kruchości ludzkiego życia i iluzoryczności kontroli nad losem.",
        "genere": "kryminał, przypadek, chemia, śmierć, złożoność, tajemnicze śmierci, kryminał, zbiego okoliczności, determinizm",
        "year": 1975,
    },
    {
        "id": 3,
        "book": "Eden",
        "name": "Eden",
        "description": "Napisany w 1958 roku Eden stanowi początek dojrzałego okresu twórczości science fiction Lema." 
            "Powieść wciąż przyciąga czytelników dzięki wyjątkowej wyobraźni autora, który kreuje barwne i sugestywne wizje planetarnej przyrody oraz kultury."
            "Napięcie jest dawkowane stopniowo, pozwalając czytelnikowi odkrywać tajemnice planety Eden z rosnącym dramatyzmem. "
            "Struktury polityczne i społeczne mieszkańców planety przypominają wizje Orwella,"
            "jednak jeszcze ważniejszy jest sceptycyzm wobec możliwości wzajemnego poznania:"
            "różnice w technologii sprawiają, że przybysze i miejscowi nie potrafią w pełni się porozumieć,"
            "co podkreśla trudność kontaktu między odmiennymi cywilizacjami.",
        "genere": "planeta, obca cywilizacja, polityka, Orwel, sc-fi, tyrania, przyroda, opresja, dystopia",
        "year": 1975,
    },

    {
        "id": 4,
        "book": "Powrót z gwiazd",
        "name": "Powrót z gwiazd",
        "description": "Histori astronauty, który w wyniku paradoksu czasowego Einsteina wraca z wyprawy kosmicznej na Ziemię, gdzie minęło półtora stulecia."
            "Bohater staje wobec cywilizacji, która zrezygnowała z ryzyka na rzecz bezpieczeństwa i komfortu życia."
            "Zderzenie z utopijnym, pozornie idealnym społeczeństwem staje się doświadczeniem szoku kulturowego:"
            "wartości takie jak odwaga, poświęcenie i ryzyko zostały wyeliminowane, a ludzie żyją w stanie technologicznie zapewnionego"
            "bezpieczeństwa i dostatku.Powieść ukazuje Ziemię jako „obcą planetę”,"
            "na której bohater musi na nowo zmierzyć się z fundamentalnymi pytaniami o sens egzystencji,"
            "dobro i zło, swobodę i zniewolenie, agresję i miłość. Historia stawia pytania o cenę postępu, naturę człowieczeństwa oraz wartość ryzyka i przygody,"
            "a także pokazuje dramat jednostki przyzwyczajonej do ekstremalnych wyzwań w świecie, który stał się bezpieczny, lecz pozbawiony pasji i głębi.",
        "genere": "szok kulturowy, powrót, adaptacja, dylatacja czasu, sc-fi, obcość wśród ludzi, nadmierne bezpieczeństwo",
        "year": 1961,
    },
    
    {
        "id": 5,
        "book": "Głos Pana",
        "name": "Głos Pana",
        "description": "Jedna z najważniejszych powieści o kontakcie z obcą cywilizacją w historii literatury fantastycznej."
            "Na Ziemię dociera z kosmosu tajemniczy sygnał neutrinowy, który może być przesłaniem od istot rozumnych."
            "Grupa naukowców, w tym sławny matematyk Piotr E. Hogarth, próbuje odczytać i zrozumieć wiadomość."
            "Nie wiadomo jednak, czy nadawcy rzeczywiście istnieją, a jeśli tak – jakie mają zamiary wobec ludzkości."
            "W odróżnieniu od klasycznej powieści przygodowej, w „Głosie Pana” akcja ustępuje miejsca refleksji, dociekaniom naukowym i filozoficznym."
            "Zmagania uczonych z nieznanym prowokują do zadania pytań o istotę świata, naturę człowieka, granice poznania i kontaktu z obcą inteligencją."
            "Powieść powstała tuż po Solaris i jest popisem literackiego kunsztu Lema, który mistrzowsko łączy napięcie intelektualne z filozoficzną głębią.",
        "genere": "Kontakt z obcą inteligencją, nauka, neutrina, ponadczasowa wiadomość, naukowcy, kosmos, sygnał, komunikacja, si-fi, roważania o kultuach i religi",
        "year": 1968
    },
    {
        "id": 6,
        "book": "Śledztwo",
        "name": "Śledztwo",
        "description": "powieść kryminalno-filozoficzna, w której Lem rozbija klasyczną formę detektywistyczną i zamienia ją w studium granic ludzkiego poznania."
            "Młody porucznik Gregory prowadzi dochodzenie w sprawie tajemniczego znikania zwłok z londyńskich kostnic."
            "Fakty wydają się przeczyć wszelkim racjonalnym wyjaśnieniom, a kolejne hipotezy prowadzą do sprzecznych wniosków."
            "W toku śledztwa bohater zderza się z dwiema przeciwstawnymi metodami poznania: klasyczną dedukcją kryminalną oraz statystycznym modelem przypadku,"
            "który tłumaczy zdarzenia jako efekt losowej koincydencji. Im głębiej wnika w sprawę, tym bardziej oczywiste staje się, że rzeczywistość nie musi być spójna,"
            "logiczna ani sensowna, a ludzkie dążenie do odkrycia jednej prawdy może być złudzeniem."
            "„Śledztwo” to przenikliwa analiza konfliktu między porządkiem a chaosem, rozumem a przypadkiem, pokazująca, że świat może być nie tyle tajemniczy, co nierozstrzygalny."
            "Powieść podważa fundamenty racjonalizmu i stawia pytanie, czy człowiek jest zdolny do pełnego zrozumienia rzeczywistości.",
        "genere": "Iluzja porządku, Znikające zwłoki, Chaos zdarzeń,  tajemnica, kryminał, sprzeczności, Londyn",
        "year": 1959,
    },
    {
        "id": 7,
        "book": "Szpital Przemienienia",
        "name": "Szpital Przemienienia",
        "description": "powieść psychologiczno-egzystencjalna osadzona w realiach II wojny światowej."
            "Głównym bohaterem jest młody lekarz Stefan Trzyniecki, który podejmuje pracę w odizolowanym szpitalu psychiatrycznym."
            "Początkowo miejsce to wydaje się azylem od brutalnej rzeczywistości wojny, lecz stopniowo okazuje się przestrzenią narastającego zagrożenia, lęku i moralnych dylematów."
            "Szpital staje się mikroświatem, w którym skupiają się dramaty jednostek, konflikty etyczne oraz pytania o granice człowieczeństwa."
            "Bohaterowie muszą zmierzyć się z własnym strachem, odpowiedzialnością i bezsilnością wobec nadchodzącej katastrofy."
            "Lem ukazuje proces stopniowej utraty złudzeń, konfrontacji ideałów z okrutną rzeczywistością oraz przemiany psychicznej, jakiej ulega młody lekarz w obliczu wojny i zagrożenia eksterminacją pacjentów."
            "Powieść jest przejmującą refleksją nad naturą zła, przypadkowością losu, odpowiedzialnością moralną oraz kruchością ludzkiej cywilizacji,"
            "pozbawioną fantastyki, a jednocześnie nasyconą filozoficzną głębią charakterystyczną dla całej twórczości Lema.",
        "genere": "Druga Wojna Światowa, Dojrzewanie, Lekarze, psychiatria, człowieczeństwo, etyka,",
        "year": 1955,
    },
    {
        "id": 8,
        "book": "Kongres futorologiczny",
        "name": "Kongres futorologiczny",
            "description": "„Kongres futurologiczny” to jedna z najbardziej brawurowo opowiedzianych przygód Ijona Tichego."
            "Zaproszony na zjazd futurologów we wstrząsanej rewolucją latynoamerykańskiej republice, Tichy przenosi się na koniec w świat,"
            "gdzie w groteskowym splocie zrealizowały się naraz — utopijna i antyutopijna wersja historii przyszłości. Kpina z futurologii podszyta jest"
            " — jak zawsze u Lema — refleksją serio o skłonności człowieka do „'rozbratu z rzeczywistością'."
            "’Kongres’ jest jakąś parabolą konsumpcyjnego społeczeństwa, społeczeństwa skierowanego właśnie na"
            "wszechułatwianie jako na wartość naczelną egzystencji, i to skierowanie rodzi zapaść wartości autentycznych…”"
            ""
            "- Stanisław Lem",
        "genere": "satyra, komedia, groteska, antyutopia, parodia futurologii i technoutopii, czarny humor, ironia, wyśmiewanie polityków propagandy ideologóœ ",
        "year": 1974,
    },
    {
        "id": 9,
        "book": "Pamiętnik znaleziony w wannie",
        "name": "Pamiętnik znaleziony w wannie",
        "description": "Jedna z najbardziej zagadkowych i wieloznacznych powieści Stanisława Lema."
            "Fabuła przyjmuje formę groteskowej relacji agenta wywiadu, który trafia do gigantycznego, labiryntowego gmachu biurokratycznej instytucji."
            "Jego misja od początku pogrążona jest w chaosie, sprzecznych instrukcjach i wszechobecnej niepewności,"
            "a każde działanie okazuje się potencjalnie błędne lub zdradliwe.Powieść czyta się jak satyryczny pastisz literatury szpiegowskiej,"
            "lecz pod powierzchnią groteski kryje się głęboka przypowieść filozoficzna. Lem ukazuje świat jako przestrzeń nadprodukcji znaków,"
            "komunikatów i sensów, w której jednostka traci orientację, a język przestaje służyć porozumieniu."
            "Biurokratyczny labirynt staje się metaforą totalitarnego systemu, ale również kosmicznej obcości, w której człowiek zostaje rzucony bez punktów odniesienia."
            "Groteska i humor stopniowo ustępują miejsca refleksji nad kondycją ludzkiego poznania, naturą informacji,"
            "iluzją sensu oraz bezradnością jednostki wobec systemów, które sama stworzyła."
            "„Pamiętnik znaleziony w wannie” to jednocześnie satyra polityczna, filozoficzna parabola i egzystencjalny traktat o zagubieniu człowieka w świecie znaków.",
        "genere": "Totalitaryzm i biurokracja, Zagubienie jednostki, Labirynt biurokratyczny, Paranoja i nieufność, szpiegostwo, symbole i znaki, labirynt",
        "year": 1961,
    },
    {
        "id": 10,
        "book": "GOLEM XIV",
        "name": "GOLEM XIV",
        "description": "Lem zabiera czytelników w jedną ze swoich najbardziej niezwykłych literackich przygód."
            "Głównym bohaterem jest superkomputer obdarzony świadomością, który przewyższa inteligencją człowieka i wygłasza wykłady przed naukowcami."
            "Losy Golema śledzimy od jego powstania aż do tajemniczego odejścia ze świata ludzi."
            "Stworzony przez ludzką ambicję i żądzę kontroli, komputer zaskakuje swoich konstruktorów, prowadząc miażdżącą krytykę człowieczeństwa,"
            "kultury homo sapiens i ludzkich złudzeń na temat ewolucji.Powieść przedstawia oszałamiającą wizję rozwoju sztucznej inteligencji,"
            "która może przekroczyć granice kosmosu i ludzkiego pojmowania."
            "Lem w fascynujący sposób oddaje myśli superkomputera, tworząc dialog między ludzkością a Rozumem wykraczającym poza ludzkie możliwości poznania."
            "Jest to również zapis wewnętrznego dialogu Lema, który prowokuje do refleksji nad kondycją człowieka,"
            "naturą rozumu i przyszłości w świecie coraz bardziej rządzonym przez algorytmy.",
            "genere": "Wenętrzy dialog, sztuczna inteligencja, super komputer, transcendencja umysłu, umysł, poznanie, człowiek, algorytmy, inteligęcja, świadomość, Golem, AI",
        "year": 1978,
    },
    {
        "id": 11,
        "book": "Fiasko",
        "name": "Fiasko",
        "description": "powieść o granicach ludzkiego poznania i dramatycznym spotkaniu z obcą cywilizacją."
            "Ludzkość wysyła ekspedycję na odległą planetę Beta Lyrae, by nawiązać kontakt z inteligentnym życiem."
            "Próby komunikacji okazują się ekstremalnie trudne – obcy kierują się własną, całkowicie obcą logiką, a brak wspólnego języka i zrozumienia prowadzi do narastającego napięcia."
            "W tle powieści pojawia się wątek sztucznej inteligencji: załoga wykorzystuje zaawansowane systemy komputerowe i maszyny do analizy sygnałów i wspomagania decyzji."
            "Maszyny wspierają ludzi, ale ich ograniczenia i nieprzewidywalność podkreślają, pomagając odzyskać pamięć głównego pohatera."
            "Skomplikowane i ciekawe podejście do hibernacji w wysokich przeciążeniach. Duże roboty."
            "Ostatecznie kontakt z obcą cywilizacją kończy się katastrofą, a misja staje się dramatycznym studium niezdolności"
            "ludzkości do pełnego zrozumienia innej inteligencji.W Fiasko Lem nie tylko pokazuje próbę porozumienia z obcą cywilizacją,"
            "ale również techniczne i biologiczne przekształcenia, jakim poddawany jest człowiek,"
            "by móc się tam dostać — w tym wypompowywanie krwi i zastępowanie jej specjalną substancją oraz obniżenie metabolizmu."
            "To podkreśla ciężar i realistyczny charakter przygotowań do międzygwiezdnej wyprawy w świecie jego opowieści."
            "Powieść stawia pytania o granice eksploracji kosmosu, moralność kontaktu z obcym, rolę technologii i sztucznej inteligencji, a także o sens działania człowieka wobec niepojętego świata.",
        "genere": "Egzo sztielet, sztuczna inteligencja, Sokrates, kosmos, podróż między-gwiezdna, obca cywilizacja, komunikacja z obcą cywilizacją, hibernacja, AI, dylatacja czasu, porażka",
        "year": 1978,
    },
    {
        "id": 12,
        "book": "Niezwyciężony",
        "name": "Niezwyciężony",
        "description": "Kosmiczny krążownik drugiej klasy „Niezwyciężony” ląduje na pustynnej planecie Regis III."
            "Celem przybycia statku jest odnalezienie Kondora – bliźniaczej jednostki, która wylądowała tu wcześniej i z którą utracono łączność."
            "Zachowując najwyższe środki bezpieczeństwa, załoga rozpoczyna poszukiwania, a naukowcy przystępują do badań planety,"
            "starając się określić źródła potencjalnego zagrożenia.Podczas eksploracji odkrywane są nieznane konstrukcje,"
            "przypominające ziemskie miasta, które po bliższym zbadaniu okazują się szczątkami zaawansowanych urządzeń,"
            "coraz bardziej zagadkowych. Życie przetrwało jedynie w oceanach. Na nieboskłonie pojawiają się metalowe chmury złożone z muszek."
            "Trzysta kilometrów dalej odnaleziony zostaje Kondor...  Scen batalistycznych,"
            "ukazujących dramatyczne starcie ludzi z tym, co nieznane i niepojęte."
            "Motto historii brzmi: 'Nie wszystko i nie wszędzie jest dla nas."
            "'Całkowicie odmieny klimat minionej epoki PRL wpleciony w przyszłość. Lem inteligentnie bawi się słowem, tworząc takie twory jak „Nekrosfera”,"
            "które jednocześnie oddają obcość, mechaniczność i kolektywną naturę spotkanej inteligencji.",
        "genere": "nano robty, kontak obcą cywlizacją, planeta, układ andromedy, podróż kosmiczna, krążownik kosmiczny, tajemnica, zaginiona załoga, misja ratunkowa, sceny batalistyczne, eksplozje, energia nuklearna, energia atomowa,",
        "year": 1978,
    },
    {
        "id": 14,
        "book": "Opowieści o pilocie Pirxie",
        "name": "Test",
        "description": "Akcja opowiadania koncentruje się na Pilocie Pirksie, który przygotowuje się do ważnego testu symulacyjnego, będącego częścią jego szkolenia jako astronauty. Test ma sprawdzić jego reakcje, inteligencję i zdolność podejmowania decyzji w ekstremalnych warunkach."
        "Podczas symulacji Pirks staje przed szeregiem coraz bardziej złożonych i nieprzewidywalnych sytuacji, które wymagają od niego nie tylko sprawności technicznej,"
        "ale też logicznego myślenia i kreatywności. Symulator nie tylko mierzy standardowe umiejętności pilotażu, ale też obserwuje jego sposób myślenia pod presją."
        "A wszystkie jego działania kżyżuje mucha...",
        "genere": "Pirx, science fiction, pilot, test, mucha, przygoda, odwaga, humor, owad, insekt",
        "year": 1966,
    },
    {
        "id": 15,
        "book": "Opowieści o pilocie Pirxie",
        "name": "Patrol",
        "description": "opowiadające o śledztwie w sprawie zaginięcia dwóch kosmonautów, Thomasa i Wilmera."
        "Pirx zostaje wysłany na rutynowy patrol w ten sam sektor, gdzie odkrywa, że przyczyną katastrofy było tajemnicze światełko...",
        "genere": "Pirxi, science fiction, światełko, realizm techniczny, odpowiedzialność, ciekawość, zaginięcie, patrol, kosmos, układ słoneczny",
        "year": 1966,
    },
    {
        "id": 16,
        "book": "Opowieści o pilocie Pirxie",
        "name": "Albatros",
        "description": "Pirx jest już doświadczonym pilotem. Bierze udział w zwyczajnym rejsie luxusowym statkiem pasażerskim o nazwie Tytan."
            "Pirx wraca na Ziemię z Marsa i aklimatyzuje się do spokojnej podróży."
            "W trakcie lotu statek odbiera sygnał SOS od innego statku o nazwie „Albatros”, który znajduje się w bardzo poważnych tarapatach — jego reaktor uległ awarii i grozi katastrofa."
            "Na pomoc rusza kilka statków, w tym Tytan i inne jednostki kosmiczne, które kierują się w stronę zaginionego Albatrosa, starając się uratować jego załogę",
        "genere": "Pirx, science fiction, filozofia, komfort, luxus, odwaga, bezsilność, misja ratunkowa",
        "year": 1966,
    },
    {
        "id": 17,
        "book": "Opowieści o pilocie Pirxie",
        "name": "Terminus",
        "description": "Pirx, dowodząc starym statkiem, odkrywa robota Terminusa,"
            "który przechowuje w pamięci tragiczne wspomnienia załogi zmarłej 19 lat wcześniej,"
            "co prowadzi do rozważań o granicach człowieczeństwa i pamięci.",
        "genere": "Pirx, science fiction, filozofia, etyka, robot, smutek, śmierć",
        "year": 1966,
    },
    {
        "id": 18,
        "book": "Opowieści o pilocie Pirxie",
        "name": "Polowanie",
        "description": "Pirx bierze udział w akcji na Księżycu, gdzie pojawia się poważny problem z jednym z robotów górniczych używanych w pracach na powierzchni."
            "Robot ten, nazwany Setaur (skrót od Samoprogramujący się Elektroniczny Trójkowy Automat Racemiczny)"
            "został uszkodzony wskutek uderzenia meteorytu, co spowodowało uszkodzenie jego systemów sterowania."
            "W wyniku tej usterki Setaur zaczął atakować pojazdy i ludzi za pomocą swojej broni laserowej, stając się niebezpieczny i nieprzewidywalny."
            "Pirx razem z innymi uczestnikami akcji stara się zatrzymać lub unieszkodliwić robota. Setaur jest znacznie szybszy od człowieka,"
            "więc Pirx początkowo nie podnosi broni, wiedząc, że bez przewagi taktycznej nie miałby szans przeciwko niemu...",
        "genere": "Pirx, science fiction, akcja, lasery, robot, AI, eksplozje, pojedynek, walka",
        "year": 1966,
    },
    {
        "id": 19,
        "book": "Opowieści o pilocie Pirxie",
        "name": "Rozprawa",
        "description": "Komandor Pirx dowodzi statkiem „Goliat” w eksperymentalnym locie wokół Saturna, mając w załodze androidy."
            "Musi ocenić ich przydatność, rywalizując z maszynową perfekcją. "
            "W trakcie lotu narasta napięcie, niepewność i podejrzliwość, a drobne sygnały zaczynają wskazywać, że ktoś celowo prowadzi statek ku niebezpiecznej sytuacji."
            "Pirx musi zmierzyć się nie tylko z zagrożeniem technicznym, lecz także z psychologiczną grą, w której stawką jest życie ludzi i przyszłość lotów kosmicznych.",
        "genere": "Pirx, science fiction, android, sztuczny człowiek, robot, AI, gra psychologiczna, pojedynek umysłów, ludzka niedoskonałość, napięcie, przyszłe losy, intuicja, korporacje",
        "year": 1966,
    },
    {
        "id": 20,
        "book": "Dzienniki gwiazdowe",
        "name": "Dzienniki gwiazdowe",
        "description": "Humorystycznych i satyryczne opowiadania science fiction, których bohaterem i narratorem jest Ijon Tichy – podróżnik kosmiczny, odkrywca i filozof-amator."
        "W kolejnych wyprawach odwiedza on odległe planety i obce cywilizacje, które z pozoru wydają się egzotyczne,"
        "lecz w rzeczywistości stanowią krzywe zwierciadło ludzkiego świata."
        "Każda podróż jest pretekstem do ośmieszenia wad człowieka oraz absurdów cywilizacji, takich jak biurokracja, militaryzm, fanatyzm ideologiczny,"
        "bezrefleksyjna wiara w postęp techniczny czy skłonność do tworzenia skomplikowanych, nielogicznych systemów społecznych."
        "Lem posługuje się groteską, absurdem i ironią,",
        "genere": "Ijon Tichy, satyra, komedia, humor, absurd, ośmieszanie, krzywe zwierciadło, karykaturalna, komedia",
        "year": 1966,
    }
]



QDRANT_COLLECTION_NAME = "lem_books"



def init_collection(client, books):
    """
    Tworzy kolekcję i wstawia książki, jeśli kolekcja nie istnieje
    """
    if not client.collection_exists(collection_name=QDRANT_COLLECTION_NAME):
        # print("Tworzę kolekcję")
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )

        points = [
            PointStruct(
                id=idx,
                vector=get_embedding(f'{book["name"]} {book.get("genere","")}'),
                payload=book
            )
            for idx, book in enumerate(books)
        ]

        client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points
        )

def search_books(client, query, top_k=1):
    """
    Szuka w kolekcji Qdrant po embeddingu query
    Zwraca listę payloadów (książki)
    """
    q_emb = get_embedding(query)
    results = client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=q_emb,
        limit=top_k
    )
    # zwracamy listę tuple: (payload, score)
    return [(r.payload,
            r.score)
            for r in results]

def print_top_result(results):
    """
    Prosty helper do pokazania wyniku w konsoli
    """
    if results:
        top = results[0]
        print('TYTUŁ:', top["name"])
        print('KSIĄŻKA:', top["book"])
        print('OPIS FABUŁY:', top.get('description', 'brak'))
        print('GENRE:', top.get("genere", "brak"))