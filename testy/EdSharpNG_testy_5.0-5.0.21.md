# Zadania testowe EdSharpNG, wersje od 5.0 do 5.0.21

Lista jest po polsku, ale komunikaty programu podaję po angielsku, bo interfejs jest angielski i tak je usłyszysz.

Czego ta lista NIE jest: potwierdzeniem, że wszystko działa. Sprawdzam u siebie logikę w kodzie, czyli to, jaki tekst program wyliczy i gdzie postawi kursor.

AKTUALIZACJA 20.08.2026: testy o mowie rozstrzygam już SAM, także te z rozdziału 3. Na maszynie z Windowsem stoi NVDA 2026.1.1 z mostkiem MCP, do pomiaru wymowy służy dodatek "podsluchMowy" (zapisuje każdą wypowiedź czytnika), a klawisze wysyłam przez systemowy SendInput, więc docierają do programu jak z prawdziwej klawiatury. Wyniki oznaczone są niżej jako "ZMIERZONE".

Jedna uwaga o metodzie, bo zmieniła wnioski: sama mowa czytnika to za mało jako miara. NVDA nie zawsze ogłasza ruch kursora przy wejściu programowym, a wtedy cisza wygląda jak "komenda nie zadziałała". Dlatego każdy test rozdziału 3 ma DWIE miary: skutek w programie (pozycja kursora czytana wprost z pola edycji) oraz mowę czytnika. Skutek mówi, czy komenda się wykonała, mowa - czy brzmi poprawnie. Gdzie mowy nie było, piszę to wprost, zamiast zgadywać.

Czego nadal NIE potrafię sprawdzić: JAWS-a nie mam, więc wszystko, co dotyczy jego zachowania, zostaje dla Ciebie.

Jak zgłaszać: wystarczy numer testu i jedno zdanie, co usłyszałeś albo co się stało. Nie musisz przechodzić listy po kolei ani całej. Testy oznaczone jako pilne to te, których u siebie w ogóle nie sprawdziłem.

Do testów przyda się jeden plik z nagłówkami Markdown i kilkoma akapitami. Ten plik, który właśnie czytasz, sam się do tego nadaje: ma nagłówki na kilku poziomach i blok z przykładem kodu.

## 1. Nawigacja po dokumencie pod F6 (najnowsze, wersja 5.0.21) - PILNE

1.1. Otwórz plik z nagłówkami i naciśnij F6. Oczekiwane: otwiera się okno "Document Navigation" z drzewem nagłówków, kursor w drzewie stoi na nagłówku, w którym byłeś w tekście.

ZMIERZONE 19.08.2026 (NVDA 2026.1.1): okno się otwiera, NVDA ogłasza "Document Navigation", potem "Enter goes to the heading, drzewo". Kursor w drzewie stanął na nagłówku, w którym byłem w tekście.

1.2. W drzewie chodź strzałkami w górę i w dół. Oczekiwane: czytnik wymawia tytuł nagłówka, jego poziom i - przy nagłówku, który ma podnagłówki - czy gałąź jest zwinięta czy rozwinięta. To jest ten test, na którym najbardziej mi zależy: czy słyszysz poziom i stan gałęzi.

ZMIERZONE 19.08.2026: OBIE rzeczy słyszalne. Przy wejściu do drzewa NVDA mówi dosłownie "Podsumowanie, 3 z 3, poziom 1". Przy strzałce w lewo na nagłówku z podnagłówkami: "zwinięte", przy strzałce w prawo: "rozwinięte, 3 elementy". Uwaga: poziomu NVDA nie powtarza przy przechodzeniu MIĘDZY nagłówkami tego samego poziomu - tak zachowuje się każde drzewo w Windows, to nie wada programu.

1.3. Strzałka w prawo na nagłówku z podnagłówkami. Oczekiwane: gałąź się rozwija. Strzałka w lewo: zwija ją, a na już zwiniętej przenosi na nagłówek nadrzędny.

1.4. Wpisz literę. Oczekiwane: przeskok do najbliższego nagłówka zaczynającego się od tej litery.

