# Test za pripremanje ispita

Generalna quiz aplikacija za pripremu ispita. Oblasti i pitanja se automatski učitavaju iz JSON fajla.

Na prvoj stranici se bira test. Dostupni testovi su navedeni u `tests.json` (naslov, opis i JSON fajl s pitanjima). Novi test se dodaje tako da se doda JSON fajl s pitanjima i novi zapis u `tests.json`. Statistika i historija pitanja vode se zasebno za svaki test.

Test „FULL Test Grad“ objedinjuje 5 propisa (355 pitanja); izvori i napomene su u `izvori/IZVORI.md`.

Svaki test sadrži 10 nasumičnih pitanja sa garantovanim najmanje jednim pitanjem iz svake oblasti.

---

## Napomena

Sva pitanja i odgovori u ovoj aplikaciji su **generisani korištenjem Claude AI agenata**.

**Ovo NISU zvanična ispitna pitanja.** Aplikacija služi isključivo kao pomoćno sredstvo za pripremu i učenje relevantnog materijala. Ne garantujemo tačnost informacija - uvijek provjerite sa originalnim izvorima. Autor ne odgovara za sadrzaj.
