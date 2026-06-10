#!/usr/bin/env python3
"""Generate a ~25 page study summary PDF of Zakon o upravnom postupku FBiH."""

from fpdf import FPDF


class ZUPSummaryPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("ArialUni", size=8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Zakon o upravnom postupku FBiH — Rezime za učenje", align="C")
            self.ln(5)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("ArialUni", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Stranica {self.page_no()}/{{nb}}", align="C")

    def title_page(self):
        self.add_page()
        self.ln(40)
        self.set_font("ArialUni", "B", 28)
        self.set_text_color(0, 51, 102)
        self.multi_cell(0, 14, "ZAKON O UPRAVNOM\nPOSTUPKU FBiH", align="C")
        self.ln(8)
        self.set_font("ArialUni", "B", 18)
        self.set_text_color(0, 102, 153)
        self.cell(0, 12, "Rezime za učenje", align="C")
        self.ln(15)
        self.set_font("ArialUni", "", 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "Sveobuhvatan pregled svih dijelova i glava zakona", align="C")
        self.ln(5)
        self.cell(0, 8, "(čl. 1–305)", align="C")
        self.ln(20)
        self.set_draw_color(0, 102, 153)
        self.set_line_width(0.5)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(10)
        self.set_font("ArialUni", "", 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "\"Službene novine FBiH\", br. 2/1998, 48/1999 i 61/2022", align="C")
        self.ln(6)
        self.cell(0, 8, "Pripremljeno za pripremu stručnog ispita", align="C")

    def chapter_title(self, title):
        self.set_font("ArialUni", "B", 15)
        self.set_text_color(0, 51, 102)
        self.set_fill_color(230, 240, 250)
        self.cell(0, 12, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def section_title(self, title):
        self.set_font("ArialUni", "B", 12)
        self.set_text_color(0, 80, 130)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def subsection_title(self, title):
        self.set_font("ArialUni", "BI", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("ArialUni", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet_point(self, text, indent=15):
        self.set_font("ArialUni", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(indent, 6, "  \u2022")
        self.multi_cell(0, 6, text)
        self.ln(1)

    def key_point(self, label, text):
        self.set_font("ArialUni", "B", 10)
        self.set_text_color(0, 80, 130)
        w = self.get_string_width(label + ": ") + 2
        self.cell(w, 6, label + ": ")
        self.set_font("ArialUni", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def important_box(self, text):
        self.set_fill_color(255, 248, 220)
        self.set_draw_color(200, 180, 100)
        self.set_line_width(0.3)
        self.set_font("ArialUni", "B", 10)
        self.set_text_color(150, 100, 0)
        self.cell(0, 7, "  VAŽNO:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("ArialUni", "", 10)
        self.set_text_color(80, 60, 0)
        self.multi_cell(0, 6, "  " + text, fill=True)
        self.ln(3)

    def table_header(self, cols, widths):
        self.set_font("ArialUni", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True)
        self.ln()

    def table_row_multi(self, cols, widths):
        self.set_font("ArialUni", "", 9)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(30, 30, 30)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=(i == 0))
        self.ln()

    def table_row(self, col1, col2, header=False):
        if header:
            self.set_font("ArialUni", "B", 10)
            self.set_fill_color(0, 51, 102)
            self.set_text_color(255, 255, 255)
        else:
            self.set_font("ArialUni", "", 9)
            self.set_fill_color(245, 245, 245)
            self.set_text_color(30, 30, 30)
        self.cell(80, 7, col1, border=1, fill=True)
        self.cell(0, 7, col2, border=1, fill=header, new_x="LMARGIN", new_y="NEXT")

    def separator(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)


def build_pdf():
    pdf = ZUPSummaryPDF()
    pdf.alias_nb_pages()
    pdf.add_font("ArialUni", "", "/Library/Fonts/Arial Unicode.ttf")
    pdf.add_font("ArialUni", "B", "/Library/Fonts/Arial Unicode.ttf")
    pdf.add_font("ArialUni", "I", "/Library/Fonts/Arial Unicode.ttf")
    pdf.add_font("ArialUni", "BI", "/Library/Fonts/Arial Unicode.ttf")

    # ===========================
    # TITLE PAGE
    # ===========================
    pdf.title_page()

    # ===========================
    # TABLE OF CONTENTS
    # ===========================
    pdf.add_page()
    pdf.set_font("ArialUni", "B", 18)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, "SADRŽAJ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    toc = [
        ("PRVI DIO — OPĆE ODREDBE", ""),
        ("  I. Osnovna načela", "čl. 1–17a"),
        ("  II. Nadležnost (uklj. službene osobe, pravna pomoć, izuzeća)", "čl. 18–47"),
        ("  III. Stranka i njeno zastupanje", "čl. 48–62"),
        ("  IV. Komuniciranje organa i stranaka (uklj. zapisnik)", "čl. 63–79"),
        ("  V. Dostavljanje pismena", "čl. 80–96"),
        ("  VI. Rokovi", "čl. 97–100"),
        ("  VII. Povrat u pređašnje stanje", "čl. 101–106"),
        ("  VIII. Održavanje reda", "čl. 107–110"),
        ("  IX. Troškovi postupka", "čl. 111–120"),
        ("DRUGI DIO — PRVOSTEPENI POSTUPAK", ""),
        ("  X. Pokretanje postupka i zahtjevi stranaka", "čl. 121–132"),
        ("  XI. Postupak do donošenja rješenja", "čl. 133–199"),
        ("  XII. Rješenje", "čl. 200–217"),
        ("  XIII. Zaključak", "čl. 218–220"),
        ("TREĆI DIO — PRAVNI LIJEKOVI", ""),
        ("  XIV. Žalba (redovni pravni lijek)", "čl. 221–245"),
        ("  XV. Obnova postupka", "čl. 246–257"),
        ("  XVI. Osobiti slučajevi poništavanja, ukidanja i mijenjanja", "čl. 258–266"),
        ("ČETVRTI DIO — IZVRŠENJE", "čl. 267–290"),
        ("PETI DIO — PROVOĐENJE ZAKONA, PRELAZNE I ZAVRŠNE ODREDBE", "čl. 291–305"),
        ("", ""),
        ("TABELARNI PREGLEDI I PITANJA ZA VJEŽBU", ""),
    ]
    for title, articles in toc:
        if not title:
            pdf.ln(2)
            continue
        bold = not title.startswith("  ")
        if bold:
            pdf.set_font("ArialUni", "B", 11)
            pdf.set_text_color(0, 51, 102)
        else:
            pdf.set_font("ArialUni", "", 10)
            pdf.set_text_color(30, 30, 30)
        if articles:
            pdf.cell(140, 7, title, new_x="RIGHT")
            pdf.set_font("ArialUni", "I", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 7, articles, new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)

    # ======================================================================
    # PRVI DIO — OPĆE ODREDBE
    # ======================================================================

    # =====================================================
    # GLAVA I: OSNOVNA NAČELA (čl. 1–17a)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("I. OSNOVNA NAČELA (čl. 1–17a)")

    pdf.section_title("1.1. Važenje zakona i primjena (čl. 1–3)")
    pdf.body_text(
        "Zakon o upravnom postupku FBiH (ZUP) je temeljni procesni zakon koji reguliše postupanje "
        "organa uprave u Federaciji BiH. Po ovom zakonu dužni su postupati organi uprave Federacije i "
        "kantona, gradske i općinske službe za upravu, te institucije s javnim ovlastima kad u upravnim "
        "stvarima neposredno primjenjujući propise rješavaju o pravima, obavezama ili pravnim interesima "
        "građana, pravnih lica ili drugih stranaka (čl. 1)."
    )
    pdf.body_text(
        "Poseban postupak (čl. 2): Pojedina pitanja postupka za određenu upravnu oblast mogu se samo "
        "izuzetno, posebnim federalnim zakonom, urediti drugačije, ali ne smiju biti suprotna načelima "
        "ovog zakona. Supsidijarna primjena (čl. 3): U oblastima sa posebnim postupkom, po odredbama "
        "ZUP-a postupa se u svim pitanjima koja nisu uređena tim posebnim zakonom."
    )

    pdf.section_title("1.2. Načelo zakonitosti (čl. 4)")
    pdf.body_text(
        "Organi koji vode upravni postupak rješavaju na osnovu zakona i drugih propisa, kao i općih "
        "akata institucija koje imaju javne ovlasti (st. 1). U upravnim stvarima u kojima je organ "
        "ovlašten rješavati po slobodnoj ocjeni (diskrecionom ovlaštenju), rješenje mora biti doneseno "
        "u granicama ovlaštenja i u skladu s ciljem s kojim je ovlaštenje dato (st. 2). Pravila "
        "postupka utvrđena ovim zakonom važe i za slučajeve u kojima je organ, odnosno institucija "
        "koja ima javne ovlasti, ovlašten da u upravnim stvarima rješava po slobodnoj ocjeni (st. 3)."
    )

    pdf.section_title("1.3. Zaštita prava građana i javnog interesa (čl. 5)")
    pdf.body_text(
        "Organi su dužni strankama omogućiti da što lakše zaštite i ostvare svoja prava, pri čemu vode "
        "računa da ostvarivanje njihovih prava ne bude na štetu prava drugih lica ni u suprotnosti s "
        "javnim interesom (st. 1). Službena osoba mora upozoriti stranku na njeno pravo (st. 2). "
        "Kad se na osnovu zakona strankama nalažu kakve obaveze, prema njima će se primjenjivati one "
        "mjere predviđene propisima koje su za njih povoljnije, ako se takvim mjerama postiže cilj "
        "zakona (st. 3)."
    )

    pdf.section_title("1.4. Načelo efikasnosti (čl. 6)")
    pdf.body_text(
        "Dobra organizacija na izvršavanju poslova organa osigurava brzo, potpuno i kvalitetno "
        "rješavanje upravnih stvari uz svestrano razmatranje tih stvari."
    )

    pdf.section_title("1.5. Načelo materijalne istine (čl. 7)")
    pdf.body_text(
        "U postupku se mora utvrditi pravo stanje stvari i moraju se utvrditi sve činjenice koje su "
        "od važnosti za donošenje zakonitog i pravilnog rješenja."
    )

    pdf.section_title("1.6. Načelo saslušanja stranke (čl. 8)")
    pdf.body_text(
        "Prije donošenja rješenja stranci se mora pružiti mogućnost da se izjasni o svim činjenicama "
        "i okolnostima koje su važne za donošenje rješenja. Rješenje se može donijeti bez prethodnog "
        "izjašnjenja stranke samo u slučajevima kad je to zakonom dopušteno."
    )

    pdf.section_title("1.7. Slobodna ocjena dokaza (čl. 9)")
    pdf.body_text(
        "Koje će činjenice uzeti kao dokazane odlučuje ovlašteno službeno lice po svom uvjerenju, na "
        "osnovu savjesne i brižljive ocjene svakog dokaza posebno i svih dokaza zajedno, te na osnovu "
        "rezultata cjelokupnog postupka."
    )

    pdf.section_title("1.8. Samostalnost u rješavanju (čl. 10)")
    pdf.body_text(
        "Organ vodi upravni postupak i donosi rješenje samostalno, u okviru ovlasti datih zakonom, "
        "drugim propisima i općim aktima (st. 1). Ovlaštena službena osoba organa nadležnog za vođenje "
        "postupka samostalno utvrđuje činjenice i okolnosti i na osnovu utvrđenih činjenica i okolnosti "
        "primjenjuje propise, odnosno opće akte na konkretni slučaj (st. 2)."
    )

    pdf.section_title("1.9. Pravo žalbe, konačnost, pravomoćnost (čl. 11–13)")
    pdf.body_text(
        "Protiv prvostepenog rješenja stranka ima pravo žalbe (čl. 11). Protiv rješenja donesenog u "
        "drugom stupnju žalba NIJE dopuštena."
    )
    pdf.key_point("Konačno rješenje (čl. 12)",
                  "Rješenje protiv kojeg se ne može izjaviti žalba u upravnom postupku.")
    pdf.key_point("Pravomoćno rješenje (čl. 13)",
                  "Rješenje protiv kojeg se ne može izjaviti ni žalba ni pokrenuti upravni spor.")
    pdf.important_box(
        "Razlika: Konačno rješenje je iscrpilo upravni put (žalbu), ali se još može osporavati "
        "u upravnom sporu. Pravomoćno je kad se ne može ni sudski osporavati."
    )

    pdf.section_title("1.10. Ekonomičnost postupka (čl. 14)")
    pdf.body_text(
        "Postupak se ima voditi brzo i sa što manje troškova i gubitka vremena za stranku, ali tako "
        "da se pribavi sve što je potrebno za pravilno utvrđivanje činjeničnog stanja i za donošenje "
        "zakonitog i pravilnog rješenja."
    )

    pdf.section_title("1.11. Pomoć neukoj stranci (čl. 15)")
    pdf.body_text(
        "Organ se stara da neznanje i neukost stranke i drugog učesnika u postupku ne bude na štetu "
        "prava koja im pripadaju."
    )

    pdf.section_title("1.12. Jezik i pismo (čl. 16)")
    pdf.body_text(
        "Upravni postupak se vodi na bosanskom, hrvatskom ili srpskom jeziku. Službena pisma su "
        "latinica i ćirilica."
    )

    pdf.section_title("1.13. Pojam \"organ\" i Jedinstveno upravno mjesto (čl. 17, 17a)")
    pdf.body_text(
        "Čl. 17 definira pojam \"organ\" u smislu ovog zakona. Čl. 17a uvodi jedinstveno upravno "
        "mjesto: ako je za ostvarenje nekog prava potrebno voditi više upravnih postupaka, stranci "
        "se omogućava da na jednom mjestu podnese sve zahtjeve, koji se po službenoj dužnosti "
        "dostavljaju nadležnim organima. Ovo je moderna reforma usmjerena na smanjenje birokratije."
    )

    # =====================================================
    # GLAVA II: NADLEŽNOST (čl. 18–35)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("II. NADLEŽNOST (čl. 18–47)")

    pdf.section_title("2.1. Stvarna i mjesna nadležnost (čl. 18–26)")
    pdf.body_text(
        "Nadležnost se dijeli na stvarnu (koji organ rješava) i mjesnu (na kojem području). "
        "Nijedan organ ne može preuzeti određenu upravnu stvar iz nadležnosti drugog organa (čl. 20). "
        "Nadležnost se NE može mijenjati dogovorom stranaka, dogovorom organa i stranaka, ni dogovorom "
        "organa, osim ako je zakonom drugačije određeno."
    )

    pdf.subsection_title("Određivanje mjesne nadležnosti (čl. 21):")
    pdf.bullet_point("Nepokretnost — prema mjestu gdje se nepokretnost nalazi")
    pdf.bullet_point("Pravno lice — prema sjedištu pravnog lica")
    pdf.bullet_point("Fizičko lice — prema prebivalištu stranke")

    pdf.body_text(
        "Na nadležnost se pazi po službenoj dužnosti (čl. 24). Stranke sa diplomatskim imunitetom "
        "imaju poseban tretman (čl. 25). Prostorno ograničenje regulirano je čl. 26."
    )

    pdf.section_title("2.2. Sukob nadležnosti (čl. 27–35)")
    pdf.body_text(
        "Sukob nadležnosti rješava se prema nivoima vlasti. Ovo je jedna od najvažnijih tema za ispit."
    )

    pdf.subsection_title("Na nivou Federacije (čl. 28):")
    pdf.bullet_point("Tač. 1: Između federalnih organa uprave, između fed. organa i fed. ustanova, i između fed. ustanova — Vlada Federacije")
    pdf.bullet_point("Tač. 2: Između organa uprave dva ili više kantona — Vrhovni sud FBiH")
    pdf.bullet_point("Tač. 3: Između institucija s javnim ovlastima iz 2+ kantona, kao i sukobe između tih institucija i federalnih organa uprave — Vrhovni sud FBiH")
    pdf.bullet_point("Tač. 4: Između federalnih organa uprave/ustanova i kantonalnih organa uprave/ustanova, kao i federalnih i kantonalnih institucija s javnim ovlastima — Vrhovni sud FBiH")
    pdf.body_text("Između vlada dva ili više kantona, odnosno između Vlade Federacije i vlade kantona — rješava Vrhovni sud FBiH (čl. 29).")

    pdf.subsection_title("U kantonu (čl. 31):")
    pdf.bullet_point("Između kantonalnih organa — rješava vlada kantona")
    pdf.bullet_point("Između kantonalnih institucija s javnim ovlastima — najviši sud kantona")

    pdf.subsection_title("U općini (čl. 32):")
    pdf.bullet_point("Između općinskih službi iste općine — rješava općinski načelnik")
    pdf.bullet_point("Između općinskih službi 2+ općina — rješava najviši sud kantona")

    pdf.subsection_title("U gradu (čl. 33):")
    pdf.bullet_point("Između gradskih službi — rješava gradonačelnik")
    pdf.bullet_point("Između gradskih i općinskih službi — rješava najviši sud kantona")

    # =====================================================
    # SLUŽBENE OSOBE, PRAVNA POMOĆ, IZUZEĆA (čl. 36–47)
    # =====================================================
    pdf.add_page()
    pdf.section_title("2.3. Službena osoba ovlaštena za vođenje postupka i rješavanje (čl. 36–39)")
    pdf.body_text(
        "Rješenje u upravnom postupku donosi rukovodilac organa uprave, ako propisima nije drugačije "
        "određeno (čl. 36, st. 1). Rukovodilac može ovlastiti drugu službenu osobu istog organa za "
        "rješavanje, ili drugu stručnu službu za vođenje postupka odnosno poduzimanje radnji u postupku "
        "prije donošenja rješenja (čl. 36, st. 2). O ovlaštenju se donosi posebno rješenje koje sadrži "
        "lične podatke službenih osoba i obim njihovih ovlaštenja (čl. 36, st. 3). Ovlaštenje za "
        "rješavanje obuhvata i vođenje postupka (čl. 36, st. 4)."
    )
    pdf.body_text(
        "Kad je za rješavanje nadležna Vlada Federacije ili vlada kantona, postupak vodi ovlaštena "
        "osoba ili tijelo koje odredi vlada (čl. 37). Kad je nadležan dom Parlamenta FBiH ili općinsko "
        "vijeće, postupak vodi ovlaštena osoba ili komisija (čl. 38). U institucijama sa javnim ovlastima "
        "rješenje donosi rukovodilac institucije (čl. 39)."
    )

    pdf.section_title("2.4. Pravna pomoć (čl. 40–41)")
    pdf.body_text(
        "Za radnje izvan područja nadležnog organa, organ zamoljava drugi organ uprave da ih izvrši "
        "(čl. 40). Zamoljeni organi i institucije s javnim ovlastima dužni su postupiti po molbi u "
        "granicama svog područja i djelokruga, bez odgađanja, a najkasnije u roku od 10 dana od dana "
        "prijema molbe (čl. 41, st. 2). Pravna pomoć za pojedine radnje može se tražiti i od sudova "
        "(čl. 41, st. 3). Za pravnu pomoć sa inozemnim organima primjenjuje se načelo reciprociteta "
        "(čl. 41, st. 4)."
    )

    pdf.section_title("2.5. Izuzeće službenih osoba (čl. 42–47)")
    pdf.body_text(
        "Izuzeće je institut koji obezbjeđuje nepristrasnost u postupku."
    )
    pdf.subsection_title("Obavezno izuzeće (čl. 42) — službena osoba se MORA izuzeti ako:")
    pdf.bullet_point("Je u predmetu stranka, suovlaštenik, suobveznik, svjedok, vještak, punomoćnik ili zakonski zastupnik stranke")
    pdf.bullet_point("Je sa strankom srodnik po krvi u pravoj liniji ili u pobočnoj do 4. stepena, bračni drug ili srodnik po tazbini do 2. stepena")
    pdf.bullet_point("Je sa strankom u odnosu staraoca, usvojioca ili hranioca")
    pdf.bullet_point("Je u prvostepenom postupku učestvovala u vođenju postupka ili u donošenju rješenja")

    pdf.body_text(
        "Stranka može zahtijevati izuzeće i iz drugih razloga koji dovode u sumnju nepristrasnost (čl. 44). "
        "Službena osoba za koju je zatraženo izuzeće ne može obavljati radnje u postupku do donošenja "
        "zaključka, osim onih koje ne trpe odgađanje (čl. 44, st. 2). O izuzeću se odlučuje zaključkom "
        "(čl. 45, st. 8). Protiv zaključka o izuzeću nije dopuštena žalba (čl. 46, st. 2)."
    )

    pdf.subsection_title("Ko odlučuje o izuzeću (čl. 45):")
    pdf.table_row("Službena osoba", "Ko odlučuje o izuzeću", header=True)
    pdf.table_row("U fed. organu uprave / fed. ustanovi", "Rukovodilac tog organa/ustanove (st. 1)")
    pdf.table_row("U gradskoj / općinskoj službi", "Gradonačelnik / općinski načelnik (st. 2)")
    pdf.table_row("U org. u sastavu organa uprave", "Rukovodilac organa uprave (st. 3)")
    pdf.table_row("Rukovodilac organa (fed./kant.)", "Vlada Federacije / vlada kantona (st. 4)")
    pdf.table_row("Gradonačelnik / općinski načelnik", "Gradsko / općinsko vijeće (st. 5)")
    pdf.table_row("Služb. osoba u instituciji s javn. ovl.", "Rukovodilac te institucije (st. 6)")
    pdf.ln(3)

    pdf.body_text(
        "Odredbe o izuzeću se primjenjuju i na izuzeće zapisničara (čl. 47)."
    )

    # =====================================================
    # GLAVA III: STRANKA I NJENO ZASTUPANJE (čl. 48–62)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("III. STRANKA I NJENO ZASTUPANJE (čl. 48–62)")

    pdf.section_title("3.1. Pojam stranke (čl. 48–49)")
    pdf.body_text(
        "Stranka je lice po čijem zahtjevu se pokreće postupak, protiv koga se vodi postupak, ili "
        "koje radi zaštite svojih prava i pravnih interesa ima pravo učestvovati u postupku (čl. 48). "
        "To može biti fizičko ili pravno lice (čl. 49). Ombudsmen može prisustvovati postupku."
    )

    pdf.section_title("3.2. Procesna sposobnost i zastupnici (čl. 52–55)")
    pdf.body_text(
        "Procesnu sposobnost ima stranka koja je potpuno poslovno sposobna (čl. 52). Za stranku bez "
        "procesne sposobnosti radnje poduzima zakonski zastupnik. Privremeni zastupnik se postavlja "
        "kad je to potrebno zbog hitnosti (čl. 54). Zajednički predstavnik — kad više stranaka nastupa "
        "sa istim zahtjevom (čl. 55)."
    )

    pdf.section_title("3.3. Punomoćnik (čl. 56–60)")
    pdf.body_text(
        "Stranka može odrediti punomoćnika koji će je zastupati u postupku (čl. 56). Punomoćnik može "
        "biti svaka potpuno poslovno sposobna osoba, OSIM osobe koja se bavi nadripisarstvom (čl. 57, "
        "st. 1). Punomoć se daje pismeno ili usmeno u zapisnik (čl. 58). Punomoć NE prestaje smrću "
        "stranke, gubitkom njene procesne sposobnosti ili promjenom zakonskog zastupnika (čl. 60, st. 2)."
    )
    pdf.important_box(
        "Bitno za ispit: Punomoć ne prestaje smrću stranke! Punomoćnik nastavlja zastupanje dok "
        "nasljednici ne odrede drugačije."
    )

    pdf.section_title("3.4. Stručni pomagač (čl. 62)")
    pdf.body_text(
        "Stručni pomagač pomaže stranci, ali je NE zastupa. Razlika od punomoćnika — nema ovlaštenje "
        "za poduzimanje radnji u ime stranke."
    )

    # =====================================================
    # GLAVA IV: KOMUNICIRANJE (čl. 63–72)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("IV. KOMUNICIRANJE ORGANA I STRANAKA (čl. 63–79)")

    pdf.section_title("4.1. Podnesci (čl. 63, 67)")
    pdf.body_text(
        "Podnesci se mogu podnositi: pismeno, elektronskim putem, usmeno na zapisnik, faksom ili "
        "telegrafski (čl. 63). Ako podnesak ima formalni nedostatak, ne može se odmah odbaciti — "
        "organ mora dati rok za ispravku. Ako stranka ne ispravi u roku, smatra se da podnesak nije "
        "ni podnesen (čl. 67)."
    )

    pdf.section_title("4.2. Pozivanje (čl. 69–72)")
    pdf.body_text(
        "Pozivanje se ne vrši radi dostavljanja rješenja (čl. 69). Noćno pozivanje je dopušteno "
        "samo izuzetno za hitne mjere (čl. 71). Pozvana osoba dužna je da se odazove pozivu (čl. 72)."
    )

    pdf.section_title("4.3. Zapisnik (čl. 73–79)")
    pdf.body_text(
        "O usmenoj raspravi i drugim važnijim radnjama u postupku, kao i o važnijim usmenim izjavama "
        "stranaka ili trećih osoba, sastavlja se zapisnik (čl. 73, st. 1). O manje važnim radnjama "
        "sastavlja se samo službena zabilješka u spisu."
    )
    pdf.body_text(
        "U zapisnik se unosi: naziv organa, broj i datum, mjesto i predmet, imena prisutnih osoba "
        "(čl. 74). Zapisnik mora biti vođen uredno — ne smije se ništa brisati, a precrtana mjesta "
        "moraju ostati čitljiva (čl. 75). Prije zaključenja zapisnik se pročita saslušanim osobama "
        "koje imaju pravo na primjedbe (čl. 76)."
    )
    pdf.key_point("Dokazna snaga (čl. 77)",
                  "Zapisnik sastavljen sukladno zakonu jeste JAVNA ISPRAVA i dokaz o toku i sadržini "
                  "radnje postupka i datih izjava. Dozvoljeno je dokazivati netačnost zapisnika (st. 2).")
    pdf.body_text(
        "Za vijećanje i glasanje kolegijalnog organa sastavlja se poseban zapisnik (čl. 78)."
    )

    pdf.section_title("4.4. Razgledanje spisa i obavještavanje o toku postupka (čl. 79)")
    pdf.body_text(
        "Stranke imaju pravo razgledati spise predmeta i o svom trošku prepisati potrebne spise "
        "(čl. 79, st. 1). NE mogu se razgledati ni prepisivati: zapisnik o vijećanju i glasanju, "
        "službeni referati i nacrti rješenja, kao ni spisi koji se vode kao povjerljivi (čl. 79, st. 4). "
        "Ombudsmen i društvene organizacije sa pravnim interesom također imaju pravo na razgledanje "
        "spisa (čl. 79, st. 2)."
    )

    # =====================================================
    # GLAVA V: DOSTAVLJANJE PISMENA (čl. 80–96)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("V. DOSTAVLJANJE PISMENA (čl. 80–96)")

    pdf.section_title("5.1. Načini dostavljanja (čl. 80)")
    pdf.body_text(
        "Dostavljanje se vrši: preko pošte, elektronskim putem ili putem službene osobe organa."
    )

    pdf.section_title("5.2. Osobno i posredno dostavljanje (čl. 83–84)")
    pdf.body_text(
        "Obavezno osobno dostavljanje (čl. 83) — za rješenja i druga pismena od kojih teče rok. "
        "Posredno dostavljanje (čl. 84) — predaja odraslom članu domaćinstva ili susjedu ako "
        "osobno dostavljanje nije moguće."
    )

    pdf.section_title("5.3. Pribijanje na vrata i javno priopćenje (čl. 86, 92)")
    pdf.body_text(
        "Pribijanje na vrata (čl. 86) — kad ni osobno ni posredno dostavljanje nije uspjelo. "
        "Javno priopćenje (čl. 92) — dostava objavljivanjem na oglasnoj tabli organa; smatra se "
        "izvršenom nakon 15 dana od dana isticanja na oglasnoj tabli."
    )

    pdf.key_point("Dostavnica (čl. 95)", "Službeni dokaz o izvršenom dostavljanju.")

    # =====================================================
    # GLAVA VI: ROKOVI (čl. 97–100)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("VI. ROKOVI (čl. 97–100)")

    pdf.body_text(
        "Računanje rokova (čl. 98): Kad se rok računa po danima, dan dostave se ne računa, a rok "
        "teče od narednog dana. Rokovi po mjesecima ili godinama ističu onog dana koji po broju "
        "odgovara danu kad je dostava izvršena."
    )
    pdf.body_text(
        "Praznik i nedjelja (čl. 99): Ako posljednji dan roka pada na praznik, nedjelju ili drugi "
        "neradni dan, rok ističe istekom prvog narednog radnog dana."
    )

    # =====================================================
    # GLAVA VII: POVRAT U PREĐAŠNJE STANJE (čl. 101–106)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("VII. POVRAT U PREĐAŠNJE STANJE (čl. 101–106)")

    pdf.body_text(
        "Ako stranka propusti rok iz opravdanog razloga, može tražiti povrat u pređašnje stanje."
    )
    pdf.key_point("Rok za prijedlog (čl. 103)",
                  "8 dana od prestanka razloga koji je prouzrokovao propuštanje.")
    pdf.key_point("Apsolutni rok (čl. 103)",
                  "3 mjeseca od dana propuštanja — nakon toga povrat se ne može tražiti ni pod kojim uvjetima.")
    pdf.important_box(
        "Dva roka za povrat: subjektivni 8 dana i objektivni 3 mjeseca. Apsolutni rok je nepovratno "
        "prekluzivan."
    )

    # =====================================================
    # GLAVA VIII: ODRŽAVANJE REDA (čl. 107–110)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("VIII. ODRŽAVANJE REDA (čl. 107–110)")

    pdf.body_text(
        "Organ koji vodi postupak stara se o održavanju reda tokom postupka. Za narušavanje reda "
        "može se izreći kazna do 50 KM (čl. 109)."
    )

    # =====================================================
    # GLAVA IX: TROŠKOVI POSTUPKA (čl. 111–120)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("IX. TROŠKOVI POSTUPKA (čl. 111–120)")

    pdf.body_text(
        "Kad je postupak pokrenut po službenoj dužnosti a povoljno za stranku, troškove snosi organ "
        "(čl. 111). Stranka može biti oslobođena troškova postupka (čl. 118) — o tome odlučuje organ "
        "koji vodi postupak."
    )

    # ======================================================================
    # DRUGI DIO — PRVOSTEPENI POSTUPAK
    # ======================================================================

    # =====================================================
    # GLAVA X: POKRETANJE POSTUPKA (čl. 121–132)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("X. POKRETANJE POSTUPKA I ZAHTJEVI STRANAKA (čl. 121–132)")

    pdf.section_title("10.1. Pokretanje postupka (čl. 121–123)")
    pdf.body_text(
        "Postupak se pokreće po službenoj dužnosti ili zahtjevu stranke (čl. 121). Postupak je pokrenut "
        "čim organ izvrši ma koju radnju u cilju vođenja postupka (čl. 123)."
    )

    pdf.section_title("10.2. Izmjena zahtjeva i odustanak (čl. 128–129)")
    pdf.body_text(
        "Stranka može izmijeniti zahtjev do donošenja rješenja u prvom stupnju (čl. 128). Stranka može "
        "odustati od zahtjeva u toku cijelog postupka (čl. 129)."
    )

    pdf.section_title("10.3. Poravnanje (čl. 132)")
    pdf.body_text(
        "Stranke sa protivnim interesima mogu se poravnati u toku postupka. Poravnanje ima snagu "
        "izvršnog rješenja."
    )

    # =====================================================
    # GLAVA XI: POSTUPAK DO DONOŠENJA RJEŠENJA (čl. 133–199)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("XI. POSTUPAK DO DONOŠENJA RJEŠENJA (čl. 133–199)")

    pdf.section_title("11.1. Opća načela ispitnog postupka (čl. 133–138)")
    pdf.body_text(
        "Službena osoba upotpunjava činjenično stanje i pribavlja podatke po službenoj dužnosti (čl. 134). "
        "Izjava stranke može biti usmena ili pismena; moguća je i putem video komunikacije (čl. 136)."
    )

    pdf.section_title("11.2. Skraćeni postupak (čl. 139)")
    pdf.body_text(
        "Organ može rješavati u skraćenom postupku u 4 zakonska slučaja — kad se činjenično stanje "
        "može utvrditi na temelju općepoznatih činjenica, službenih podataka, podnesenih dokaza, ili "
        "kad je propisima dopušteno rješavati na osnovu činjenica koje nisu potpuno utvrđene."
    )

    pdf.section_title("11.3. Poseban ispitni postupak (čl. 140)")
    pdf.body_text(
        "Provodi se kad se ne može rješavati u skraćenom postupku — utvrđuju se sve činjenice i "
        "okolnosti bitne za rješavanje."
    )

    pdf.section_title("11.4. Prethodno pitanje (čl. 142–146)")
    pdf.body_text(
        "Organ može sam raspraviti prethodno pitanje, ali takvo rješavanje djeluje samo u toj stvari "
        "(čl. 142). Organ MORA prekinuti postupak kad je prethodno pitanje: krivično djelo, "
        "valjanost braka ili utvrđivanje očinstva (čl. 143)."
    )

    pdf.section_title("11.5. Usmena rasprava (čl. 147–156)")
    pdf.body_text(
        "Obavezna kad: učestvuju 2+ stranaka s protivnim interesima, provodi se uviđaj, saslušavaju "
        "svjedoci ili vještaci; moguća putem video komunikacije (čl. 147). "
        "Usmena rasprava je javna (čl. 148). Isključenje javnosti moguće radi zaštite morala, "
        "sigurnosti, obiteljskog života ili čuvanja tajni."
    )
    pdf.key_point("Rok pozivanja (čl. 150)", "Najmanje 8 dana od poziva do rasprave.")

    pdf.section_title("11.6. Dokazivanje (čl. 157–199)")

    pdf.subsection_title("Dokazna sredstva (čl. 157):")
    pdf.bullet_point("Isprave")
    pdf.bullet_point("Svjedoci")
    pdf.bullet_point("Izjava stranke")
    pdf.bullet_point("Vještaci")
    pdf.bullet_point("Uviđaj")

    pdf.body_text(
        "Općepoznate činjenice se ne dokazuju. Od stranke se ne smije tražiti da pribavi uvjerenja "
        "iz službenih evidencija kojima organ raspolaže (čl. 158)."
    )

    pdf.key_point("Uvjerenja iz služb. evidencije (čl. 169)", "Izdaje se istog dana, najkasnije u roku od 5 dana.")
    pdf.key_point("Uvjerenja bez služb. evidencije (čl. 170)", "Rok za izdavanje je 8 dana.")

    pdf.subsection_title("Svjedoci (čl. 171–175):")
    pdf.body_text(
        "Svjedok može biti svaka fizička osoba. Službena osoba organa NE može biti svjedok (čl. 171). "
        "Postoje razlozi za uskraćivanje svjedočenja (čl. 174). Svjedoci se saslušavaju pojedinačno "
        "(čl. 175)."
    )

    pdf.subsection_title("Vještaci i uviđaj (čl. 187, 192):")
    pdf.body_text(
        "Vještak NE polaže zakletvu (čl. 187, st. 5). Uviđaj se provodi kad je za utvrđivanje "
        "neke činjenice ili za razjašnjenje bitnih okolnosti potrebno neposredno opažanje službene "
        "osobe (čl. 192)."
    )

    # =====================================================
    # GLAVA XII: RJEŠENJE (čl. 200–217)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("XII. RJEŠENJE (čl. 200–217)")

    pdf.section_title("12.1. Donošenje uz učešće više organa (čl. 201–202)")
    pdf.body_text(
        "Kad rješenje donose dva ili više organa, ili kad je za donošenje potrebna suglasnost drugog "
        "organa, taj organ mora dati suglasnost u roku od 15 dana (čl. 202)."
    )

    pdf.section_title("12.2. Sastavni dijelovi rješenja (čl. 204)")
    pdf.bullet_point("Naziv organa koji donosi rješenje")
    pdf.bullet_point("Broj i datum rješenja")
    pdf.bullet_point("Uvod")
    pdf.bullet_point("Dispozitiv (izreka)")
    pdf.bullet_point("Obrazloženje")
    pdf.bullet_point("Uputstvo o pravnom lijeku")
    pdf.bullet_point("Potpis ovlaštene osobe i pečat organa")

    pdf.section_title("12.3. Pogrešno uputstvo o pravnom lijeku (čl. 208)")
    pdf.body_text(
        "Ako je uputstvo pogrešno, stranka može postupiti po propisima ili po uputstvu — bez štete "
        "po svoja prava."
    )

    pdf.section_title("12.4. Vrste rješenja (čl. 212–215)")
    pdf.key_point("Usmeno rješenje (čl. 212)", "Mora se izdati u pismenoj formi u roku od 8 dana.")
    pdf.key_point("Djelimično rješenje (čl. 213)", "Rješava samo o nekim zahtjevima ako su zreli za rješavanje.")
    pdf.key_point("Dopunsko rješenje (čl. 214)", "Rješava o zahtjevu o kojem nije odlučeno glavnim rješenjem.")
    pdf.key_point("Privremeno rješenje (čl. 215)", "Ukida se rješenjem o glavnoj stvari.")

    pdf.section_title("12.5. Rokovi za donošenje rješenja (čl. 216)")
    pdf.table_row("Situacija", "Rok", header=True)
    pdf.table_row("Skraćeni postupak", "15 dana")
    pdf.table_row("Bez ispitnog postupka", "30 dana")
    pdf.table_row("Sa ispitnim postupkom", "60 dana")
    pdf.ln(3)
    pdf.important_box(
        "Šutnja administracije: Ako organ ne donese rješenje u zakonskom roku, stranka ima pravo "
        "izjaviti žalbu kao da je njen zahtjev odbijen."
    )

    pdf.section_title("12.6. Ispravka grešaka (čl. 217)")
    pdf.body_text(
        "Greške u pisanju, računanju i druge očite greške mogu se ispraviti U SVAKO VRIJEME — "
        "rješenjem ili zaključkom."
    )

    # =====================================================
    # GLAVA XIII: ZAKLJUČAK (čl. 218–220)
    # =====================================================
    pdf.separator()
    pdf.chapter_title("XIII. ZAKLJUČAK (čl. 218–220)")
    pdf.body_text(
        "Zaključkom se odlučuje o pitanjima koja se tiču postupka, a ne o samoj upravnoj stvari. "
        "Protiv zaključka se može izjaviti posebna žalba samo kad je to zakonom predviđeno; u "
        "protivnom, zaključak se pobija žalbom na rješenje."
    )

    # ======================================================================
    # TREĆI DIO — PRAVNI LIJEKOVI
    # ======================================================================

    # =====================================================
    # GLAVA XIV: ŽALBA (čl. 221–245)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("XIV. ŽALBA — REDOVNI PRAVNI LIJEK (čl. 221–245)")

    pdf.section_title("14.1. Pravo na žalbu (čl. 221–222)")
    pdf.body_text(
        "Stranka ima pravo žalbe protiv svakog prvostepenog rješenja (čl. 221). IZUZETAK: Protiv "
        "rješenja Vlade FBiH i vlade kantona donesenih u prvom stupnju NEMA žalbe (čl. 222, st. 5) — "
        "ali se može pokrenuti upravni spor."
    )

    pdf.section_title("14.2. Posebna pravila za rješenja po čl. 201/202")
    pdf.body_text(
        "Kad je rješenje doneseno uz suglasnost drugog organa (čl. 201/202), drugostepeni organ "
        "može to rješenje samo PONIŠTITI, ne može ga izmijeniti (čl. 225)."
    )

    pdf.section_title("14.3. Rokovi i postupak sa žalbom (čl. 227–235)")
    pdf.key_point("Rok za žalbu (čl. 227)", "15 dana od dostavljanja rješenja.")
    pdf.body_text(
        "U toku roka za žalbu rješenje se NE može izvršiti, osim u slučaju hitnih mjera (čl. 228). "
        "Stranka može u žalbi navoditi nove činjenice, ali mora obrazložiti zašto ih ranije nije "
        "iznijela (čl. 229)."
    )
    pdf.key_point("Predaja žalbe (čl. 230)", "Žalba se predaje prvostepenom organu.")
    pdf.body_text(
        "Prvostepeni organ može zamijeniti rješenje novim ako je žalba opravdana (čl. 232). "
        "Prosljeđivanje žalbe drugostepenom organu — u roku od 8 dana (čl. 235)."
    )

    pdf.section_title("14.4. Odluke drugostepenog organa (čl. 236)")
    pdf.body_text("Drugostepeni organ može:")
    pdf.bullet_point("Odbiti žalbu kao neosnovanu")
    pdf.bullet_point("Poništiti prvostepeno rješenje")
    pdf.bullet_point("Izmijeniti prvostepeno rješenje")

    pdf.section_title("14.5. Vraćanje na ponovni postupak (čl. 239)")
    pdf.body_text(
        "Kad drugostepeni organ vrati predmet na ponovni postupak, prvostepeni organ dužan je "
        "donijeti novo rješenje u roku od 15 dana."
    )

    pdf.section_title("14.6. Šutnja administracije u žalbenom postupku (čl. 243–245)")
    pdf.body_text(
        "Kad prvostepeni organ nije donio rješenje u roku, drugostepeni organ traži spise u roku "
        "od 3 dana (čl. 243). Rok za donošenje rješenja po žalbi je 30 dana (čl. 244). "
        "Drugostepeno rješenje se dostavlja stranci u roku od 5 dana od prijema spisa (čl. 245)."
    )

    # =====================================================
    # GLAVA XV: OBNOVA POSTUPKA (čl. 246–257)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("XV. OBNOVA POSTUPKA (čl. 246–257)")

    pdf.section_title("15.1. Razlozi za obnovu (čl. 246)")
    pdf.body_text("Zakon predviđa 11 razloga za obnovu postupka:")
    pdf.bullet_point("Nove činjenice ili novi dokazi")
    pdf.bullet_point("Rješenje zasnovano na lažnoj ispravi")
    pdf.bullet_point("Rješenje zasnovano na lažnom iskazu svjedoka ili vještaka")
    pdf.bullet_point("Ukinuta sudska presuda koja je bila osnov rješenja")
    pdf.bullet_point("Rješenje zasnovano na neistinitim navodima stranke")
    pdf.bullet_point("Prethodno pitanje riješeno drugačije")
    pdf.bullet_point("Postojanje razloga za izuzeće službene osobe")
    pdf.bullet_point("Rješenje donijela neovlaštena osoba")
    pdf.bullet_point("Kolegijalni organ odlučio bez potrebnog kvoruma")
    pdf.bullet_point("Stranka nije imala mogućnost učešća u postupku")
    pdf.bullet_point("Zakonski zastupnik ili jezik — nedostaci")

    pdf.section_title("15.2. Rokovi za obnovu (čl. 249)")
    pdf.key_point("Subjektivni rok", "30 dana od saznanja za razlog obnove.")
    pdf.key_point("Apsolutni rok", "5 godina od dostavljanja rješenja stranci.")
    pdf.important_box(
        "IZUZETNO: Za razloge iz tač. 2, 3 i 5 (lažna isprava, lažni iskaz, neistiniti navodi) "
        "obnova se može tražiti i NAKON 5 godina!"
    )

    pdf.section_title("15.3. Podnošenje prijedloga (čl. 252)")
    pdf.body_text(
        "Prijedlog za obnovu postupka predaje se prvostepenom organu ili organu koji je donio rješenje."
    )

    # =====================================================
    # GLAVA XVI: OSOBITI SLUČAJEVI PONIŠTAVANJA, UKIDANJA I MIJENJANJA (čl. 258–266)
    # =====================================================
    pdf.add_page()
    pdf.chapter_title("XVI. PONIŠTAVANJE, UKIDANJE I MIJENJANJE (čl. 258–266)")

    pdf.section_title("16.1. Mijenjanje u vezi s upravnim sporom (čl. 258)")
    pdf.body_text(
        "Organ može izmijeniti rješenje u vezi s pokrenutim upravnim sporom, pod zakonskim uvjetima."
    )

    pdf.section_title("16.2. Zahtjev za zaštitu zakonitosti (čl. 259)")
    pdf.body_text(
        "Tužilac može podnijeti zahtjev za zaštitu zakonitosti u roku od 30 dana. Objava odluke "
        "u roku od 3 mjeseca."
    )

    pdf.section_title("16.3. Poništenje po pravu nadzora (čl. 260)")
    pdf.body_text("Rješenje se poništava u sljedećim slučajevima:")
    pdf.bullet_point("1) Stvarno nenadležan organ ga je donio")
    pdf.bullet_point("2) O istoj stvari postoji ranije pravomoćno rješenje")
    pdf.bullet_point("3) Doneseno bez suglasnosti drugog organa (čl. 201/202)")
    pdf.bullet_point("4) Mjesno nenadležan organ ga je donio")
    pdf.bullet_point("5) Rješenje doneseno pod prisilom, iznudom ili ucjenom")
    pdf.body_text(
        "Ukidanje (čl. 260, st. 2): Rješenje se može ukinuti ako je njime očigledno povrijeđen "
        "materijalni zakon."
    )

    pdf.section_title("16.4. Ko poništava i rokovi (čl. 261)")
    pdf.body_text("Poništava drugostepeni organ; ako nema drugostepenog — Vlada FBiH / vlada kantona.")

    pdf.table_row("Razlog", "Rok", header=True)
    pdf.table_row("Tač. 1–3 (nenadlež., pravomoć., suglasnost)", "5 godina")
    pdf.table_row("Tač. 4 (mjesna nenadležnost)", "1 godina")
    pdf.table_row("Tač. 5 (prisila, iznuda, ucjena)", "BEZ roka")
    pdf.table_row("Ukidanje (st. 2 — povreda mater. zakona)", "1 godina")
    pdf.ln(3)

    pdf.section_title("16.5. Ukidanje/mijenjanje pravomoćnog uz pristanak (čl. 262)")
    pdf.body_text(
        "Pravomoćno rješenje može se ukinuti ili izmijeniti uz pristanak stranke, ako se time ne "
        "vrijeđa pravo trećeg lica."
    )

    pdf.section_title("16.6. Vanredno ukidanje (čl. 263)")
    pdf.body_text(
        "Izvršno rješenje može se ukinuti ako je to potrebno radi otklanjanja teške i neposredne "
        "opasnosti po život i zdravlje ljudi, javnu sigurnost ili javni moral."
    )

    pdf.section_title("16.7. Ništavost rješenja (čl. 264–265)")
    pdf.body_text("Ništavim se oglašava rješenje u 5 slučajeva:")
    pdf.bullet_point("1) Doneseno u stvari iz sudske nadležnosti")
    pdf.bullet_point("2) Njegovo izvršenje bi predstavljalo kažnjivo djelo")
    pdf.bullet_point("3) Nemoguće ga je izvršiti")
    pdf.bullet_point("4) Doneseno bez zahtjeva stranke (kad je zahtjev potreban)")
    pdf.bullet_point("5) Sadrži nepravilnost koja je zakonom izričito predviđena kao razlog ništavosti")
    pdf.body_text(
        "Ništavost se može utvrđivati U SVAKO DOBA, po službenoj dužnosti ili prijedlogu stranke, "
        "tužioca ili ombudsmena (čl. 265)."
    )

    pdf.section_title("16.8. Pravne posljedice (čl. 266)")
    pdf.important_box(
        "PONIŠTAVANJE / NIŠTAVOST = retroaktivno djelovanje — poništavaju se SVE pravne posljedice "
        "od samog početka.\n"
        "UKIDANJE = pro futuro — ne poništava dosadašnje posljedice, ali sprečava nastanak budućih."
    )

    # ======================================================================
    # ČETVRTI DIO — IZVRŠENJE RJEŠENJA I ZAKLJUČAKA
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("ČETVRTI DIO: IZVRŠENJE (čl. 267–290)")

    pdf.section_title("17.1. Izvršnost rješenja (čl. 267)")
    pdf.body_text(
        "Prvostepeno rješenje postaje izvršno: istekom roka za žalbu ako žalba nije izjavljena, "
        "ili dostavom rješenja kad žalba nije dopuštena. Zastarjelost izvršenja: 5 godina."
    )

    pdf.section_title("17.2. Administrativno vs sudsko izvršenje (čl. 272–274)")
    pdf.body_text(
        "Administrativno izvršenje (čl. 272) — za nenovčane obaveze; provodi ga prvostepeni organ "
        "(čl. 274). Sudsko izvršenje (čl. 273) — za novčane obaveze."
    )

    pdf.section_title("17.3. Nenovčane obaveze — sredstva izvršenja (čl. 281–284)")
    pdf.bullet_point("Izvršenje preko drugih osoba")
    pdf.bullet_point("Prinuda — prisilna novčana kazna (prva kazna max 50 KM)")
    pdf.bullet_point("Neposredna prisila — kao krajnje sredstvo")

    pdf.section_title("17.4. Izvršenje radi osiguranja (čl. 286–290)")
    pdf.body_text(
        "Izvršenje radi osiguranja može se odrediti i prije nego što rješenje postane izvršno, "
        "ako bi bez toga bilo onemogućeno ili znatno otežano izvršenje. Donosi se privremeni zaključak."
    )

    # ======================================================================
    # PETI DIO — PROVOĐENJE ZAKONA, PRELAZNE I ZAVRŠNE ODREDBE
    # ======================================================================
    pdf.separator()
    pdf.chapter_title("PETI DIO: PROVOĐENJE ZAKONA (čl. 291–305)")

    pdf.section_title("18.1. Institucije sa javnim ovlastima (čl. 291)")
    pdf.body_text(
        "Institucije kojima su prenesena javna ovlašenja imaju ograničenja u pogledu primjene "
        "prinudnih mjera."
    )

    pdf.section_title("18.2. Službena osoba — uslovi (čl. 292)")
    pdf.body_text(
        "Službena osoba mora imati odgovarajuću stručnu spremu, radno iskustvo i položen stručni ispit."
    )

    pdf.section_title("18.3. Odgovornost (čl. 293)")
    pdf.body_text(
        "Povreda odredaba ovog zakona predstavlja težu povredu radne dužnosti. Organ je dužan "
        "obavijestiti stranku o odgovornoj osobi u roku od 3 dana."
    )

    pdf.section_title("18.4. Godišnji izvještaji (čl. 294)")
    pdf.body_text("Organi su dužni sačinjavati i dostavljati godišnje izvještaje o radu u upravnom postupku.")

    pdf.section_title("18.5. Nadzor (čl. 297)")
    pdf.body_text(
        "Nadzor nad primjenom zakona vrše: Federalno ministarstvo pravde (za federalne organe) i "
        "kantonalni organ za pravosuđe (za kantonalne organe)."
    )

    pdf.section_title("18.6. Kaznene odredbe (čl. 298–300)")
    pdf.body_text("Zakon predviđa tri nivoa kaznenih odredbi:")

    # Penalty table
    widths = [25, 55, 55, 55]
    pdf.table_header(["Čl.", "Institucija (KM)", "Odgovorna osoba (KM)", "Opis"], widths)
    pdf.table_row_multi(["298", "2.000 – 8.000", "300 – 1.200", "Teže povrede (15 razloga)"], widths)
    pdf.table_row_multi(["299", "1.500 – 6.000", "200 – 800", "Srednje povrede"], widths)
    pdf.table_row_multi(["300", "1.000 – 4.000", "150 – 600", "Lakše povrede"], widths)
    pdf.ln(3)

    pdf.section_title("18.7. Stupanje na snagu (čl. 305)")
    pdf.body_text("Zakon stupa na snagu 8. dana od dana objavljivanja u \"Službenim novinama FBiH\".")

    # ======================================================================
    # TABELARNI PREGLEDI
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("TABELARNI PREGLED: KLJUČNI ROKOVI")

    pdf.body_text("Pregled svih bitnih zakonskih rokova na jednom mjestu:")
    pdf.ln(2)

    w = [95, 95]
    pdf.table_header(["Situacija", "Rok"], w)
    pdf.table_row_multi(["Rješavanje bez ispitnog postupka (čl. 216)", "30 dana"], w)
    pdf.table_row_multi(["Rješavanje sa ispitnim postupkom (čl. 216)", "60 dana"], w)
    pdf.table_row_multi(["Skraćeni postupak (čl. 216)", "15 dana"], w)
    pdf.table_row_multi(["Rok za žalbu (čl. 227)", "15 dana"], w)
    pdf.table_row_multi(["Prosljeđivanje žalbe drugostepenom (čl. 235)", "8 dana"], w)
    pdf.table_row_multi(["Rješenje po žalbi (čl. 244)", "30 dana"], w)
    pdf.table_row_multi(["Vraćanje — novo rješenje (čl. 239)", "15 dana"], w)
    pdf.table_row_multi(["Dostava drugostep. rješenja (čl. 245)", "5 dana od prijema spisa"], w)
    pdf.table_row_multi(["Šutnja admin. — traži spise (čl. 243)", "3 dana"], w)
    pdf.table_row_multi(["Suglasnost drugog organa (čl. 202)", "15 dana"], w)
    pdf.table_row_multi(["Usmeno rješenje u pisanoj formi (čl. 212)", "8 dana"], w)
    pdf.table_row_multi(["Javno priopćenje (čl. 92)", "15 dana na oglasnoj tabli"], w)
    pdf.table_row_multi(["Pozivanje na usmenu raspravu (čl. 150)", "8 dana prije rasprave"], w)
    pdf.table_row_multi(["Uvjerenja iz služb. evidencija (čl. 169)", "Isti dan, najkasnije 5 dana"], w)
    pdf.table_row_multi(["Uvjerenja bez služb. evidencija (čl. 170)", "8 dana"], w)
    pdf.table_row_multi(["Povrat u pređašnje stanje (čl. 103)", "8 dana (subj.) / 3 mj. (obj.)"], w)
    pdf.table_row_multi(["Obnova postupka (čl. 249)", "30 dana (subj.) / 5 god. (obj.)"], w)
    pdf.table_row_multi(["Zahtjev za zaštitu zakonitosti (čl. 259)", "30 dana / objava 3 mjeseca"], w)
    pdf.table_row_multi(["Zastarjelost izvršenja (čl. 267)", "5 godina"], w)
    pdf.table_row_multi(["Obavijest stranci o odgovor. osobi (čl. 293)", "3 dana"], w)

    # ======================================================================
    # SUKOB NADLEŽNOSTI — TABELA
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("TABELARNI PREGLED: SUKOB NADLEŽNOSTI")

    pdf.body_text("Pregled ko rješava sukob nadležnosti na svakom nivou:")
    pdf.ln(2)

    w2 = [95, 95]
    pdf.table_header(["Između koga", "Ko rješava"], w2)
    pdf.table_row_multi(["Fed. organi uprave / fed. ustanove (čl. 28/1)", "Vlada Federacije"], w2)
    pdf.table_row_multi(["Organi 2+ kantona (čl. 28/2)", "Vrhovni sud FBiH"], w2)
    pdf.table_row_multi(["Institucije s javn. ovl. 2+ kant. (čl. 28/3)", "Vrhovni sud FBiH"], w2)
    pdf.table_row_multi(["Fed. i kant. organi/ustanove/inst. (čl. 28/4)", "Vrhovni sud FBiH"], w2)
    pdf.table_row_multi(["Vlade 2+ kant. / Vlada FBiH i vl. kant. (29)", "Vrhovni sud FBiH"], w2)
    pdf.table_row_multi(["Kantonalni organi (čl. 31)", "Vlada kantona"], w2)
    pdf.table_row_multi(["Kant. institucije s javnim ovlastima", "Najviši sud kantona"], w2)
    pdf.table_row_multi(["Općinske službe iste općine (čl. 32)", "Općinski načelnik"], w2)
    pdf.table_row_multi(["Općinske službe 2+ općina (čl. 32)", "Najviši sud kantona"], w2)
    pdf.table_row_multi(["Gradske službe (čl. 33)", "Gradonačelnik"], w2)
    pdf.table_row_multi(["Gradske i općinske službe (čl. 33)", "Najviši sud kantona"], w2)

    # ======================================================================
    # PONIŠTAVANJE/UKIDANJE — TABELA
    # ======================================================================
    pdf.separator()
    pdf.chapter_title("TABELARNI PREGLED: VANREDNI PRAVNI LIJEKOVI")

    pdf.body_text("Uporedni pregled instituta poništavanja, ukidanja i ništavosti:")
    pdf.ln(2)

    w3 = [45, 50, 50, 45]
    pdf.table_header(["Institut", "Razlog", "Rok", "Dejstvo"], w3)
    pdf.table_row_multi(["Poništ. tač. 1-3", "Nenadlež./pravomoć.", "5 godina", "Retroaktivno"], w3)
    pdf.table_row_multi(["Poništ. tač. 4", "Mjesna nenadlež.", "1 godina", "Retroaktivno"], w3)
    pdf.table_row_multi(["Poništ. tač. 5", "Prisila/ucjena", "Bez roka", "Retroaktivno"], w3)
    pdf.table_row_multi(["Ukidanje čl.260/2", "Povreda mat. zak.", "1 godina", "Pro futuro"], w3)
    pdf.table_row_multi(["Vanredno ukid. 263", "Opasnost po život", "Bez roka", "Pro futuro"], w3)
    pdf.table_row_multi(["Ništavost čl.264", "5 zakonskih razl.", "U svako doba", "Retroaktivno"], w3)
    pdf.table_row_multi(["Obnova čl. 246", "11 razloga", "30 d./5 god.", "Novi postupak"], w3)
    pdf.ln(3)

    pdf.important_box(
        "Zapamtite: Poništavanje i ništavost = retroaktivno (ex tunc). Ukidanje = pro futuro (ex nunc). "
        "Ovo je jedna od najčešćih ispitnih tema!"
    )

    # ======================================================================
    # KAZNENE ODREDBE — DETALJNA TABELA
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("TABELARNI PREGLED: KAZNENE ODREDBE (čl. 298–300)")

    pdf.section_title("Tri nivoa kaznenih odredbi:")
    pdf.ln(2)

    wk = [30, 55, 55, 50]
    pdf.table_header(["Član", "Institucija (KM)", "Odgovorna osoba", "Nivo"], wk)
    pdf.table_row_multi(["Čl. 298", "2.000 – 8.000", "300 – 1.200 KM", "Teže povrede"], wk)
    pdf.table_row_multi(["Čl. 299", "1.500 – 6.000", "200 – 800 KM", "Srednje povrede"], wk)
    pdf.table_row_multi(["Čl. 300", "1.000 – 4.000", "150 – 600 KM", "Lakše povrede"], wk)
    pdf.ln(4)

    pdf.body_text(
        "Čl. 298 predviđa 15 razloga za teže kazne, uključujući: nepoštivanje rokova za rješavanje, "
        "neizdavanje uvjerenja u roku, nepostupanje po načelima zakona, neprimjenu elektronske komunikacije "
        "kad je propisana, i slično. Nadzor vrši Federalno ministarstvo pravde (za federalne organe) "
        "i kantonalni organ za pravosuđe (za kantonalne organe)."
    )

    # ======================================================================
    # PITANJA ZA VJEŽBU
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("PITANJA ZA VJEŽBU")

    pdf.body_text("Koristite ova pitanja za provjeru znanja. Odgovori se nalaze u prethodnim poglavljima.")
    pdf.ln(3)

    questions = [
        ("1.", "Šta je razlika između konačnog i pravomoćnog rješenja? (čl. 12–13)"),
        ("2.", "U kojem roku organ mora donijeti rješenje u skraćenom postupku, a u kojem sa ispitnim postupkom? (čl. 216)"),
        ("3.", "Ko rješava sukob nadležnosti između organa dva ili više kantona? (čl. 28)"),
        ("4.", "U kojem roku se žalba mora izjaviti? (čl. 227)"),
        ("5.", "Može li stranka navoditi nove činjenice u žalbi? Pod kojim uvjetom? (čl. 229)"),
        ("6.", "Koliko razloga za obnovu postupka predviđa zakon i koji su apsolutni rokovi? (čl. 246, 249)"),
        ("7.", "U kojim slučajevima se obnova može tražiti i nakon 5 godina? (čl. 249)"),
        ("8.", "Šta je razlika između poništavanja i ukidanja rješenja u pogledu pravnih posljedica? (čl. 266)"),
        ("9.", "Navedite 5 razloga za ništavost rješenja. (čl. 264)"),
        ("10.", "Ko vrši nadzor nad primjenom zakona na federalnom, a ko na kantonalnom nivou? (čl. 297)"),
        ("11.", "Kada usmena rasprava MORA biti održana? (čl. 147)"),
        ("12.", "Ko rješava sukob nadležnosti između općinskih službi iste općine? (čl. 32)"),
        ("13.", "U kojem roku se izdaju uvjerenja iz službene evidencije? (čl. 169)"),
        ("14.", "Može li punomoć prestati smrću stranke? (čl. 60, st. 2)"),
        ("15.", "Šta je šutnja administracije i koja prava stranka ima? (čl. 216)"),
        ("16.", "U kojem roku prvostepeni organ prosljeđuje žalbu drugostepenom? (čl. 235)"),
        ("17.", "Koji je rok za povrat u pređašnje stanje? (čl. 103)"),
        ("18.", "Da li vještak polaže zakletvu u upravnom postupku? (čl. 187)"),
        ("19.", "Ko rješava sukob nadležnosti između vlada dva ili više kantona? (čl. 29)"),
        ("20.", "U kojim slučajevima se poništava rješenje po pravu nadzora bez vremenskog ograničenja? (čl. 261)"),
        ("21.", "Koje su kazne za institucije prema čl. 298? (čl. 298)"),
        ("22.", "Šta je privremeno rješenje i kako prestaje? (čl. 215)"),
        ("23.", "U kojem roku drugostepeni organ mora donijeti rješenje po žalbi? (čl. 244)"),
        ("24.", "Navedite dokazna sredstva prema ZUP-u. (čl. 157)"),
        ("25.", "Kad organ MORA prekinuti postupak radi prethodnog pitanja? (čl. 143)"),
    ]

    for num, q in questions:
        pdf.set_font("ArialUni", "B", 10)
        pdf.set_text_color(0, 51, 102)
        w_num = pdf.get_string_width(num + " ") + 2
        pdf.cell(w_num, 7, num + " ")
        pdf.set_font("ArialUni", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 7, q)
        pdf.ln(2)

    # ======================================================================
    # ODGOVORI NA PITANJA (KRATKI)
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("KRATKI ODGOVORI NA PITANJA ZA VJEŽBU")

    answers = [
        ("1.", "Konačno = nema žalbe u upravnom postupku, ali može upravni spor. Pravomoćno = nema ni žalbe ni upravnog spora."),
        ("2.", "Skraćeni: 15 dana. Bez ispitnog: 30 dana. Sa ispitnim: 60 dana."),
        ("3.", "Vrhovni sud FBiH."),
        ("4.", "15 dana od dostavljanja rješenja."),
        ("5.", "Da, ali mora obrazložiti zašto ih ranije nije iznijela."),
        ("6.", "11 razloga. Subjektivni rok 30 dana, objektivni 5 godina."),
        ("7.", "Tač. 2 (lažna isprava), tač. 3 (lažni iskaz), tač. 5 (neistiniti navodi)."),
        ("8.", "Poništavanje = retroaktivno (ex tunc), sve posljedice se brišu. Ukidanje = pro futuro (ex nunc), sprečava samo buduće."),
        ("9.", "Sudska nadležnost, kažnjivo djelo, nemoguće izvršenje, bez zahtjeva stranke, zakonom predviđena nepravilnost."),
        ("10.", "Federalno ministarstvo pravde (fed.); kantonalni organ za pravosuđe (kant.)."),
        ("11.", "Kad učestvuju 2+ stranaka s protivnim interesima, uviđaj, svjedoci, vještaci."),
        ("12.", "Općinski načelnik."),
        ("13.", "Istog dana, najkasnije 5 dana."),
        ("14.", "NE — punomoć ne prestaje smrću stranke."),
        ("15.", "Ako organ ne odluči u roku, stranka može uložiti žalbu kao da je zahtjev odbijen."),
        ("16.", "8 dana."),
        ("17.", "Subjektivni 8 dana od prestanka razloga, apsolutni 3 mjeseca."),
        ("18.", "NE — vještak ne polaže zakletvu u upravnom postupku."),
        ("19.", "Vrhovni sud FBiH."),
        ("20.", "Tač. 5 — prisila, iznuda, ucjena — BEZ roka."),
        ("21.", "Institucija: 2.000–8.000 KM; odgovorna osoba: 300–1.200 KM."),
        ("22.", "Privremeno rješenje se ukida rješenjem o glavnoj stvari."),
        ("23.", "30 dana."),
        ("24.", "Isprave, svjedoci, izjava stranke, vještaci, uviđaj."),
        ("25.", "Kad je prethodno pitanje: krivično djelo, valjanost braka ili utvrđivanje očinstva."),
    ]

    for num, a in answers:
        pdf.set_font("ArialUni", "B", 9)
        pdf.set_text_color(0, 51, 102)
        w_num = pdf.get_string_width(num + " ") + 2
        pdf.cell(w_num, 6, num + " ")
        pdf.set_font("ArialUni", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, a)
        pdf.ln(1)

    # ======================================================================
    # KLJUČNI POJMOVI — RJEČNIK
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("KLJUČNI POJMOVI — RJEČNIK")

    pdf.body_text("Kratka objašnjenja najvažnijih pojmova iz zakona:")
    pdf.ln(2)

    glossary = [
        ("Upravna stvar",
         "Svaka stvar u kojoj organ uprave neposredno primjenjujući propise rješava o pravu, "
         "obavezi ili pravnom interesu stranke."),
        ("Stranka",
         "Lice po čijem zahtjevu se pokreće postupak, protiv koga se vodi, ili koje radi zaštite "
         "svojih prava ima pravo učestvovati u postupku (čl. 48)."),
        ("Konačnost",
         "Rješenje protiv kojeg se ne može izjaviti žalba u upravnom postupku. Može se pokrenuti "
         "upravni spor (čl. 12)."),
        ("Pravomoćnost",
         "Rješenje protiv kojeg se ne može izjaviti ni žalba ni pokrenuti upravni spor (čl. 13)."),
        ("Izvršnost",
         "Svojstvo rješenja koje omogućava njegovo prisilno provođenje. Prvostepeno rješenje postaje "
         "izvršno istekom roka za žalbu ili dostavom kad žalba nije dopuštena (čl. 267)."),
        ("Diskrecionom ovlaštenje",
         "Ovlaštenje organa da rješava po slobodnoj ocjeni, ali u granicama zakona i u skladu "
         "s ciljem ovlaštenja (čl. 4)."),
        ("Šutnja administracije",
         "Situacija kad organ ne donese rješenje u zakonskom roku. Stranka ima pravo žalbe kao "
         "da je zahtjev odbijen (čl. 216)."),
        ("Supsidijarna primjena",
         "Primjena odredaba ZUP-a u svim pitanjima koja nisu uređena posebnim zakonom (čl. 3)."),
        ("Nadriprisar",
         "Lice koje se bavi pružanjem pravne pomoći bez odgovarajuće kvalifikacije. Ne može biti "
         "punomoćnik u postupku (čl. 57, st. 1)."),
        ("Obnova postupka",
         "Vanredni pravni lijek kojim se traži ponovno vođenje postupka zbog zakonom određenih "
         "razloga (čl. 246–257)."),
        ("Ništavost",
         "Najteži oblik nezakonitosti rješenja. Utvrđuje se u svako doba, retroaktivno djeluje. "
         "Pet zakonskih razloga (čl. 264)."),
        ("Poništavanje po pravu nadzora",
         "Vanredni pravni lijek kojim viši organ poništava rješenje nižeg iz razloga navedenih u "
         "čl. 260 (nenadležnost, prisila, itd.)."),
    ]

    for term, definition in glossary:
        pdf.set_font("ArialUni", "B", 10)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 7, term, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("ArialUni", "", 9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5.5, "    " + definition)
        pdf.ln(2)

    # ======================================================================
    # SHEMA POSTUPKA — TEKSTUALNI OPIS TOKA
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("TOK UPRAVNOG POSTUPKA — PREGLED")

    pdf.section_title("Faza 1: Pokretanje postupka")
    pdf.body_text(
        "Postupak se pokreće po službenoj dužnosti ili zahtjevu stranke (čl. 121). "
        "Pokrenut je čim organ izvrši bilo koju radnju u cilju vođenja postupka (čl. 123). "
        "Organ provjerava svoju nadležnost (stvarnu i mjesnu) po službenoj dužnosti."
    )

    pdf.section_title("Faza 2: Ispitni postupak ili skraćeni postupak")
    pdf.body_text(
        "Ako su uvjeti ispunjeni (čl. 139), provodi se skraćeni postupak — rješenje u 15 dana. "
        "U protivnom, provodi se poseban ispitni postupak (čl. 140) sa uviđajem, saslušanjem "
        "svjedoka, vještačenjem i usmenom raspravom po potrebi. Organ upotpunjava činjenično stanje "
        "i pribavlja podatke po službenoj dužnosti (čl. 134)."
    )

    pdf.section_title("Faza 3: Donošenje rješenja")
    pdf.body_text(
        "Organ donosi rješenje sa svim propisanim elementima (čl. 204): naziv organa, broj, datum, "
        "uvod, dispozitiv, obrazloženje, uputstvo o pravnom lijeku, potpis i pečat. "
        "Rokovi: 30 dana (bez ispitnog) ili 60 dana (sa ispitnim postupkom). "
        "Ako organ ne odluči u roku — nastupa šutnja administracije (čl. 216)."
    )

    pdf.section_title("Faza 4: Pravni lijekovi")
    pdf.body_text(
        "A) REDOVNI — Žalba (čl. 221–245): rok 15 dana; predaje se prvostepenom organu; "
        "drugostepeni odlučuje u 30 dana.\n\n"
        "B) VANREDNI:\n"
        "  - Obnova postupka (čl. 246–257): 11 razloga, rok 30 dana / 5 godina\n"
        "  - Poništenje po pravu nadzora (čl. 260): 5 razloga, rokovi 1–5 god. ili bez roka\n"
        "  - Zahtjev za zaštitu zakonitosti (čl. 259): tužilac, 30 dana\n"
        "  - Ukidanje/mijenjanje pravomoćnog uz pristanak stranke (čl. 262)\n"
        "  - Vanredno ukidanje (čl. 263): opasnost po život/sigurnost\n"
        "  - Ništavost (čl. 264): 5 razloga, u svako doba"
    )

    pdf.section_title("Faza 5: Izvršenje")
    pdf.body_text(
        "Rješenje postaje izvršno istekom roka za žalbu ili dostavom kad žalba nije dopuštena. "
        "Administrativno izvršenje za nenovčane obaveze (čl. 272), sudsko za novčane (čl. 273). "
        "Zastarjelost izvršenja: 5 godina (čl. 267)."
    )

    pdf.separator()

    pdf.section_title("Pregled osnovnih načela — kratki podsjetnik")
    pdf.body_text(
        "1. Zakonitost (čl. 4) — rješavanje na osnovu zakona\n"
        "2. Zaštita prava i javnog interesa (čl. 5) — upozoriti stranku; primjena povoljnijih mjera\n"
        "3. Efikasnost (čl. 6) — brzo, potpuno, kvalitetno\n"
        "4. Materijalna istina (čl. 7) — utvrditi pravo stanje stvari\n"
        "5. Saslušanje stranke (čl. 8) — pravo na izjašnjenje\n"
        "6. Slobodna ocjena dokaza (čl. 9) — po uvjerenju službenog lica\n"
        "7. Samostalnost (čl. 10) — u okviru zakonskih ovlaštenja\n"
        "8. Pravo žalbe (čl. 11) — protiv prvostepenog\n"
        "9. Ekonomičnost (čl. 14) — brzo, sa što manje troškova\n"
        "10. Pomoć neukoj stranci (čl. 15) — neznanje ne smije štetiti pravima"
    )

    # ======================================================================
    # SAVJETI ZA UČENJE
    # ======================================================================
    pdf.add_page()
    pdf.chapter_title("SAVJETI ZA UČENJE")

    pdf.section_title("Prioritetne teme za ispit:")
    pdf.bullet_point("Osnovna načela (čl. 1–17a) — razumjeti svako načelo i znati ga objasniti")
    pdf.bullet_point("Rokovi — naučiti napamet sve ključne rokove (koristite tabelu rokova)")
    pdf.bullet_point("Žalba — cjelokupan postupak od izjavljivanja do odluke drugostepenog organa")
    pdf.bullet_point("Vanredni pravni lijekovi — razlika poništavanje/ukidanje/ništavost")
    pdf.bullet_point("Sukob nadležnosti — ko rješava na kojem nivou")
    pdf.bullet_point("Rješenje — sastavni dijelovi, vrste, rokovi donošenja")
    pdf.bullet_point("Obnova postupka — 11 razloga i rokovi")

    pdf.section_title("Metode učenja:")
    pdf.bullet_point("Koristite tabele u ovom rezimeu za brzo ponavljanje")
    pdf.bullet_point("Rješavajte pitanja za vježbu BEZ gledanja u odgovore")
    pdf.bullet_point("Pravite vlastite kartice (flashcards) za ključne brojeve i rokove")
    pdf.bullet_point("Čitajte originalni tekst zakona paralelno sa ovim rezimeom")
    pdf.bullet_point("Posebnu pažnju obratite na IZUZETKE od pravila — to su česte ispitne zamke")

    pdf.section_title("Najčešće zamke na ispitu:")
    pdf.bullet_point("Brkanje konačnog i pravomoćnog rješenja")
    pdf.bullet_point("Miješanje retroaktivnog dejstva (poništavanje) i pro futuro dejstva (ukidanje)")
    pdf.bullet_point("Zaboravljanje da se obnova za lažnu ispravu/iskaz može tražiti i NAKON 5 godina")
    pdf.bullet_point("Protiv rješenja Vlade FBiH u prvom stupnju NEMA žalbe (ali ima upravni spor)")
    pdf.bullet_point("Vještak NE polaže zakletvu")
    pdf.bullet_point("Punomoć NE prestaje smrću stranke")
    pdf.bullet_point("Poništenje po tač. 5 (prisila) nema vremenski rok")

    pdf.section_title("Struktura zakona — kratki pregled:")
    pdf.body_text(
        "PRVI DIO — Opće odredbe (čl. 1–120): Načela, nadležnost, stranke, komuniciranje, "
        "dostavljanje, rokovi, povrat u pređašnje stanje, red, troškovi.\n"
        "DRUGI DIO — Prvostepeni postupak (čl. 121–220): Pokretanje, ispitni postupak, dokazivanje, "
        "rješenje, zaključak.\n"
        "TREĆI DIO — Pravni lijekovi (čl. 221–266): Žalba, obnova, poništavanje/ukidanje/ništavost.\n"
        "ČETVRTI DIO — Izvršenje (čl. 267–290): Administrativno i sudsko izvršenje.\n"
        "PETI DIO — Provođenje, prelazne i završne odredbe (čl. 291–305): Nadzor, kazne, stupanje na snagu."
    )

    pdf.ln(5)
    pdf.set_draw_color(0, 102, 153)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("ArialUni", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Izvor: \"Službene novine FBiH\", br. 2/1998, 48/1999 i 61/2022", align="C")
    pdf.ln(5)
    pdf.cell(0, 8, "Rezime pripremljen za pripremu stručnog ispita", align="C")

    # ===========================
    # OUTPUT
    # ===========================
    output_path = "/Users/kenan/Projects/Kerim/test-tuzilastvo/ZUP_FBiH_Rezime_Glava.pdf"
    pdf.output(output_path)
    print(f"PDF generisan: {output_path}")
    print(f"Ukupno stranica: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
