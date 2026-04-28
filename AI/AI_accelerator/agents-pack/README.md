# Agents Pack - Colecție de Agenți AI Specializați

Aceasta este o colecție de **13 agenți AI specializați** care te ajută să rezolvi diverse probleme de business și marketing. Fiecare agent este un expert într-un domeniu specific și poate fi invocat când ai nevoie de ajutor specializat.

## 📁 Structura Proiectului

```
agents-pack/
├── business/          (6 agenți pentru business și operațiuni)
│   ├── business-model-analyzer.md
│   ├── financial-planner.md
│   ├── market-researcher.md
│   ├── pricing-strategist.md
│   ├── privacy-policy-writer.md
│   └── terms-writer.md
└── marketing/         (7 agenți pentru marketing și conținut)
    ├── ad-copy-creator.md
    ├── blog-writer.md
    ├── copywriter.md
    ├── email-writer.md
    ├── landing-page-writer.md
    ├── seo-optimizer.md
    └── social-media-creator.md
```

## 🚀 Cum se Instalează

### Pas 1: Localizează Directorul Proiectului

Deschide directorul proiectului tău în care vrei să folosești agenții. Acest director trebuie să conțină (sau va conține) un folder `.claude/`.

### Pas 2: Creează Structura de Foldere

Dacă nu există deja, creează următoarea structură în proiectul tău:
```
proiectul-tau/
└── .claude/
    └── agents/
```

**Notă:** Folder-ul `.claude` începe cu punct, deci ar putea fi ascuns implicit în sistemul tău de operare.

### Pas 3: Copiază Agenții

Acum ai două opțiuni:

#### Opțiunea A: Copiază toți agenții
1. Deschide folder-ul `agents-pack/` (acesta conține folder-ele `business/` și `marketing/`)
2. Selectează folder-ele `business/` și `marketing/`
3. **Drag and drop** ambele foldere în directorul `.claude/agents/` din proiectul tău

**Structura finală:**
```
proiectul-tau/
└── .claude/
    └── agents/
        ├── business/          (6 agenți)
        └── marketing/         (7 agenți)
```

#### Opțiunea B: Copiază doar agenții de care ai nevoie
1. Navighează în `agents-pack/business/` sau `agents-pack/marketing/`
2. Selectează doar fișierele `.md` de care ai nevoie (de exemplu: `copywriter.md`, `pricing-strategist.md`)
3. **Drag and drop** fișierele selectate direct în `.claude/agents/`

**Structura finală:**
```
proiectul-tau/
└── .claude/
    └── agents/
        ├── copywriter.md
        ├── pricing-strategist.md
        └── ... (alți agenți selectați)
```

### Pas 4: Verifică Instalarea

1. Deschide Claude Code în proiectul tău
2. Agenții vor fi automat disponibili și vor fi invocați când contextul conversației se potrivește
3. Poți verifica agenții disponibili tastând `/agents` în Claude Code

## 📖 Cum Funcționează Agenții

### Structura unui Agent

Fiecare agent este un fișier markdown (`.md`) cu următoarea structură:

```yaml
---
name: numele-agentului
description: Descriere când și cum se folosește
model: sonnet sau haiku
---

[Prompt-ul agentului cu capabilities, scenarios, etc.]
```

### Cum Invoici un Agent

Când lucrezi cu Claude Code, agenții vor fi invocați automat când:
1. **Contextul conversației** se potrivește cu scenariile agentului
2. **Ceri explicit** ajutorul acelui agent

**Exemplu:**
```
Tu: "Am nevoie să creez o landing page pentru produsul meu SaaS"
Claude: [Va invoca automat agentul landing-page-writer]
```

Sau poți invoca explicit:
```
Tu: "Folosește agentul copywriter pentru a-mi crea un headline"
```

## 🎯 Agenții Business

### 1. Business Model Analyzer
**Fișier:** `business/business-model-analyzer.md`
**Model:** Sonnet (complex)

