#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Weryfikacja listy testow EdSharpNG wobec KODU.

Kazdy komunikat cytowany w liscie musi istniec jako literal w EdSharp.cs.
Kazdy skrot cytowany w liscie musi byc zarejestrowany w CreateMenuItem albo
obsluzony w Handle*Key. Kontrola negatywna: celowo bledne cytaty MUSZA oblac,
inaczej test przechodzi zawsze i nic nie dowodzi.
"""
import re, sys, pathlib

REPO = pathlib.Path("/mnt/d/projekty/edsharp-pr")
CS = (REPO / "EdSharp.cs").read_text(encoding="utf-8", errors="replace")
HOT = (REPO / "Hotkeys.ini").read_text(encoding="utf-8", errors="replace")
LISTA = (REPO / "testy/EdSharpNG_testy_5.0-5.0.21.md").read_text(encoding="utf-8")

# Wersja kodu BEZ komentarzy liniowych.  Bez tego trafienie w komentarzu
# ("a bare \"Removed\" is ambiguous...", "crashed the Control+H HTML") udaje
# realny literal i daje falszywy alarm - zmierzone.
CS_KOD = "\n".join(
    ("" if l.lstrip().startswith("//") else re.sub(r"//.*$", "", l))
    for l in CS.splitlines()
)

# --- komunikaty cytowane w liscie testow (musza byc literalami w kodzie) ---
KOMUNIKATY = [
    "No headings!", "Last heading!", "First heading!",
    "Last heading at this level!", "First heading at this level!",
    "Above ", "Below ", ", heading ", "Heading ",
    "Document Navigation", "Enter goes to the heading",
    "Last bookmark!", "First bookmark!", "No bookmark!", "Bookmark removed",
    "Bookmarks",
    "Numbered file ", "Numbered Files", "No numbered files are assigned!",
    "Opening ", "No disk file is open for this command!",
    "Word wrap", "Unwrap", "Guard", "Clear formatting",
    "Toggle bulleted list", "Toggle numbered list", "Insert Markdown link",
    "List copied",
    "Preview", "Preview detached", "Editing", "Synced", "Detached",
    "Elements list", "No link at cursor",
    "Removed from list", "List is now empty", "This is a folder, not a file",
    "Deleted from disk", "Delete canceled",
    "Close Window",
]
# celowo bledne - MUSZA oblac (kontrola waznosci testu)
KOMUNIKATY_KONTROLA = ["Removed", "No items", "Not a file", "Spis tresci", "Returning"]

# --- chordy cytowane w liscie: (chord, skad ma pochodzic) ---
# 'menu' = CreateMenuItem, 'handler' = obslugiwane w Handle*Key (bez wpisu w menu)
CHORDY_MENU = [
    ("F6", "Document Navigation ..."),
    ("Shift+F6", "Go to Contents"),
    ("Control+F6", "Search for Topic ..."),
    ("Alt+F6", "Search for Topic Again"),
    ("Control+Shift+F12", "Go to Section"),
    ("Control+Enter", "Section Break"),
    ("Control+Shift+Enter", "Trim Blanks"),
    ("Control+PageDown", "Next Section"),
    ("Control+PageUp", "Prior Section"),
    ("Control+Shift+PageDown", "Next Section at Same Level"),
    ("Control+Shift+PageUp", "Prior Section at Same Level"),
    ("Alt+Down", "Next Sentence"),
    ("Alt+Up", "Prior Sentence"),
    ("Control+Down", "Next Paragraph"),
    ("Control+Up", "Prior Paragraph"),
    ("Alt+Right", "Next Chunk"),
    ("Alt+Left", "Prior Chunk"),
    ("Alt+PageDown", "Next Part"),
    ("Alt+PageUp", "Prior Part"),
    ("Control+K", "Set Bookmar&k"),
    ("Control+Shift+K", "Clear Bookmark"),
    ("Alt+K", "Go to Bookmark"),
    ("Shift+PageDown", "Next Bookmark"),
    ("Shift+PageUp", "Prior Bookmark"),
    ("Alt+Shift+F2", "Numbered Files ..."),
    ("Control+F4", "&Close Window"),
    ("Control+Shift+F4", "Close All but Current Window"),
    ("Alt+F9", "Append from Clipboard"),
    ("Control+F9", "Compiler"),
    ("Control+F12", "&Word Wrap"),
    ("Alt+Shift+F6", "Baseline ..."),
    ("Alt+Shift+F10", "Reset Configuration"),
    ("Control+Shift+F6", "Format Code"),
    ("Control+F2", "Next Baseline"),
    ("Control+Shift+F2", "Prior Baseline"),
    ("Control+Alt+D0", "Go to Special Folder"),
    ("F7", "Spell Check"),
    ("Control+F7", "Guard Document"),
    ("Control+Shift+F7", "No Guard"),
    ("Control+Shift+C", "Copy Rich Text"),
    ("Alt+C", "Copy Append"),
    ("Alt+X", "Cut Append"),
    ("Control+Space", "Select Chunk"),
    ("Shift+Back", "Chunk"),
    ("Alt+R", "Recent Files ..."),
    ("Alt+L", "List Favorites ..."),
    ("Control+&L", "Set Favorite"),
    ("Control+Shift+L", "Clear Favorite"),
    ("Alt+Home", "Home Character"),
    ("Alt+End", "End Character"),
    ("Alt+T", "Topic"),
    ("Alt+Shift+T", "Text Contents"),
    ("F2", "Special Character ..."),
    ("F4", "Current Windows ..."),
    ("Shift+F4", "Windows Open"),
    ("F1", "Documentation"),
    ("Control+F1", "Key Describer"),
    ("Alt+Shift+H", "Hotkey Summary"),
]

def menu_map():
    d = {}
    for m in re.finditer(r'CreateMenuItem\("([^"]*)",\s*"([^"]*)"', CS):
        # pomin zakomentowane linie
        start = CS.rfind("\n", 0, m.start()) + 1
        if CS[start:m.start()].lstrip().startswith("//"):
            continue
        d[m.group(1)] = m.group(2)
    return d

MENU = menu_map()
wyniki = []

def spr(nazwa, warunek):
    wyniki.append((bool(warunek), nazwa))

# 1. komunikaty obecne w kodzie
for s in KOMUNIKATY:
    spr("komunikat w kodzie: %r" % s, ('"%s"' % s) in CS)

# 2. kontrola waznosci: stare/nieistniejace komunikaty MUSZA byc nieobecne
for s in KOMUNIKATY_KONTROLA:
    spr("KONTROLA (musi byc NIEOBECNY): %r" % s, ('"%s"' % s) not in CS_KOD)

# 3. chordy: nazwa komendy istnieje i ma DOKLADNIE ten chord
for chord, nazwa in CHORDY_MENU:
    got = MENU.get(nazwa)
    spr("chord %s -> %r (kod: %r)" % (chord, nazwa, got), got == chord)

# 4. kontrola waznosci chordow: stare przypisania MUSZA byc nieaktualne
for chord, nazwa in [("Alt+7", "Append from Clipboard"), ("Alt+0", "Compiler"),
                     ("Control+W", "&Word Wrap"), ("Alt+Shift+D6", "Baseline ..."),
                     ("F6", "Go to Section"), ("Control+D4", "Format Code")]:
    spr("KONTROLA (stary chord NIE obowiazuje): %s != %r" % (chord, nazwa),
        MENU.get(nazwa) != chord)

# 5. chordy obslugiwane w handlerach, nie w menu (nie moga byc w CreateMenuItem)
for chord_opis, wzor in [
    ("Control+W (Close Window, handler)", r"keyData != \(Keys\.Control \| Keys\.W\)"),
    ("Alt+cyfra (pliki numerowane)", r"HandleFileSlotKey"),
    ("Control+cyfra (okna)", r"HandleWindowNumberKey"),
    ("Control+Shift+cyfra (naglowki/listy)", r"HandleEditorFormattingKey"),
    ("Control+Alt+strzalki (przenoszenie sekcji)", r"HandleSectionMoveKey"),
    ("F7 w podgladzie (lista elementow)", r"keyCodeF7 == Keys\.F7"),
]:
    spr("handler obsluguje: %s" % chord_opis, re.search(wzor, CS) is not None)

# 6. parser naglowkow JEST fence-aware (twierdzenie testu 1.9 i 2.6)
body = CS[CS.find("GetMarkdownSectionHeadings(string"):]
body = body[:body.find("} // GetMarkdownSectionHeadings")]
spr("parser naglowkow pomija bloki kodu (fence)", "MarkdownReview_FindFenceRanges" in body)

# 7. Ctrl+H usuniete (twierdzenie testu 7.8)
spr("Control+H NIE jest zadnym skrotem",
    "Control+H" not in CS_KOD and "Control+&H" not in CS_KOD)
spr('KONTROLA: brak komendy "HTML Format"', '"HTML Format"' not in CS_KOD)

# 8. F6 i przeniesiony Go to Section opisane w Hotkeys.ini (mowiony opis)
spr("Hotkeys.ini: Document Navigation=F6", re.search(r"^Document Navigation=F6,", HOT, re.M) is not None)
spr("Hotkeys.ini: Go to Section=Control+Shift+F12", re.search(r"^Go to Section=Control\+Shift\+F12,", HOT, re.M) is not None)
spr("Hotkeys.ini: zdania NIE obiecuja, ze EdSharp czyta",
    re.search(r"^Next Sentence=Alt\+DownArrow, [^\n]*screen reader reads it", HOT, re.M) is not None)

# 9. pole pamieci miejsca w drzewie (test 1.7)
spr("pamiec miejsca w drzewie F6", "DocumentNavigationLastOffset" in CS)

# 10. lista testow nie cytuje komunikatu, ktorego w kodzie nie ma
cytaty = set(re.findall(r'"([A-Z][^"\n]{2,60})"', LISTA))
# Cytaty zlozone (komunikat + wstawiona nazwa pliku/cyfra) sprawdzamy po
# STALEJ czesci, bo pelnego zdania w kodzie nie ma i byc nie moze.
POMIN = {"Otwórz za pomocą", "Zawsze używaj tej aplikacji", "Akapit z listą",
         "EdSharp przeczyta", "HTML Format",
         "Parafia Wszystkich Świętych oraz żarówka"}
CZLONY = {"Above": "Above ", "Below": "Below ", "Heading 3": "Heading ",
          "Instalacja, heading 3": ", heading ",
          "Installation, heading 3": ", heading ",
          "Opening": "Opening ",
          "Numbered file 3 is empty!": " is empty!",
          "Numbered file 3 not found!": " not found!",
          "Numbered file 3 is nazwa.md": "Numbered file "}
# "Removed" wystepuje w liscie SWIADOMIE jako komunikat HISTORYCZNY
# ("dawniej mowil samo Removed") - jego BRAK w kodzie jest dowodem naprawy,
# nie bledem listy.  Sprawdzane osobno nizej.
POMIN.add("Removed")
brakujace = []
for c in sorted(cytaty):
    if c in POMIN:
        continue
    szukaj = CZLONY.get(c, c)
    if ('"%s"' % szukaj) not in CS_KOD:
        brakujace.append(c)
spr("kazdy cytat z listy ma pokrycie w kodzie (brakuje: %s)" % (brakujace or "nic"), not brakujace)

ok = sum(1 for w, _ in wyniki if w)
print("WYNIK: %d/%d PASS" % (ok, len(wyniki)))
for w, n in wyniki:
    if not w:
        print("  FAIL: %s" % n)
sys.exit(0 if ok == len(wyniki) else 1)
