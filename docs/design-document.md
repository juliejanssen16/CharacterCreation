# JourHelp Design Document

## 1. Doel

JourHelp is een rustige, persoonlijke informatiesite over OCD, autisme, DID/DIS en neurodivergente of mentale gezondheidservaringen. De site helpt bezoekers woorden, herkenning en praktische steun te vinden zonder professionele zorg te vervangen.

Het ontwerp richt zich op:

- begrijpelijke uitleg voor mensen die zichzelf herkennen, zoekende zijn of al een diagnose hebben;
- lage cognitieve belasting door rustige navigatie, korte blokken en duidelijke secties;
- neurodiversiteit-bevestigende taal;
- praktische hulpmiddelen zoals support cards, sensory profiles, saved sections en calm plans;
- tweetaligheid voor Engels en Nederlands.

## 2. Doelgroep

Primaire gebruikers:

- neurodivergente bezoekers die informatie zoeken over autisme, OCD, DID/DIS, masking, burn-out, prikkelverwerking en zelfbegrip;
- laat-herkende of zelfonderzoekende bezoekers;
- supporters zoals vrienden, partners, familieleden en begeleiders;
- bezoekers die snel een rustige uitleg, tool of woordenlijst nodig hebben.

Belangrijke gebruikersbehoeften:

- "Ik wil mezelf beter begrijpen."
- "Ik wil uitleg die niet kil of pathologiserend voelt."
- "Ik ben overprikkeld en heb iets simpels nodig."
- "Ik wil mijn behoeften kunnen delen met iemand anders."
- "Ik wil bronnen vinden zonder door te veel informatie te moeten zoeken."

## 3. Productprincipes

1. Calm first  
   De interface moet zacht, voorspelbaar en niet schreeuwerig aanvoelen.

2. Respectful by default  
   Content gebruikt bevestigende taal en vermijdt cure-focused framing.

3. Practical over decorative  
   Visuele keuzes ondersteunen lezen, navigeren en regulatie.

4. Private where possible  
   Persoonlijke tools gebruiken lokale opslag alleen met expliciete toestemming.

5. Clear boundaries  
   JourHelp is educatief en ondersteunend, niet diagnostisch of medisch adviserend.

## 4. Informatiearchitectuur

De huidige site bestaat uit meerdere pagina-achtige views binnen `index.html`.

Hoofdgebieden:

- Autism home: uitgebreide gids met secties over sensory needs, masking, self-diagnosis, burn-out, support, relationships, accommodations en community.
- OCD home: uitleg over OCD, types, symptomen, behandeling, tips, stories, FAQ en crisisinformatie.
- Quizzes: laagdrempelige reflectievragen voor OCD en autisme.
- Resources: boeken, websites, apps/tools en community-bronnen.
- Toolbox: opgeslagen secties en persoonlijke support tools.
- Calm plan: lokaal bewaarbaar plan voor signalen, hulp, woorden, dingen om te vermijden en contactpersonen.
- Glossary: doorzoekbare begrippenlijst.
- Supporter view: gids voor mensen die iemand willen steunen.
- DID home: rustige gids over dissociatieve identiteitsstoornis met uitleg over dissociatie, delen/systemen, mythes, grounding, support en professionele hulp.
- Overlap guide: uitleg over overlap tussen OCD, autisme en verwante ervaringen.
- Disclaimer en about/contact.

Navigatiepatroon:

- topnavigatie met topic-tabs;
- sticky menu-rij met mega menu, delen, opslaan en globale zoekfunctie;
- hash-routing voor deelbare sectielinks;
- floating reading tools voor terug naar boven en overwhelm reset.

## 5. Kernflows

### 5.1 Bezoeker zoekt herkenning

1. Start op Autism of OCD home.
2. Gebruikt mega menu, cards of globale search.
3. Leest secties in korte blokken.
4. Slaat nuttige secties op in de toolbox.
5. Gebruikt eventueel glossary of resources voor verdieping.

### 5.2 Bezoeker is overprikkeld

1. Zet low stimulation mode aan.
2. Gebruikt overwhelm reset of calm plan.
3. Leest korte, praktische steun in plaats van lange content.
4. Kan later terugkomen via saved sections.

### 5.3 Bezoeker wil behoeften uitleggen

1. Gaat naar support tools of request tools.
2. Vult support card, sensory profile, accommodation request, boundary script of explanation tool in.
3. Kopieert de gegenereerde tekst.
4. Slaat eventueel lokaal op wanneer consent is gegeven.

### 5.4 Bezoeker wil recente research

1. Opent Recent Autism Studies.
2. Site laadt `data/autism-studies.json`.
3. Bezoeker opent PubMed-link of meldt een artikel dat niet past.
4. Feed wordt onderhouden via `scripts/update_autism_studies.py`.

## 6. Visueel Ontwerp

Huidige stijl:

- zachte roze/witte basis met veel witruimte;
- kleine border radii rond 6-8px voor rustige UI-elementen;
- Inter als primaire font in `index.html`;
- cards, chips, pills en tool panels met subtiele borders;
- prikkelarme modus met grijstinten, minder animatie en soberdere accenten.

Richtlijnen voor uitbreiding:

- behoud compacte, scanbare secties;
- gebruik cards alleen voor herhaalbare items of tools;
- vermijd drukke animaties, felle gradients en zware schaduwen;
- maak knoppen voorspelbaar en consistent;
- zorg dat tekst op mobiel nooit overlapt of krap aanvoelt;
- medische disclaimers moeten zichtbaar blijven bij diagnostische of research-gerelateerde content.

## 7. Interactieontwerp