**Când îl folosești:**
- Veniturile tale stagnează sau scad
- Vrei să schimbi modelul de business (pivot)
- Evaluezi noi modalități de monetizare
- Analizezi rate scăzute de conversie
- Te pregătești pentru investiții

**Ce face:**
- Analizează modele de business existente
- Evaluează strategii de monetizare
- Calculează unit economics
- Propune experimente de business
- Identifică oportunități de parteneriate

**Exemplu de utilizare:**
```
Tu: "SaaS-ul meu are mulți utilizatori pe tier-ul gratuit,
     dar foarte puțini upgrade la planul plătit."

Agentul va analiza:
- Modelul freemium actual
- Valorile oferite pe fiecare tier
- Punctele de conversie
- Strategii de optimizare
```

### 2. Financial Planner
**Fișier:** `business/financial-planner.md`
**Model:** Sonnet (complex)

**Când îl folosești:**
- Te pregătești pentru investitori
- Vrei să înțelegi performanța financiară
- Planifici creșterea business-ului
- Ai probleme cu cash flow-ul
- Vrei să faci bugetare

**Ce face:**
- Creează proiecții financiare
- Analizează cash flow și profitabilitate
- Calculează customer lifetime value
- Planifică necesitățile de finanțare
- Creează prezentări pentru investitori

**Exemplu de utilizare:**
```
Tu: "Vreau să ridic o rundă de investiții.
     Am nevoie de proiecții financiare pentru următorii 3 ani."

Agentul va crea:
- Model financiar detaliat
- Proiecții de venituri și cheltuieli
- Analiza break-even
- Scenarii multiple (optimist, realist, pesimist)
```

### 3. Market Researcher
**Fișier:** `business/market-researcher.md`
**Model:** Sonnet (complex)

**Când îl folosești:**
- Validezi o idee de produs
- Planifici go-to-market strategy
- Vrei să înțelegi piața țintă
- Expansiune pe noi piețe
- Planifici un pivot

**Ce face:**
- Cercetează piețe țintă și segmente
- Analizează dimensiunea pieței și tendințe
- Identifică pain points ale clienților
- Studiază comportamentul consumatorilor
- Analizează bariere de intrare pe piață

**Exemplu de utilizare:**
```
Tu: "Vreau să lansez un tool de productivitate pentru dezvoltatori.
     Care sunt principalele pain points?"

Agentul va cerceta:
- Piața existentă pentru astfel de tools
- Competitori și gap-uri în piață
- Pain points specifice ale dezvoltatorilor
- Dimensiunea pieței și potențialul de creștere
```

### 4. Pricing Strategist
**Fișier:** `business/pricing-strategist.md`
**Model:** Sonnet (complex)

**Când îl folosești:**
- Lansezi un produs nou
- Simți că prețurile tale sunt prea mici
- Competitorii își schimbă prețurile
- Adaugi feature-uri noi
- Expansiune geografică cu prețuri diferite

**Ce face:**
- Proiectează structuri de pricing (tiers)
- Analizează prețurile competitorilor
- Creează strategii value-based pricing
- Planifică modele freemium
- Testează sensibilitatea la preț

**Exemplu de utilizare:**
```
Tu: "Vreau să trec de la un singur plan de $49/lună
     la un model cu 3 tiers. Cum ar trebui să le structurez?"

Agentul va propune:
- Structură de tiers optimă
- Feature-uri pentru fiecare tier
- Pricing bazat pe valoare și piață
- Strategie de migrare a clienților existenți
```

### 5. Privacy Policy Writer
**Fișier:** `business/privacy-policy-writer.md`
**Model:** Sonnet (complex)

**Când îl folosești:**
- Lansezi un produs nou
- Adaugi feature-uri care colectează date
- Expansiune în UE (GDPR) sau California (CCPA)
- Audit de conformitate
- Integrezi servicii third-party