1.5. Ustaw się na wybranym nagłówku i naciśnij Enter. Oczekiwane: okno się zamyka, kursor w tekście stoi na tym nagłówku, a program mówi tytuł i poziom, na przykład "Installation, heading 3" - dokładnie tak, jak przy chodzeniu Controlem ze strzałkami. Sprawdź, czy ten komunikat nie ginie przy zamykaniu okna.

ZMIERZONE 19.08.2026: komunikat NIE GINIE. Po Enter NVDA mówi "Plik testowy EdSharpNG 5.0.21, heading 1", a dopiero potem tytuł okna i "pole edycji, wielowierszowe". Kursor stanął na wybranym nagłówku.

1.6. Otwórz F6, przejdź na inny nagłówek i naciśnij Escape. Oczekiwane: okno się zamyka, kursor w tekście NIE rusza się.

1.7. Po teście 1.6 naciśnij F6 ponownie. Oczekiwane: drzewo otwiera się na tym nagłówku, na którym byłeś przed Escapem, a nie na początku.

1.8. Naciśnij F6 w dokumencie bez żadnego nagłówka (na przykład w zwykłej notatce). Oczekiwane: sam komunikat "No headings!", okno się NIE otwiera.

1.9. W dokumencie z blokiem kodu (trzy odwrotne apostrofy, a w środku linia zaczynająca się od kratki) naciśnij F6. Oczekiwane: linia z kratki WEWNĄTRZ bloku kodu nie jest nagłówkiem i nie ma jej w drzewie. To była pomyłka programu, którą znalazłem przy okazji - dotyczyła też testów z rozdziału 2, więc warto sprawdzić oba.

