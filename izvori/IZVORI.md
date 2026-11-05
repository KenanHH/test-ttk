# Izvori za „FULL Test Grad“

Test `questions-answers-propisi-ispit.json` (355 pitanja) pokriva cijele propise iz oglasa. Svako pitanje ima u polju `obrazlozenje` navedene član i stav na kojima se temelji. Pitanja su pisana isključivo prema tekstovima iz ovog foldera, a zatim je svaki odgovor provjeren slijepo (odgovori iz teksta bez uvida u ključ).

> Ovo NISU zvanična ispitna pitanja. Tekstovi iz ovog foldera su kopije s javnih stranica i nisu zvanični prečišćeni tekstovi, pa provjerite sa službenim glasilima.

| Oblast u testu | Pitanja | Propis | Izvor | Datoteka |
|---|---|---|---|---|
| Zakon o upravnom postupku FBiH | 120 | ZUP FBiH, Sl. novine FBiH 2/98, 48/99, 61/22 | https://www.paragraf.ba/propisi/fbih/zakon-o-upravnom-postupku.html | `zup-fbih.txt` |
| Zakon o eksproprijaciji FBiH | 70 | Sl. novine FBiH 70/07, 36/10, 25/12, 8/15 (odluka US), 34/16 | https://www.paragraf.ba/propisi/fbih/zakon-o-eksproprijaciji.html | `zakon-o-eksproprijaciji-fbih.txt` |
| Zakon o državnoj službi u TK | 90 | Sl. novine TK 11/2024 (prečišćeni tekst) | https://www.paragraf.ba/propisi/tuzlanskog-kantona/zakono-drzavnoj-sluzbi-u-tuzlanskom-kantonu.html | `zakon-o-drzavnoj-sluzbi-tk.txt` |
| Odluka o raspolaganju nekretninama Grada Tuzla | 45 | Odluka o uvjetima i načinu pribavljanja i raspolaganja nekretninama u vlasništvu Grada Tuzla, Sl. glasnik Grada Tuzla 5/19, 6/19, 4/21, 9/22, 2/23, 9/23, 3/26 | vidi dolje | `odluka-grad-tuzla-nekretnine-konsolidovano.txt`, `odluka-grad-tuzla-izmjene-pregled.md` |
| Pravilnik o javnom konkursu za raspolaganje nekretninama | 30 | Pravilnik o postupku javnog konkursa za raspolaganje nekretninama u vlasništvu Federacije BiH, kantona, općina i gradova, Sl. novine FBiH 17/14 (5.3.2014., br. 02-02-2-759/14) | službeni PDF broja 17/14 (https://www.sluzbenenovine.ba/page/i/bRXEpvBizgw=, uz prijavu) | `pravilnik-javni-konkurs-17-14.txt`, `pravilnik-javni-konkurs-17-14-sl-novine-fbih.pdf` |

## Odluka Grada Tuzla: službeni glasnici

Svi na https://grad.tuzla.ba/wp-content/uploads/2014/11/ :

- 5/19 (osnovni tekst, čl. 1-41): `SLUZBENI-GLASNIK-TUZLA-5-2019.pdf`
- 6/19: `SLUZBENI-GLASNIK-TUZLA-6-2019.pdf`
- 4/21: `SLUZBENI-GLASNIK-TUZLA-4-2021-FINAL-STAMPA.pdf`
- 9/22: `SLUZBENI-GLASNIK-TUZLA-9-22-FINAL-STAMPA.pdf`
- 2/23: `SLUZBENI-GLASNIK-2-23-FINAL-STAMPA.pdf`
- 9/23: `SLUZBENI-GLASNIK-TUZLA-9-23-FINAL-STAMPA.pdf`
- 3/26: `SG-broj-3-2026.pdf`

Službeni prečišćeni tekst Odluke nije pronađen, pa je konsolidovani tekst napravljen ručno iz osnovnog teksta i šest izmjena (svaki izmijenjeni član ima oznaku, npr. `[izmijenjen: 4/21]`). Nisu provjerena izdanja 1/2024, 12/2025, 9/2026 i 10/2026, pa kasnije izmjene nisu isključene.

## Napomene i otvorena pitanja

- **Eksproprijacija:** Odluka Ustavnog suda FBiH iz Sl. novina 8/15 (prema nepotvrđenom izvoru: čl. 31 st. 2, 3 i 5) nije označena u tekstu na paragraf.ba. Za čl. 31 (tri pitanja) važi tekst nakon izmjene 34/16. Čl. 12 st. (2)-(3) nije korišten u pitanjima.
- **Zakon o državnoj službi TK:** u tekstu su neki interni stavovi pogrešno upućeni (npr. čl. 31 st. 10, čl. 43 st. 5, čl. 95 st. 10, čl. 106); ti članovi nisu korišteni. Provjerite da je 11/2024 i dalje važeći prečišćeni tekst.
- **Pravilnik 17/14:** u službenom tekstu postoje pogrešna interna upućivanja (čl. 7 st. 2 upućuje na čl. 5 umjesto čl. 3; čl. 18 upućuje na čl. 6, 7 i 9; čl. 13 st. 2 nema jednu riječ; čl. 12 kaže „kaucije“, a ostali članovi „kapara“). Pitanja se ne oslanjaju na ta upućivanja. Stavovi (1)-(3) u čl. 7, 9, 10, 11 i 12 vraćeni su po rasporedu originala.
- **ZUP:** 35 pitanja za čl. 121-305 preuzeto je iz ranijeg testa „ZUP FBiH — glave X–XVI“ nakon ponovne provjere prema tekstu.