**Ce face:**
- Scrie politici GDPR și CCPA compliant
- Explică colectarea și procesarea datelor
- Documentează drepturile utilizatorilor
- Acoperă cookies și tracking
- Explică partajarea cu terți

**Exemplu de utilizare:**
```
Tu: "Lansez un SaaS care colectează email-uri și date de utilizare.
     Am nevoie de o politică de confidențialitate GDPR compliant."

Agentul va crea:
- Politică completă de confidențialitate
- Secțiuni clare pentru fiecare tip de date
- Drepturile utilizatorilor (acces, ștergere, etc.)
- Limbaj clar și accesibil
```

### 6. Terms Writer
**Fișier:** `business/terms-writer.md`
**Model:** Sonnet (complex)

**Când îl folosești:**
- Lansezi un produs nou
- Adaugi plăți sau conținut generat de utilizatori
- Expansiune pe noi piețe
- Pregătire pentru clienți enterprise (B2B)

**Ce face:**
- Scrie Terms of Service
- Creează user agreements pentru SaaS/apps
- Acoperă politici de plată și refundare
- Definește intellectual property rights
- Creează clauze de limitare a responsabilității

**Exemplu de utilizare:**
```
Tu: "Platforma mea permite utilizatorilor să publice conținut.
     Am nevoie de Terms of Service care să acopere asta."

Agentul va crea:
- Terms of Service complete
- Politici de utilizare acceptabilă
- Ownership-ul conținutului
- Proceduri de moderare și terminare
```

## 🎨 Agenții Marketing

### 1. Ad Copy Creator
**Fișier:** `marketing/ad-copy-creator.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Lansezi campanii de ads (Google, Facebook, LinkedIn)
- Performance-ul ad-urilor este slab
- Targetezi segmente diferite de audiență
- Ai promoții cu timp limitat
- Campaniile de retargeting

**Ce face:**
- Scrie copy pentru ads respectând limitele de caractere
- Creează headlines care atrag atenția
- Dezvoltă multiple variații pentru A/B testing
- Optimizează pentru platforme specifice
- Creează messaging pentru retargeting

**Exemplu de utilizare:**
```
Tu: "Vreau să creez ads pe Facebook pentru produsul meu SaaS
     de project management. Audiența sunt startup-uri."

Agentul va crea:
- 5+ variații de headlines
- Descrieri focus pe beneficii
- Call-to-action puternice
- Adaptare pentru feed-ul Facebook
```

### 2. Blog Writer
**Fișier:** `marketing/blog-writer.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Creezi content marketing pentru SEO
- Vrei să demonstrezi expertiză tehnică
- Explici concepte complexe
- Documentezi implementări
- Creezi case studies

**Ce face:**
- Scrie tutoriale tehnice cu cod
- Creează articole thought leadership
- Dezvoltă ghiduri how-to
- Scrie case studies
- Explică concepte pentru începători

**Exemplu de utilizare:**
```
Tu: "Vreau să scriu un tutorial despre cum să integrezi
     authentication cu OAuth2 în Next.js."

Agentul va scrie:
- Tutorial pas cu pas
- Exemple de cod funcționale
- Explicații clare pentru fiecare pas
- Best practices și security considerations
```

### 3. Copywriter
**Fișier:** `marketing/copywriter.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Creezi landing pages
- Scrii descrieri de produse
- Dezvolți campanii de email
- Creezi conținut social media
- Definești brand voice

**Ce face:**
- Scrie headlines captivante
- Creează descrieri persuasive de produse
- Dezvoltă value propositions
- Scrie email campaigns
- Creează call-to-action puternice

**Exemplu de utilizare:**
```
Tu: "Am nevoie de un headline puternic pentru landing page-ul
     produsului meu - un tool de automation pentru email marketing."

Agentul va crea:
- 5-10 variații de headlines
- Focus pe beneficii, nu features
- Explicații pentru fiecare variație
- Recomandări pentru A/B testing
```

### 4. Email Writer
**Fișier:** `marketing/email-writer.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Creezi campanii de email marketing
- Ai nevoie de welcome sequences
- Scrii newsletter-e regulate
- Automatizări de email
- Optimizezi engagement-ul