Belangrijke interacties:

- `setLang(l)`: wisselt tussen Engels en Nederlands via `data-en` en `data-nl`;
- `setTopic(t)`: wisselt tussen Autism en OCD;
- `navTo(page, sec)`: toont pagina's en scrollt naar secties;
- `shareCurrentPage()`: deelt of kopieert de huidige pagina/sectie;
- `toggleSaveCurrent()`: bewaart pagina's of secties lokaal;
- `renderGlobalSearch()`: zoekt door JourHelp-content;
- `toggleLowStim()`: schakelt prikkelarme modus;
- calm plan en autism tools gebruiken localStorage na consent;
- Recent Autism Studies wordt via `fetch('data/autism-studies.json')` geladen.

Ontwerpverwachting:

- elke interactieve tool moet een duidelijke lege staat, ingevulde staat en fout/ontbrekende-input staat hebben;
- copy/share-acties moeten korte feedback geven;
- lokale opslag moet optioneel blijven en begrijpelijk worden uitgelegd;
- alle tools moeten ook bruikbaar zijn zonder account of server.

## 8. Contentstrategie

Tone of voice:

- warm, direct, rustig en bevestigend;
- geen dramatische of klinisch afstandelijke toon;
- erkenning zonder diagnose te beloven;
- duidelijke waarschuwingen bij crisis, medische beslissingen en research.

Contentregels:

- gebruik identity-first taal waar passend, maar erken persoonlijke voorkeuren;
- label quizzes en tools als reflectie, niet als diagnose;
- plaats disclaimers dicht bij gevoelige content;
- geef praktische voorbeelden bij abstracte concepten;
- houd beide talen inhoudelijk gelijkwaardig.

## 9. Technische Architectuur

Huidige structuur:

- `index.html`: hoofdapp met markup, CSS en veel inline JavaScript/data.
- `data/autism-studies.json`: gegenereerde PubMed-feed.
- `scripts/update_autism_studies.py`: haalt en filtert recente PubMed-artikelen.
- `README.md`: projectnotitie met copyright/disclaimer.
- `docs/CNAME` en `CNAME`: domeinconfiguratie.
- `script.js` en `style.css`: lijken nog een oudere Diary Character Creator/Pink Diary Studio implementatie te bevatten.

Client-side opslag:

- saved sections;
- calm plan;
- autism support/tool data;
- consent-instellingen;
- low stimulation voorkeur.

Externe afhankelijkheden:

- Google Fonts voor Inter;
- PubMed/NCBI E-utilities voor de research update;
- externe links naar bronnen en communities.

## 10. Privacy en Veiligheid

Privacyprincipes:

- persoonlijke tooldata blijft lokaal in de browser;
- lokale opslag gebeurt alleen na toestemming;
- geen accountflow of centrale database in de huidige architectuur;
- contactformulier moet geen gevoelige medische gegevens aanmoedigen.

Veiligheidsprincipes:

- crisisinformatie moet snel vindbaar zijn;
- disclaimers moeten duidelijk maken dat JourHelp geen professionele zorg vervangt;
- research-feed moet cure-focused, dehumaniserende of onveilige framing actief filteren;
- bezoekers moeten problematische research-items kunnen melden.

## 11. Accessibility

Belangrijke eisen:

- volledige bediening met toetsenbord;
- zichtbare focus-states;
- voldoende contrast, zeker in low stimulation mode;
- semantische headings per sectie;
- knoppen met duidelijke tekst of aria-labels;
- geen essentiële informatie alleen via kleur;
- animaties uitschakelbaar of beperkt via low stimulation mode.

Aanbevolen verbeteringen:

- test alle modals en overlays op focus trapping;
- controleer screenreader labels voor generated tool content;
- maak icon-only knoppen consequent voorzien van `aria-label`;
- voeg `prefers-reduced-motion` ondersteuning toe naast de handmatige low-stim toggle.

## 12. Onderhoud en Uitbreiding

Prioriteiten:

1. Breng code-organisatie op orde door inline data/renderfuncties op termijn te splitsen in modules.
2. Ruim of archiveer de oudere `script.js` en `style.css` als ze niet meer gebruikt worden.
3. Maak een content-review checklist voor medische claims, research links en taalconsistentie.
4. Voeg simpele regressietests toe voor routing, language toggle, saved sections en PubMed JSON-rendering.
5. Documenteer hoe de PubMed-update wekelijks wordt uitgevoerd.

Nieuwe features moeten voldoen aan:

- past bij calm-first principe;
- werkt mobiel;
- werkt zonder account;
- respecteert lokale opslag en consent;
- bevat disclaimer wanneer de feature diagnostisch, medisch of crisisgevoelig kan worden geïnterpreteerd.

## 13. Open Vragen

- Moet JourHelp primair een informatiesite blijven, of meer een persoonlijke toolbox worden?
- Moet de research-feed handmatig gemodereerd worden voordat items zichtbaar zijn?
- Welke talen zijn na Nederlands en Engels gewenst?
- Moet het contactformulier via mailto, backend of externe form service lopen?
- Wordt de oudere Diary Character Creator-code bewaard als apart project of verwijderd uit deze repo?

## 14. Succescriteria

JourHelp is succesvol wanneer:

- bezoekers snel herkennen waar ze heen moeten;
- content steunend voelt zonder diagnostische beloftes;
- tools concrete woorden opleveren die mensen kunnen gebruiken;
- opgeslagen secties en calm plan betrouwbaar werken;
- de site rustig en bruikbaar blijft op mobiel;
- nieuwe content veilig, respectvol en onderhoudbaar kan worden toegevoegd.
