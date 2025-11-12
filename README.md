![Language](https://img.shields.io/badge/language-Python-F7DF1E?logo=python&logoColor=black) ![Repo Size](https://img.shields.io/github/repo-size/Renato-4132/Casa-Facile) ![Windows Support](https://img.shields.io/badge/Windows-✔️-blue?logo=windows) ![macOS Support](https://img.shields.io/badge/macOS-✔️-lightgrey?logo=apple)
![Linux Support](https://img.shields.io/badge/Linux-✔️-yellow?logo=linux)

https://renato-4132.github.io/Casa-Facile/

![main 1](https://github.com/user-attachments/assets/41fc7803-7ec7-4742-bac0-3b2c8fb91ca2)


helpcasafacilepro@gmail.com

# 🏡 Casa Facile Pro

**La tua soluzione completa per la gestione delle finanze domestiche!**

_"Casa Facile Pro" è un'applicazione desktop sviluppata in Python con Tkinter, progettata per aiutarti a tenere traccia delle tue spese e entrate, gestire le categorie, monitorare le utenze e molto altro, in modo semplice e intuitivo._

---

## 🎁 Perché è gratuito?

- ✅ Il codice è aperto: chiunque può usarlo.
- ✅ Nessuna licenza da pagare.
- ✅ Creato da comunità o enti no-profit.
- ✅ Nessuna pubblicità né tracciamento.

### 🌟 Cosa ci guadagni tu?
- 💸 Zero costi — risparmi davvero.
- 🙅‍♂️ Zero pubblicità — niente interruzioni fastidiose.
- 🔧 Più controllo — sai cosa fa il programma.
- 🌱 Cresce nel tempo — grazie a contributi liberi.

---

## 2. Requisiti di sistema

- **Windows 10** o superiore
- **Linux** (tutte le versioni supportate)
- **Mac**
- **Python 3.7** o successivo
- **Librerie necessarie:** `python`, `tkcalendar`, `psutil`, `win32print`, `win32api`, `win32con`
- **Stampante consigliata** per la funzione di stampa

> Per utilizzare correttamente l’applicazione, è richiesta una risoluzione minima dello schermo di **1280×800 pixel**.  
> Si consiglia l’uso su un monitor da almeno **14 pollici** per una migliore leggibilità.

---

## 3. Installazione e avvio

- **Questo programma si basa su Python.**  
  Puoi scaricare Python dal sito ufficiale:  
  [https://www.python.org/downloads/](https://www.python.org/downloads/)

- **Installazione Python su Windows:**
- Puoi usare l'installer AUTOMATICO .Zip
- oppure Manualmente:
- Scaricare l’ultima versione di Python 3 (**assicurati che sia Python 3.8 o superiore**).  
  Scegli l’installer appropriato per il tuo sistema (es. "Windows installer (64-bit)").  
  Esegui il file `.exe` scaricato.  
  **MOLTO IMPORTANTE:** Nella prima schermata dell’installazione, assicurati di spuntare la casella **"Add Python X.X to PATH"** (dove X.X è la versione di Python).  
  Questo è fondamentale per poter eseguire l’applicazione da qualsiasi posizione.  
  Clicca su "Install Now" e segui le istruzioni.

- **I plugin pip python sono autoinstallanti, ma per buona promemoria, allego come installarli manualmente.**

- **Su Linux:**
  ```bash
  sudo apt install tkcalendar 
  ```
  In alternativa puoi usare i pacchetti python pip:
  ```bash
  pip install tkcalendar 
  ```

- **Su Windows:**  
  Apri il terminale (Prompt dei comandi) e digita:
  ```bash
  py -m pip install tkcalendar win32print win32api win32con
  ```

1. **Scarica il programma da GitHub:**  
   [Scarica Casa Facile.pyw](https://github.com/Renato-4132/Casa-Facile/raw/main/Casa%20Facile.pyw)  
   *(Se cliccando il link il file viene aperto come testo nel browser, fai clic destro sul link e scegli "Salva PAGINA con nome..." per scaricarlo.)*
2. **Crea una cartella sul desktop** con un nome a tua scelta.
3. **Copia il file** all’interno della cartella e avvia `Casa Facile.pyw`
   (con doppio click o da terminale).
4. **Alla prima esecuzione,** verranno creati i database e installate le dipendenze.


## 💡 Cos'è "Casa Facile Pro"?

_"Casa Facile Pro" è la tua piattaforma personale per una gestione finanziaria domestica senza stress. Con un'interfaccia intuitiva e funzionalità robuste, ti permette di avere sempre sotto controllo le tue finanze. Dimentica i fogli di calcolo complessi e le note sparse: qui hai tutto ciò che ti serve in un unico posto._

- **Controllo Totale:** Registra ogni spesa ed entrata con facilità.
- **Organizzazione:** Categorizza le transazioni per una visione chiara di dove vanno i tuoi soldi.
- **Pianificazione:** Gestisci le ricorrenze per le spese fisse (affitto, bollette, abbonamenti).
- **Analisi:** Ottieni statistiche dettagliate per capire meglio le tue abitudini di spesa.

---

## ⚙️ Come Funziona?

L’applicazione è progettata per essere semplice da usare, ma potente nelle sue funzionalità.  
Ecco una panoramica delle sue aree principali:

### 📅 Calendario e Riepilogo

Il calendario ti offre una visione immediata delle tue giornate finanziarie, con colori che indicano entrate (verde), uscite (rosso) o entrambi (giallo).  
Sotto il calendario, trovi un riepilogo annuale e mensile delle tue finanze.

- **Navigazione Facile:** Seleziona un giorno per vedere le transazioni specifiche.
- **Colorazione Intuitiva:** Riconosci a colpo d’occhio i giorni con attività finanziarie.
- **Riepiloghi Rapidi:** Controlla entrate, uscite e differenze per mese e anno.

### 📊 Statistiche e Inserimento

Sul lato destro dell’interfaccia principale, trovi la sezione per l’inserimento di nuove spese/entrate e le statistiche dettagliate.

- **Inserimento Semplice:** Aggiungi transazioni con data, categoria, descrizione, importo e tipo (entrata/uscita).
- **Modifica e Cancella:** Gestisci le voci esistenti con facilità.
- **Ricorrenze:** Imposta spese o entrate che si ripetono giornalmente, mensilmente o annualmente.
- **Visualizzazione Statistiche:** Scegli tra statistiche giornaliere, mensili, annuali o totali per categoria.

---

## 🚀 Come Usarla al Meglio?

Per sfruttare al massimo "Casa Facile Pro", ecco alcuni suggerimenti e le funzionalità aggiuntive che la rendono unica:

### 🏷️ Gestione Categorie

Crea e personalizza le tue categorie di spesa e entrata.  
Questo ti aiuterà a organizzare meglio le tue finanze e a ottenere statistiche più precise.

- **Aggiungi Nuove Categorie:** Personalizza l'app in base alle tue esigenze.
- **Modifica e Cancella:** Mantieni le tue categorie sempre aggiornate.

### 💰 Saldo Conto Corrente

Tieni traccia del saldo del tuo conto corrente.  
Inserisci l’ultimo saldo e la data, e l’app calcolerà il saldo aggiornato in base alle tue transazioni.

- **Aggiornamento Facile:** Inserisci il saldo più recente per una visione sempre aggiornata.
- **Previsioni:** Visualizza il saldo stimato per mese, anno e totale.

### 👥 Rubrica Contatti

Una rubrica integrata per gestire i tuoi contatti personali, con campi per nome, telefono, email e note.

- **Gestione Completa:** Aggiungi, modifica, cancella e cerca contatti.
- **Esportazione:** Esporta la rubrica in formato testo o JSON.

### 💧💡🔥 Gestione Utenze

Monitora i consumi di acqua, luce e gas.  
Inserisci le letture precedenti e attuali per calcolare il consumo e tenere traccia delle tue bollette.

- **Tracciamento Consumi:** Inserisci le letture mensili per calcolare il consumo.
- **Anagrafiche:** Salva i dettagli dei fornitori di utenze.
- **Report:** Visualizza ed esporta i consumi per anno.

### 🔄 Backup, Import/Export e Stampa

"Casa Facile Pro" offre funzionalità complete per la gestione dei tuoi dati:

- **Backup Incrementale:** I tuoi dati sono al sicuro con backup automatici.
- **Importa/Esporta Database:** Sposta i tuoi dati tra diverse installazioni o per archiviarli.
- **Stampa Report:** Genera report dettagliati delle tue finanze in formato stampabile.

---

## 🔙 [← Torna alla Pagina Principale](https://github.com/Renato-4132/Casa-Facile)

---

© 2025 Casa Facile Pro. Tutti i diritti riservati.