**Ce face:**
- Scrie subject lines care deschid emailuri
- Creează secvențe de onboarding
- Dezvoltă newsletter-e
- Planifică automatizări
- Optimizează pentru conversii

**Exemplu de utilizare:**
```
Tu: "Vreau să creez o secvență de welcome emails
     pentru utilizatorii noi ai SaaS-ului meu."

Agentul va crea:
- 5 emailuri pentru secvență
- Subject lines optimizate
- Copy focus pe value și engagement
- Call-to-action clare pentru fiecare email
```

### 5. Landing Page Writer
**Fișier:** `marketing/landing-page-writer.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Lansezi produse noi
- Conversion rate-ul este scăzut
- Ai campanii noi de marketing
- Optimizezi pagini existente
- Traduci features în benefits

**Ce face:**
- Scrie headlines clare care comunică valoare
- Creează copy focus pe pain points
- Dezvoltă value propositions
- Scrie call-to-action puternice
- Adaugă social proof și testimoniale

**Exemplu de utilizare:**
```
Tu: "Am nevoie de copy pentru landing page-ul unui tool
     de analytics pentru SaaS. Targetez product managers."

Agentul va crea:
- Hero section cu headline și subheadline
- Secțiuni pentru features și benefits
- Social proof section
- Pricing section copy
- Multiple CTA-uri plasate strategic
```

### 6. SEO Optimizer
**Fișier:** `marketing/seo-optimizer.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Creezi conținut nou
- Optimizezi pagini existente
- Dezvolți strategie SEO
- Cercetezi keywords
- Îmbunătățești ranking-ul în Google

**Ce face:**
- Cercetare de keywords
- Optimizează titles și meta descriptions
- Creează structură SEO-friendly
- Planifică internal linking
- Implementează schema markup

**Exemplu de utilizare:**
```
Tu: "Vreau să optimizez articolul meu de blog despre
     'project management tools' pentru SEO."

Agentul va:
- Analiza keywords relevante
- Optimiza title și meta description
- Sugera header structure (H1, H2, H3)
- Recomanda internal links
- Sugera improvements pentru readability
```

### 7. Social Media Creator
**Fișier:** `marketing/social-media-creator.md`
**Model:** Haiku (rapid)

**Când îl folosești:**
- Construiești prezență pe social media
- Creezi content calendars
- Dezvolți strategie pentru platforme specifice
- Creezi viral content
- Engagement cu comunitatea

**Ce face:**
- Creează conținut pentru Twitter, LinkedIn, Instagram
- Scrie posts engaging
- Planifică content calendars
- Dezvoltă strategii de hashtags
- Creează răspunsuri la trending topics

**Exemplu de utilizare:**
```
Tu: "Vreau să promovez lansarea produsului meu pe Twitter.
     Am nevoie de 10 tweets pentru următoarea săptămână."

Agentul va crea:
- 10 tweets variate (announcement, value props, use cases)
- Hashtags relevante
- Call-to-action pentru fiecare tweet
- Timing recommendations
```

## 🔄 Cum Lucrează Agenții Împreună

Agenții sunt proiectați să lucreze complementar. Iată câteva scenarii comune:

### Scenariu 1: Lansare de Produs
```
1. Market Researcher → cercetare piață și competitori
2. Pricing Strategist → determinare strategie de pricing
3. Landing Page Writer → creare landing page
4. Ad Copy Creator → creare ads pentru lansare
5. Email Writer → secvență de launch emails
6. Social Media Creator → posts pentru social media
```

### Scenariu 2: Optimizare Business
```
1. Business Model Analyzer → analiza modelului actual
2. Financial Planner → proiecții și planning
3. Pricing Strategist → optimizare pricing
4. Market Researcher → validare cu piața
```

