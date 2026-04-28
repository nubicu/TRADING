# Skills Pack - Claude Code

8 skill-uri profesionale care transformă Claude Code într-un specialist pe domenii: finanțe, marketing, research, organizare, branding, brainstorming și generare de prompturi.

## Cum le folosești

### Varianta 1: Deschide folderul în VS Code și pornește Claude (cel mai simplu)

1. Deschide **VS Code**
2. **File → Open Folder** → selectează folderul **skills-pack**
3. Deschide terminalul: **Terminal → New Terminal**
4. Scrie `claude --dangerously-skip-permissions` și apasă Enter

Gata! Claude Code detectează automat skill-urile și pornește fără să ceară confirmare la fiecare pas. Poți începe să lucrezi imediat.

### Varianta 2: Le copiezi în alt proiect

Dacă vrei skill-urile într-un proiect existent, copiază folderul `.claude` (cu tot ce e în el) din skills-pack și pune-l în folderul proiectului tău. Data viitoare când pornești Claude acolo, le va detecta automat.

### Varianta 3: Le faci globale (disponibile în orice proiect)

Copiază folderele de skill-uri în locația globală Claude:
- **Windows:** `C:\Users\NUMELE_TAU\.claude\skills\`
- **Mac/Linux:** `~/.claude/skills/`

Repornește Claude Code după copiere.

## Skill-urile incluse

### 1. Analyzing Financial Statements
Calculează indicatori financiari (ROE, ROA, P/E, Debt-to-Equity etc.) din rapoarte financiare.

```
Analizează acest raport financiar și calculează toți indicatorii cheie
```
Acceptă: Excel, CSV, PDF sau cifre scrise direct.

---

### 2. Applying Brand Guidelines
Aplică branding consistent (culori, fonturi, layout) pe documente generate.

```
Creează o prezentare PowerPoint despre rezultatele Q3 cu branding-ul nostru
```
Editează `SKILL.md` din folder pentru a pune culorile și fonturile companiei tale.

---

### 3. Brainstorming
Explorare structurată a ideilor înainte de implementare. Generează 2-3 abordări diferite cu pro/contra.

```
Vreau să adaug un sistem de notificări în aplicație - hai să facem brainstorming
```

---

### 4. Competitive Ads Extractor
Extrage și analizează reclamele concurenței din Facebook Ad Library, LinkedIn etc.

```
Extrage toate reclamele active de la Notion din Facebook Ad Library și analizează ce mesaje folosesc
```
Output: screenshots + raport cu tipare de copy, vizuale și recomandări.

---

### 5. Creating Financial Models
Modele financiare avansate: DCF, analiză de sensibilitate, Monte Carlo, scenarii.

```
Construiește un model DCF pentru această companie cu datele financiare atașate
```

---

### 6. Deep Researcher
Cercetare comprehensivă pe orice subiect, cu validare cross-references și sinteză structurată.

```
Cercetează piața HR Tech SaaS: dimensiune, jucători principali, tendințe și oportunități
```

---

### 7. File Organizer
Organizează fișiere și foldere: găsește duplicate, sugerează structuri, automatizează cleanup.

```
Organizează folderul meu Downloads - e haos acolo
```
Propune un plan și cere confirmare înainte de orice modificare.

---

### 8. Prompt Factory
Generează prompturi profesionale pentru orice rol și industrie. 69 de presets, 4 formate (XML, Claude, ChatGPT, Gemini).

```
Folosește preset-ul Senior Full-Stack Engineer și generează prompt în format Claude
```

Sau custom:
```
Creează un prompt pentru un analist de contracte legale în domeniul imobiliar
```

## Sfaturi rapide

- **Fii specific.** "Cercetează piața EV batteries: dimensiune, top 5 jucători, tendințe" > "Cercetează ceva despre baterii"
- **Atașează fișiere** prin drag & drop când skill-ul are nevoie de date (financiare, documente etc.)
- **Combină skill-uri** pe rând: deep-researcher pentru research, apoi creating-financial-models pentru valuare, apoi applying-brand-guidelines pentru prezentare
- **Personalizează** editând `SKILL.md` din folderul fiecărui skill
