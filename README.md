
## 🏠 CASA FACILE PRO [![Sito Web](https://img.shields.io/badge/SITO_UFFICIALE-VISITA-4f46e5?style=flat-square&logo=google-chrome&logoColor=white)](https://renato-4132.github.io/Casa-Facile/)
### Il centro di comando per la tua gestione domestica, dalle spese quotidiane al risparmio intelligente.

<img width="1283" height="655" alt="main categorie" src="https://github.com/user-attachments/assets/3534e37e-06dc-4c19-87dd-cf62ad2f9aa2" />

---

![Windows](https://img.shields.io/badge/Windows-✔️-blue?style=flat-square&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-✔️-lightgrey?style=flat-square&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-✔️-yellow?style=flat-square&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)
![Versione](https://img.shields.io/badge/VERSIONE-9.5-orange?style=flat-square)
![Visite](https://visitor-badge.laobi.icu/badge?page_id=Renato-4132.Casa-Facile&left_text=VISITE%20TOTALI&color=4f46e5)

---

### 🚀 L'ESSENZA DEL SOFTWARE
**Casa Facile Pro** è un ecosistema **Open Source** Gratuito, progettato per chi vuole il controllo totale sulle proprie finanze senza rinunciare alla **Privacy**. Unisce la potenza di un software gestionale alla semplicità di un'app domestica.

Nota Tecnica sulla Sync: Casa Facile Pro evita deliberatamente le API bancarie (PSD2) per proteggere la privacy dell'utente ed evitare i costi di sottoscrizione che renderebbero il progetto a pagamento. Crediamo in un software libero da canoni e da occhi indiscreti.

* 🛡️ **Zero Cloud**: I tuoi dati risiedono solo sul tuo PC.
* 💰 **Smart Saving**: Algoritmi per il confronto prezzi e risparmio.
* 📱 **Mobile Ready**: Accesso rapido tramite QR Code.
* 📑 **Paperless**: Archiviazione digitale di tutti i tuoi documenti PDF.

---

### 🔥 POTENZA IN 20+ FUNZIONI
1.  **Calendario Heartbeat**: Vista globale dei tuoi impegni finanziari.
2.  **Gestione Ricorrenze**: Automatizza i movimenti fissi.
3.  **Grafici Drill-Down**: Analisi visiva profonda delle spese.
4.  **Archivio PDF**: Collega i documenti ai movimenti.
5.  **Monitor Utenze**: Tieni d'occhio i consumi di luce, gas e acqua.
6.  **Simulatore Risparmio**: Calcola come raggiungere i tuoi obiettivi.
7.  **Proiezione 31/12**: Prevedi il saldo a fine anno.
8.  **Webserver Wi-Fi**: Consulta i dati dallo smartphone in rete locale/remota.
9.  **Confronto Prezzi**: Ottimizza la tua spesa alimentare.
10. **Ammortamento Mutui**: Calcola rate e interessi reali - Piani Ammortamento.
11. **Generatore QR Code**: Configura i promemoria con un colpo d'occhio.
12. **Configurazione & Backup**: Configurabile - Dati sempre esportabili e sicuri.
13. **Rubrica Vcard/Android**: Esporta/importa i contatti dal tuo smartphone.
14. **Stampa Report**: Documentazione professionale pronta all'uso.
15. **Saldo Bancario**: Riconciliazione immediata dei conti.
16. **Ricerca Multi-Filtro**: Trova ogni centesimo in un istante.
17. **Profili Multi-Utente**: Gestisci più persone con database separati.
18. **Sicurezza Password**: Accesso protetto e crittografato.
19. **Esportazione TXT**: Per una lettura grezza e veloce dei dati.
20. **Aggregazione Categorie**: Raggruppa le spese per aree tematiche.

---
🛡️ PERCHÉ NON USIAMO LA SINCRONIZZAZIONE BANCARIA?

Molti ci chiedono perché Casa Facile Pro non si colleghi direttamente al conto corrente.
La risposta è semplice: la tua sicurezza e indipendenza non hanno prezzo.

    🚫 Nessun Costo Nascosto: I servizi di aggregazione bancaria (come GoCardless o Tink) impongono canoni mensili
       elevati o costi per singola transazione. Per mantenere il software 100% Gratuito e Open Source, 
       abbiamo scelto di non gravare sugli utenti con abbonamenti forzati.

    🔒 Privacy Totale (Zero Intermediari): La sincronizzazione automatica obbliga a far passare i tuoi dati 
       finanziari attraverso server di terze parti. Con Casa Facile Pro, nessuno (nemmeno noi) può vedere quanto
       spendi o dove acquisti. I tuoi dati restano sul tuo PC.

    ⚠️ Protezione contro il "Data Leak": Eliminando il ponte tra banca e software, annulliamo il rischio che le 
       tue credenziali o i tuoi saldi vengano esposti in caso di attacchi hacker ai server degli aggregatori.

    🧠 Consiglio per l'uso: Per una gestione veloce, utilizza la funzione di Saldo Bancario per riconciliare 
       i conti manualmente o sfrutta l'inserimento rapido. Il controllo manuale è il primo passo verso un
       risparmio consapevole!

### 📺 [Guarda il Video Dimostrativo)](https://github.com/Renato-4132/Casa-Facile/raw/main/Casa-Facile.mp4)
📩 ASSISTENZA TECNICA

Per bug, suggerimenti o supporto: helpcasafacilepro@gmail.com

## ⚙️ INSTALLAZIONE

### 🟦 Windows (Automatico)
Metodo consigliato per utenti Windows.
1. Scarica l'installer: [**C.F.Win.Installer.zip**](https://github.com/Renato-4132/Casa-Facile/raw/main/C.F.Win.Installer.zip)
2. Estrai ed esegui il file EXE.
> **Nota:** Rieseguendo l'installer potrai creare nuovi profili utente separati.

### 🟩 Manuale (Tutti i SO)
**Prerequisito:** Python 3.13+.
> ⚠️ **IMPORTANTE:** Durante l'installazione di Python, spunta la casella **"Add Python to PATH"**.

1. Crea una cartella dedicata (il nome della cartella sarà il tuo **Nome Profilo**).
2. Inserisci il file `Casa Facile.pyw` all'interno.
3. Se il software non parte, installa le librerie mancanti con questo comando:

```bash
pip install tkcalendar google-genai requests segno pypiwin32