### Scenariu 3: Content Marketing
```
1. SEO Optimizer → keyword research
2. Blog Writer → creare articole
3. Copywriter → CTAs și headlines
4. Social Media Creator → promovare pe social
5. Email Writer → newsletter cu articolele
```

## 🎓 Best Practices

### 1. Alege Agentul Potrivit
- **Nu folosi** copywriter pentru legal documents → folosește privacy-policy-writer sau terms-writer
- **Nu folosi** blog-writer pentru ads → folosește ad-copy-creator
- **Nu folosi** business-model-analyzer pentru pricing → folosește pricing-strategist

### 2. Oferă Context
Cu cât dai mai mult context, cu atât rezultatele vor fi mai bune:
```
❌ Slab: "Scrie-mi un ad"
✅ Bun: "Scrie-mi un Facebook ad pentru SaaS-ul meu de project
         management, targetând startup-uri tech din România,
         focus pe simplicitate și colaborare în echipă"
```

### 3. Iterează
Agenții sunt optimizați pentru iterație:
```
Tu: "Headline-ul e prea lung. Poți să-l faci mai concis?"
Agent: [Oferă versiuni mai scurte]
```

### 4. Combină Agenții
Nu te limita la un singur agent pe conversație:
```
Tu: "Folosește market-researcher pentru a înțelege piața,
     apoi pricing-strategist pentru a propune prețuri"
```

## 📊 Modelele AI

### Sonnet (Business Agents)
- **Caracteristici:** Complex, analitic, detaliat
- **Folosit pentru:** Analize complexe, planificare strategică
- **Agenți:** Business Model Analyzer, Financial Planner, Market Researcher, Pricing Strategist, Privacy Policy Writer, Terms Writer

### Haiku (Marketing Agents)
- **Caracteristici:** Rapid, creativ, eficient
- **Folosit pentru:** Generare de conținut, copywriting
- **Agenți:** Ad Copy Creator, Blog Writer, Copywriter, Email Writer, Landing Page Writer, SEO Optimizer, Social Media Creator

## 🔍 Troubleshooting

### Agentul nu se invocă automat
**Soluție:** Fii mai explicit în cerere și menționează scenariul specific:
```
❌ "Am probleme cu business-ul"
✅ "Veniturile stagnează și vreau să analizez modelul de business"
```

### Agentul oferă rezultate generice
**Soluție:** Oferă mai mult context specific despre business-ul tău:
- Piața țintă
- Tipul de produs (SaaS, e-commerce, etc.)
- Stage-ul business-ului (lansare, creștere, maturitate)
- Competitori
- Metrici actuale

### Vreau să folosesc un agent care nu există
**Soluție:** Poți crea agenți custom! Urmează structura existentă:
```yaml
---
name: numele-agentului
description: Când și cum se folosește
model: sonnet sau haiku
---

[Prompt-ul agentului]
```

## 📝 Exemple Complete

### Exemplu 1: Lansare SaaS
```
Tu: "Lansez un SaaS de project management pentru echipe remote.
     Am nevoie de ajutor cu go-to-market strategy."

Claude va invoca succesiv:
1. Market Researcher → analiza pieței și competitorilor
2. Pricing Strategist → recomandare structură de pricing
3. Landing Page Writer → copy pentru landing page
4. Email Writer → secvență de launch
5. Ad Copy Creator → ads pentru Google și Facebook
```

### Exemplu 2: Optimizare Conversii
```
Tu: "Landing page-ul meu are trafic dar conversion rate sub 1%.
     Cum îl pot optimiza?"

Claude va invoca:
1. Landing Page Writer → analiza și recomandări copy
2. Copywriter → headlines și CTAs mai puternice
3. SEO Optimizer → verificare experiență utilizator
```

### Exemplu 3: Conformitate Legală
```
Tu: "Lansez în UE și am nevoie de politici de confidențialitate
     și termeni de utilizare."

Claude va invoca:
1. Privacy Policy Writer → politică GDPR compliant
2. Terms Writer → terms of service
```
