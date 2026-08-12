#!/usr/bin/env bash
# Budowa EdSharpNG + instalatora Inno Setup na Garfieldzie, BEZ maszyny glownej.
#
# Uzycie:
#   ./build_installer_garfield.sh 5.0.2
#
# Wynik:
#   dist/EdSharpNG_Setup_<wersja>.exe
#
# Wymaga (sprawdzone 13.08.2026 na Garfieldzie):
# - Windows .NET Framework csc.exe + jsc.exe (sa w C:\Windows\Microsoft.NET),
# - UIAutomationProvider/Types w GAC,
# - Inno Setup 6 per-user: C:\Users\g\AppData\Local\Programs\Inno Setup 6,
# - uruchomienie z WSL, repo na /mnt/d/projekty/edsharp-pr.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="${1:-}"
STAGE="/mnt/c/EdSharp"
ISCC="/mnt/c/Users/g/AppData/Local/Programs/Inno Setup 6/ISCC.exe"
LOG_BUILD="$ROOT/BuildEdSharp.log"
LOG_ISCC="/tmp/edsharp-iscc-${VERSION:-brak}.log"

if [[ -z "$VERSION" || ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Uzycie: $0 <wersja, np. 5.0.2>" >&2
    exit 2
fi
if [[ ! -x /mnt/c/Windows/System32/cmd.exe ]]; then
    echo "BLAD: brak cmd.exe Windows pod /mnt/c/Windows/System32/cmd.exe" >&2
    exit 1
fi
if [[ ! -x "$ISCC" ]]; then
    echo "BLAD: brak Inno Setup: $ISCC" >&2
    echo "Zainstaluj: winget install --id JRSoftware.InnoSetup -e" >&2
    exit 1
fi

cd "$ROOT"
echo "[1/5] Budowa EdSharpNG.exe i EdSharp.dll..."
/mnt/c/Windows/System32/cmd.exe /c BuildEdSharp.cmd
if grep -aEq 'error (CS|JS)[0-9]+' "$LOG_BUILD"; then
    echo "BLAD kompilacji - patrz $LOG_BUILD" >&2
    grep -aE 'error (CS|JS)[0-9]+' "$LOG_BUILD" >&2 || true
    exit 1
fi
[[ -s EdSharpNG.exe && -s EdSharp.dll ]] || {
    echo "BLAD: build nie utworzyl EdSharpNG.exe/EdSharp.dll" >&2
    exit 1
}

# Nie wydawaj dwoch roznych buildow pod tym samym numerem.
OUT="$ROOT/dist/EdSharpNG_Setup_${VERSION}.exe"
if [[ -e "$OUT" ]]; then
    echo "BLAD: $OUT juz istnieje. Podbij wersje." >&2
    exit 1
fi

echo "[2/5] Staging do C:\\EdSharp (SourceDir zaszyty w .iss)..."
rm -rf "$STAGE"
mkdir -p "$STAGE"
# Kopiujemy sledzone pliki, zeby staging nie dostal .git, logow ani starych buildow.
while IFS= read -r -d '' rel; do
    src="$ROOT/$rel"
    dst="$STAGE/$rel"
    mkdir -p "$(dirname "$dst")"
    cp -a "$src" "$dst"
done < <(git ls-files -z)
# Artefakty buildu sa ignorowane, ale wymagane przez instalator.
cp -a EdSharpNG.exe EdSharp.dll "$STAGE/"
# Zasoby pobrane best-effort przez BuildEdSharp.cmd (ignorowane przez git).
for rel in Ude.dll Convert; do
    [[ -e "$ROOT/$rel" ]] && cp -a "$ROOT/$rel" "$STAGE/"
done

# Wersje zmieniamy TYLKO w stagingu - build nie brudzi repo.
python3 - "$STAGE/EdSharp_Setup.iss" "$VERSION" <<'PY'
import re, sys
path, ver = sys.argv[1], sys.argv[2]
raw = open(path, 'rb').read()
# Zachowaj CRLF i kodowanie bajt-w-bajt; wersje sa ASCII.
for key in (b'AppVersion', b'VersionInfoVersion'):
    raw, n = re.subn(rb'(?m)^' + key + rb'=.*?\r?$', key + b'=' + ver.encode(), raw)
    if n != 1:
        raise SystemExit(f'BLAD: oczekiwano jednej linii {key.decode()}, znaleziono {n}')
open(path, 'wb').write(raw)
PY

echo "[3/5] Kontrola wymaganych plikow instalatora..."
python3 - "$STAGE" <<'PY'
import os, re, sys
stage = sys.argv[1]
iss = open(os.path.join(stage, 'EdSharp_Setup.iss'), encoding='utf-8', errors='replace').read()
missing = []
for line in iss.splitlines():
    s = line.strip()
    if s.startswith(';') or 'Source:' not in s or 'skipifsourcedoesntexist' in s.lower():
        continue
    m = re.search(r'Source:\s*"([^"]+)"', s)
    if not m:
        continue
    rel = m.group(1).replace('\\', '/')
    if '*' in rel:
        continue
    if not os.path.isfile(os.path.join(stage, rel)):
        missing.append(rel)
if missing:
    raise SystemExit('BLAD: brak wymaganych plikow: ' + ', '.join(missing))
print('Wszystkie wymagane pliki sa obecne.')
PY

echo "[4/5] Kompilacja instalatora Inno Setup $VERSION..."
"$ISCC" 'C:\EdSharp\EdSharp_Setup.iss' >"$LOG_ISCC" 2>&1
if ! grep -q 'Successful compile' "$LOG_ISCC"; then
    echo "BLAD Inno Setup - patrz $LOG_ISCC" >&2
    tail -30 "$LOG_ISCC" >&2
    exit 1
fi

mkdir -p "$ROOT/dist"
cp -a "$STAGE/EdSharpNG_Setup.exe" "$OUT"

echo "[5/5] Weryfikacja swiezosci i tozsamosci binarki..."
cmp -s "$ROOT/EdSharpNG.exe" "$STAGE/EdSharpNG.exe" || {
    echo "BLAD: staging zawiera inna binarke niz swiezy build" >&2
    exit 1
}
[[ "$OUT" -nt "$ROOT/EdSharpNG.exe" ]] || {
    echo "BLAD: instalator nie jest nowszy niz binarka" >&2
    exit 1
}

sha256sum "$ROOT/EdSharpNG.exe" "$OUT"
echo "GOTOWE: $OUT"