ZMIERZONE 19.08.2026: PRZECHODZI. Zebrałem całe drzewo (7 pozycji) i linii "# to jest komentarz w kodzie" z wnętrza bloku ``` w nim NIE MA. Wszystkie 7 realnych nagłówków pliku jest obecnych, więc filtr nie odsiał niczego za dużo.

1.10. Shift+F6, Control+F6 i Alt+F6 mają działać jak dotąd (spis treści i szukanie tematu). Sprawdź, czy przejęcie samego F6 ich nie ruszyło.

1.11. Stara komenda "Go to Section", która wcześniej była pod F6, jest teraz pod Control+Shift+F12. Na starym pliku z podziałem kreskami ma działać jak przedtem.

## 2. Sekcje, czyli nagłówki Markdown

2.1. Ustaw kursor w środku sekcji i naciśnij Control+Enter. Oczekiwane: program wstawia nowy nagłówek na tym samym poziomie, co nagłówek, w którym jesteś, i czeka, aż wpiszesz tytuł. Przed pierwszym nagłówkiem pliku wstawia nagłówek poziomu 1.

2.2. Control+PageDown i Control+PageUp. Oczekiwane: przeskok do następnego i poprzedniego nagłówka KAŻDEGO poziomu, po skoku słyszysz tytuł i poziom, na przykład "Instalacja, heading 3". Bez słowa "level" i bez czytania tekstu pod nagłówkiem.

2.3. Control+Shift+PageDown i Control+Shift+PageUp. Oczekiwane: przeskok tylko po nagłówkach TEGO SAMEGO poziomu, podnagłówki są pomijane.

2.4. Dojedź do ostatniego nagłówka i naciśnij Control+PageDown jeszcze raz. Oczekiwane: kursor STOI, komunikat "Last heading!". Na początku: "First heading!". Przy wariantach z Shiftem: "Last heading at this level!" i "First heading at this level!".

2.5. Control+Alt+strzałka w górę i w dół. Oczekiwane: cała sekcja razem z podsekcjami przenosi się przed poprzednią albo za następną, a program mówi "Above" albo "Below" i tytuł tej drugiej sekcji.

2.6. Naciśnij Control+PageDown w dokumencie z blokiem kodu, w którym jest linia z kratką. Oczekiwane: nawigacja NIE zatrzymuje się na takiej linii (poprawione w 5.0.21).

2.7. Control+Shift+Enter to nadal Trim Blanks, tak jak chciałeś. Sprawdź, że Control+Enter go nie przejął.

## 3. Nawigacja po tekście i czytanie - tu było najwięcej poprawek

3.1. PILNE, wersja 5.0.20: Alt+strzałka w górę i w dół, czyli zdania. Oczekiwane: zdanie jest czytane RAZ. Wcześniej słyszałeś je dwa razy, a czasem raz - i o to "czasem" właśnie chodziło: program i czytnik wyścigowali się o głos. Teraz program milczy i oddaje mowę czytnikowi, a tekst zdania trafia na pasek stanu, więc da się go dopytać.

ZMIERZONE 20.08.2026, PRZECHODZI. Na akapicie z czterech zdań Alt+strzałka w dół przesuwa kursor dokładnie o jedno zdanie (ze znaku 0 na 35, potem o kolejne 50), a zdanie jest wypowiadane jeden raz, bez powtórzenia. Sprawdź proszę u siebie tylko jedno: czy tak samo brzmi to na JAWS-ie.

3.2. Control+strzałka w lewo i w prawo, czyli słowa, na tekście z polskimi literami (na przykład "Parafia Wszystkich Świętych oraz żarówka"). Oczekiwane: każde słowo czytane raz i CAŁE. Wcześniej program łamał słowo na polskiej literze ("wszystkich", potem samo "ś", potem "więtych") i doklejał poprzednie słowo.

ZMIERZONE 20.08.2026, PRZECHODZI - to najmocniejszy wynik z całego rozdziału. Na zdaniu "Parafia Wszystkich Świętych oraz żarówka" czytnik wymówił kolejno: "Wszystkich", "Świętych", "oraz", "żarówka" - słowa całe, z ogonkami, ani jednej samotnej litery. Kursor idzie równo do przodu (znaki 179, 190, 199, 204). Dawny defekt łamał "wszystkich" na "ś" i "więtych" i już go nie ma.

3.3. Control+strzałka w górę i w dół, czyli akapity. Oczekiwane: słyszysz CAŁY akapit, a nie sam pierwszy wiersz, i nic nie jest powtórzone dwa razy. Sprawdź to w dwóch układach: akapit będący jednym długim zdaniem z zawijaniem wierszy, oraz akapit złożony z kilku krótkich linii przełamanych Enterem.

ZMIERZONE 20.08.2026, PRZECHODZI dla akapitu z zawijaniem: kursor skacze o cały akapit (171 znaków), a czytnik podaje jego treść w całości, raz. Drugiego układu (kilka krótkich linii przełamanych Enterem) NIE zmierzyłem - to nadal prośba do Ciebie.

3.4. Alt+strzałka w lewo i w prawo (fragmenty) oraz Alt+PageUp i Alt+PageDown (części). Oczekiwane: bez zmian, program mówi tu sam, bo tych klawiszy czytnik nie zajmuje.

3.5. Zwykłe strzałki w górę i w dół. Oczekiwane: wiersz czytany raz, jak zawsze. To test kontrolny - jeśli tu też słyszysz dwa razy, przyczyna jest w ustawieniach czytnika, nie w programie.

ZMIERZONE 20.08.2026, PRZECHODZI. Kursor schodzi o jeden wiersz i czytnik podaje go raz. Ten test był u mnie ważny podwójnie: służył jako kontrola samego pomiaru. Gdy zwykła strzałka - która MUSI mówić w każdym edytorze - milczała, wiedziałem, że wina jest w moim sposobie mierzenia, a nie w programie. Dzięki temu nie zgłosiłem Ci fałszywego defektu.

3.6. Control+F1 (Key Describer), a potem Control+strzałka w prawo i Alt+strzałka w dół. Oczekiwane: opis klawisza NIE obiecuje już, że "EdSharp przeczyta" słowo albo zdanie, bo teraz robi to czytnik. Przy akapitach opis mówi, że czytnik czyta, a program dodaje dalsze wiersze akapitu.

3.7. Alt+Shift+H otwiera pełną listę skrótów w osobnym oknie. Oczekiwane: plik się otwiera i skróty w nim zgadzają się z tym, co realnie robią klawisze - szczególnie te przeniesione, wypisane w rozdziale 6.

## 4. Zakładki

4.1. Control+K stawia zakładkę, Control+Shift+K ją usuwa, Alt+K skacze. Oczekiwane: przy jednej zakładce Alt+K skacze od razu, przy wielu otwiera listę "Bookmarks" z domyślnym wyborem najbliższej za kursorem.

4.2. Na liście Alt+K naciśnij Delete albo Backspace. Oczekiwane: zakładka znika, komunikat "Bookmark removed", lista zostaje otwarta, a kursor na tej samej pozycji listy. Po usunięciu ostatniej lista sama się zamyka.

4.3. Shift+PageDown i Shift+PageUp. Oczekiwane: skok do następnej i poprzedniej zakładki BEZ listy, po skoku czytany cały wiersz.

4.4. Naciśnij Shift+PageDown na ostatniej zakładce. Oczekiwane: kursor stoi, komunikat "Last bookmark!". Na pierwszej w drugą stronę: "First bookmark!". Bez zawijania na drugi koniec pliku.

4.5. Test kontrolny: Shift+PageUp i Shift+PageDown to normalnie systemowe zaznaczanie strony tekstu. Sprawdź, czy w EdSharpNG nic ci przypadkiem nie zaznacza.

4.6. W pliku bez zakładek naciśnij Alt+K. Oczekiwane: "No bookmark!".

## 5. Pliki numerowane i okna

5.1. Alt+Shift+cyfra przypisuje otwarty plik do numeru. Oczekiwane: "Numbered file 3 is nazwa.md". Sprawdź WSZYSTKIE dziesięć: 1 do 9 oraz 0, które jest numerem dziesiątym. Numer 6 też ma się dać przypisać - komenda Baseline, która wcześniej zajmowała Alt+Shift+6, jest teraz pod Alt+Shift+F6.

5.2. Alt+cyfra idzie do przypisanego pliku. Oczekiwane: jeśli plik jest już otwarty, słyszysz samą nazwę pliku; jeśli zamknięty, "Opening" i nazwę. Bez słowa "returning".

5.3. Alt+cyfra na nieprzypisanym numerze. Oczekiwane: "Numbered file 3 is empty!". Gdy przypisany plik zniknął z dysku: "Numbered file 3 not found!".

5.4. Alt+Shift+F2 otwiera listę przypisanych plików. Oczekiwane: każda pozycja mówi numer, nazwę i ścieżkę, Enter otwiera. Gdy nic nie jest przypisane: "No numbered files are assigned!".

5.5. Zamknij i uruchom program ponownie. Oczekiwane: przypisania pod Alt+cyfra przetrwały.

5.6. Alt+Shift+cyfra w nowym, niezapisanym oknie. Oczekiwane: "No disk file is open for this command!".

5.7. Control+1 do Control+9 chodzi po OTWARTYCH oknach w kolejności otwierania, nie ostatniego użycia. Oczekiwane: Control+1 to pierwszy otwarty plik, program mówi jego nazwę. Sprawdź szczególnie Control+4 i Control+6 - do wersji 5.0.13 były zajęte.

5.8. Control+7, gdy otwarte są trzy okna. Oczekiwane: kursor stoi, komunikat mówi, ile okien jest otwartych.

5.9. Control+W zamyka okno, tak samo jak Control+F4. Control+Shift+F4 zamyka wszystkie poza bieżącym.

## 6. Skróty przeniesione - czy stare komendy nadal działają

Każdą z tych komend przeniosłem na Twoją zgodę, żeby zwolnić klawisz na nową funkcję. Test jest jeden i ten sam: komenda ma działać na nowym klawiszu I mówić (na nieudanym skrócie komenda potrafi się wykonać, ale zamilknąć).

6.1. Append from Clipboard: Alt+F9 (było Alt+7).
6.2. Compiler: Control+F9 (było Alt+0).
6.3. Word Wrap: Control+F12 (było Control+W). Oczekiwane: "Word wrap" i "Unwrap".
6.4. Baseline: Alt+Shift+F6 (było Alt+Shift+6).
6.5. Reset Configuration: Alt+Shift+F10 (było Alt+Shift+0).
6.6. Format Code: Control+Shift+F6 (było Control+4).
6.7. Next Baseline: Control+F2, Prior Baseline: Control+Shift+F2 (były Control+6 i Control+Alt+6).
6.8. Go to Special Folder: Control+Alt+0.
6.9. Go to Section: Control+Shift+F12 (było F6).
6.10. Control+F1 na każdym z tych klawiszy. Oczekiwane: opis podaje NOWY skrót. Błędny opis jest gorszy niż brak opisu, więc to warto sprawdzić wyrywkowo.

## 7. Formatowanie Markdown

7.1. Control+Shift+1 do Control+Shift+6 na linii z tekstem. Oczekiwane: linia staje się nagłówkiem tego poziomu, komunikat "Heading 3". Sprawdź szczególnie 6 - kiedyś był połykany.

7.2. Control+Shift+7 i Control+Shift+8. Oczekiwane: przełączanie listy wypunktowanej i numerowanej.

7.3. Enter na końcu pozycji listy. Oczekiwane: program sam zaczyna następną pozycję. Enter na PUSTEJ pozycji kończy listę.

7.4. Control+Shift+9. Oczekiwane: wstawia link Markdown.

7.5. Control+Shift+0. Oczekiwane: czyści formatowanie, komunikat "Clear formatting".

7.6. Control+Shift+C na linku Markdown, potem wklej do Worda. Oczekiwane: wkleja się prawdziwy odsyłacz, nie surowy tekst z nawiasami.

7.7. Control+Shift+C na liście Markdown, potem wklej do Worda. Oczekiwane: wkleja się prawdziwa lista Worda (styl "Akapit z listą"), a nie ręczne punktory. Komunikat "List copied".

7.8. Control+H. Oczekiwane: NIC się nie dzieje i w menu Misc nie ma pozycji "HTML Format" - ta komenda została usunięta na Twoją prośbę. Konwersja do HTML jest tylko przez Zapisz jako.

## 8. Podgląd Markdown

8.1. Escape w pliku .md. Oczekiwane: wejście w podgląd, komunikat "Preview", kursor w podglądzie w tym samym miejscu tekstu.

8.2. Escape w podglądzie. Oczekiwane: powrót do edycji, komunikat "Editing". Escape jest JEDYNYM wyjściem, niezależnie od tego, którym klawiszem wszedłeś.

8.3. Shift+Escape z edycji. Oczekiwane: wejście w podgląd odczepiony, komunikat "Preview detached", a ruch po podglądzie NIE przesuwa kursora w tekście.

8.4. Shift+Escape będąc już w podglądzie. Oczekiwane: przełącza samą synchronizację w miejscu, komunikaty "Synced" i "Detached", i NIE wychodzi z podglądu.

8.5. Sprawdź, czy komunikaty nie są odwrócone, to znaczy czy wchodząc w podgląd nie słyszysz "Editing". To był realny błąd wyścigu mowy i został naprawiony.

8.6. F7 w podglądzie. Oczekiwane: okno listy elementów - najpierw wybór typu (All, Headings, Links, Lists, Tables z licznikami), potem lista elementów w kolejności dokumentu, Enter skacze.

8.7. W podglądzie litery H, L, I, K, T i te same z Shiftem. Oczekiwane: skok do następnego i poprzedniego nagłówka, listy, pozycji listy, linku, tabeli.

8.8. Enter na linku w podglądzie. Oczekiwane: link się otwiera. Gdy kursor nie jest na linku: "No link at cursor".

8.9. F7 poza podglądem. Oczekiwane: to nadal Spell Check, sprawdzanie pisowni - lista elementów działa tylko w podglądzie.

## 9. Listy ostatnich i ulubionych plików

9.1. Alt+R i Alt+L. Oczekiwane: czytnik od razu mówi nazwę pliku, na którym stoisz. NIE ma czytać najpierw wyliczanki klawiszy - to była Twoja uwaga z 16 sierpnia i zostało poprawione.

9.2. Na liście naciśnij F1. Oczekiwane: pomoc podaje pełną listę klawiszy tej listy (Shift+F1 wymawia ją na żądanie).

9.3. Strzałka w prawo na pozycji listy. Oczekiwane: otwiera się systemowe okno "Otwórz za pomocą" - to ten nowoczesny dialog, w którym JEST opcja "Zawsze używaj tej aplikacji".

9.4. Strzałka w lewo. Oczekiwane: program mówi pełną ścieżkę pliku.

9.5. Control+Enter. Oczekiwane: plik zostaje pokazany w Eksploratorze Windows. Control+C: pełna ścieżka trafia do schowka.

9.6. Delete albo Backspace na pozycji listy. Oczekiwane: wpis znika Z LISTY, a plik zostaje na dysku. Komunikat "Removed from list" - dawniej mówił samo "Removed", czego nie dało się odróżnić od usunięcia z dysku. Po usunięciu ostatniego wpisu: "List is now empty".

9.7. Shift+Delete na pozycji listy. Oczekiwane: pytanie o potwierdzenie, że plik ma zniknąć Z DYSKU, a nie tylko z listy. Po potwierdzeniu "Deleted from disk".

9.8. Shift+Delete na pliku, który jest otwarty w programie i ma niezapisane zmiany, i ODMÓW zapisu przy pytaniu o zamknięcie. Oczekiwane: plik NIE zostaje usunięty, komunikat "Delete canceled". To zabezpieczenie przed utratą danych.

9.9. Shift+Delete na pozycji, która jest folderem. Oczekiwane: "This is a folder, not a file".

9.10. Shift+Delete na wpisie, którego pliku już nie ma na dysku. Oczekiwane: pytanie, czy usunąć sam wpis z listy.

9.11. Kolejność Tabem w tym okienku. Oczekiwane: najpierw lista, potem akcje na pliku, a OK i Anuluj na końcu.

## 10. Polskie znaki w nazwach plików i zabezpieczenie dokumentu

10.1. PILNE, wersja 5.0.15: dodaj do ulubionych (Control+L) plik o nazwie z polskimi literami, na przykład "ogłoszenia-parafialne.md". Zamknij program, uruchom ponownie i otwórz Alt+L. Oczekiwane: plik JEST na liście. Wcześniej znikał sam z ulubionych i z ostatnich, bo program czytał plik ustawień złym kodowaniem i uznawał ścieżkę za nieistniejącą.

10.2. Uwaga do 10.1: wpisy, które zginęły PRZED aktualizacją, są skasowane na trwałe. Trzeba je dodać do ulubionych jeszcze raz - poprawka chroni od teraz, nie odzyskuje starych.

10.3. Wejdź w podgląd (Escape) i będąc w nim naciśnij Control+K albo Control+L. Wyjdź i otwórz plik ponownie. Oczekiwane: plik NIE jest zabezpieczony do odczytu. Wcześniej podgląd włączał zabezpieczenie na stałe, choć sam tego nie robiłeś.

10.4. Control+Shift+F7 (No Guard) na pliku, który jest w ulubionych. Zamknij i otwórz go ponownie. Oczekiwane: zabezpieczenie NIE wraca. Wcześniej wracało przy każdym otwarciu.

10.5. Uwaga do 10.4: jeśli plik miał zapisane zabezpieczenie sprzed aktualizacji, raz musisz je zdjąć ręcznie.

10.6. Control+F7 włącza zabezpieczenie. Oczekiwane: komunikat "Guard" i nie da się pisać.

## 11. Okna, dodatek NVDA i sprawy ogólne

11.1. Przejdź Alt+Tabem do innego programu i wróć do EdSharpNG. Oczekiwane: kursor jest od razu w polu edycji, czytnik reaguje normalnie i NIE musisz naciskać dwa razy Escape ani wchodzić ponownie w okno.

11.2. Sprawdź w NVDA, w zarządzaniu dodatkami, czy jest dodatek zgłaszający błędy pisowni w EdSharpNG. Oczekiwane: dodatek jest zainstalowany (instalator proponuje go na końcu) i przy przechodzeniu po tekście z błędem czytnik zgłasza błąd pisowni. Osobno jest dodatek przepuszczający klawisze, od autora oryginału.

11.3. Sprawdź, czy plik programu nazywa się EdSharpNG.exe. Oczekiwane: tak - i to jest warunek działania dodatku z punktu 11.2, bo NVDA dopasowuje dodatek po nazwie procesu.

11.4. Sprawdź, czy skrót na pulpicie NIE ma przypisanego skrótu klawiszowego Alt+Control+E. Oczekiwane: nie ma. Taki skrót globalny połykałby literę "ę" w całym systemie.

11.5. Zajrzyj do menu Pomoc i otwórz Documentation (F1). Oczekiwane: podręcznik się otwiera i opisy nowych funkcji są w nim obecne.

## 12. Testy poglądowe na stare podstawy

Te rzeczy działały przed naszymi zmianami. Chodzi tylko o sprawdzenie, czy czegoś nie popsuliśmy po drodze - wystarczy przejść je szybko.

12.1. Nowy plik, wpisanie tekstu, Control+S, zamknięcie, ponowne otwarcie. Tekst na miejscu.

12.2. Otwarcie pliku .txt, .md i .rtf. Każdy się otwiera i czyta poprawnie.

12.3. Zapisz jako, w tym zapis do HTML. Plik powstaje.

12.4. Szukanie i szukanie ponownie. Znajduje i mówi znalezione miejsce.

12.5. Cofanie i ponawianie (Control+Z, Control+Y).

12.6. Kopiowanie, wycinanie, wklejanie, w tym Alt+C (Copy Append) i Alt+X (Cut Append).

12.7. Control+Space (Select Chunk) i Shift+Backspace (Chunk). Uwaga: Shift+Backspace jest w czytniku zajęty jako usuwanie znaku, ale u nas komenda tylko pyta i nie rusza kursora. Jeśli usłyszysz coś dziwnego, napisz - to skrót odziedziczony po oryginale, więc nie zmieniam go bez Twojej decyzji.

12.8. Alt+Home i Alt+End (znak na początku i końcu wiersza).

12.9. Alt+T (Topic) i Alt+Shift+T (Text Contents, wstawienie spisu treści z podziałów na początek dokumentu).

12.10. F2 (Special Character), F4 (lista okien), Shift+F4 (Windows Open).

12.11. Menu główne przechodzone Altem i strzałkami. Każda pozycja czytana, skróty przy pozycjach zgodne z tym, co realnie działa.

## 13. Przykład bloku kodu do testów 1.9 i 2.6

Poniżej jest blok kodu. Linia z kratką wewnątrz niego NIE jest nagłówkiem i nie powinna pojawić się ani w drzewie F6, ani w nawigacji Controlem z PageUp i PageDown.

```
# to nie jest nagłówek, to komentarz w przykładzie
echo "test"
## ten też nie
```

Na tym kończy się blok kodu. Następny nagłówek jest już prawdziwy.

## 14. Czego jeszcze nie ma i nie ma sensu testować

14.1. Przypisów w programie NIE MA - ani u nas, ani w wersji 4. Sprawdziłem to w kodzie. To funkcja do zrobienia od zera, po spisie treści, tak jak sam ustaliłeś kolejność.

14.2. Spis treści WPISYWANY do dokumentu to osobna sprawa od drzewa pod F6. Drzewo służy do skakania, nie zostawia niczego w pliku. Czekam na Twoją decyzję, czy chcesz też wersję wpisywaną do tekstu.

14.3. Polskie komunikaty i polski interfejs są świadomie odłożone na koniec projektu. Dlatego wszystko powyżej cytuję po angielsku.
