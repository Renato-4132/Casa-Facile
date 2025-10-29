#!/usr/bin/env python3
# 🔧 Moduli standard Python
import os
import sys
import csv
import json
import html
import math
import uuid
import random
import socket
import ctypes
import shutil
import hashlib
import calendar
import platform
import datetime
import tempfile
import threading
import subprocess
import webbrowser
import importlib.util

# 🌐 Network e URL
import urllib.parse
import urllib.request
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from collections import defaultdict

# 🎨 Interfaccia grafica Tkinter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel, Label, Button

# 🔒 Alias personalizzato (se serve per escaping HTML)
import html as html_escape  # facoltativo se serve solo una volta


# URL del file su GitHub (sostituiscilo con il tuo link reale)
URL_PDF = "https://raw.githubusercontent.com/Renato-4132/Casa-Facile/refs/heads/main/Casa%20Facile.pdf"
GITHUB_FILE_URL = "https://raw.githubusercontent.com/Renato-4132/Casa-Facile/refs/heads/main/Casa%20Facile.pyw"
ICON_URL = "https://github.com/Renato-4132/Casa-Facile/blob/main/casa-facile.png?raw=true"
NOME_FILE = "Casa Facile.pyw"  # Nome del file da salvare
REPO_OWNER = "Renato-4132"
REPO_NAME = "Casa-Facile"
NAME = "Casa-Facile"
EXPORTDB_DIR = "export"
DB_DIR = "db"
DB_FILE = os.path.join(DB_DIR, "spese_db.json")
DATI_FILE = os.path.join(DB_DIR,"rubrica.json")
UTENZE_DB = os.path.join(DB_DIR, "utenze_db.json")
SALDO_FILE = os.path.join(DB_DIR, "saldo_db.json")
SUPERMERCATI_DB = os.path.join(DB_DIR, "supermercati.json")
EXPORT_FILES = "export"
EXP_DB = os.path.join(DB_DIR, EXPORTDB_DIR)
PW_FILE = os.path.join(DB_DIR, "password.json")
MEM_CAT = os.path.join(DB_DIR, "memoria_categorie.json")
PORTA_DB = os.path.join(DB_DIR, "webserver_port.json")
RIMANDA_FILE = os.path.join(DB_DIR, "update.json")
PROMEMORIA_FILE = os.path.join(DB_DIR, "promemoria.json")
ICON_NAME = "casa-facile.png"

APRI_BROWSER = False
URL_QST = "https://forms.gle/VidTCh7ySkWHCAE6A"

# Imposta timeout self.show_custom_warning
# millisecondi
WARN_TIMEOUT = 20000  # millisecondi

# Imposta a True se vuoi chiusura con conferma self.show_custom_warning
# Imposta a False per forzare timeout chiusura  self.show_custom_warning
USE_WAIT_WINDOW = False

# 🔁 Imposta working directory
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 🔁 Nome directory
current_folder = os.path.basename(os.getcwd())

#Tolleranza SmartCat
toll = 30 #Euro

#Versione
VERSION = "8.8"

# ⏱️ Attiva/disattiva Timer Iconizza
ICONIZZA_INATTIVITA = True
# ⏱️ 5 minuti in millisecondi Timer Iconizza
TIMEOUT_INATTIVITA_MS = 300000

#Calcola la data limite usando la variabile ANNI_DA_MANTENERE
ANNI_DA_MANTENERE = 10

CATEGORIE_PREDEFINITE = [
    "Affettati",
    "Acqua",
    "Animali Domestici",
    "Articoli Bimbi",
    "Assorbenza",
    "Auto e Elettronica",
    "Birre",
    "Biscotti",
    "Bucato",
    "Caffè e Bevande",
    "Cancelleria/Party",
    "Carne",
    "Carta Casa/Igiene",
    "Carta e Alluminio",
    "Casalinghi/Tessile",
    "Cereali Colazione",
    "Cibi Etnici",
    "Cioccolato",
    "Conserve Pesce",
    "Cosmetici",
    "Cura dei Capelli",
    "Cura del Corpo",
    "Dolciumi e Caramelle",
    "Farine e Lieviti",
    "Formaggi Freschi",
    "Formaggi Stagionati",
    "Frutta Fresca",
    "Gastronomia",
    "Gelati",
    "Giardino e Fai da",
    "Igiene Persona",
    "Insalate Pronte",
    "Integratori/Sanitari",
    "Latte e Burro",
    "Latticini e Yogurt",
    "Legumi Secchi/Scatole",
    "Liquori e Distillati",
    "Marmellate/Creme",
    "Merende e Snack",
    "Molluschi/Crostacei",
    "Olio",
    "Ortaggi e Tuberi",
    "Pane e Panini",
    "Pasta Fresca",
    "Pasta Secca",
    "Pesce",
    "Piatti Pronti",
    "Pizze Surgelate",
    "Pollame",
    "Prodotti Bio",
    "Prodotti Dietetici",
    "Prodotti Veg/Vegan",
    "Pulizia Casa",
    "Riso",
    "Salumi",
    "Salse e Condimenti",
    "Snack Panetteria",
    "Snack Salati",
    "Sottoli/Sottaceti",
    "Spugne e Guanti",
    "Succhi/Bibite",
    "Surgelati Pesce",
    "Surgelati Vari",
    "Surgelati Verdura",
    "Sushi e Tartare",
    "Uova",
    "Varie",
    "Verdura Fresca",
    "Vini e Spumanti",
]


class CasaFacileWebHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path
        cookie = self.headers.get("Cookie", "")
        is_logged_in = "logged_in=true" in cookie
        if path == "/login":
            html = self.server.app.html_login(self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return
        elif path == "/logoff":
            self.send_response(303)
            self.send_header("Set-Cookie", "logged_in=false; Path=/")
            self.send_header("Location", "/login")
            self.end_headers()
            return
        if not is_logged_in:
            self.send_response(303)
            self.send_header("Location", "/login")
            self.end_headers()
            return
        if path == "/":
            html = self.server.app.html_form()
        elif path == "/gestione_categorie":
            html = self.server.app.html_gestione_categorie() 
        elif path.startswith("/stats"):
            html = self.server.app.stats_mensili_html()
        elif path.startswith("/lista"):
            html = self.server.app.html_lista_spese_mensili()
        elif path.startswith("/menu_esplora"):
            html = self.server.app.pagina_menu_esplora()
        elif path.startswith("/cerca_avanzata"):
            params = parse_qs(urlparse(self.path).query)
            html = self.server.app.pagina_risultati_avanzati(params)
        elif path.startswith("/modifica"):
            params = parse_qs(urlparse(self.path).query)
            html = self.server.app.modifica_voce_form(params)
        elif path.startswith("/report_annuo"):
            params = parse_qs(urlparse(self.path).query)
            html = self.server.app.pagina_statistiche_annuali_web()
        elif path.startswith("/utenze"):
            params = parse_qs(urlparse(self.path).query)
            anno = params.get("anno", [str(datetime.datetime.now().year)])[0]
            html = self.server.app.genera_html_utenze(UTENZE_DB, anno)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return
        elif path.startswith("/consultazione_supermercati"):
            html = self.server.app.genera_html_consultazione() 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return
        else:
            self.send_error(404, "Pagina non trovata")
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


    def do_POST(self):
        path = self.path
        cookie = self.headers.get("Cookie", "")
        is_logged_in = "logged_in=true" in cookie

        if path.startswith("/check_login"):
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            params = parse_qs(body)
            password = params.get("password", [""])[0].strip()

            if not self.server.app.leggi_hash():
                self.server.app.salva_hash(password)
                success = True
            else:
                success = self.server.app.verifica_password(password)

            if success:
                self.send_response(303)
                self.send_header("Set-Cookie", "logged_in=true; Path=/")
                self.send_header("Location", "/")
            else:
                self.send_response(303)
                self.send_header("Location", "/login?error=1")
            self.end_headers()
            return

        if not is_logged_in:
            self.send_response(303)
            self.send_header("Location", "/login")
            self.end_headers()
            return

        if path == "/":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            params = parse_qs(body)

            voce = {
                "date": params.get("data", ["01-01-2024"])[0],
                "categoria": params.get("categoria", ["Generica"])[0],
                "descrizione": params.get("descrizione", [""])[0],
                "importo": float(params.get("importo", ["0"])[0]),
                "tipo": params.get("tipo", ["Uscita"])[0]
            }

            self.server.app.aggiungi_voce_web(voce)
            self.server.app.carica_db_web()
            self.server.app.refresh_gui()
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if path == "/salva_categoria":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            params = parse_qs(body)
            operazione = params.get("operazione", [""])[0]
            if operazione == "aggiungi":
                self.server.app.add_categoria_web(params)
            elif operazione == "modifica":
                self.server.app.modifica_categoria_web(params)
            self.server.app.carica_db_web()
            self.server.app.refresh_gui()
            self.send_response(303)
            self.send_header("Location", "/gestione_categorie?status=success")
            self.end_headers()
            return
            
        if path == "/cancella_categoria":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            params = parse_qs(body)
            self.server.app.cancella_categoria_web(params)
            self.server.app.carica_db_web()
            self.server.app.refresh_gui()
            self.send_response(303)
            self.send_header("Location", "/gestione_categorie?status=deleted")
            self.end_headers()
            return
        if path == "/salva_modifica":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            params = parse_qs(body)
            self.server.app.salva_modifica_voce(params)
            self.server.app.refresh_gui()
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if path == "/cancella":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            params = parse_qs(body)
            giorno = params.get("data", [""])[0]
            idx = int(params.get("idx", ["-1"])[0])
            self.server.app.cancella_voce_web(giorno, idx)
            self.server.app.refresh_gui()
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
            return

        self.send_error(404, "Pagina POST non gestita")



class GestioneSpese(tk.Tk):

    CATEGORIA_RIMOSSA = "Categoria Rimossa"
    
    def __init__(self):
        super().__init__()

        self.withdraw()
        self.update_idletasks()
        
        initial_width = 1230
        initial_height = 620
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self._window_geometry = None
        self.load_window_geometry()

        if self._window_geometry:
            self.geometry(self._window_geometry)
        else:
            x = (screen_width // 2) - (initial_width // 2)
            y = (screen_height // 2) - (initial_height // 2)
            self.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        
        if not self.gestione_login():
            self.destroy()
            return  # oppure self.destroy(); exit()

        self.resizable(True, True)
        self.minsize(1230, 620)
        self.lift()
        self.focus_force()
        self.after(250, self.deiconify)
        
        self.set_app_icon()
        
        self.current_folder = current_folder
        self.backup_formato = 'zip'
               
        self.stats_view_mode = tk.StringVar(value="tabella")
        
        barra_menu = tk.Menu(self, background="black", foreground="white")
        self.config(menu=barra_menu)

        # ──────────────── GESTIONE DATI ────────────────
        menu_gestione = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="🗂️ Gestione", menu=menu_gestione)
        menu_gestione.add_command(label="👥 Utenze", accelerator="Ctrl+U", command=self.utenze)
        self.bind_all("<Control-u>", lambda e: self.utenze())
        menu_gestione.add_command(label="📅 Rubrica", accelerator="Ctrl+R", command=self.rubrica_app)
        self.bind_all("<Control-r>", lambda e: self.rubrica_app())
        menu_gestione.add_command(label="📋 Promemoria", accelerator="Ctrl+Y", command=self.gestisci_promemoria)
        self.bind_all("<Control-y>", lambda e: self.gestisci_promemoria())
        menu_gestione.add_separator()
        menu_gestione.add_command(label="📅 Stampa", accelerator="Ctrl+P", command=self.anteprima_e_stampa_txt)
        self.bind_all("<Control-p>", lambda e: self.anteprima_e_stampa_txt())
        menu_gestione.add_command(label="💰 Saldo", accelerator="Ctrl+S", command=self.open_saldo_conto)
        self.bind_all("<Control-s>", lambda e: self.open_saldo_conto())
        menu_gestione.add_command(label="📋 Controllo", accelerator="Ctrl+Z", command=self.calcola_mancanti)
        self.bind_all("<Control-z>", lambda e: self.calcola_mancanti())
        menu_gestione.add_command(label="📋 Calcolatrice", accelerator="Ctrl+E", command=self.apri_calcolatrice)
        self.bind_all("<Control-e>", lambda e: self.apri_calcolatrice())
        menu_gestione.add_command(label="📋 Cancella Voci Bulk", command=self.apri_cancella_spese_treeview_unica)
        
        menu_gestione.add_command(label="📋 Lista Spesa", command=self.spesa_supermercato)
         
        menu_gestione.add_command(label="✖️ Salva e chiudi", accelerator="Ctrl+Q", command=self._on_close)
        self.bind_all("<Control-q>", lambda e: 
        self._on_close())
        menu_gestione.add_separator()
        menu_gestione.add_command(label="✖️ Riduci a icona",accelerator="Ctrl+X",command=self.iconify)
        self.bind_all("<Control-x>", lambda e: self.iconify())
        
        # ──────────────── RICORRENZE ────────────────
        menu_ricorrenze = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="♻️ Ricorrenze", menu=menu_ricorrenze)
        menu_ricorrenze.add_command(label="📋 Ricorrenze", accelerator="Ctrl+T", command=self.mostra_ricorrenza_popup)
        self.bind_all("<Control-t>", lambda e: self.mostra_ricorrenza_popup())
        menu_ricorrenze.add_command(label="📋 Lista Ricorrenze", accelerator="Ctrl+L", command=self.mostra_lista_ricorrenze)
        self.bind_all("<Control-l>", lambda e: self.mostra_lista_ricorrenze())
        menu_ricorrenze.add_command(label="📋 Scadenze mese", accelerator="Ctrl+J", command=self.scadenze_mese)
        self.bind_all("<Control-j>", lambda e: self.scadenze_mese())

        # ──────────────── ANALISI E REPORT ────────────────
        menu_analisi = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="📊 Analisi", menu=menu_analisi)
        menu_analisi.add_command(label="🔍 Cerca", accelerator="Ctrl+F", command=self.cerca_operazioni)
        self.bind_all("<Control-f>", lambda e: self.cerca_operazioni())
        menu_analisi.add_command(label="📊 Confronta", accelerator="Ctrl+C", command=self.open_compare_window)
        self.bind_all("<Control-c>", lambda e: self.open_compare_window())
        menu_analisi.add_command(label="📊 Time Machine", accelerator="Ctrl+T", command=self.time_machine)
        self.bind_all("<Control-t>", lambda e: self.time_machine())
        menu_analisi.add_command(label="📂 Aggrega", accelerator="Ctrl+G", command=self.gruppo_categorie)
        self.bind_all("<Control-g>", lambda e: self.gruppo_categorie())
        menu_analisi.add_command(label="📋 Report", accelerator="Ctrl+L", command=self.calcola_statistiche_annuali)
        self.bind_all("<Control-l>", lambda e: self.calcola_statistiche_annuali())
        menu_analisi.add_command(label="📋 Grafici", accelerator="Alt+H", command=self.mostra_analisi_grafici)
        self.bind_all("<Alt-h>", lambda e: self.mostra_analisi_grafici())

        # ──────────────── FINANZE ────────────────
        menu_finanze = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="💸 Finanze", menu=menu_finanze)
        menu_finanze.add_command(label="📊 Finanziamenti", accelerator="Ctrl+O", command=self.calcolo_mutuo_prestito)
        self.bind_all("<Control-o>", lambda e: self.calcolo_mutuo_prestito())

        # ──────────────── ESTRAZIONI ────────────────
        menu_estrazioni = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="🗃️ Estrazioni", menu=menu_estrazioni)
        menu_estrazioni.add_command(label="📅 Estrai Giorno", accelerator="Alt+J", command=self.export_giorno_forzato)
        self.bind_all("<Alt-j>", lambda e: self.export_giorno_forzato())
        menu_estrazioni.add_command(label="📅 Estrai Mese", accelerator="Alt+K", command=self.export_month_detail)
        self.bind_all("<Alt-k>", lambda e: self.export_month_detail())
        menu_estrazioni.add_command(label="📊 Estrai Anno", accelerator="Alt+L", command=self.export_anno_dettagliato)
        self.bind_all("<Alt-l>", lambda e: self.export_anno_dettagliato())

        # ──────────────── CATEGORIE ────────────────
        menu_categorie = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="📆 Categorie", menu=menu_categorie)
        menu_categorie.add_command(label="⏰ Analisi Categorie", accelerator="Ctrl+K", command=self.open_analisi_categoria)
        self.bind_all("<Control-k>", lambda e: self.open_analisi_categoria())
        menu_categorie.add_command(label="⏰ Suggerisci Categorie", accelerator="Ctrl+Shift+K", command=self.apri_categorie_suggerite)
        self.bind_all("<Control-Shift-K>", lambda e: self.apri_categorie_suggerite())
        menu_categorie.add_command(label="⏰ Gestisci Categorie", accelerator="Ctrl+Shift+T", command=self.mostra_categorie_popup)
        self.bind_all("<Control-Shift-T>", lambda e: self.mostra_categorie_popup())
        menu_categorie.add_command(label="⏰ Gestisci Categorie Bulk", accelerator="Ctrl+Shift+S", command=self.apri_cancella_multiplo)
        self.bind_all("<Control-Shift-S>", lambda e: self.apri_cancella_multiplo())

        # ──────────────── WEBSERVER ────────────────
        menu_webserver = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="🌐 Webserver", menu=menu_webserver)
        menu_webserver.add_command(label="🌐 Apri WebServer", command=self.apri_webserver)
        menu_webserver.add_command(label="🌐 Apri Web Port", command=self.apri_webserver_port)

        # ──────────────── DATABASE ────────────────
        menu_db = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="💾 Database", menu=menu_db)
        menu_db.add_command(label="📥 Importa DB", command=self.import_db)
        menu_db.add_command(label="📤 Esporta DB", command=self.export_db)
        menu_db.add_command(label="📤 Reset DB", command=self.show_reset_dialog)
        menu_db.add_command(label="📤 Esegui Backup", command=self.esegui_backup_zip)
        
        # ──────────────── INFO ────────────────
        menu_info = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="🛈 Info", menu=menu_info)
        menu_info.add_command(label="🛈 Info", command=self.show_info_app, accelerator="Ctrl+I")
        self.bind_all("<Control-i>", lambda e: self.show_info_app())
        menu_info.add_command(label="📘 Apri Manuale", command=self.scarica_manuale, accelerator="Ctrl+M")
        self.bind_all("<Control-m>", lambda e: self.scarica_manuale())

        # ──────────────── SISTEMA ────────────────
        menu_sistema = tk.Menu(barra_menu, tearoff=0)
  
        # Carica Server
        #threading.Thread(target=self.start_web_server, daemon=True).start()

        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        if not os.path.exists(EXP_DB):
            os.makedirs(EXP_DB)
            
        backup_incrementale(DB_FILE)
        backup_incrementale(SALDO_FILE)
        backup_incrementale(DATI_FILE)
        backup_incrementale(UTENZE_DB)

        
        backup_incrementale(PW_FILE)
        backup_incrementale(MEM_CAT)
        backup_incrementale(PORTA_DB)
        
        backup_incrementale(RIMANDA_FILE)
        backup_incrementale(PROMEMORIA_FILE)
        backup_incrementale(SUPERMERCATI_DB)
        self.aggiorna_titolo_finestra()
        
        self.categoria_bloccata = False
        self.suggerimenti_attivi = True # ⛔ Disattiva suggerimento categoria=spesa

        #Timeout Iconizza
        if ICONIZZA_INATTIVITA:
            self._timeout_inattivita = TIMEOUT_INATTIVITA_MS
            self._timer_inattivita = None
            self._attiva_timer_inattivita()
        
        self.categorie = ["Generica", self.CATEGORIA_RIMOSSA]
        self.categorie_tipi = {"Generica": "Uscita", self.CATEGORIA_RIMOSSA: "Uscita"}
        self.spese = {}
        self.ricorrenze = {}  
        self.modifica_idx = None
        self.stats_refdate = datetime.date.today()
        self.load_db()
        self.carica_memoria_descrizioni()

        style = ttk.Style()
        self.configure(bg="#1e1e1e")

        style.configure("RedBold.TLabelframe.Label", foreground="red", font=("Arial", 10, "bold"))
        style.configure("Custom.Treeview", font=("Arial", 10))
        style.configure("Custom.Treeview.Heading", font=("Arial", 10))
        style.configure("Stat.Custom.Treeview", font=("Arial", 10))
        style.configure("Stat.Custom.Treeview.Heading", font=("Arial", 10))
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10))
        style.configure("Big.Treeview", font=("Arial", 10), rowheight=20)
        style.configure("Big.Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("BlackFrame.TFrame", background="#2e2e2e")
        
        style.configure("Highlight.TCombobox", foreground="red")
        style.configure('Border.TCombobox', fieldbackground='white', relief='solid', borderwidth=1) 

        style.configure("Timer.TLabel", foreground="gray", font=("Helvetica", 10, "bold"))
        style.configure("Saldo.TLabel", foreground="green", font=("Arial", 14))

        style.configure("Yellow.TButton", background="yellow", foreground="black", font=("Arial", 8), width=2)
        style.map("Yellow.TButton", background=[("active", "#ffeb99")])
        style.configure("Giallo.TButton", background="yellow", foreground="black", font=("Arial", 8))
        style.map("Giallo.TButton", background=[("active", "#ffeb99")])
        style.configure("Verde.TButton", background="#32CD32", foreground="black", font=("Arial", 8))
        style.map("Verde.TButton", background=[("active", "#b2fab2")])
        style.configure("Rosso.TButton", background="red", foreground="black", font=("Arial", 8))
        style.map("Rosso.TButton", background=[("active", "#ff9999")])
        style.configure("Arancio.TButton", background="#FFA500", foreground="black", font=("Arial", 8))
        style.map("Arancio.TButton", background=[("active", "#F7DC6F")])
        style.configure("Blu.TButton", background="dodgerblue", foreground="black", font=("Arial", 8))
        style.map("Blu.TButton", background=[("active", "#3399FF")])

        style.configure("GreenOutline.TButton", foreground="green", background="#dff0d8",
                        borderwidth=2, relief="solid", font=("Arial", 10, "bold"))
        style.map("GreenOutline.TButton", bordercolor=[("!disabled", "green")], foreground=[("!disabled", "green")])

        style.configure("RedOutline.TButton", foreground="red", background="#f2dede",
                        borderwidth=2, relief="solid", font=("Arial", 10, "bold"))
        style.map("RedOutline.TButton", bordercolor=[("!disabled", "red")], foreground=[("!disabled", "red")])

        main_frame = ttk.Frame(self, style="BlackFrame.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        cal_frame = ttk.Frame(main_frame, style="BlackFrame.TFrame")
        cal_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        today = datetime.date.today()
        
        self.cal = Calendar(
            cal_frame,
            selectmode="day",
            year=today.year,
            month=today.month,
            day=today.day,
            date_pattern="dd-mm-yyyy",
            locale="it_IT",
            font=("Arial", 10),
            weekendbackground="lightblue",
            weekendforeground="darkblue",
            selectbackground="blue",
            showothermonthdays=False
        )
        
        self.cal.pack(fill="both", expand=True)

        legenda = ttk.Frame(cal_frame, style="BlackFrame.TFrame")
        legenda.pack(pady=(4, 0))
        btn_oggi = ttk.Button(legenda, text="↺ Oggi", command=self.goto_today, width=8, style="Giallo.TButton")
        btn_oggi.pack(side="left", padx=3)

        ttk.Label(legenda, text="Entrata", background="lightgreen", width=8, anchor="center", font=("Arial", 10)).pack(side="left", padx=3)
        ttk.Label(legenda, text="Uscita", background="lightcoral", width=8, anchor="center", font=("Arial", 10)).pack(side="left", padx=3)
        ttk.Label(legenda, text="Entrata+Uscita", background="khaki", width=14, anchor="center", font=("Arial", 10)).pack(side="left", padx=3)
        ttk.Label(legenda, text="Weekend", background="lightblue", font=("Arial", 10), width=10, anchor="center").pack(side="left", padx=3)
        ttk.Label(legenda, text="Sel.", background="blue", foreground="white", font=("Arial", 10), width=6, anchor="center").pack(side="left", padx=3)

        oggi = datetime.date.today()
        self.cal.calevent_create(oggi, "Oggi", "today")
        self.cal.tag_config("today", background="gold", foreground="black")

        try:
           self.cal._header_month.config(font=("Arial", 14, "bold"))
           self.cal._header_year.config(font=("Arial", 14, "bold"))
        except:
           pass

        
        self.cal.pack(fill="x", expand=True, padx=10, pady=5)
        self.cal.tag_config("verde", background="lightgreen")
        self.cal.tag_config("rosso", background="lightcoral")
        self.cal.tag_config("misto", background="khaki")

        self.cal.bind("<<CalendarSelected>>", self.on_calendar_change)
        self.cal.bind("<<CalendarMonthChanged>>", self.on_month_changed)
        self.colora_giorni_spese()
         
        self.estratto_month_var = tk.StringVar(value=f"{today.month:02d}")
        self.estratto_year_var = tk.StringVar(value=str(today.year))

        current_year = today.year
        self.years = [str(y) for y in range(current_year - 15, current_year + 11)]
        self.months = [
            "01 - Gennaio", "02 - Febbraio", "03 - Marzo", "04 - Aprile", "05 - Maggio", "06 - Giugno",
            "07 - Luglio", "08 - Agosto", "09 - Settembre", "10 - Ottobre", "11 - Novembre", "12 - Dicembre"
        ]

        riepilogo_frame = ttk.Frame(cal_frame)
        riepilogo_frame.pack(fill=tk.X, padx=2, pady=(8, 8))

        self.totalizzatore_mese_frame = ttk.LabelFrame(riepilogo_frame, text="⚙️ Riepilogo Mese Attuale", style="RedBold.TLabelframe")
        self.totalizzatore_mese_frame.pack(side="left", fill="both", expand=True, padx=(0, 4))
        self.totalizzatore_mese_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.totalizzatore_mese_frame, text="Totale Entrate mese:", foreground="green", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(6,0), pady=(2, 0))
        self.totalizzatore_mese_entrate_label = ttk.Label(self.totalizzatore_mese_frame, text="0.00 €", foreground="green", font=("Arial", 10, "bold"))
        self.totalizzatore_mese_entrate_label.grid(row=0, column=1, sticky="e", padx=(0,6), pady=(2, 0))
        
        ttk.Label(self.totalizzatore_mese_frame, text="Totale Uscite mese:", foreground="red", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=(6,0), pady=(2, 0))
        self.totalizzatore_mese_uscite_label = ttk.Label(self.totalizzatore_mese_frame, text="0.00 €", foreground="red", font=("Arial", 10, "bold"))
        self.totalizzatore_mese_uscite_label.grid(row=1, column=1, sticky="e", padx=(0,6), pady=(2, 0))

        ttk.Label(self.totalizzatore_mese_frame, text="Differenza mese:", foreground="blue", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=(6,0), pady=(2, 4))
        self.totalizzatore_mese_diff_label = ttk.Label(self.totalizzatore_mese_frame, text="0.00 €", foreground="blue", font=("Arial", 10, "bold"))
        self.totalizzatore_mese_diff_label.grid(row=2, column=1, sticky="e", padx=(0,6), pady=(2, 4))

        self.totalizzatore_frame = ttk.LabelFrame(riepilogo_frame, text="⚙️ Riepilogo Anno Attuale", style="RedBold.TLabelframe")
        self.totalizzatore_frame.pack(side="left", fill="both", expand=True, padx=(4, 0))
        self.totalizzatore_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.totalizzatore_frame, text="Totale Entrate:", foreground="green", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=(6,0), pady=(2, 0))
        self.totalizzatore_entrate_label = ttk.Label(self.totalizzatore_frame, text="0.00 €", foreground="green", font=("Arial", 10, "bold"))
        self.totalizzatore_entrate_label.grid(row=0, column=1, sticky="e", padx=(0,6), pady=(2, 0))

        ttk.Label(self.totalizzatore_frame, text="Totale Uscite:", foreground="red", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=(6,0), pady=(2, 0))
        self.totalizzatore_uscite_label = ttk.Label(self.totalizzatore_frame, text="0.00 €", foreground="red", font=("Arial", 10, "bold"))
        self.totalizzatore_uscite_label.grid(row=1, column=1, sticky="e", padx=(0,6), pady=(2, 0))
        
        ttk.Label(self.totalizzatore_frame, text="Differenza:", foreground="blue", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=(6,0), pady=(2, 4))
        self.totalizzatore_diff_label = ttk.Label(self.totalizzatore_frame, text="0.00 €", foreground="blue", font=("Arial", 10, "bold"))
        self.totalizzatore_diff_label.grid(row=2, column=1, sticky="e", padx=(0,6), pady=(2, 4))

        self.spese_mese_frame = ttk.LabelFrame(cal_frame, text="Analisi Mese Attuale", style="RedBold.TLabelframe")
        self.spese_mese_frame.pack(fill=tk.BOTH, expand=False, padx=2, pady=(2,4))
        self.spese_mese_tree = ttk.Treeview(
            self.spese_mese_frame,
            style="Custom.Treeview",
            columns=("Data", "Categoria", "Descrizione", "Importo", "Tipo"),
            show="headings",
            height=30  
        )
        self.spese_mese_tree.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.spese_mese_tree.bind("<Double-1>", self.on_spese_mese_tree_double_click) 
        
        self.spese_mese_tree.heading("Data", text="Data")
        self.spese_mese_tree.heading("Categoria", text="Categoria")
        self.spese_mese_tree.heading("Descrizione", text="Descrizione")
        self.spese_mese_tree.heading("Importo", text="Importo (€)")
        self.spese_mese_tree.heading("Tipo", text="Tipo")
        self.spese_mese_tree.column("Data", width=80, anchor="center")
        self.spese_mese_tree.column("Categoria", width=120, anchor="center")
        self.spese_mese_tree.column("Descrizione", width=100, anchor="center")
        self.spese_mese_tree.column("Importo", width=82, anchor="e")
        self.spese_mese_tree.column("Tipo", width=50, anchor="center")
        self.spese_mese_tree.tag_configure('entrata', foreground='green')
        self.spese_mese_tree.tag_configure('uscita', foreground='red')
        for col in self.spese_mese_tree["columns"]:
            self.spese_mese_tree.heading(col, command=lambda _col=col: self.treeview_sort_column(self.spese_mese_tree, _col, False))
 
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stat_frame = ttk.LabelFrame(right_frame, text="⚙️ Riepilogo Avanzato", style="RedBold.TLabelframe")
        stat_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=(8, 8))
        stat_frame.rowconfigure(3, weight=1)
        stat_frame.columnconfigure(0, weight=1)
        mode_frame = ttk.Frame(stat_frame)
        mode_frame.grid(row=0, column=0, sticky="ew", padx=6, pady=(4, 0))
        
        self.bind("<Escape>", lambda e: self.mostra_treeview_statistiche() if self.stats_view_mode.get() != "tabella" else None)


        self.stats_mode = tk.StringVar(value="giorno")

        stat_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=(8, 8))
        stat_frame.rowconfigure(3, weight=1)
        stat_frame.columnconfigure(0, weight=1)
        mode_frame = ttk.Frame(stat_frame)
        mode_frame.grid(row=0, column=0, sticky="ew", padx=6, pady=(4, 0))
        self.stats_mode = tk.StringVar(value="giorno")
        self.STATO_CORRENTE = 0
        self.STATI_VISTA = ["tabella", "grafico", "grafico_mensile", "grafico_saldo"]
        self.LABEL_PROSSIMO_STATO = [
            "📊",
            "📈",
            "⚖️",
            "📋"
        ]
        label_iniziale = self.LABEL_PROSSIMO_STATO[ (self.STATO_CORRENTE + 1) % len(self.STATI_VISTA) ]
        self.btn_ciclico = ttk.Button(mode_frame, text=label_iniziale, command=self.cicla_visualizzazione_statistiche, width=2, style="Blu.TButton")
        self.btn_ciclico.pack(side=tk.LEFT, padx=(5, 2)) 
        self.bind("<Right>", lambda e: self.cicla_visualizzazione_statistiche())
        self.bind("<Left>", lambda e: self.cicla_indietro())
        self.btn_analisi = ttk.Button(mode_frame, text="🔍", command=lambda: self.mostra_analisi_grafici(), width=2, style="Blu.TButton")
        self.btn_analisi.pack(side=tk.LEFT, padx=1) 
        ttk.Button(mode_frame, text="?", command=lambda: self.mostra_help(), width=2, style="Yellow.TButton").pack(side=tk.LEFT, padx=(1, 5))
        self.btn_giorno = ttk.Button(mode_frame, text="📅 Giorno", command=lambda: self.set_stats_mode("giorno"), width=9, style="Blu.TButton")
        self.btn_giorno.pack(side=tk.LEFT, padx=1)
        self.btn_mese = ttk.Button(mode_frame, text="📅 Mese", command=lambda: self.set_stats_mode("mese"), width=9, style="Blu.TButton")
        self.btn_mese.pack(side=tk.LEFT, padx=1)
        self.btn_anno = ttk.Button(mode_frame, text="📅 Anno", command=lambda: self.set_stats_mode("anno"), width=9, style="Blu.TButton")
        self.btn_anno.pack(side=tk.LEFT, padx=1)
        self.btn_totali = ttk.Button(mode_frame, text="📅 Totali", command=lambda: self.set_stats_mode("totali"), width=9, style="Blu.TButton")
        self.btn_totali.pack(side=tk.LEFT, padx=1)

        lbl_saldo_tot = ttk.Label(mode_frame, text="💰", style="Saldo.TLabel")
        lbl_saldo_tot.pack(side="right", anchor="e", padx=5)

        lbl_saldo_tot.bind("<Enter>", lambda e: self.show_tooltip_saldo(e))
        lbl_saldo_tot.bind("<Leave>", self.hide_tooltip_saldo)
        btn_spesa_super_icon = ttk.Label(
            mode_frame,
            text="🛒",
            cursor="hand2",
            style="Saldo.TLabel"
        )
        btn_spesa_super_icon.bind('<Button-1>', lambda e: self.spesa_supermercato())
        btn_spesa_super_icon.pack(side="right", anchor="e", padx=(0, 5))

        self.filtri_temporali = [self.btn_giorno, self.btn_mese, self.btn_anno, self.btn_totali]
        mode_frame_right = ttk.Frame(mode_frame)
        mode_frame_right.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.stats_label = ttk.Label(stat_frame, text="")
        self.stats_label.grid(row=1, column=0, sticky="w", padx=6, pady=(2, 0))
        totali_row = ttk.Frame(stat_frame)
        totali_row.grid(row=2, column=0, sticky="ew", padx=6, pady=(2, 0))
        self.totali_label = ttk.Label(totali_row, text="", font=("Arial", 11))
        
        self.totali_label.pack(side=tk.LEFT)
        self.considera_ricorrenze_var = tk.BooleanVar(value=True)
        self.chk_ricorrenze = tk.Checkbutton(
            totali_row,
            text="Includi movimenti futuri nei totali",
            bg="yellow",
            activebackground="gold",
            variable=self.considera_ricorrenze_var,
            command=self.refresh_gui,
            font=("Arial", 8)
        )
        self.chk_ricorrenze.pack(side=tk.RIGHT, padx=12)
        table_container = tk.Frame(stat_frame)
        table_container.grid(row=3, column=0, sticky="nsew", padx=4, pady=4)
        self.stats_table = ttk.Treeview(table_container, columns=("A", "B", "C", "D", "E", "F"), show="headings",style="Stat.Custom.Treeview")
        self.stats_table.pack(fill=tk.BOTH, expand=True)
        self.stats_text_area = tk.Text(table_container, wrap=tk.WORD, state=tk.DISABLED, bg="#F0F0F0")
        headers = {
            "A": "🗓️ Data",
            "B": "📂 Categoria",
            "C": "📝 Descrizione",
            "D": "💰 Importo (€)",
            "E": "📌 Tipo",
            "F": "✏️ Modifica"
        }
        for col in ("A", "B", "C", "D", "E", "F"):
            self.stats_table.heading(col, text=headers[col], command=lambda _col=col: self.treeview_sort_column(self.stats_table, _col, False))
        self.stats_table.column("A", width=100, anchor="center")
        self.stats_table.column("B", width=150, anchor="center")
        self.stats_table.column("C", width=250, anchor="w")
        self.stats_table.column("D", width=100, anchor="e")
        self.stats_table.column("E", width=80, anchor="center")
        self.stats_table.column("F", width=60, anchor="center")
        self.set_stats_mode("giorno")
        self.stats_table.tag_configure("uscita", foreground="red")
        self.stats_table.tag_configure("entrata", foreground="green")
        self.stats_table.bind("<Double-1>", self.on_stats_table_double_click)
        self.stats_table.bind("<ButtonRelease-1>", self.on_table_click)
        self.stats_table.bind("<Button-3>", self.on_stats_table_right_click)

        form_frame = ttk.LabelFrame(right_frame, text="⚙️ Registra o Modifica Movimento", style="RedBold.TLabelframe")
        form_frame.pack(fill=tk.X, padx=2, pady=(8, 8))
        form_frame.grid_columnconfigure(1, weight=1)

        row = 0
        ttk.Label(form_frame, text="Data spesa:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="e")

        self.data_spesa_var = tk.StringVar(value=today.strftime("%d-%m-%Y"))

        data_frame = ttk.Frame(form_frame)
        data_frame.grid(row=row, column=1, columnspan=2, sticky="w")

        self.data_spesa_entry = ttk.Entry(
            data_frame,
            width=15,
            font=("Arial", 10, "bold"),
            textvariable=self.data_spesa_var
        )
        self.data_spesa_entry.pack(side="left")

        self.btn_cal_data_spesa = ttk.Button(
            data_frame,
            text="📅",
            width=2,
            command=lambda: self.mostra_calendario_popup(self.data_spesa_entry, self.data_spesa_var),
            style="Yellow.TButton"
        )
             
        self.btn_cal_data_spesa.pack(side="left", padx=4)

        self.btn_reset_data_spesa = ttk.Button(
            data_frame,
            text="↺",
            command=self.reset_data_spesa,
            style="Yellow.TButton"
        )
        self.btn_reset_data_spesa.pack(side="left", padx=4)

        self.blocca_data_var = tk.BooleanVar(value=False)
        self.checkbox_blocca_data = tk.Checkbutton(
            data_frame,
            text="Blocca data",
            variable=self.blocca_data_var,
            command=self.on_blocca_data_changed
        )
        self.checkbox_blocca_data.pack(side="left", padx=4)
        btn_importa_popup = ttk.Button(data_frame, text="📥 Importa", command=self.apri_finestra_importa, style="Blu.TButton")
        btn_importa_popup.pack(side="left", padx=6)
        row += 1
        
        ttk.Label(form_frame, text="🔍 Seleziona categoria:").grid(row=row, column=0, sticky="e")
        combo_frame = ttk.Frame(form_frame)
        combo_frame.grid(row=row, column=1, sticky="w", columnspan=2)  

        self.cat_sel = tk.StringVar(value=self.categorie[0])
        
        self.cat_menu = ttk.Combobox(combo_frame, textvariable=self.cat_sel, values=sorted(self.categorie), state="readonly", width=25, font=("Arial", 11, "bold"))
        self.cat_menu.pack(side="left")
        
        self.label_smartcat = ttk.Label(combo_frame, text="💡 SmartCat attiva", foreground="red", font=("Arial", 9, "bold"))
        self.label_smartcat.pack(side="left", padx=(6, 0))
        
        self.btn_spese_simili = ttk.Button(combo_frame, text=f"🔍 Voci simili ± {toll}", style="Blu.TButton", command=self.mostra_spese_simili)

        self.btn_spese_simili.pack(side="left", padx=(6, 0))
        self.btn_spese_simili.pack_forget()  # 👈 lo nascondi all'avvio

        if not self.suggerimenti_attivi:
            self.label_smartcat.config(text="🛠️ SmartCat disattiva", foreground="green")
            self.aggiorna_bottone_spese_simili(visibile=False)
        else:
             self.label_smartcat.config(text="💡 SmartCat attiva", foreground="red")
             
        self.cat_menu.bind("<<ComboboxSelected>>", self.on_categoria_changed)
        row += 1
        
        ttk.Label(form_frame, text="ℹ️ Descrizione:").grid(row=row, column=0, sticky="e")
        def convalida_descrizione(nuovo_valore_1):
         return len(nuovo_valore_1) <= 30

        vdesc = form_frame.register(convalida_descrizione)
        self.desc_entry = ttk.Entry(form_frame, width=30, validate="key", validatecommand=(vdesc, "%P"))
        self.desc_entry.grid(row=row, column=1, sticky="w")
        row += 1
        
        ttk.Label(form_frame, text="💰 Importo (€):⏎").grid(row=row, column=0, sticky="e")
        importo_frame = ttk.Frame(form_frame)
        
        calc_button = ttk.Button(importo_frame, text="🛠", style="Yellow.TButton", command=self.apri_calcolatrice)
        calc_button.pack(side="right")

        def convalida_input(nuovo_valore_2):
         if nuovo_valore_2 == "":
              return True  
         import re
         # Imposta massimo
         return len(nuovo_valore_2) <= 8 and re.match(r"^\d*[.,]?\d{0,2}$", nuovo_valore_2) is not None

        vcmd = form_frame.register(convalida_input)       
        self.imp_entry = ttk.Entry(importo_frame, width=12, validate="key", validatecommand=(vcmd, "%P"))  
        self.imp_entry.pack(side=tk.LEFT)      
        self.imp_entry.bind("<KeyRelease>", self.aggiorna_categoria_automatica)
        self.imp_entry.bind("<Return>", lambda event: self.add_spesa()) 
        self.imp_entry.bind("<KP_Enter>", lambda event: self.add_spesa()) 
        importo_frame.grid(row=row, column=1, sticky="w")
       
        row += 1

        pannello_bottoni = tk.Frame(form_frame)
        pannello_bottoni.grid(row=row, column=1, columnspan=8, sticky="w", pady=4)

        self.btn_aggiungi = ttk.Button(pannello_bottoni, text="💸 Aggiungi Movimento", command=self.add_spesa, style="Verde.TButton")
        self.btn_aggiungi.pack(side="left", padx=4)
        self.btn_reset_form = ttk.Button(pannello_bottoni,text="↺",width=2,command=self.reset_form, style="Giallo.TButton")
        self.btn_reset_form.pack(side="left", padx=(4, 0))
        self.btn_modifica = ttk.Button(pannello_bottoni, text="💾 Salva Modifica", command=self.salva_modifica, state=tk.DISABLED, style="Verde.TButton")
        self.btn_modifica.pack(side="left", padx=4)
        self.btn_cancella = ttk.Button(pannello_bottoni, text="❌ Cancella", command=self.cancella_voce, state=tk.DISABLED, style="Rosso.TButton")
        self.btn_cancella.pack(side="left", padx=4)
        btn_ricorrenze = ttk.Button(pannello_bottoni, text="♻️ Ricorrenze", command=lambda: self.mostra_ricorrenza_popup(), style="Blu.TButton")
        btn_ricorrenze.pack(side="left", padx=4)
        self.btn_gestisci_categorie = ttk.Button(pannello_bottoni, text="✅ Categorie", command=lambda: self.mostra_categorie_popup(), style="Blu.TButton")
        self.btn_gestisci_categorie.pack(side="left", padx=4)
        btn_scadenze_mese = ttk.Button(pannello_bottoni, text="✅", command=lambda: self.scadenze_mese(), style="Blu.TButton", width=2)
        btn_scadenze_mese.pack(side="left", padx=4)
        #btn_calcola_mancanti_popup = ttk.Button(pannello_bottoni, text="📥", command=self.calcola_mancanti, style="Blu.TButton", width=2)
        #btn_calcola_mancanti_popup.pack(side="left", padx=4)
        self.btn_promemoria = ttk.Button(pannello_bottoni, text="📝", command=self.gestisci_promemoria, style="Blu.TButton", width=2)
        self.btn_promemoria.pack(side="left", padx=4)

        row += 1

        style.configure('GreenOutline.TButton', foreground='green', background='#dff0d8', borderwidth=2, relief='solid', font=('Arial', 10, 'bold'))
        style.map('GreenOutline.TButton',
            bordercolor=[('!disabled', 'green')], foreground=[('!disabled', 'green')]
        )
        style.configure('RedOutline.TButton', foreground='red', background='#f2dede', borderwidth=2, relief='solid', font=('Arial', 10, 'bold'))
        style.map('RedOutline.TButton',
            bordercolor=[('!disabled', 'red')], foreground=[('!disabled', 'red')]
        )
        cat_default_type = self.categorie_tipi.get(self.cat_sel.get(), "Uscita")
        self.tipo_spesa_var = tk.StringVar(value=cat_default_type)
        btn_style = 'GreenOutline.TButton' if self.tipo_spesa_var.get() == "Entrata" else 'RedOutline.TButton'
        self.btn_tipo_spesa = ttk.Button(
            importo_frame,
            text=self.tipo_spesa_var.get(),
            width=10,
            command=self.toggle_tipo_spesa,
            style=btn_style,
            takefocus=0
        )
        self.btn_tipo_spesa.pack(side=tk.LEFT, padx=8)
        self.metodo_pagamento_var = tk.StringVar(value="") 
        metodi = ["", "💰 Contanti", "🔄 RID/SDD", "🏦 Bonifico", "💎 C.Credito", "💳 C.Debito", ]
        self.metodo_pagamento_combobox = ttk.Combobox(
            importo_frame, 
            textvariable=self.metodo_pagamento_var, 
            values=metodi,
            state="readonly",
            style="Border.TCombobox",
            width=10
        )
        self.metodo_pagamento_combobox.pack(side=tk.LEFT, padx=4) 
        self.metodo_pagamento_combobox.bind("<<ComboboxSelected>>", self.aggiorna_descrizione_con_simbolo)
        row += 1
        self.lbl_tipo_percentuale = ttk.Label(importo_frame, text="", font=("Arial", 9, "bold"))
        self.lbl_tipo_percentuale.pack(side=tk.LEFT, padx=4)
        self.on_categoria_changed(manuale=False)
        self.refresh_gui()
        self.after(1000, self.check_aggiornamento_con_api)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def aggiorna_descrizione_con_simbolo(self, event=None):
        simboli_metodo = {
            "💰 Contanti": "💰",
            "🔄 RID/SDD": "🔄",
            "💎 C.Credito": "💎",
            "💳 C.Debito": "💳",
            "🏦 Bonifico": "🏦"
        }
        desc_attuale = self.desc_entry.get().strip()
        metodo_selezionato = self.metodo_pagamento_var.get()
        desc_pulita = desc_attuale
        simboli_possibili = list(simboli_metodo.values()) 
        simbolo_trovato = None
        for simbolo in simboli_possibili:
            if desc_pulita.startswith(simbolo):
                simbolo_trovato = simbolo
                desc_pulita = desc_pulita[len(simbolo_trovato):].lstrip() 
                break 
        nuovo_simbolo = simboli_metodo.get(metodo_selezionato, '')
        
        if not desc_pulita and metodo_selezionato:
            testo_base_da_inserire = metodo_selezionato
        else:
            testo_base_da_inserire = desc_pulita
            
        self.desc_entry.delete(0, tk.END)
        if nuovo_simbolo:
            nuova_desc = f"{nuovo_simbolo} {desc_pulita}".strip()
            self.desc_entry.insert(0, nuova_desc)
        else:
            self.desc_entry.insert(0, desc_pulita)
        self.desc_entry.icursor(tk.END)

    def mostra_treeview_statistiche(self):
        self.STATO_CORRENTE = 0
        self.toggle_stats_view("tabella")
        self.btn_ciclico.config(text=self.LABEL_PROSSIMO_STATO[1])
    def cicla_visualizzazione_statistiche(self):
        NUOVO_STATO = (self.STATO_CORRENTE + 1) % len(self.STATI_VISTA)
        tipo_vista = self.STATI_VISTA[NUOVO_STATO]
        self.toggle_stats_view(tipo_vista)
        nuova_label = self.LABEL_PROSSIMO_STATO[NUOVO_STATO]
        self.btn_ciclico.config(text=nuova_label)
        self.STATO_CORRENTE = NUOVO_STATO
    def cicla_indietro(self, event=None):
        NUOVO_STATO = (self.STATO_CORRENTE - 1) % len(self.STATI_VISTA)
        tipo_vista = self.STATI_VISTA[NUOVO_STATO]
        self.toggle_stats_view(tipo_vista)
        nuova_label = self.LABEL_PROSSIMO_STATO[(NUOVO_STATO + 1) % len(self.STATI_VISTA)]
        self.btn_ciclico.config(text=nuova_label)
        self.STATO_CORRENTE = NUOVO_STATO

    def toggle_stats_view(self, tipo="grafico"):
        parent_frame = None
        if hasattr(self, 'stats_table') and self.stats_table and self.stats_table.winfo_exists():
            parent_frame = self.stats_table.master
            self.stats_table.destroy()
        if hasattr(self, 'stats_canvas') and self.stats_canvas and self.stats_canvas.winfo_exists():
            if parent_frame is None:
                parent_frame = self.stats_canvas.master
            self.stats_canvas.destroy()
        if parent_frame is None and hasattr(self, 'stats_container_frame'):
            parent_frame = stat_frame
        for btn in self.filtri_temporali:
            btn.pack_forget()
        if hasattr(self, 'stats_label'):
            self.stats_label.grid_remove()
        if hasattr(self, 'totali_label'):
            self.totali_label.pack_forget()
        if tipo in ("grafico", "grafico_mensile", "grafico_saldo"):
            self.stats_canvas = tk.Canvas(parent_frame, bg="white")
            self.stats_canvas.pack(fill=tk.BOTH, expand=True)
            nomi_mesi_italiano = [
                "", "Gen", "Feb", "Mar", "Apr", "Mag", "Giu", 
                "Lug", "Ago", "Set", "Ott", "Nov", "Dic"
            ]
            oggi = datetime.date.today()
            anno_corrente = oggi.year
            if tipo == "grafico":
                self.stats_view_mode.set("grafico")
                category_totals = defaultdict(float)
                for giorno, entries in self.spese.items():
                    if giorno.year != anno_corrente: # Filtra solo l'anno corrente
                        continue
                    for entry in entries:
                        if isinstance(entry, dict):
                            categoria = entry.get("categoria", "Altro")
                            importo = entry.get("importo", 0)
                            tipo_voce = entry.get("tipo", "")
                        elif isinstance(entry, tuple) and len(entry) >= 4:
                            categoria = entry[0]
                            importo = entry[2]
                            tipo_voce = entry[3]
                        else:
                            continue
                        if tipo_voce == "Uscita" and importo > 0:
                            category_totals[categoria] += importo
                self.data_for_chart = [{'label': cat, 'value': val} for cat, val in category_totals.items()]
                self.data_for_chart.sort(key=lambda x: x['value'], reverse=True)
                self.total_value = sum(item['value'] for item in self.data_for_chart)
                if not self.data_for_chart:
                    self.stats_canvas.after(50, lambda: self.stats_canvas.create_text(
                        self.stats_canvas.winfo_width() // 2, self.stats_canvas.winfo_height() // 2,
                        text="Nessuna spesa da visualizzare", font=("Helvetica", 16), fill="gray"
                    ))
                    return
                self.stats_canvas.bind("<Configure>", self.draw_bar_chart)
                self.stats_canvas.after(100, self.draw_bar_chart) 
            elif tipo == "grafico_mensile":
                self.visualizza_tutti_gli_anni = False
                self.stats_view_mode.set("grafico_mensile")
                mensili = defaultdict(lambda: {"Entrata": 0.0, "Uscita": 0.0})
                for giorno, entries in self.spese.items():
                    if giorno.year != anno_corrente: continue
                    for entry in entries:
                        if isinstance(entry, dict):
                            imp = entry.get("importo", 0)
                            tipo_voce = entry.get("tipo", "")
                        elif isinstance(entry, tuple) and len(entry) >= 4:
                            imp = entry[2]
                            tipo_voce = entry[3]
                        else: continue
                        mese = giorno.month
                        if tipo_voce in ("Entrata", "Uscita"):
                            mensili[mese][tipo_voce] += imp
                self.data_for_chart = []
                for mese in range(1, 13):
                    self.data_for_chart.append({
                        "label": nomi_mesi_italiano[mese],
                        "entrata": mensili[mese]["Entrata"],
                        "uscita": mensili[mese]["Uscita"]
                    })
                self.stats_canvas.bind("<Configure>", self.draw_mensile_chart)
                self.stats_canvas.after(100, self.draw_mensile_chart) 
            elif tipo == "grafico_saldo":
                self.visualizza_tutti_gli_anni = False
                self.stats_view_mode.set("grafico_saldo")
                mensili = defaultdict(lambda: {"Entrata": 0.0, "Uscita": 0.0})
                for giorno, entries in self.spese.items():
                    if giorno.year != anno_corrente: continue
                    for entry in entries:
                        if isinstance(entry, dict):
                            imp = entry.get("importo", 0)
                            tipo_voce = entry.get("tipo", "")
                        elif isinstance(entry, tuple) and len(entry) >= 4:
                            imp = entry[2]
                            tipo_voce = entry[3]
                        else: continue
                        mese = giorno.month
                        if tipo_voce == "Entrata":
                            mensili[mese]["Entrata"] += imp
                        elif tipo_voce == "Uscita":
                            mensili[mese]["Uscita"] += imp
                self.data_for_chart = []
                max_abs_val = 0
                for mese in range(1, 13):
                    saldo = mensili[mese]["Entrata"] - mensili[mese]["Uscita"]
                    self.data_for_chart.append({
                        "label": nomi_mesi_italiano[mese],
                        "saldo": saldo
                    })
                    if abs(saldo) > max_abs_val:
                        max_abs_val = abs(saldo)
                if max_abs_val == 0:
                    self.stats_canvas.after(50, lambda: self.stats_canvas.create_text(
                        self.stats_canvas.winfo_width() // 2, self.stats_canvas.winfo_height() // 2,
                        text="Nessun saldo disponibile (tutti i saldi sono zero).",
                        font=("Helvetica", 12), fill="gray"
                    ))
                    return
                self.stats_canvas.bind("<Configure>", self.draw_saldo_chart)
                self.stats_canvas.after(100, self.draw_saldo_chart) 
        else: # tipo == "tabella"
            self.stats_table = ttk.Treeview(parent_frame, columns=("A", "B", "C", "D", "E", "F"), show="headings", style="Stat.Custom.Treeview")
            headers = {
                "A": "🗓️ Data", "B": "📂 Categoria", "C": "📝 Descrizione",
                "D": "💰 Importo (€)", "E": "📌 Tipo", "F": "✏️ Modifica"
            }
            for col in headers:
                self.stats_table.heading(col, text=headers[col], command=lambda _col=col: self.treeview_sort_column(self.stats_table, _col, False))
            self.stats_table.column("A", width=100, anchor="center")
            self.stats_table.column("B", width=150, anchor="center")
            self.stats_table.column("C", width=250, anchor="w")
            self.stats_table.column("D", width=100, anchor="e")
            self.stats_table.column("E", width=80, anchor="center")
            self.stats_table.column("F", width=60, anchor="center")
            
            self.set_stats_mode("giorno")
            self.stats_table.tag_configure("uscita", foreground="red")
            self.stats_table.tag_configure("entrata", foreground="green")
            self.stats_table.bind("<Double-1>", self.on_stats_table_double_click)
            self.stats_table.bind("<ButtonRelease-1>", self.on_table_click)
            self.stats_table.bind("<Button-3>", self.on_stats_table_right_click)
            self.stats_table.pack(fill=tk.BOTH, expand=True) 
            if hasattr(self, 'stats_label'):
                self.stats_label.grid()
            if hasattr(self, 'totali_label'):
                self.totali_label.pack(side=tk.LEFT)
            self.stats_view_mode.set("tabella")
            for btn in self.filtri_temporali:
                btn.pack(side=tk.LEFT, padx=1)
                
    def draw_bar_chart(self, event=None):
        if self.stats_view_mode.get() != "grafico":
            return
        canvas = self.stats_canvas
        canvas.delete("all")
        if not hasattr(self, 'visualizza_tutti_gli_anni'):
            self.visualizza_tutti_gli_anni = False
        def toggle_anni():
            self.visualizza_tutti_gli_anni = not self.visualizza_tutti_gli_anni
            self.draw_bar_chart()
        canvas.update_idletasks()
        btn_text = "🗓 Tutti gli anni" if not self.visualizza_tutti_gli_anni else "📅 Solo anno corrente"
        btn_toggle = ttk.Button(canvas, text=btn_text, command=toggle_anni, style="Blu.TButton")
        canvas.create_window(canvas.winfo_width() - 10, 2, window=btn_toggle, anchor="ne")
        category_totals = defaultdict(float)
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        for giorno, entries in self.spese.items():
            if hasattr(giorno, "year") and (self.visualizza_tutti_gli_anni or giorno.year == anno_corrente):
                for entry in entries:
                    if isinstance(entry, dict):
                        categoria = entry.get("categoria", "Altro")
                        importo = entry.get("importo", 0)
                        tipo = entry.get("tipo", "")
                    elif isinstance(entry, tuple) and len(entry) >= 4:
                        categoria = entry[0]
                        importo = entry[2]
                        tipo = entry[3]
                    else:
                        continue
                    try:
                        importo = float(str(importo).replace(",", ".").replace("€", "").strip())
                    except Exception:
                        importo = 0
                    if tipo.lower() == "uscita" and importo > 0:
                        category_totals[categoria] += importo
        self.data_for_chart = [
            {'label': cat, 'value': val}
            for cat, val in category_totals.items()
            if val > 0
        ]
        self.data_for_chart.sort(key=lambda x: x['value'], reverse=True)
        self.data_for_chart = self.data_for_chart[:40] # Categorie Visulalizzate in tabella
        self.total_value = sum(item['value'] for item in self.data_for_chart)

        if not self.data_for_chart or self.total_value == 0:
            canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2,
                               text="Nessuna spesa da visualizzare", font=("Arial", 12))
            return
        COLORS = ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#A3A3A3", "#5AD45A"]
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        CHART_LEFT = 50
        CHART_RIGHT = canvas_width - 20
        CHART_TOP = 50
        CHART_BOTTOM = canvas_height - 130
        CHART_AREA_WIDTH = CHART_RIGHT - CHART_LEFT
        CHART_HEIGHT = CHART_BOTTOM - CHART_TOP
        if CHART_AREA_WIDTH < 100 or CHART_HEIGHT < 50:
            canvas.create_text(canvas_width // 2, canvas_height // 3,
                               text="Area di disegno insufficiente.", font=("Arial", 12))
            return
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        if self.visualizza_tutti_gli_anni:
            anni_presenti = [giorno.year for giorno in self.spese.keys() if hasattr(giorno, 'year')]
            min_anno = min(anni_presenti) if anni_presenti else anno_corrente
            periodo = f"({min_anno} - {anno_corrente})"
            titolo = f"📊 Uscite per Categoria (Tutto lo Storico) {periodo}"
        else:
            periodo = f"({anno_corrente})"
            titolo = f"📊 Uscite per Categoria - Anno Corrente {periodo}"
        canvas.create_text(canvas_width // 2, CHART_TOP / 3, 
                           text=titolo, 
                           font=("Arial", 8, "bold"), fill="black")
        self.total_annuale = 0
        for giorno, entries in self.spese.items():
            if hasattr(giorno, "year") and (self.visualizza_tutti_gli_anni or giorno.year == anno_corrente):
                for entry in entries:
                    if isinstance(entry, dict):
                        tipo = entry.get("tipo", "").strip().lower()
                        importo = entry.get("importo", 0)
                    elif isinstance(entry, tuple) and len(entry) >= 4:
                        tipo = str(entry[3]).strip().lower()
                        try:
                            importo = float(entry[2])
                        except Exception:
                            importo = 0
                    else:
                        continue
                    if tipo == "uscita" and importo > 0:
                        self.total_annuale += importo
        canvas.create_line(CHART_LEFT, CHART_BOTTOM, CHART_LEFT, CHART_TOP, fill="black", width=2)
        canvas.create_line(CHART_LEFT, CHART_BOTTOM, CHART_RIGHT, CHART_BOTTOM, fill="black", width=2)
        max_value = max(item['value'] for item in self.data_for_chart)
        num_bars = len(self.data_for_chart)
        bar_space_total = CHART_AREA_WIDTH / num_bars
        bar_width = bar_space_total * 0.7
        for i, item in enumerate(self.data_for_chart):
            bar_height = (item['value'] / max_value) * CHART_HEIGHT
            x_center = CHART_LEFT + (i + 0.5) * bar_space_total
            x1 = x_center - bar_width / 2
            x2 = x_center + bar_width / 2
            y1 = CHART_BOTTOM - bar_height
            y2 = CHART_BOTTOM
            color = COLORS[i % len(COLORS)]
            tag = f"barra_{i}"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=tag)
            canvas.create_text(x_center, CHART_BOTTOM + 60, text=item['label'], anchor="n", angle=45,
                               font=("Arial", 7, "bold"), fill=color)
            canvas.create_text(x_center, y1 - 5, text=f"{item['value']:.0f}", anchor="s",
                               font=("Arial", 7, "bold"), fill=color)
            tooltip_text = f"{item['label']}: €{item['value']:.2f}"
            canvas.tag_bind(tag, "<Enter>", lambda e, t=tooltip_text: self.show_tooltip(e, t))
            canvas.tag_bind(tag, "<Leave>", self.hide_tooltip)
            data_filter = {
                "anno": None if self.visualizza_tutti_gli_anni else str(anno_corrente),
                "mese": None,
                "categoria": item["label"],
                "tipo": "Uscita"
            }
            canvas.tag_bind(tag, "<Double-1>", lambda e, f=data_filter, l=item['label']:
                            self.mostra_transazioni_popup(f, f"Uscite per {l}"))
        
        canvas.create_text(CHART_LEFT - 5, CHART_TOP, text=f"{max_value:.0f}", anchor="e",
                           font=("Arial", 7), fill="black")
        canvas.create_text(CHART_LEFT - 5, CHART_BOTTOM, text="0", anchor="e",
                           font=("Arial", 7), fill="black")
        mostrate = len(self.data_for_chart)
        totali_disponibili = len([val for val in category_totals.values() if val > 0])
        messaggio_riepilogo = (
            f"Totale Visualizzato: {self.total_value:,.2f} €  |  "
            f"Totale Anno: {self.total_annuale:,.2f} €  |  "
            f"Categorie mostrate: {mostrate} su {totali_disponibili}"
        )
        canvas.create_text(
            canvas.winfo_width() // 2,
            canvas.winfo_height() - 10,
            text=messaggio_riepilogo,
            anchor="center", 
            font=("Arial", 8, "bold"), 
            fill="#4B0082"
        )
                       
    def draw_mensile_chart(self, event=None):
        if self.stats_view_mode.get() != "grafico_mensile":
            return
        canvas = self.stats_canvas
        canvas.delete("all")
        if not hasattr(self, 'visualizza_tutti_gli_anni_mensile'):
            self.visualizza_tutti_gli_anni_mensile = False
        def toggle_anni():
            self.visualizza_tutti_gli_anni_mensile = not self.visualizza_tutti_gli_anni_mensile
            self.draw_mensile_chart()
        canvas.update_idletasks()
        btn_text = "🗓 Tutti gli anni" if not self.visualizza_tutti_gli_anni_mensile else "📅 Solo anno corrente"
        btn_toggle = ttk.Button(canvas, text=btn_text, command=toggle_anni, style="Blu.TButton")
        canvas.create_window(canvas.winfo_width() - 10, 2, window=btn_toggle, anchor="ne")
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        if self.visualizza_tutti_gli_anni_mensile:
            aggregati = {}
            for giorno, entries in self.spese.items():
                if hasattr(giorno, "year"):
                    anno = giorno.year
                    if anno not in aggregati:
                        aggregati[anno] = {"label": str(anno), "entrata": 0.0, "uscita": 0.0}
                    for entry in entries:
                        tipo = entry[3] if isinstance(entry, tuple) else entry.get("tipo", "")
                        importo = float(entry[2]) if isinstance(entry, tuple) else float(entry.get("importo", 0))
                        if tipo == "Entrata":
                            aggregati[anno]["entrata"] += importo
                        elif tipo == "Uscita":
                            aggregati[anno]["uscita"] += importo
            self.data_for_chart = [aggregati[anno] for anno in sorted(aggregati)]
        else:
            mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
            mensili = [{"label": m, "entrata": 0.0, "uscita": 0.0} for m in mesi]
            for giorno, entries in self.spese.items():
                if hasattr(giorno, "year") and giorno.year == anno_corrente:
                    mese_index = giorno.month - 1
                    for entry in entries:
                        tipo = entry[3] if isinstance(entry, tuple) else entry.get("tipo", "")
                        importo = float(entry[2]) if isinstance(entry, tuple) else float(entry.get("importo", 0))
                        if tipo == "Entrata":
                            mensili[mese_index]["entrata"] += importo
                        elif tipo == "Uscita":
                            mensili[mese_index]["uscita"] += importo
            self.data_for_chart = mensili
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        CHART_LEFT = 60
        CHART_RIGHT = canvas_width - 20
        CHART_TOP = 50
        CHART_BOTTOM = canvas_height - 80
        CHART_AREA_WIDTH = CHART_RIGHT - CHART_LEFT
        CHART_HEIGHT = CHART_BOTTOM - CHART_TOP
        if canvas_width < 100 or canvas_height < 50 or not self.data_for_chart:
            canvas.create_text(canvas_width // 2, canvas_height // 2,
                               text="Nessun dato disponibile.",
                               font=("Arial", 12), fill="gray")
            return
        max_value = max(max(item["entrata"], item["uscita"]) for item in self.data_for_chart)
        num_bars = len(self.data_for_chart)
        bar_space_total = CHART_AREA_WIDTH / num_bars
        bar_width = bar_space_total * 0.47
        canvas.create_line(CHART_LEFT, CHART_BOTTOM, CHART_LEFT, CHART_TOP, fill="black", width=2)
        canvas.create_line(CHART_LEFT, CHART_BOTTOM, CHART_RIGHT, CHART_BOTTOM, fill="black", width=2)
        for i, item in enumerate(self.data_for_chart):
            x_center = CHART_LEFT + (i + 0.5) * bar_space_total
            x_entrata_start = x_center - bar_width
            x_entrata_end = x_center
            x_uscita_start = x_center
            x_uscita_end = x_center + bar_width
            h_entrata = (item["entrata"] / max_value) * CHART_HEIGHT
            h_uscita = (item["uscita"] / max_value) * CHART_HEIGHT
            y_bottom = CHART_BOTTOM
            y_entrata_top = CHART_BOTTOM - h_entrata
            y_uscita_top = CHART_BOTTOM - h_uscita
            tag_entrata = f"entrata_{i}"
            tag_uscita = f"uscita_{i}"
            canvas.create_rectangle(x_entrata_start, y_entrata_top, x_entrata_end, y_bottom, fill="green", outline="black", tags=tag_entrata)
            canvas.create_rectangle(x_uscita_start, y_uscita_top, x_uscita_end, y_bottom, fill="red", outline="black", tags=tag_uscita)
            canvas.create_text(x_center, CHART_BOTTOM + 30, text=item["label"], anchor="n", angle=45, font=("Arial", 8))
            canvas.create_text(x_entrata_start + bar_width / 2, y_entrata_top - 5, text=f"{item['entrata']:.0f}", anchor="s", font=("Arial", 7), fill="green")
            canvas.create_text(x_uscita_start + bar_width / 2, y_uscita_top - 5, text=f"{item['uscita']:.0f}", anchor="s", font=("Arial", 7), fill="red")
            tooltip_entrata = f"{item['label']} - Entrata: €{item['entrata']:.2f}"
            tooltip_uscita = f"{item['label']} - Uscita: €{item['uscita']:.2f}"
            canvas.tag_bind(tag_entrata, "<Enter>", lambda e, t=tooltip_entrata: self.show_tooltip(e, t))
            canvas.tag_bind(tag_entrata, "<Leave>", self.hide_tooltip)
            canvas.tag_bind(tag_uscita, "<Enter>", lambda e, t=tooltip_uscita: self.show_tooltip(e, t))
            canvas.tag_bind(tag_uscita, "<Leave>", self.hide_tooltip)
            data_filter_e = {
                "anno": item["label"] if self.visualizza_tutti_gli_anni_mensile else str(anno_corrente),
                "mese": None if self.visualizza_tutti_gli_anni_mensile else i + 1,
                "categoria": None,
                "tipo": "Entrata"
            }
            data_filter_u = {
                "anno": item["label"] if self.visualizza_tutti_gli_anni_mensile else str(anno_corrente),
                "mese": None if self.visualizza_tutti_gli_anni_mensile else i + 1,
                "categoria": None,
                "tipo": "Uscita"
            }
            canvas.tag_bind(tag_entrata, "<Double-1>", lambda e, f=data_filter_e, l=item["label"]: self.mostra_transazioni_popup(f, f"Entrate {l}"))
            canvas.tag_bind(tag_uscita, "<Double-1>", lambda e, f=data_filter_u, l=item["label"]: self.mostra_transazioni_popup(f, f"Uscite {l}"))
        if self.visualizza_tutti_gli_anni_mensile:
            anni_presenti = [item["label"] for item in self.data_for_chart]
            label_periodo = f"({anni_presenti[0]} - {anni_presenti[-1]})" if anni_presenti else "(N.D.)"
            titolo_grafico = f"Entrate/Uscite Aggregate per Anno {label_periodo}"
        else:
            label_periodo = f"({anno_corrente})"
            titolo_grafico = f"Entrate/Uscite per Mese {label_periodo}"
        canvas.create_text(canvas_width // 2, CHART_TOP / 3, 
                           text=titolo_grafico, 
                           font=("Arial", 8, "bold"), fill="black")
        canvas.create_text(CHART_LEFT - 5, CHART_TOP, text=f"{max_value:.0f}", anchor="e", font=("Arial", 8), fill="black")
        canvas.create_text(CHART_LEFT - 5, CHART_BOTTOM, text="0", anchor="e", font=("Arial", 8), fill="black")
        total_entrata = sum(item["entrata"] for item in self.data_for_chart)
        total_uscita = sum(item["uscita"] for item in self.data_for_chart)
        total_saldo = total_entrata - total_uscita
        saldo_color = "green" if total_saldo >= 0 else "red"
        text_y_pos = canvas_height - 15
        x_pos_1 = CHART_LEFT + CHART_AREA_WIDTH * 0.15
        x_pos_2 = CHART_LEFT + CHART_AREA_WIDTH * 0.
        x_pos_2 = CHART_LEFT + CHART_AREA_WIDTH * 0.5
        x_pos_3 = CHART_LEFT + CHART_AREA_WIDTH * 0.85
        font_style = ("Arial", 10, "bold")
        canvas.create_text(x_pos_1, text_y_pos, 
                           text=f"Totale Entrate: €{total_entrata:,.2f}", 
                           anchor="center", font=font_style, fill="green")
        canvas.create_text(x_pos_2, text_y_pos, 
                           text=f"Totale Uscite: €{total_uscita:,.2f}", 
                           anchor="center", font=font_style, fill="red")
        canvas.create_text(x_pos_3, text_y_pos, 
                           text=f"Saldo Complessivo: €{total_saldo:,.2f}", 
                           anchor="center", font=font_style, fill=saldo_color) 
                                                     
    def show_tooltip(self, event, text):
        self.hide_tooltip()
        x = self.stats_canvas.winfo_rootx() + event.x + 10
        y = self.stats_canvas.winfo_rooty() + event.y + 10
        self.tooltip_window = tk.Toplevel(self.stats_canvas)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=text, background="#FFFFEA",
                         relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def hide_tooltip(self, event=None):
        if hasattr(self, 'tooltip_window') and self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
                           
    def draw_saldo_chart(self, event=None):
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        canvas = self.stats_canvas
        canvas.delete("all")
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        CHART_LEFT = 80
        CHART_RIGHT = canvas_width - 20
        CHART_TOP = 50
        NUOVO_SPAZIO_LEGENDA = 80 
        CHART_BOTTOM = canvas_height - NUOVO_SPAZIO_LEGENDA
        CHART_AREA_WIDTH = CHART_RIGHT - CHART_LEFT
        CHART_HEIGHT = CHART_BOTTOM - CHART_TOP
        NUOVO_OFFSET_TESTO = 30
        BAR_RATIO = 0.8
        if not hasattr(self, 'visualizza_saldo_totale'):
            self.visualizza_saldo_totale = False
        if not hasattr(self, 'visualizza_saldo_10_anni'):
            self.visualizza_saldo_10_anni = False
        if CHART_AREA_WIDTH < 100 or CHART_HEIGHT < 50:
             canvas.create_text(canvas_width // 2, canvas_height // 2,
                                 text="Area di disegno insufficiente.",
                                 font=("Arial", 12), fill="gray")
             return
        def toggle_saldo_mode():
            if not self.visualizza_saldo_totale and not self.visualizza_saldo_10_anni:
                self.visualizza_saldo_totale = True
                self.visualizza_saldo_10_anni = False
            elif self.visualizza_saldo_totale and not self.visualizza_saldo_10_anni:
                self.visualizza_saldo_totale = False
                self.visualizza_saldo_10_anni = True
            else:
                self.visualizza_saldo_totale = False
                self.visualizza_saldo_10_anni = False
            self.draw_saldo_chart()
        if self.visualizza_saldo_10_anni:
            btn_text = "📅 Solo anno corrente"
        elif self.visualizza_saldo_totale:
            btn_text = "📈 10 anni (Linea)"
        else:
            btn_text = "💰 Tutti gli anni"
        btn_toggle = ttk.Button(canvas, text=btn_text, command=toggle_saldo_mode, style="Blu.TButton")
        canvas.create_window(canvas_width - 10, 2, window=btn_toggle, anchor="ne")
        if self.visualizza_saldo_10_anni:
            transazioni_totali = []
            for giorno, entries in self.spese.items():
                if hasattr(giorno, "year") and giorno >= self.saldo_data:
                    for entry in entries:
                        importo = float(entry[2]) if isinstance(entry, tuple) else float(entry.get("importo", 0))
                        tipo = entry[3] if isinstance(entry, tuple) else entry.get("tipo", "")
                        variazione = importo if tipo == "Entrata" else -importo
                        transazioni_totali.append({"data": giorno, "variazione": variazione})
            transazioni_totali.sort(key=lambda x: x["data"])
            saldo_cumulativo_corrente = self.saldo_iniziale
            saldi_mensili_cumulativi = {}
            if hasattr(self, 'saldo_data'):
                saldi_mensili_cumulativi[self.saldo_data] = self.saldo_iniziale
            ultima_data_registrata = self.saldo_data
            for transazione in transazioni_totali:
                data_transazione = transazione["data"]
                if data_transazione.year != ultima_data_registrata.year or data_transazione.month != ultima_data_registrata.month:
                    ultima_data_registrata = data_transazione
                saldo_cumulativo_corrente += transazione["variazione"]
                if data_transazione.month == 12:
                    data_fine_mese = datetime.date(data_transazione.year + 1, 1, 1) - datetime.timedelta(days=1)
                else:
                    data_fine_mese = datetime.date(data_transazione.year, data_transazione.month + 1, 1) - datetime.timedelta(days=1)
                saldi_mensili_cumulativi[data_fine_mese] = saldo_cumulativo_corrente
            self.data_for_chart = []
            for data, saldo in sorted(saldi_mensili_cumulativi.items()):
                 self.data_for_chart.append({
                     "label": data.strftime("%m/%Y"),
                     "saldo": saldo,
                     "data": data
                 })
        elif self.visualizza_saldo_totale:
            aggregati_anno = {}
            for giorno, entries in self.spese.items():
                if hasattr(giorno, "year"):
                    anno = giorno.year
                    if anno not in aggregati_anno:
                        aggregati_anno[anno] = 0.0
                    for entry in entries:
                        tipo = entry[3] if isinstance(entry, tuple) else entry.get("tipo", "")
                        importo = float(entry[2]) if isinstance(entry, tuple) else float(entry.get("importo", 0))
                        variazione = importo if tipo == "Entrata" else -importo
                        aggregati_anno[anno] += variazione
            self.data_for_chart = [
                {"label": str(anno), "saldo": saldo} 
                for anno, saldo in sorted(aggregati_anno.items())
            ]            
        else:
            mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
            mensili_saldo = [{"label": m, "saldo": 0.0} for m in mesi]
            for giorno, entries in self.spese.items():
                if hasattr(giorno, "year") and giorno.year == anno_corrente:
                    mese_index = giorno.month - 1
                    for entry in entries:
                        tipo = entry[3] if isinstance(entry, tuple) else entry.get("tipo", "")
                        importo = float(entry[2]) if isinstance(entry, tuple) else float(entry.get("importo", 0))
                        variazione = importo if tipo == "Entrata" else -importo
                        mensili_saldo[mese_index]["saldo"] += variazione
            self.data_for_chart = mensili_saldo
        if not hasattr(self, 'data_for_chart') or not self.data_for_chart:
            canvas.create_text(canvas_width // 2, canvas_height // 2,
                                text="Nessun dato saldo disponibile.",
                                font=("Arial", 12), fill="gray")
            return
        saldi = [item["saldo"] for item in self.data_for_chart]
        max_saldo = max(saldi)
        min_saldo = min(saldi)
        buffer = (max_saldo - min_saldo) * 0.1 or 100 
        y_max = max_saldo + buffer
        y_min = min_saldo - buffer
        y_range = y_max - y_min
        def scale_y(saldo):
            if y_range == 0:
                return CHART_TOP + CHART_HEIGHT / 2
            return CHART_BOTTOM - ((saldo - y_min) / y_range) * CHART_HEIGHT
        if self.visualizza_saldo_10_anni:
            canvas.delete("y_labels", "axis") 
            canvas.create_line(CHART_LEFT, CHART_BOTTOM, CHART_LEFT, CHART_TOP, fill="black", width=2, tags="axis")
            canvas.create_text(CHART_LEFT - 5, scale_y(max_saldo), text=f"€{max_saldo:,.0f}", anchor="e", font=("Arial", 8), fill="black", tags="y_labels")
            canvas.create_text(CHART_LEFT - 5, scale_y(min_saldo), text=f"€{min_saldo:,.0f}", anchor="e", font=("Arial", 8), fill="black", tags="y_labels")
            if y_min < 0 < y_max:
                ZERO_LINE_Y = scale_y(0)
                canvas.create_line(CHART_LEFT, ZERO_LINE_Y, CHART_RIGHT, ZERO_LINE_Y, fill="gray", width=1, dash=(5, 5), tags="axis")
                canvas.create_text(CHART_LEFT - 5, ZERO_LINE_Y, text="0", anchor="e", font=("Arial", 8), fill="black", tags="y_labels")
            data_min = self.data_for_chart[0]['data']
            data_max = self.data_for_chart[-1]['data']
            data_range_days = (data_max - data_min).days or 1
            def scale_x(date):
                if data_range_days == 0:
                    return CHART_LEFT + CHART_AREA_WIDTH / 2
                days_since_start = (date - data_min).days
                return CHART_LEFT + (days_since_start / data_range_days) * CHART_AREA_WIDTH
            points = []
            for i, item in enumerate(self.data_for_chart):
                x = scale_x(item['data'])
                y = scale_y(item['saldo'])
                points.append((x, y))
                point_radius = 4
                point_id = canvas.create_oval(x - point_radius, y - point_radius, 
                                              x + point_radius, y + point_radius, 
                                              fill="blue", outline="")
                tooltip_text = f"Data: {item['label']}\nSaldo: €{item['saldo']:,.2f}"
                canvas.tag_bind(point_id, "<Enter>", lambda e, txt=tooltip_text: self.show_tooltip(e, txt))
                canvas.tag_bind(point_id, "<Leave>", self.hide_tooltip)
                if i == 0 or (item['data'].month == 1 and item['data'].day == 1):
                    canvas.create_text(x, CHART_BOTTOM + NUOVO_OFFSET_TESTO, text=item['data'].strftime("%Y"), anchor="n", angle=45, font=("Arial", 8))
            canvas.create_line(points, fill="blue", width=2, tags="line_chart")
            if data_max.year != data_min.year:
                canvas.create_text(CHART_RIGHT, CHART_BOTTOM + NUOVO_OFFSET_TESTO, text=data_max.strftime("%Y"), anchor="n", font=("Arial", 8))
        else:
            max_positive = max((item["saldo"] for item in self.data_for_chart if item["saldo"] >= 0), default=0)
            max_negative = min((item["saldo"] for item in self.data_for_chart if item["saldo"] < 0), default=0)
            ZERO_LINE_Y = CHART_TOP + CHART_HEIGHT / 2 
            canvas.delete("y_labels", "axis")
            canvas.create_line(CHART_LEFT, CHART_BOTTOM, CHART_LEFT, CHART_TOP, fill="black", width=2, tags="axis")
            canvas.create_line(CHART_LEFT, ZERO_LINE_Y, CHART_RIGHT, ZERO_LINE_Y, fill="gray", width=2, tags="axis")
            canvas.create_text(CHART_LEFT - 5, CHART_TOP, text=f"€{max_positive:,.0f}", anchor="e", font=("Arial", 8), fill="green", tags="y_labels")
            canvas.create_text(CHART_LEFT - 5, ZERO_LINE_Y, text="0", anchor="e", font=("Arial", 8), fill="black", tags="y_labels")
            canvas.create_text(CHART_LEFT - 5, CHART_BOTTOM, text=f"€{max_negative:,.0f}", anchor="e", font=("Arial", 8), fill="red", tags="y_labels")
            num_bars = len(self.data_for_chart)
            bar_space_total = CHART_AREA_WIDTH / num_bars
            bar_width = bar_space_total * BAR_RATIO
            for i, item in enumerate(self.data_for_chart):
                saldo = item["saldo"]
                if saldo >= 0:
                    bar_height = (saldo / max_positive) * (CHART_HEIGHT / 2) if max_positive else 0
                else:
                    bar_height = (abs(saldo) / abs(max_negative)) * (CHART_HEIGHT / 2) if max_negative else 0
                x_center = CHART_LEFT + (i + 0.5) * bar_space_total
                x1 = x_center - bar_width / 2
                x2 = x_center + bar_width / 2
                if saldo >= 0:
                    y1 = ZERO_LINE_Y - bar_height
                    y2 = ZERO_LINE_Y
                    color = "green"
                    text_anchor = "s"
                    text_y = y1 - 5
                else:
                    y1 = ZERO_LINE_Y
                    y2 = ZERO_LINE_Y + bar_height
                    color = "red"
                    text_anchor = "n"
                    text_y = y2 + 5
                rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                canvas.tag_bind(rect_id, "<Enter>", lambda e, txt=f"{item['label']}: €{saldo:,.2f}": self.show_tooltip(e, txt))
                canvas.tag_bind(rect_id, "<Leave>", self.hide_tooltip)
                canvas.create_text(x_center, CHART_BOTTOM + NUOVO_OFFSET_TESTO, text=item["label"], anchor="n", angle=45, font=("Arial", 8))
                if bar_height > 10:
                    canvas.create_text(x_center, text_y, text=f"€{saldo:.0f}", anchor=text_anchor, font=("Arial", 8, "bold"), fill=color)
        total_entrata = 0.0
        total_uscita = 0.0
        anni_da_includere = set()
        data_min_vis = None
        data_max_vis = None
        if self.visualizza_saldo_10_anni and self.data_for_chart:
             data_min_vis = self.data_for_chart[0]['data']
             data_max_vis = self.data_for_chart[-1]['data']
        elif self.visualizza_saldo_totale:
            anni_da_includere = set([int(item["label"]) for item in self.data_for_chart if item["label"].isdigit()])
        else:
            anni_da_includere = {anno_corrente}
        for giorno, entries in self.spese.items():
            include_entry = False
            if self.visualizza_saldo_10_anni and data_min_vis and data_max_vis:
                 if giorno >= data_min_vis and giorno <= data_max_vis:
                     include_entry = True
            elif hasattr(giorno, "year") and giorno.year in anni_da_includere:
                 include_entry = True
            if include_entry:
                for entry in entries:
                    tipo = entry[3] if isinstance(entry, tuple) else entry.get("tipo", "")
                    importo = float(entry[2]) if isinstance(entry, tuple) else float(entry.get("importo", 0))
                    if tipo == "Entrata":
                        total_entrata += importo
                    elif tipo == "Uscita":
                        total_uscita += importo
        total_saldo = total_entrata - total_uscita
        saldo_color = "green" if total_saldo >= 0 else "red"
        if self.visualizza_saldo_10_anni and self.data_for_chart:
            primo_anno = self.data_for_chart[0]['data'].year
            ultimo_anno = self.data_for_chart[-1]['data'].year
            label_periodo = f"({primo_anno} - {ultimo_anno})"
            titolo_grafico = f"📈 Saldo Conto Corrente Cumulativo {label_periodo}"
        elif self.visualizza_saldo_totale:
            anni_presenti = sorted(list(set([int(item["label"]) for item in self.data_for_chart if item["label"].isdigit()])))
            label_periodo = f"({anni_presenti[0]} - {anni_presenti[-1]})" if anni_presenti else "(N.D.)"
            titolo_grafico = f"💰 Saldo Netto Annuale Aggregato {label_periodo}"
        else:
            label_periodo = f"({anno_corrente})"
            titolo_grafico = f"📅 Saldo Netto Mensile {label_periodo}"
        canvas.create_text(canvas_width // 2, CHART_TOP / 3, 
                            text=titolo_grafico, 
                            font=("Arial", 8, "bold"), fill="black")
        text_y_pos = canvas_height - 20 
        x_pos_1 = CHART_LEFT + CHART_AREA_WIDTH * 0.15 
        x_pos_2 = CHART_LEFT + CHART_AREA_WIDTH * 0.5  
        x_pos_3 = CHART_LEFT + CHART_AREA_WIDTH * 0.85 
        font_style = ("Arial", 10, "bold")
        canvas.create_text(x_pos_1, text_y_pos, 
                            text=f"Totale Entrate: €{total_entrata:,.2f}", 
                            anchor="center", font=font_style, fill="green")
        canvas.create_text(x_pos_2, text_y_pos, 
                            text=f"Totale Uscite: €{total_uscita:,.2f}", 
                            anchor="center", font=font_style, fill="red")
        canvas.create_text(x_pos_3, text_y_pos, 
                            text=f"Saldo Complessivo: €{total_saldo:,.2f}", 
                            anchor="center", font=font_style, fill=saldo_color)

    def mostra_categorie_popup(self):
        import datetime
        if hasattr(self, 'categorie_popup') and self.categorie_popup.winfo_exists():
            self.categorie_popup.deiconify()
            self.reset_campi_categoria() 
            return
        self.categorie_popup = tk.Toplevel(self)
        self.categorie_popup.title("Gestione Categorie")
        self.categorie_popup.resizable(False, False)
        window_width = 550
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.categorie_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.categorie_popup.bind("<Escape>", lambda event: self.categorie_popup.withdraw())

        main_frame = ttk.Frame(self.categorie_popup)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        aggiungi_cat_frame = ttk.LabelFrame(main_frame, text="✅ Configurazione Categorie", style="RedBold.TLabelframe")
        aggiungi_cat_frame.pack(padx=5, pady=5, fill="both", expand=True)
        aggiungi_cat_frame.columnconfigure(1, weight=1)

        if not hasattr(self, 'nuova_cat'):
            self.nuova_cat = tk.StringVar()
            self.cat_mod_sel = tk.StringVar(value=self.categorie[0] if self.categorie else "")
            self.tipo_categoria = tk.StringVar(value="Uscita")
 
        def convalida_categoria(valore):
            return len(valore) <= 20
        vcmd_cat = aggiungi_cat_frame.register(convalida_categoria)

        ttk.Label(aggiungi_cat_frame, text="🔍 Nome:").grid(row=0, column=0, sticky="e", padx=4, pady=2)
        self.entry_nuova_cat = ttk.Entry(
            aggiungi_cat_frame,
            textvariable=self.nuova_cat,
            width=22,
            validate="key",
            validatecommand=(vcmd_cat, "%P")
        )
        self.entry_nuova_cat.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        
        ttk.Label(aggiungi_cat_frame, text="📂 Tipo:").grid(row=0, column=2, sticky="e", padx=4, pady=2)
        
        def toggle_tipo_spesa_popup_cat():
            tipo_corrente = self.tipo_categoria.get()
            nuovo_tipo = "Entrata" if tipo_corrente == "Uscita" else "Uscita"
            self.tipo_categoria.set(nuovo_tipo)
            self._aggiorna_stile_pulsante_tipo_popup()
        
        self.btn_gestisci_tipo = ttk.Button(
            aggiungi_cat_frame,
            text=self.tipo_categoria.get(),
            width=10,
            command=toggle_tipo_spesa_popup_cat,
            style='RedOutline.TButton',
            takefocus=0
        )
        self.btn_gestisci_tipo.grid(row=0, column=3, sticky="w", padx=2, pady=2)
        
        self._aggiorna_stile_pulsante_tipo_popup()

        ttk.Label(aggiungi_cat_frame, text="⚙️ Modifica:").grid(row=1, column=0, sticky="e", padx=4, pady=2)
        self.cat_mod_menu = ttk.Combobox(
            aggiungi_cat_frame,
            textvariable=self.cat_mod_sel,
            values=sorted(self.categorie),
            state="readonly",
            width=22
        )
        self.cat_mod_menu.grid(row=1, column=1, sticky="w", padx=2, pady=2)
        self.cat_mod_menu.bind("<<ComboboxSelected>>", lambda e: self.on_categoria_modifica_changed_popup())
        
        btn_frame_cat = ttk.Frame(aggiungi_cat_frame)
        btn_frame_cat.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame_cat, text="➕ Aggiungi", command=self.add_categoria, style="Verde.TButton").pack(side="left", padx=2)
        self.btn_modifica_categoria = ttk.Button(btn_frame_cat, text="⚙️ Modifica", command=self.modifica_categoria, style="Verde.TButton")
        self.btn_modifica_categoria.pack(side="left", padx=2)
        self.btn_cancella_categoria = ttk.Button(btn_frame_cat, text="❌ Cancella", command=self.cancella_categoria, style="Rosso.TButton")
        self.btn_cancella_categoria.pack(side="left", padx=2)
        ttk.Button(btn_frame_cat, text="✨", command=self.apri_categorie_suggerite, style="Arancio.TButton", width=2).pack(side="left", padx=2)
        ttk.Button(btn_frame_cat, text="🗑️", command=self.apri_cancella_multiplo, style="Yellow.TButton").pack(side="left", padx=2)
        ttk.Button(btn_frame_cat, text="📋 Elenco", command=self.mostra_tutte_le_categorie, style="Arancio.TButton").pack(side="left", padx=2)
        
        ttk.Button(btn_frame_cat,text="↺", width=2, command=self.reset_campi_categoria,style="Giallo.TButton").pack(side="left", padx=2)

        ttk.Button(main_frame, text="❌ Chiudi", command=self.categorie_popup.withdraw, style="Giallo.TButton").pack(side="bottom", pady=(0, 2))

        self.aggiorna_combobox_categorie()
        self.reset_campi_categoria()
        if not self.categorie:
            self.cat_mod_menu['state'] = 'disabled'

    def _aggiorna_stile_pulsante_tipo_popup(self):
        tipo = self.tipo_categoria.get()
        btn_style = 'GreenOutline.TButton' if tipo == "Entrata" else 'RedOutline.TButton'
        self.btn_gestisci_tipo.config(
            text=tipo,
            style=btn_style
        )
    
    def on_categoria_modifica_changed_popup(self):
        nome = self.cat_mod_sel.get()
        tipo = self.categorie_tipi.get(nome, "Uscita")
        self.nuova_cat.set(nome)
        
        self.tipo_categoria.set(tipo)
        self._aggiorna_stile_pulsante_tipo_popup()
 
    def on_categoria_modifica_changed(self):
        nome = self.cat_mod_sel.get()
        tipo = self.categorie_tipi.get(nome, "Uscita")
        self.nuova_cat.set(nome)  
        self.tipo_categoria.set(tipo)

    def reset_campi_categoria(self):
        self.nuova_cat.set("")                          
        self.cat_mod_sel.set("")                        
                              
        self.tipo_categoria.set("Uscita")    
        self._aggiorna_stile_pulsante_tipo_popup()           
  
    def reset_ricorrenza_popup(self):
        oggi = datetime.date.today().strftime("%d-%m-%Y")
        self.importo_ricorrenza.set("")
        self.ricorrenza_tipo.set("Nessuna")
        self.ricorrenza_n.set(1)
        self.ricorrenza_data_inizio.set(oggi)
        self.ricorrenza_cat_sel.set(self.categorie[0])
        self.ricorrenza_desc.set("")
        self.ricorrenza_imp.set("")
        self.ricorrenza_bloccata = False
        self.ricorrenza_tipo_voce.set("Uscita")
        self.aggiorna_stile_tipo_voce_popup()
        self.ric_percentuali_label.config(text="0% Entrate / 0% Uscite", foreground="black")
        self.label_smartcat_ric.config(text="🛠️ SmartCat in attesa...", foreground="gray")
        self.ric_cat_menu.configure(style="TCombobox")

    def mostra_ricorrenza_popup(self):
        oggi = datetime.date.today().strftime("%d-%m-%Y")
        if hasattr(self, 'ricorrenza_popup') and self.ricorrenza_popup.winfo_exists():
            self.reset_ricorrenza_popup()
            self.ricorrenza_popup.deiconify()
            return

        self.ricorrenza_popup = tk.Toplevel(self)
        self.ricorrenza_popup.title("Gestione Ricorrenze")
        self.ricorrenza_popup.resizable(False, False)
        self.ricorrenza_popup.protocol("WM_DELETE_WINDOW", self.ricorrenza_popup.withdraw)
        
        self.ricorrenza_bloccata = False
        
        self.ricorrenza_popup.bind("<Escape>", lambda event: self.ricorrenza_popup.withdraw())

        window_width = 650
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.ricorrenza_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        if not hasattr(self, 'importo_ricorrenza'):
            self.importo_ricorrenza = tk.StringVar()
            self.ricorrenza_tipo = tk.StringVar(value="Nessuna")
            self.ricorrenza_n = tk.IntVar(value=1)
            self.ricorrenza_data_inizio = tk.StringVar(value=oggi)
            self.ricorrenza_cat_sel = tk.StringVar(value=self.categorie[0])
            self.ricorrenza_desc = tk.StringVar()
            self.ricorrenza_imp = tk.StringVar()
            self.ricorrenza_tipo_voce = tk.StringVar(value="Uscita")
            self.ricorrenza_bloccata = False

        def on_ric_cat_selected(event=None, manuale=True):
            if manuale:
                self.ricorrenza_bloccata = True
                self.label_smartcat_ric.config(text="🛠️ SmartCat disattivata", foreground="green")
                self.ric_percentuali_label.config(text="0% Entrate / 0% Uscite", foreground="black")

            categoria = self.ricorrenza_cat_sel.get()
            tipo = self.categorie_tipi.get(categoria, "Uscita")
            self.ricorrenza_tipo_voce.set(tipo)
            self.aggiorna_stile_tipo_voce_popup()
            if self.ricorrenza_bloccata:
                self.ric_cat_menu.configure(style="TCombobox")

        def aggiorna_categoria_automatica_ricorrenza(*args):
            valore_imp = self.ricorrenza_imp.get().replace(",", ".").strip()
            if not valore_imp:
                self.ric_percentuali_label.config(text="0% Entrate / 0% Uscite", foreground="black")
                self.ricorrenza_bloccata = False
                self.ricorrenza_cat_sel.set("Generica")
                self.ricorrenza_tipo_voce.set("Uscita")
                self.aggiorna_stile_tipo_voce_popup()
                self.label_smartcat_ric.config(text="🛠️ SmartCat in attesa...", foreground="gray")
                self.ric_cat_menu.configure(style="TCombobox")
                return
            if self.ricorrenza_bloccata:
                return
            try:
                imp_corrente = float(valore_imp)
            except ValueError:
                self.ric_percentuali_label.config(text="0% Entrate / 0% Uscite", foreground="black")
                return

            oggi_ric = datetime.date.today()
            un_anno_fa = oggi_ric - datetime.timedelta(days=365)
            
            frequenze_per_categoria_tipo = {}
            for d, lista in self.spese.items():
                if d < un_anno_fa:
                    continue
                for voce in lista:
                    try:
                        categoria, _, importo, tipo = voce[:4]
                        if categoria not in frequenze_per_categoria_tipo:
                            frequenze_per_categoria_tipo[categoria] = {"Entrata": 0, "Uscita": 0, "importi": []}
                        frequenze_per_categoria_tipo[categoria][tipo] += 1
                        frequenze_per_categoria_tipo[categoria]["importi"].append(importo)
                    except (ValueError, IndexError):
                        continue

            if not self.suggerimenti_attivi:
                self.ricorrenza_bloccata = False
                self.label_smartcat_ric.config(text="🛠️ SmartCat disattivata", foreground="green")
                self.ric_cat_menu.configure(style="TCombobox")
                
                categoria_selezionata = self.ricorrenza_cat_sel.get()
                percentuale_entrate, percentuale_uscite = 0.0, 0.0
                if categoria_selezionata in frequenze_per_categoria_tipo:
                    conteggi = frequenze_per_categoria_tipo[categoria_selezionata]
                    totale = conteggi["Entrata"] + conteggi["Uscita"]
                    if totale > 0:
                        percentuale_entrate = (conteggi["Entrata"] / totale) * 100
                        percentuale_uscite = (conteggi["Uscita"] / totale) * 100
                self.ric_percentuali_label.config(text=f'{percentuale_entrate:.0f}% Entrate / {percentuale_uscite:.0f}% Uscite', foreground="black")
                return

            miglior_punteggio = float("inf")
            categoria_migliore = None
            if frequenze_per_categoria_tipo:
                for categoria, dati in frequenze_per_categoria_tipo.items():
                    if not dati["importi"]:
                        continue
                    
                    media_importi = sum(dati["importi"]) / len(dati["importi"])
                    diff = abs(media_importi - imp_corrente)
                    bonus_frequenza = math.log(dati["Entrata"] + dati["Uscita"] + 1) * 0.5
                    punteggio = diff - bonus_frequenza

                    if punteggio < miglior_punteggio:
                        miglior_punteggio = punteggio
                        categoria_migliore = categoria

            if categoria_migliore and not self.ricorrenza_bloccata:
                self.ricorrenza_cat_sel.set(categoria_migliore)
                
                conteggi = frequenze_per_categoria_tipo.get(categoria_migliore, {"Entrata": 0, "Uscita": 0})
                totale = conteggi["Entrata"] + conteggi["Uscita"]
                if totale > 0:
                    percentuale_entrate = (conteggi["Entrata"] / totale) * 100
                    percentuale_uscite = (conteggi["Uscita"] / totale) * 100
                else:
                    percentuale_entrate, percentuale_uscite = 0.0, 0.0

                self.ric_percentuali_label.config(text=f'{percentuale_entrate:.0f}% Entrate / {percentuale_uscite:.0f}% Uscite', foreground="black")
                
                on_ric_cat_selected(manuale=False)
                self.label_smartcat_ric.config(text="💡 SmartCat attiva", foreground="red")
                style = ttk.Style()
                
                self.ric_cat_menu.configure(style="Highlight.TCombobox")
                self.ric_cat_menu.after(2000, lambda: self.ric_cat_menu.configure(style="TCombobox"))
            
        self.ricorrenza_imp.trace_add("write", aggiorna_categoria_automatica_ricorrenza)

        ric_frame = ttk.LabelFrame(self.ricorrenza_popup, text="🔄 Pianificazione Ricorrenze", style="RedBold.TLabelframe")
        ric_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        style = ttk.Style()
        
        row = 0
        ttk.Label(ric_frame, text="🔍 Categoria:").grid(row=row, column=0, sticky="e", padx=2, pady=2)
        self.ric_cat_menu = ttk.Combobox(ric_frame, textvariable=self.ricorrenza_cat_sel, values=sorted(self.categorie), state="readonly", width=22, font=("Arial", 11, "bold"))
        self.ric_cat_menu.grid(row=row, column=1, sticky="w", padx=2, pady=2)
        self.ric_cat_menu.bind("<<ComboboxSelected>>", on_ric_cat_selected)
        
        info_frame = ttk.Frame(ric_frame)
        info_frame.grid(row=row, column=2, columnspan=3, sticky="w", padx=2, pady=2)
        
        self.label_smartcat_ric = ttk.Label(info_frame, text="🛠️ SmartCat in attesa...", foreground="gray")
        self.label_smartcat_ric.pack(side="left", padx=2, pady=2)
        
        row += 1

        ttk.Label(ric_frame, text="💰 Importo (€):").grid(row=row, column=0, sticky="e", padx=2, pady=2)
        ttk.Button(ric_frame, text="🛠", style="Yellow.TButton", command=self.apri_calcolatrice).grid(row=row, column=1, sticky="e", padx=2, pady=2)
        
   
        def convalida_importo(valore):
            if valore == "":
              return True  
            import re
            return len(valore) <= 7 and re.fullmatch(r"^\d*[.,]?\d{0,2}$", valore) is not None
        vcmd_importo = ric_frame.register(convalida_importo)  
        self.ric_imp_entry = ttk.Entry(ric_frame, width=20, textvariable=self.ricorrenza_imp, validate="key", validatecommand=(vcmd_importo, "%P"))  
        
        self.ric_imp_entry.grid(row=row, column=1, sticky="w", padx=2, pady=2)
        
        self.ric_percentuali_label = ttk.Label(info_frame, text="0% Entrate / 0% Uscite", foreground="black")
        self.ric_percentuali_label.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        
        row += 1

        ttk.Label(ric_frame, text="ℹ️ Descrizione:").grid(row=row, column=0, sticky="e", padx=2, pady=2)
        
        def convalida_descrizione(valore):
            return len(valore) <= 30
        vdesc = ric_frame.register(convalida_descrizione)
        self.ric_desc_entry = ttk.Entry(ric_frame, width=25, textvariable=self.ricorrenza_desc, validate="key", validatecommand=(vdesc, "%P"))
        self.ric_desc_entry.grid(row=row, column=1, sticky="w", padx=2, pady=2)
        row += 1
        ttk.Label(ric_frame, text="Tipo:").grid(row=row, column=0, sticky="e", padx=2, pady=2)
        self.ricorrenza_tipo_voce.set("Uscita")

        def toggle_tipo_voce():
            tipo_corrente = self.ricorrenza_tipo_voce.get()
            nuovo_tipo = "Entrata" if tipo_corrente == "Uscita" else "Uscita"
            self.ricorrenza_tipo_voce.set(nuovo_tipo)
            self.aggiorna_stile_tipo_voce_popup()

        def aggiorna_stile_tipo_voce_popup():
            tipo = self.ricorrenza_tipo_voce.get()
            colore_sfondo = "#dff0d8" if tipo == "Entrata" else "#f2dede"
            colore_testo = "green" if tipo == "Entrata" else "red"
            self.btn_tipo_voce.config(
                text=tipo,
                bg=colore_sfondo,
                fg=colore_testo,
                relief="solid",
                bd=2,
                font=("Arial", 10, "bold")
            )

        self.btn_tipo_voce = tk.Button(
            ric_frame,
            text=self.ricorrenza_tipo_voce.get(),
            command=toggle_tipo_voce
        )
        self.btn_tipo_voce.grid(row=row, column=1, sticky="w", padx=2, pady=2)

        self.aggiorna_stile_tipo_voce_popup = aggiorna_stile_tipo_voce_popup
        self.aggiorna_stile_tipo_voce_popup()

        row += 1

        ripeti_frame = ttk.Frame(ric_frame)
        ripeti_frame.grid(row=row, column=0, columnspan=6, sticky="w", padx=2, pady=2)
        
        ttk.Label(ripeti_frame, text="📅 Ripeti:").pack(side="left", padx=2, pady=2)
        self.ric_combo = ttk.Combobox(ripeti_frame, values=["Nessuna", "Ogni giorno", "Ogni mese", "Ogni anno"], width=10, state="readonly", textvariable=self.ricorrenza_tipo)
        self.ric_combo.pack(side="left", padx=2, pady=2)

        ttk.Label(ripeti_frame, text="Ripeti volte:").pack(side="left", padx=10, pady=2)

        def convalida_ric_n(valore):
            if valore == "":
                self.ricorrenza_n.set(1) 
                return True
            try:
                n = int(valore)
                return True
            except ValueError:
                self.ricorrenza_n.set(1)
                return False
        self.ric_n_entry = ttk.Entry(
            ripeti_frame,
            width=4,
            textvariable=self.ricorrenza_n,
        )
        self.ric_n_entry.pack(side="left", padx=2, pady=2)
        self.ric_n_entry.bind("<FocusOut>", lambda event: convalida_ric_n(self.ricorrenza_n.get()))
        self.ric_n_entry.bind("<Return>", lambda event: convalida_ric_n(self.ricorrenza_n.get()))
        self.ric_n_entry.bind("<KP_Enter>", lambda event: convalida_ric_n(self.ricorrenza_n.get()))
        
        
        self.ric_n_entry.pack(side="left", padx=2, pady=2)

        ttk.Label(ripeti_frame, text="Inizio:").pack(side="left", padx=10, pady=2)
        ric_data_frame = ttk.Frame(ripeti_frame)
        ric_data_frame.pack(side="left")
        self.ric_data_entry = ttk.Entry(ric_data_frame, textvariable=self.ricorrenza_data_inizio, width=15, font=("Arial", 10, "bold"))
        self.ric_data_entry.pack(side="left")
        btn_cal_popup = ttk.Button(
            ric_data_frame,
            text="📅",
            command=lambda: self.mostra_calendario_popup(self.ric_data_entry, self.ricorrenza_data_inizio),
            style="Yellow.TButton"
        )
        btn_cal_popup.pack(side="left", padx=4)

        self.btn_reset_ric_data = ttk.Button(
            ric_data_frame,
            text="↺",
            command=self.reset_ric_data_inizio,
            style="Yellow.TButton"
        )
        self.btn_reset_ric_data.pack(side="left", padx=4)
        row += 1

        btn_frame = ttk.Frame(self.ricorrenza_popup)
        btn_frame.pack(pady=10)

        self.btn_add_ricorrenza = ttk.Button(btn_frame, text="📂 Aggiungi", command=self.add_ricorrenza, style="Verde.TButton")
        self.btn_add_ricorrenza.pack(side="left", padx=4)

        self.btn_reset_ricorrenza = ttk.Button(btn_frame, text="↺", width=2, style="Giallo.TButton", command=self.reset_ricorrenza_popup)
        self.btn_reset_ricorrenza.pack(side="left", padx=4)

   
        #self.btn_cancella_ricorrenza = ttk.Button(btn_frame, text="❌ Cancella", command=self.del_ricorrenza, style="Rosso.TButton")
        #self.btn_cancella_ricorrenza.pack(side="left", padx=4)

        self.btn_modifica_ricorrenza = ttk.Button(btn_frame, text="♻️ Lista", command=self.mostra_lista_ricorrenze, style="Arancio.TButton")
        self.btn_modifica_ricorrenza.pack(side="left", padx=4)

        self.btn_chiudi_ricorrenza = ttk.Button(btn_frame, text="❌ Chiudi", command=self.ricorrenza_popup.withdraw, style="Giallo.TButton")
        self.btn_chiudi_ricorrenza.pack(side="left", padx=4)
 
    def gestisci_promemoria(self):
        def salva_promemoria():
            promemoria_text = promemoria_text_widget.get("1.0", tk.END).strip()
            data = {"promemoria": promemoria_text}
            
            try:
                with open(PROMEMORIA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                self.show_custom_warning("Salvataggio", "Promemoria salvato con successo!")
                chiudi_promemoria_popup()
            except Exception as e:
                self.show_custom_warning("Errore di salvataggio", f"Impossibile salvare il file: {e}")

        def carica_promemoria():
            if os.path.exists(PROMEMORIA_FILE):
                try:
                    with open(PROMEMORIA_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        promemoria = data.get("promemoria", "")
                        promemoria_text_widget.delete("1.0", tk.END)
                        promemoria_text_widget.insert("1.0", promemoria)
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    self.show_custom_warning("Errore di caricamento", f"Impossibile caricare il file promemoria.json: {e}")
                    pass

        def chiudi_promemoria_popup():
            promemoria_popup.grab_release()
            promemoria_popup.destroy()

        def esporta_promemoria():
            now = datetime.date.today()
            promemoria_text = promemoria_text_widget.get("1.0", tk.END).strip()
            filename = f"Promemoria_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")],
                initialdir=EXPORT_FILES,
                initialfile=filename,
                title="Esporta Promemoria",
                confirmoverwrite=False,
                parent=promemoria_popup
            )

            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return
                
                try:
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(promemoria_text)  
                    chiudi_promemoria_popup()
                except Exception as e:
                    self.show_custom_warning("Errore di esportazione", f"Impossibile salvare il file: {e}")
 
        if hasattr(self, 'popup_calendario') and self.popup_calendario and self.popup_calendario.winfo_exists():
            self.popup_calendario.destroy()
            self.popup_calendario = None
            self.unbind_all('<Button-1>')
            self.unbind_all('<Escape>')

        promemoria_popup = tk.Toplevel(self)
        promemoria_popup.title("📝 Promemoria")
        promemoria_popup.resizable(True, True)
        promemoria_popup.withdraw()
        promemoria_popup.transient(self)
        #promemoria_popup.grab_set()
        promemoria_popup.bind('<Escape>', lambda e: chiudi_promemoria_popup())
        
        main_frame = ttk.Frame(promemoria_popup, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)

        promemoria_text_widget = tk.Text(main_frame, wrap="word", width=50, height=15)
        promemoria_text_widget.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="nsew")

        btn_salva_promemoria = ttk.Button(main_frame, text="✅ Salva", command=salva_promemoria, style="Verde.TButton")
        btn_salva_promemoria.grid(row=1, column=0, padx=5, sticky="e")
        btn_esporta_promemoria = ttk.Button(main_frame, text="📄 Esporta", command=esporta_promemoria, style="Arancio.TButton")
        btn_esporta_promemoria.grid(row=1, column=1, padx=5, sticky="we")
        btn_cancella_promemoria = ttk.Button(main_frame, text="❌ Chiudi", command=chiudi_promemoria_popup, style="Giallo.TButton")
        btn_cancella_promemoria.grid(row=1, column=2, padx=5, sticky="w")

        carica_promemoria()
        
        self.update_idletasks() 
        window_width = 800 
        window_height = 400   
        app_x = self.winfo_rootx()
        app_y = self.winfo_rooty()
        app_width = self.winfo_width()
        app_height = self.winfo_height()
        center_x = app_x + (app_width // 2) - (window_width // 2)
        center_y = app_y + (app_height // 2) - (window_height // 2)
        promemoria_popup.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')       
        promemoria_popup.deiconify()
        
    def colora_giorni_spese(self):
        if not os.path.exists(DB_FILE):
            return
        self.cal.calevent_remove('all')  
        
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

        giornate = db.get("spese", [])  
        for giorno in giornate:
            try:
                data_str = giorno.get("date", "")
                data = datetime.datetime.strptime(data_str, "%d-%m-%Y").date()

                tipi = {entry.get("tipo", "").lower() for entry in giorno.get("entries", [])}

                if "entrata" in tipi and "uscita" in tipi:
                    tag = "misto"
                elif "entrata" in tipi:
                    tag = "verde"
                elif "uscita" in tipi:
                    tag = "rosso"
                else:
                    continue
                self.cal.calevent_create(data, "", tag)
            except Exception as e:
                print(f"Errore su giorno {giorno}: {e}")
        oggi = datetime.date.today()
        self.cal.calevent_create(oggi, "Oggi", "today")

        self.cal.tag_config("verde", background="lightgreen", foreground="black")
        self.cal.tag_config("rosso", background="lightcoral", foreground="black")
        self.cal.tag_config("misto", background="khaki", foreground="black")
        self.cal.tag_config("today", background="gold", foreground="black")
        
    def on_calendar_change(self, event=None):
        try:
            data = self.cal.selection_get()
            if not data:
                return

            if not self.blocca_data_var.get():
                self.data_spesa_var.set(data.strftime("%d-%m-%Y"))

            mese_corrente = self.estratto_month_var.get()
            anno_corrente = self.estratto_year_var.get()

            mese_da_cal = f"{data.month:02d}"
            anno_da_cal = str(data.year)

            if mese_corrente != mese_da_cal:
                self.estratto_month_var.set(mese_da_cal)
                self.estratto_month_var.set(self.months[data.month - 1])
                
            if anno_corrente != anno_da_cal:
                self.estratto_year_var.set(anno_da_cal)
                self.estratto_year_var.set(anno_da_cal)


            self.after(100, lambda: self.apply_estratto("giorno"))
            
        except Exception as e:
            print(f"Errore durante il cambio data: {e}")
            
    def on_month_changed(self, event=None):
        m, y = self.cal.get_displayed_month()
        primo = datetime.date(y, m, 1)

        if self.cal.selection_get() != primo:
            self.cal.selection_set(primo)
 
        if not self.blocca_data_var.get():
           self.data_spesa_var.set(primo.strftime("%d-%m-%Y"))
        
        self.estratto_month_var.set(self.months[m-1])
        self.estratto_year_var.set(str(y))
        
        self.apply_estratto("giorno")
    
    def aggiorna_titolo_finestra(self):
        current_folder = os.path.basename(os.getcwd())
        self.title(f"💰 {NAME} Pro v {VERSION}  — Email: helpcasafacilepro@gmail.com —  Utente:► {current_folder}")
              
    def aggiorna_bottone_spese_simili(self, visibile=True):
        if visibile:
            if not self.btn_spese_simili.winfo_ismapped():
                self.btn_spese_simili.pack(side="left", padx=(6, 0))
        else:
            if self.btn_spese_simili.winfo_ismapped():
                self.btn_spese_simili.pack_forget()

    def aggiorna_categoria_automatica(self, event=None):
        if not self.suggerimenti_attivi:
            self.label_smartcat.config(text="🛠️ SmartCat disattiva", foreground="green")
            self.aggiorna_bottone_spese_simili(visibile=False)
            return

        valore = self.imp_entry.get().replace(",", ".").strip()
        if not valore:
            self.categoria_bloccata = False
            self.aggiorna_bottone_spese_simili(visibile=False)
            self.cat_sel.set("Generica") 
            self.label_smartcat.config(text="🛠️ SmartCat in attesa...", foreground="gray") 
            self.tipo_spesa_var.set("Uscita") 
            self.aggiorna_stile_tipo_spesa()
        
            self.lbl_tipo_percentuale.config(text="0% Entrate / 0% Uscite ")  
            
            return

        try:
            imp_corrente = float(valore)
        except ValueError:
            return

        oggi = datetime.date.today()
        un_anno_fa = oggi - datetime.timedelta(days=365)
    
        frequenze = {}
        spese_valide = []
        for d, lista in self.spese.items():
            if d < un_anno_fa:
                continue
            for voce in lista:
                try:
                    categoria, _, importo, _ = voce[:4]
                    frequenze[categoria] = frequenze.get(categoria, 0) + 1
                    spese_valide.append((categoria, importo))
                except ValueError:
                    continue
    
        if not spese_valide:
            return

        miglior_punteggio = float("inf")
        categoria_migliore = None

        categorie_gia_valutate = set()
    
        for categoria, importo in spese_valide:
            if categoria in categorie_gia_valutate:
                continue
            categorie_gia_valutate.add(categoria)

            diff = abs(importo - imp_corrente)
        
            bonus_frequenza = math.log(frequenze.get(categoria, 1)) * 0.5 # Il valore 0.5 può essere regolato
        
            punteggio = diff - bonus_frequenza

            if punteggio < miglior_punteggio:
                miglior_punteggio = punteggio
                categoria_migliore = categoria
    
        if categoria_migliore and not self.categoria_bloccata:
            self.cat_sel.set(categoria_migliore)
            self.on_categoria_changed(manuale=False)
            self.label_smartcat.config(text="💡 SmartCat attiva", foreground="red")
            self.btn_spese_simili.pack(side="left", padx=(6, 0))

            style = ttk.Style()
            
            self.cat_menu.configure(style="Highlight.TCombobox")
            self.cat_menu.after(2000, lambda: self.cat_menu.configure(style="TCombobox"))
         
    def mostra_spese_simili(self):
        valore = self.imp_entry.get().replace(",", ".").strip()
        try:
            target = float(valore)
        except ValueError:
            self.show_custom_warning("Errore", "Importo mancante o non valido.")
            return
        tolleranza = int(self.spin_tolleranza.get()) if hasattr(self, "spin_tolleranza") else 10
        limite_basso = target - tolleranza
        limite_alto = target + tolleranza

        voci_simili = [
            (d, *voce)
            for d, lista in self.spese.items()
            for voce in lista
            if len(voce) >= 4 and isinstance(voce[2], (int, float)) and limite_basso <= voce[2] <= limite_alto
        ]

        if not voci_simili:
            self.show_custom_warning("Nessuna corrispondenza", "Nessuna spesa trovata con questo importo.")
            return
            
        style = ttk.Style()
        
        popup = tk.Toplevel(self)
        popup.title(f"Spese simili a €{target:.2f}")
        popup.resizable(False, False)
        popup.bind("<Escape>", lambda e: popup.destroy())

        larghezza, altezza = 650, 460
        x = (popup.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (popup.winfo_screenheight() // 2) - (altezza // 2)
        popup.geometry(f"{larghezza}x{altezza}+{x}+{y}")

        label_range = tk.Label(
            popup,
            text=f"🔎 Spese comprese tra €{limite_basso:.2f} e €{limite_alto:.2f}",
            font=("Arial", 11),
            bg="white"
        )
        label_range.pack(pady=(10, 4))

        tk.Label(
            popup,
            text="🎯 Margine di tolleranza (€):",
            font=("Arial", 10),
            bg="white"
        ).pack(pady=(4, 2))

        tolleranza_var = tk.StringVar(value=str(tolleranza))

        def aggiorna_auto(*args):
            try:
                nuovo_tolleranza = int(tolleranza_var.get())
            except ValueError:
                return

            limite_basso = target - nuovo_tolleranza
            limite_alto = target + nuovo_tolleranza

            label_range.config(text=f"🔎 Spese comprese tra €{limite_basso:.2f} e €{limite_alto:.2f}")

            nuove_voci = [
                (d, *voce)
                for d, lista in self.spese.items()
                for voce in lista
                if len(voce) >= 4 and isinstance(voce[2], (int, float)) and limite_basso <= voce[2] <= limite_alto
            ]

            for item in tree.get_children():
                tree.delete(item)

            nuove_voci.sort(key=lambda x: x[0], reverse=True)
            for voce in nuove_voci:
                try:
                    if len(voce) == 6:
                        data, categoria, descrizione, importo, tipo, _ = voce
                    else: 
                        data, categoria, descrizione, importo, tipo = voce

                    tag = "entrata" if tipo.lower() == "entrata" else "uscita"
                    tree.insert("", tk.END, values=(
                        data.strftime("%d-%m-%Y"),
                        tipo,
                        categoria,
                        descrizione,
                        f"€{importo:.2f}"
                    ), tags=(tag,))
                except Exception:
                    continue

        spin_tolleranza_popup = tk.Spinbox(
            popup,
            from_=0,
            to=100,
            increment=1,
            width=6,
            font=("Arial", 10),
            justify="center",
            textvariable=tolleranza_var
        )
        spin_tolleranza_popup.pack(pady=(0, 10))
        tolleranza_var.trace_add("write", aggiorna_auto)

        columns = ("data", "tipo", "categoria", "descrizione", "importo")
        headers = {
            "data": "📅 Data",
            "tipo": "💼 Tipo",
            "categoria": "📂 Categoria",
            "descrizione": "📝 Descrizione",
            "importo": "💶 Importo"
        }

        tree = ttk.Treeview(popup, columns=columns, show="headings", height=10)
        tree.pack(padx=12, pady=(0, 6), fill="both", expand=True)
        tree.bind("<Double-1>", lambda e: usa_categoria())

        for col in columns:
            tree.heading(col, text=headers[col], command=lambda c=col: sort_column(tree, c, False))

        tree.column("data", width=90, anchor="center")
        tree.column("tipo", width=80, anchor="center")
        tree.column("categoria", width=120, anchor="w")
        tree.column("descrizione", width=220, anchor="w")
        tree.column("importo", width=80, anchor="e")
        voci_simili.sort(key=lambda x: x[0], reverse=True)
        
        for voce in voci_simili:
            try:
                if len(voce) == 6:
                    data, categoria, descrizione, importo, tipo, _ = voce
                else: 
                    data, categoria, descrizione, importo, tipo = voce
                
                tag = "entrata" if tipo.lower() == "entrata" else "uscita"
                tree.insert("", tk.END, values=(
                    data.strftime("%d-%m-%Y"),
                    tipo,
                    categoria,
                    descrizione,
                    f"€{importo:.2f}"
                ), tags=(tag,))
            except Exception as e:
                print(f"[Voce malformata]: {voce} → {e}")
                continue
        tree.tag_configure("entrata", foreground="green")
        tree.tag_configure("uscita", foreground="red")
        
        def usa_categoria():
            selezione = tree.selection()
            if not selezione:
                self.show_custom_warning("Attenzione", "Seleziona una spesa per copiarne la categoria.")
                return
            valori = tree.item(selezione[0], "values")
            self.cat_sel.set(valori[2])
            self.on_categoria_changed(manuale=True)
            popup.destroy()

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=(4, 12))

        ttk.Button(btn_frame, text="📥 Usa questa categoria", style="Blu.TButton", command=usa_categoria).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="❌ Chiudi", style="Giallo.TButton", command=popup.destroy).pack(side="left", padx=8)


        def sort_column(tv, col, reverse):
            def extract(val):
                try:
                    if col == "importo":
                        return float(val.replace("€", "").replace(",", "").strip())
                    elif col == "data":
                        return datetime.datetime.strptime(val, "%d-%m-%Y")
                    return str(val).lower()
                except:
                    return val

            idx = columns.index(col)
            dati = [(tv.item(k)["values"], k) for k in tv.get_children()]
            try:
                dati.sort(key=lambda x: extract(x[0][idx]), reverse=reverse)
            except Exception as e:
                print(f"[Errore ordinamento '{col}']: {e}")
                return
        
            for i, (valori, k) in enumerate(dati):
                tv.move(k, "", i)

            tv.heading(col, command=lambda: sort_column(tv, col, not reverse))

    def load_window_geometry(self):
        if not os.path.exists(DB_FILE):
            return
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._window_geometry = data.get("_window_geometry", None)
        except Exception:
            self._window_geometry = None

    def save_window_geometry(self):
        geometry = self.geometry()
        self._window_geometry = geometry
        try:
            data = {}
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            data["_window_geometry"] = geometry
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Errore salvataggio geometria finestra:", e)



    def _on_close_lock(self):
        try:
            if sys.platform != "win" and _lock_file_handle:
                _lock_file_handle.close()
                lock_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                lock_file_path = os.path.join(lock_dir, 'casa_facile.lock')
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
                    print("🗑️ File di lock cancellato.")
        except Exception as e:
            print(f"⚠️ Errore durante la pulizia del lock file: {e}")

    def _on_close(self):
        print("🔚 Chiusura dell'app in corso...")
        self.save_window_geometry()
        self.save_db()
        try:
            if hasattr(self, "server"):
                self.server.shutdown()
                self.server.server_close()
                print("🌐 Web server chiuso.")
            else:
                print("🌐 Nessun web server attivo.")
        except Exception as e:
            print(f"⚠️ Web server non attivo o errore in chiusura: {e}")
        try:
            self.destroy()
        except Exception as e:
            print(f"⚠️ Errore nella chiusura della GUI: {e}")
        self._on_close_lock()
        sys.exit(0)

        
    def carica_memoria_descrizioni(self):
        if os.path.exists(MEM_CAT):
           with open(MEM_CAT, "r", encoding="utf-8") as f:
            self.memoria_descrizioni_categoria = json.load(f)
        else:
            self.memoria_descrizioni_categoria = {}

    def load_db(self):
        if not os.path.exists(DB_FILE):

            self.db = {
                "categorie": ["Generica"],
                "categorie_tipi": {"Generica": "Uscita"},
                "spese": [],
                "ricorrenze": {},
                "_window_geometry": None
            }
            self.categorie = self.db["categorie"]
            self.categorie_tipi = self.db["categorie_tipi"]
            self.spese = {}
            self.ricorrenze = self.db["ricorrenze"]
            self._window_geometry = self.db["_window_geometry"]
            return

        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                self.db = json.load(f)

            self.categorie = self.db.get("categorie", ["Generica"])
            self.categorie_tipi = self.db.get("categorie_tipi", {"Generica": "Uscita"})
            self.spese = {}
            for obj in self.db.get("spese", []):
                d = datetime.datetime.strptime(obj["date"], "%d-%m-%Y").date()
                entries = []
                for e in obj.get("entries", []):
                    if "id_ricorrenza" in e:
                        entries.append((e["categoria"], e["descrizione"], float(e["importo"]), e["tipo"], e["id_ricorrenza"]))
                    else:
                        entries.append((e["categoria"], e["descrizione"], float(e["importo"]), e["tipo"]))
                self.spese[d] = entries
            self.ricorrenze = self.db.get("ricorrenze", {})
            self._window_geometry = self.db.get("_window_geometry", None)
            self.carica_saldo()
            
        except Exception as e:
            print("Errore caricamento DB:", e)
            self.db = {
                "categorie": ["Generica"],
                "categorie_tipi": {"Generica": "Uscita"},
                "spese": [],
                "ricorrenze": {},
                "_window_geometry": None
            }

            self.categorie = self.db["categorie"]
            self.categorie_tipi = self.db["categorie_tipi"]
            self.spese = {}
            self.ricorrenze = {}
            self._window_geometry = None
            self.carica_saldo()
            
    def save_db(self):
        ten_years_ago = datetime.date.today() - datetime.timedelta(days=365 * ANNI_DA_MANTENERE)
        spese_da_rimuovere = [d for d in self.spese.keys() if d < ten_years_ago]
        for d in spese_da_rimuovere:
            del self.spese[d]

        categorie_tipi_ordinati = dict(sorted(self.categorie_tipi.items()))
        data = {
            "categorie": self.categorie,
            "categorie_tipi": categorie_tipi_ordinati,
            "spese": [
                {"date": d.strftime("%d-%m-%Y"), "entries": [
                    {"categoria": c, "descrizione": desc, "importo": imp, "tipo": tipo, **({"id_ricorrenza": rid} if len(entry) == 5 else {})}
                        for entry in sp
                        for c, desc, imp, tipo, *rest in [entry]
                        for rid in [rest[0] if rest else None]
                ]} for d, sp in self.spese.items()
            ],
            "ricorrenze": self.ricorrenze
        }
        if self._window_geometry is not None:
            data["_window_geometry"] = self._window_geometry
        else:
            try:
                data["_window_geometry"] = self.geometry()
            except Exception:
                pass
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        with open(MEM_CAT, "w", encoding="utf-8") as f:
            json.dump(self.memoria_descrizioni_categoria, f, ensure_ascii=False, indent=2)

    def reset_form(self):
        today = datetime.date.today()
        self.data_spesa_var.set(today.strftime("%d-%m-%Y"))
        self.desc_entry.delete(0, tk.END)
        self.imp_entry.delete(0, tk.END)
        self.blocca_data_var.set(False)
        self.metodo_pagamento_var.set("")
        self.cat_sel.set(self.categorie[0])
        self.suggerimenti_attivi = True
        self.categoria_bloccata = False 
        self.on_categoria_changed(manuale=False) 
        self.btn_aggiungi["state"] = tk.NORMAL
        
    def toggle_tipo_spesa(self):
        v = self.tipo_spesa_var.get()
        nuovo = "Entrata" if v == "Uscita" else "Uscita"
        self.tipo_spesa_var.set(nuovo)
        self.btn_tipo_spesa.config(text=nuovo)
        new_style = 'GreenOutline.TButton' if nuovo == "Entrata" else 'RedOutline.TButton'
        self.btn_tipo_spesa.config(style=new_style)

    def aggiorna_combobox_categorie(self):
        altre = sorted([c for c in self.categorie if c != "Generica"], key=str.lower)
        ordinata = ["Generica"] + altre if "Generica" in self.categorie else altre

        self.categorie = ordinata
        self.cat_menu["values"] = self.categorie
        self.cat_mod_menu["values"] = self.categorie

        if "Generica" in self.categorie:
            idx = self.categorie.index("Generica")
            self.cat_menu.current(idx)
            self.cat_mod_menu.current(idx)
        elif self.categorie:
            self.cat_menu.current(0)
            self.cat_mod_menu.current(0)

    def on_categoria_changed(self, event=None, manuale=True):
        if manuale:
            self.categoria_bloccata = True
        cat = self.cat_sel.get()
        tipo_cat = self.categorie_tipi.get(cat, "Uscita")
        self.tipo_spesa_var.set(tipo_cat)
        self.btn_tipo_spesa.config(text=tipo_cat)
        new_style = 'GreenOutline.TButton' if tipo_cat == "Entrata" else 'RedOutline.TButton'
        self.btn_tipo_spesa.config(style=new_style)
        tipo_cat_suggerito, perc_entrate, perc_uscite = self.suggerisci_tipo_categoria(cat)
        self.lbl_tipo_percentuale.config(
            text=f"{perc_entrate}% Entrate / {perc_uscite}% Uscite"
        )
        self.label_smartcat.config(text="🛠️ SmartCat disattiva", foreground="green")
        self.aggiorna_bottone_spese_simili(visibile=False)

    def mostra_tutte_le_categorie(self):
        popup = tk.Toplevel(self)
        popup.title("📋 Elenco Categorie")
        popup.resizable(False, False)
        popup.geometry("320x420")
        popup.transient(self)
        popup.lift()
        popup.focus_force()

        popup.bind("<Escape>", lambda e: (popup.grab_release(), popup.destroy()))

        frame = ttk.Frame(popup, padding=10)
        frame.pack(fill="both", expand=True)

        label = ttk.Label(frame, text="Categorie disponibili:", font=("Arial", 11, "bold"))
        label.pack(pady=(0, 10))

        text = tk.Text(frame, font=("Arial", 10), height=18, wrap="none", state="normal")
        text.pack(fill="both", expand=True)

        text.tag_configure("entrata", foreground="green")
        text.tag_configure("uscita", foreground="red")

        for nome in sorted(self.categorie, key=lambda x: x.lower()):

            tipo = self.categorie_tipi.get(nome, "Uscita")
            riga = f"• {nome}  ("
            text.insert("end", riga)
            if tipo == "Entrata":
                text.insert("end", tipo, "entrata")
            else:
                text.insert("end", tipo, "uscita")
            text.insert("end", ")\n")

        text.config(state="disabled") 
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="❌ Chiudi", style='Giallo.TButton', command=lambda: (popup.grab_release(), popup.destroy()),).pack()

        
    def add_categoria(self):
        nome = self.nuova_cat.get().strip()

        tipo = self.tipo_categoria.get()

        if not nome or nome in self.categorie or nome == self.CATEGORIA_RIMOSSA:
            self.reset_campi_categoria()
            self.show_custom_warning("Attenzione", "Nome categoria vuoto, già esistente o riservato.")
            return
        self.categorie.append(nome)
        self.categorie_tipi[nome] = tipo
        self.aggiorna_combobox_categorie()
        self.save_db()
        self.refresh_gui()
        self.reset_campi_categoria()  
        if hasattr(self, 'ricorrenza_popup') and self.ricorrenza_popup.winfo_exists():
            if hasattr(self, 'ric_cat_menu'):
                self.ric_cat_menu['values'] = sorted(self.categorie)
        self.show_custom_info("Attenzione", f"La categoria '{nome}' '{tipo}' è stata aggiunta.")

    def modifica_categoria(self):
        old_nome = self.cat_mod_sel.get()
        if not old_nome:
            self.show_custom_warning("Attenzione", "Seleziona una categoria da modificare.")
            return

        if old_nome == "Generica":
         self.show_custom_warning("Attenzione", "La categoria 'Generica' non può essere rinominata.")
         self.reset_campi_categoria()  
         return
        new_nome = self.nuova_cat.get().strip()
        if not new_nome:
            self.show_custom_warning("Attenzione", "Inserisci il nuovo nome della categoria.")
            return
        if new_nome == old_nome:
            tipo = self.tipo_categoria.get()
            self.categorie_tipi[new_nome] = tipo
            self.save_db()
            self.refresh_gui()
            self.show_custom_info("Info", f"Tipo categoria '{new_nome}' aggiornato a ''{tipo}'.")
            self.reset_campi_categoria()  
            return
        if new_nome in self.categorie:
            self.show_custom_warning("Attenzione", "Esiste già una categoria con questo nome.")
            return
        idx = self.categorie.index(old_nome)
        self.categorie[idx] = new_nome
        nuovo_tipo = self.tipo_categoria.get()

        self.categorie_tipi[new_nome] = nuovo_tipo

        if new_nome != old_nome:
            self.categorie_tipi.pop(old_nome, None)

        for d in self.spese:
            new_entries = []
            for entry in self.spese[d]:
                if entry[0] == old_nome:
                    entry = (new_nome,) + entry[1:]
                new_entries.append(entry)
            self.spese[d] = new_entries
        self.cat_menu["values"] = self.categorie
        self.cat_mod_menu["values"] = self.categorie
        self.save_db()
        self.refresh_gui()
        self.show_custom_info("Attenzione", f"Categoria '{old_nome}' rinominata in '{new_nome}' '{nuovo_tipo}' .")
        self.aggiorna_combobox_categorie()
        self.reset_campi_categoria() 
        if hasattr(self, 'ricorrenza_popup') and self.ricorrenza_popup.winfo_exists():
            if hasattr(self, 'ric_cat_menu'):
                self.ric_cat_menu['values'] = sorted(self.categorie)

    def conferma_cancella_categoria(self, cat):
        popup = tk.Toplevel(self)
        popup.title("Conferma eliminazione")
        popup.resizable(False, False)

        width, height = 320, 160
        popup.withdraw()
        popup.update_idletasks()
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        x = parent_x + (parent_w // 2) - (width // 2)
        y = parent_y + (parent_h // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.deiconify()
        popup.grab_set()
        popup.configure(bg="#FFFACD")

        messaggio_var = tk.StringVar()
        messaggio_var.set(
            f"Eliminare la categoria '{cat}'?\nLe spese saranno Mantenute ma etichettate\n'{self.CATEGORIA_RIMOSSA}'."
        )

        label = tk.Label(
            popup,
            textvariable=messaggio_var,
            font=("Arial", 10),
            justify="center",
            wraplength=280,
            bg="#FFFACD"
        )
        label.pack(pady=8, padx=10)

        elimina_importi_var = tk.BooleanVar()

        def aggiorna_messaggio(*_):
            if elimina_importi_var.get():
                messaggio_var.set(
                    f"Eliminare la categoria '{cat}'?\nLe spese e gli importi saranno eliminati."
                )
            else:
                messaggio_var.set(
                    f"Eliminare la categoria '{cat}'?\nLe spese saranno etichettate '{self.CATEGORIA_RIMOSSA}'."
                )

        elimina_importi_var.trace_add("write", aggiorna_messaggio)

        tk.Checkbutton(
            popup,
            text="Elimina TUTTO anche gli importi associati",
            variable=elimina_importi_var,
            bg="#FFFACD",
            anchor="w",
            selectcolor="#FFFACD",
            activebackground="#FFFACD",
            highlightthickness=0,
            relief="flat",
            borderwidth=0
        ).pack(pady=(0, 6), padx=10, anchor="w")

        frame = tk.Frame(popup, bg="#FFFACD")
        frame.pack(pady=4)

        result = {"ok": False, "elimina_importi": False}

        def do_ok():
            result["ok"] = True
            result["elimina_importi"] = elimina_importi_var.get()
            popup.destroy()

        def do_cancel():
            popup.destroy()

        b1 = ttk.Button(frame, text="Elimina", style="Rosso.TButton", command=do_ok)
        b2 = ttk.Button(frame, text="Annulla", style="Giallo.TButton", command=do_cancel)
        b1.pack(side="left", padx=8)
        b2.pack(side="right", padx=8)

        popup.wait_window()
        return result

    def cancella_categoria(self):
        cat = self.cat_mod_sel.get()
        if not cat:
            self.show_custom_warning("Attenzione", "Seleziona una categoria da cancellare.")
            return
        if cat in ("Generica", self.CATEGORIA_RIMOSSA):
            self.show_custom_warning("Attenzione", f"Non puoi cancellare la categoria '{cat}'.")
            self.reset_campi_categoria()
            return

        conferma = self.conferma_cancella_categoria(cat)
        if not conferma["ok"]:
            return
        elimina_importi = conferma["elimina_importi"]

        if cat in self.categorie:
            self.categorie.remove(cat)
        if cat in self.categorie_tipi:
            del self.categorie_tipi[cat]

        for giorno in list(self.spese):
            nuove_spese = []
            for voce in self.spese[giorno]:
                voce_cat = voce[0]
                if voce_cat == cat:
                    if not elimina_importi:
                        nuove_spese.append((self.CATEGORIA_RIMOSSA,) + voce[1:])

                else:
                    nuove_spese.append(voce)

            if nuove_spese:
                self.spese[giorno] = nuove_spese
            else:
                del self.spese[giorno]

        self.save_db()
        self.refresh_gui()
        self.on_categoria_changed()
        self.aggiorna_combobox_categorie()
        self.reset_campi_categoria()
        if hasattr(self, 'ricorrenza_popup') and self.ricorrenza_popup.winfo_exists():
            if hasattr(self, 'ric_cat_menu'):
                self.ric_cat_menu['values'] = sorted(self.categorie)
                
    def apri_calcolatrice(self):
        def inserisci(valore):
            entry_var.set(entry_var.get() + valore)
        def cancella():
            entry_var.set("")
            cronologia_text.config(state="normal")
            cronologia_text.delete("1.0", tk.END)
            cronologia_text.config(state="disabled")
        def calcola(event=None):
            try:
                espressione = entry_var.get().replace('%', '/100')
                risultato = eval(espressione)
                cronologia_text.config(state="normal")
                cronologia_text.insert(tk.END, f"{espressione} = {risultato}\n")
                cronologia_text.config(state="disabled")
                entry_var.set(str(risultato))
            except Exception:
                entry_var.set("Errore")
        def usa_risultato_ricorrenze():
            try:
                risultato = entry_var.get()
                self.ricorrenza_imp.set(risultato)
                calcolatrice.destroy()
            except Exception as e:
                entry_var.set("Errore")
        def usa_risultato_principale():
            try:
                risultato = entry_var.get()
                self.imp_entry.delete(0, tk.END) 
                self.imp_entry.insert(0, risultato) 
                calcolatrice.destroy()
            except Exception as e:
                entry_var.set("Errore")
        calcolatrice = tk.Toplevel(self)
        calcolatrice.withdraw()
        calcolatrice.title("Calcolatrice")
        calcolatrice.resizable(True, True)
        calcolatrice.configure(bg="white")
        calcolatrice.bind("<Escape>", lambda e: calcolatrice.destroy())
        calcolatrice.bind("<Return>", calcola)
        calcolatrice.bind("<KP_Enter>", calcola)
        larghezza, altezza = 310, 310
        calcolatrice.update_idletasks()
        x = (calcolatrice.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (calcolatrice.winfo_screenheight() // 2) - (altezza // 2)
        calcolatrice.geometry(f"{larghezza}x{altezza}+{x}+{y}")
        calcolatrice.deiconify()
        entry_var = tk.StringVar()
        entry = ttk.Entry(
            calcolatrice,
           textvariable=entry_var,
            font=("Arial", 16),
            justify="right"
        )
        entry.pack(fill="x", padx=10, pady=10)
        cronologia_text = tk.Text(calcolatrice, height=4, width=30, wrap="word", state="disabled")
        cronologia_text.pack(fill="x", padx=10, pady=(0, 10))
        tasti = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "%", "+"]
        ]
        for riga in tasti:
            frame = ttk.Frame(calcolatrice)
            frame.pack(expand=True, fill="both")
            for tasto in riga:
                comando = lambda val=tasto: inserisci(val)
                stile_bottone = "Num.TButton" if tasto.isdigit() or tasto == "." else "Arancio.TButton"
                bottone = ttk.Button(
                    frame,
                    text=tasto,
                    style=stile_bottone,
                    command=comando
                )
                bottone.pack(side="left", expand=True, fill="both", padx=1, pady=1)
        frame_finale = ttk.Frame(calcolatrice)
        frame_finale.pack(fill="x", padx=10, pady=10)
        bottone_c = ttk.Button(
            frame_finale,
            text="C",
            style="Giallo.TButton",
            command=cancella
        )
        bottone_c.pack(side="left", expand=True, fill="x", padx=1)
        bottone_usa_ricorrenze = ttk.Button(
            frame_finale,
            text="Usa in Ricorrenze",
            style="Blu.TButton",
            command=usa_risultato_ricorrenze
        )
        bottone_usa_ricorrenze.pack(side="left", expand=True, fill="x", padx=1)
        bottone_usa_normale = ttk.Button(
            frame_finale,
            text="Usa in Principale",
            style="Blu.TButton",
            command=usa_risultato_principale
        )
        bottone_usa_normale.pack(side="left", expand=True, fill="x", padx=1)
        bottone_eq = ttk.Button(
            frame_finale,
            text="=",
            style="Verde.TButton",
            command=calcola
        )
        bottone_eq.pack(side="right", expand=True, fill="x", padx=1)

    def show_custom_warning(self, title, message):
        self._show_custom_message(title, message, "yellow", "black", "warning")

    def show_custom_info(self, title, message):
        self._show_custom_message(title, message, "lightblue", "black", "info")

    def show_custom_askyesno(self, title, message):
        dialog = tk.Toplevel(self, bg="orange")  
        dialog.withdraw() 
        dialog.title(title)
        dialog.grab_set()
        dialog.resizable(False, False)
        #dialog.transient(self)

        dialog.update_idletasks()
        w, h = 320, 140
        x = self.winfo_screenwidth() // 2 - w // 2
        y = self.winfo_screenheight() // 2 - h // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        dialog.deiconify()
        dialog.lift()              
        dialog.attributes("-topmost", True) 

        label = tk.Label(dialog, text=message, font=("Arial", 10), justify="left", padx=16, pady=12, bg="orange")
        label.pack()

        btns = tk.Frame(dialog, bg="orange")
        btns.pack(pady=(0,10))

        result = {"value": False}

        def yes():
            result["value"] = True
            dialog.destroy()

        def no():
            result["value"] = False
            dialog.destroy()
            
        b1 = ttk.Button(btns, text="Sì", style="Verde.TButton", command=yes)  
        b2 = ttk.Button(btns, text="No", style="Giallo.TButton", command=no)    
        b1.grid(row=0, column=0, padx=8)
        b2.grid(row=0, column=1, padx=8)

        dialog.wait_window()
        return result["value"]

    def _show_custom_message(self, title, message, bg, fg, icon=None):
        dialog = tk.Toplevel(self)
        dialog.attributes("-topmost", True)
        dialog.withdraw()  
        dialog.title(title)
        #dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        frame = tk.Frame(dialog, bg=bg)
        frame.pack(fill="both", expand=True)
        frame.pack_propagate(False) 
        label = tk.Label(frame, text=message, font=("Arial", 10), bg=bg, fg=fg, justify="left", padx=16, pady=12)
        label.pack()
        btn = ttk.Button(frame, text="OK", style="Verde.TButton", command=dialog.destroy)
        btn.pack(pady=(0, 10))
        btn.focus_set()
        dialog.bind("<Return>", lambda e: dialog.destroy())
        dialog.bind("<KP_Enter>", lambda e: dialog.destroy())
        dialog.bind("<Escape>", lambda e: dialog.destroy())
        dialog.update_idletasks()  
        width = label.winfo_reqwidth() + 40  
        height = label.winfo_reqheight() + btn.winfo_reqheight() + 40
        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        dialog.deiconify()  

        if USE_WAIT_WINDOW:
            dialog.wait_window()
        else:
            dialog.after(WARN_TIMEOUT, dialog.destroy)

    def reset_data_spesa(self):
        today = datetime.date.today()
        self.data_spesa_var.set(today.strftime("%d-%m-%Y"))

    def reset_ric_data_inizio(self):
        oggi = datetime.date.today()
        self.ricorrenza_data_inizio.set(oggi.strftime("%d-%m-%Y"))

    def add_ricorrenza(self):
        ric_type = self.ricorrenza_tipo.get()
        if ric_type == "Nessuna":
            self.show_custom_warning("Errore", "Seleziona un tipo di ricorrenza valido.")
            return
        try:
            n = int(self.ricorrenza_n.get())
            if n <= 0 or n > 365:
                raise ValueError
        except Exception:
            self.show_custom_warning("Errore", "Numero ripetizioni non valido (1-365)")
            return
        try:
            data_inizio = datetime.datetime.strptime(self.ricorrenza_data_inizio.get(), "%d-%m-%Y").date()
        except Exception:
            self.show_custom_warning("Errore", "Data inizio ricorrenza non valida")
            return
        
        cat = self.ricorrenza_cat_sel.get()
        desc = self.ricorrenza_desc.get().strip()

        try:
            imp_str = self.ricorrenza_imp.get().replace(",", ".")
            imp = float(imp_str)
            if imp <= 0:
                self.show_custom_warning("Errore", "L'importo non può essere negativo.")
                return
        except Exception:
            self.show_custom_warning("Errore", "Importo mancante o non valido.")
            return
       
        tipo = self.ricorrenza_tipo_voce.get()
        self.ricorrenza_tipo_voce = self.tipo_spesa_var

        ric_id = str(uuid.uuid4())
 
        id_visibile = ric_id[:8]
        simbolo_ricorrenza = "♻️"
        if desc:
            desc = f"{simbolo_ricorrenza} {desc} ID:{id_visibile}"
        else:
            desc = f"{simbolo_ricorrenza} ID:{id_visibile}"

        date_list = []
        for i in range(n):
            if ric_type == "Ogni giorno":
                d = data_inizio + datetime.timedelta(days=i)
            elif ric_type == "Ogni mese":
                month = (data_inizio.month - 1 + i) % 12 + 1
                year = data_inizio.year + (data_inizio.month - 1 + i) // 12
                day = min(data_inizio.day, [31,
                    29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                    31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
                try:
                    d = datetime.date(year, month, day)
                except Exception:
                    d = datetime.date(year, month, 1)
            elif ric_type == "Ogni anno":
                year = data_inizio.year + i
                try:
                    d = datetime.date(year, data_inizio.month, data_inizio.day)
                except Exception:
                    d = datetime.date(year, data_inizio.month, 1)
            else:
                break
            date_list.append(d)
        for d in date_list:
            if d not in self.spese:
                self.spese[d] = []
            self.spese[d].append((cat, desc, imp, tipo, ric_id))
        self.ricorrenze[ric_id] = {
            "tipo": ric_type,
            "n": n,
            "data_inizio": data_inizio.strftime("%d-%m-%Y"),
            "cat": cat,
            "desc": desc,
            "imp": imp,
            "tipo_voce": tipo,
            "date_list": [d.strftime("%d-%m-%Y") for d in date_list]
        }
        self.save_db()
        self.refresh_gui()
        self.show_custom_info("Ricorrenza aggiunta", f"Spesa/entrata ricorrente aggiunta per {n} volte.")

        oggi = datetime.date.today().strftime("%d-%m-%Y")
        self.importo_ricorrenza.set("")
        self.ricorrenza_tipo.set("Nessuna")
        self.ricorrenza_n.set(1)
        self.ricorrenza_data_inizio.set(oggi)
        self.ricorrenza_cat_sel.set(self.categorie[0])
        self.ricorrenza_desc.set("")
        self.ricorrenza_imp.set("")
        self.ricorrenza_tipo_voce.set("Uscita")
        self.btn_tipo_voce.config(text="Uscita", bg="#f2dede", fg="red")
        
    def del_ricorrenza(self):
        if not self.ricorrenze:
            self.show_custom_warning("Info", "Nessuna ricorrenza trovata.")
            return
        popup = tk.Toplevel(self)
        popup.title("Cancella Ricorrenza")
        popup.grab_set()
        popup.resizable(False, False)
        popup.geometry("+%d+%d" % (
            self.winfo_rootx() + 200,
            self.winfo_rooty() + 120
        ))
        tk.Label(popup, text="Seleziona una ricorrenza da cancellare:", font=("Arial", 10)).pack(padx=12, pady=7)
        frame = tk.Frame(popup)
        frame.pack(padx=8, pady=4)
        ric_list = list(self.ricorrenze.items())
        showlist = []
        for rid, r in ric_list[-10:]:
            tipo = r["tipo"]
            n = r["n"]
            data_inizio = r["data_inizio"]
            desc = r["desc"]
            cat = r["cat"]
            showlist.append(f"{tipo} x{n} da {data_inizio} - {cat} - {desc} ({rid[:8]})")
        ric_sel = tk.StringVar(value=showlist[0] if showlist else "")
        ric_combo = ttk.Combobox(frame, values=showlist, state="readonly", width=60, textvariable=ric_sel)
        ric_combo.grid(row=0, column=0, padx=4, pady=4)
        def get_selected_id():
            idx = showlist.index(ric_sel.get())
            return ric_list[-10:][idx][0]
        def do_ok():
            rid = get_selected_id()
            self._delete_ricorrenza_by_id(rid)
            popup.destroy()
        def do_cancel():
            popup.destroy()
        frame_btn = tk.Frame(popup)
        frame_btn.pack(pady=5)
        ttk.Button(frame_btn, text="Cancella", style="Rosso.TButton", command=do_ok).grid(row=0, column=0, padx=8)
        ttk.Button(frame_btn, text="Annulla", style="Giallo.TButton", command=do_cancel).grid(row=0, column=1, padx=8)


    def _delete_ricorrenza_by_id(self, ric_id):
        if ric_id not in self.ricorrenze:
            self.show_custom_warning("Errore", "Ricorrenza non trovata.")
            return
        for data, voci in list(self.spese.items()):
            nuove_voci = []
            for voce in voci:
                if len(voce) == 5 and voce[4] == ric_id:
                    continue
                nuove_voci.append(voce)
            if nuove_voci:
                self.spese[data] = nuove_voci
            else:
                del self.spese[data]    
        del self.ricorrenze[ric_id]
        residui = []
        for data, voci in self.spese.items():
            for voce in voci:
                if len(voce) == 5 and voce[4] == ric_id:
                    residui.append((data, voce))
        if residui:
            print("❗ Voci residue trovate:")
            for data, voce in residui:
                print("  -", data, voce)        
        if hasattr(self, "db"):
            self.db["spese"] = self.spese
            self.db["ricorrenze"] = self.ricorrenze
        self.save_db()
        self.refresh_gui()
        self.ricorrenza_cat_sel.set(self.categorie[0])
        self.ricorrenza_tipo_voce.set("Uscita")
        self.btn_tipo_voce.config(text="Uscita", bg="#f2dede", fg="red")
        
    def on_ricorrenza_double_click(self, event):
        tree = event.widget
        parent_window = tree.winfo_toplevel()
        item_id = tree.focus()
        if not item_id or item_id not in self.ricorrenze:
            return

        ricorrenza_dati = self.ricorrenze.get(item_id, {})
        if not ricorrenza_dati:
            return

        descrizione_ricorrenza = ricorrenza_dati.get("cat", "N/D")
        importo_ricorrenza = ricorrenza_dati.get("imp", 0.0)

        popup_movimenti = tk.Toplevel(parent_window)
        popup_movimenti.title(f"Movimenti di '{descrizione_ricorrenza}'")

        parent_x = parent_window.winfo_rootx()
        parent_y = parent_window.winfo_rooty()
        parent_width = parent_window.winfo_width()
        parent_height = parent_window.winfo_height()
        popup_width = 800
        popup_height = 500
        center_x = parent_x + (parent_width // 2) - (popup_width // 2)
        center_y = parent_y + (parent_height // 2) - (popup_height // 2)
        popup_movimenti.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup_movimenti.transient(parent_window)

        tree_movimenti = ttk.Treeview(
            popup_movimenti,
            columns=("data", "descrizione", "importo", "pagato", "da_pagare"),
            show="headings"
        )
        tree_movimenti.pack(fill="both", expand=True, padx=10, pady=10)

        tree_movimenti.heading("data", text="Data")
        tree_movimenti.heading("descrizione", text="Categoria")
        tree_movimenti.heading("importo", text="Importo")
        tree_movimenti.heading("pagato", text="Pagato")
        tree_movimenti.heading("da_pagare", text="Da Pagare")

        tree_movimenti.column("data", width=100)
        tree_movimenti.column("descrizione", width=300)
        tree_movimenti.column("importo", width=80)
        tree_movimenti.column("pagato", width=80)
        tree_movimenti.column("da_pagare", width=80)

        tree_movimenti.tag_configure("giallo", background="yellow", foreground="black")
        tree_movimenti.tag_configure("verde", foreground="darkgreen")
        tree_movimenti.tag_configure("rosso", foreground="darkred")
        tree_movimenti.tag_configure("grigio", foreground="gray", background="#f2f2f2")

        tree_movimenti.bind("<Double-1>", self.on_scadenza_doppio_click)

        oggi = datetime.date.today()
        ric_periodo = ricorrenza_dati.get("tipo", "").lower()
        n_volte = ricorrenza_dati.get("n", 0)
        data_inizio_str = ricorrenza_dati.get("data_inizio", "")
        data_inizio_obj = datetime.datetime.strptime(data_inizio_str, "%d-%m-%Y").date()

        for i in range(n_volte):
            if ric_periodo == "ogni mese":
                data_movimento = (data_inizio_obj.replace(day=1) + datetime.timedelta(days=32 * i)).replace(day=data_inizio_obj.day)
            elif ric_periodo == "ogni anno":
                anno_movimento = data_inizio_obj.year + i
                try:
                    data_movimento = data_inizio_obj.replace(year=anno_movimento)
                except ValueError:
                    data_movimento = data_inizio_obj.replace(year=anno_movimento, day=28)
            else:
                data_movimento = data_inizio_obj + datetime.timedelta(days=i)
            desc = ricorrenza_dati['cat']
            importo_effettivo = importo_ricorrenza
            voce_trovata = False
            if data_movimento in self.spese:
                for voce in self.spese[data_movimento]:
                    if len(voce) == 5 and voce[4] == item_id:
                        importo_effettivo = voce[2]
                        voce_trovata = True
                        break
            if voce_trovata:
                valore_importo = f"{importo_effettivo:,.2f} €"
                tag = "rosso" if ricorrenza_dati['tipo_voce'] == "Uscita" else "verde"
            elif data_movimento <= oggi:
                valore_importo = "—"
                tag = "grigio"
            else:
                valore_importo = "—"
                tag = "giallo"
            tree_movimenti.insert(
                "",
                "end",
                values=(
                    data_movimento.strftime("%d-%m-%Y"),
                    desc,
                    valore_importo,
                    ricorrenza_dati['tipo_voce'] if voce_trovata else "❌",
                    "❌" if data_movimento <= oggi else ricorrenza_dati['tipo_voce']
                ),
                tags=(tag,)
            )
        info_frame = ttk.Frame(popup_movimenti, padding=(10, 5))
        info_frame.pack(fill="x", expand=False)
        info_text = (
            f"Dettagli ricorrenza: {descrizione_ricorrenza} - "
            f"Importo: {importo_ricorrenza:,.2f} € - "
            f"Periodo: {ricorrenza_dati.get('tipo', 'N/D')} - "
            f"Durata: {n_volte} volte"
        )
        ttk.Label(info_frame, text=info_text, font=("Arial", 10)).pack(side="left")
        ttk.Button(info_frame, text="❌ Chiudi", command=popup_movimenti.destroy, style='Giallo.TButton').pack(side="right", padx=5)
        popup_movimenti.bind("<Escape>", lambda e: popup_movimenti.destroy())
        
    def add_spesa(self):

        if hasattr(self, 'ricorrenza_tipo') and self.ricorrenza_tipo.get() != "Nessuna":
            self.add_ricorrenza()
            return
        data = self.data_spesa_var.get()
        cat = self.cat_sel.get()
        desc = self.desc_entry.get().strip()
        try:
            imp = float(self.imp_entry.get().replace(",", "."))
        except ValueError:
            self.show_custom_warning("Errore", "Importo mancante o non valido.")
            return
        tipo = self.tipo_spesa_var.get()
        try:
            d = datetime.datetime.strptime(data, "%d-%m-%Y").date()
        except ValueError:
            self.show_custom_warning("Errore", "Formato data non valido.")
            return
        if d not in self.spese:
            self.spese[d] = []
        self.spese[d].append((cat, desc, imp, tipo))
        self.desc_entry.delete(0, tk.END)
        self.imp_entry.delete(0, tk.END)
        self.save_db()
        self.reset_modifica_form()
        self.refresh_gui()
        if not self.blocca_data_var.get():
            self.data_spesa_var.set(datetime.date.today().strftime("%d-%m-%Y"))
        self.categoria_bloccata = False
        self.label_smartcat.config(text="🛠️ SmartCat attiva", foreground="red")
        self.metodo_pagamento_var.set("")

    def mostra_lista_ricorrenze(self):
        def parse_data(data_str):
            if isinstance(data_str, datetime.date):
                return data_str
            try:
                return datetime.datetime.strptime(data_str, "%d-%m-%Y").date()
            except (ValueError, TypeError):
                return None

        def calcola_data_fine(data_inizio, n_volte, periodo):
            if not data_inizio or not isinstance(n_volte, int) or n_volte < 1:
                return "N/D"
            periodo = periodo.lower().strip()
            if periodo == "ogni giorno":
                data_fine_obj = data_inizio + datetime.timedelta(days=n_volte - 1)
            elif periodo == "ogni mese":
                total_months = data_inizio.month + n_volte - 1
                anno_fine = data_inizio.year + (total_months - 1) // 12
                mese_fine = (total_months - 1) % 12 + 1
                giorno_fine = data_inizio.day
                if mese_fine == 12:
                    primo_giorno_mese_successivo = datetime.date(anno_fine + 1, 1, 1)
                else:
                    primo_giorno_mese_successivo = datetime.date(anno_fine, mese_fine + 1, 1)
                ultimo_giorno_mese_fine = (primo_giorno_mese_successivo - datetime.timedelta(days=1)).day
                giorno_fine = min(giorno_fine, ultimo_giorno_mese_fine)
                data_fine_obj = datetime.date(anno_fine, mese_fine, giorno_fine)
            elif periodo == "ogni anno":
                anno_fine = data_inizio.year + n_volte - 1
                try:
                    data_fine_obj = data_inizio.replace(year=anno_fine)
                except ValueError:
                    data_fine_obj = data_inizio.replace(year=anno_fine, day=28)
            else:
                return "N/D"
            return data_fine_obj.strftime("%d-%m-%Y")

        def _delete_selected_ricorrenze():
            selected_ids = tree.selection()
            if not selected_ids:
                self.show_custom_warning("Attenzione", "Seleziona almeno una ricorrenza da cancellare.")
                return
            response = self.show_custom_askyesno("Conferma Cancellazione", "\nSei sicuro di voler cancellare \n le ricorrenze selezionate?")
            if not response:
                return
            for ric_id in list(selected_ids):
                self._delete_ricorrenza_by_id(ric_id)
            lista_window.destroy()

        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            try:
                l.sort(key=lambda t: float(t[0].replace(' €', '').replace(',', '.').strip()), reverse=reverse)
            except (ValueError, IndexError):
                l.sort(key=lambda t: t[0], reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

        lista_window = tk.Toplevel(self)
        lista_window.withdraw()
        self.update_idletasks()
        main_x = self.winfo_rootx()
        main_y = self.winfo_rooty()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        lista_window_width = 1200
        lista_window_height = 600
        center_x = main_x + (main_width // 2) - (lista_window_width // 2)
        center_y = main_y + (main_height // 2) - (lista_window_height // 2)
        lista_window.geometry(f"{lista_window_width}x{lista_window_height}+{center_x}+{center_y}")
        lista_window.transient(self)
        lista_window.title("Lista delle Ricorrenze Programmate")
        lista_window.deiconify()
        lista_window.lift()
        lista_window.bind("<Escape>", lambda e: lista_window.destroy())
        main_frame = ttk.Frame(lista_window, padding=10)
        main_frame.pack(fill="both", expand=True)
        columns = ("Categoria", "Tipo", "Importo", "Durata", "Pagate", "Data Inizio", "Data Fine", "Importo Totale", "Già Pagato", "Rimanente", "ID")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
        style = ttk.Style()
        style.map("Treeview", background=[('selected', 'lightblue')], foreground=[('selected', 'black')])
        tree.tag_configure("uscita", foreground="darkred")
        tree.tag_configure("entrata", foreground="darkgreen")
        larghezze = {"Categoria": 110, "Tipo": 50, "Importo": 60, "Durata": 30, "Pagate": 30, "Data Inizio": 60, "Data Fine": 60, "Importo Totale": 80, "Già Pagato": 60, "Rimanente": 60, "ID": 250}
        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
            tree.column(col, width=larghezze[col], anchor="center")
        tree.pack(fill="both", expand=True)
        
        evasi_per_ricorrenza = {id_ric: [] for id_ric in self.ricorrenze.keys()}
        oggi = datetime.date.today()
        for id_ricorrenza, dati in self.ricorrenze.items():
            data_inizio_str = dati.get("data_inizio", "N/D")
            data_inizio_obj = parse_data(data_inizio_str)
            if data_inizio_obj:
                if dati.get("tipo", "").lower() == "ogni mese":
                    volte_passate = (oggi.year - data_inizio_obj.year) * 12 + (oggi.month - data_inizio_obj.month)
                    for i in range(volte_passate + 1):
                        data_movimento = (data_inizio_obj.replace(day=1) + datetime.timedelta(days=32 * i)).replace(day=data_inizio_obj.day)
                        if data_movimento <= oggi:
                            evasi_per_ricorrenza[id_ricorrenza].append({
                                'data': data_movimento.strftime("%d-%m-%Y"),
                                'descrizione': f"{dati['cat']} del {data_movimento.strftime('%B')}",
                                'importo': dati['imp'],
                                'tipo': dati['tipo_voce']
                            })
      
        tree.bind("<Double-1>", self.on_ricorrenza_double_click)
        bilancio_mensile = 0.0
        for i, (id_ricorrenza, dati) in enumerate(self.ricorrenze.items()):
            cat = dati.get("cat", "Sconosciuta")
            tipo_voce = dati.get("tipo_voce", dati.get("tipo", "N/D"))
            imp = dati.get("imp", 0.0)
            n_volte = dati.get("n", 0)
            ric_periodo = dati.get("tipo", "N/D")
            data_inizio_str = dati.get("data_inizio", "N/D")
            data_inizio_obj = parse_data(data_inizio_str)
            data_fine = calcola_data_fine(data_inizio_obj, n_volte, ric_periodo)
            importo_totale = imp * n_volte if isinstance(n_volte, int) else 0.0
            volte_passate = 0
            if data_inizio_obj:
                oggi = datetime.date.today()
                if oggi >= data_inizio_obj:
                    if ric_periodo.lower() == "ogni mese":
                        diff_mesi = (oggi.year - data_inizio_obj.year) * 12 + (oggi.month - data_inizio_obj.month)
                        volte_passate = diff_mesi + 1
                    elif ric_periodo.lower() == "ogni anno":
                        volte_passate = (oggi.year - data_inizio_obj.year) + 1
                    elif ric_periodo.lower() == "ogni giorno":
                        diff_giorni = (oggi - data_inizio_obj).days
                        volte_passate = diff_giorni + 1
            volte_passate = min(volte_passate, n_volte)
            importo_gia_pagato = imp * volte_passate
            importo_rimasto = importo_totale - importo_gia_pagato
            tag = "uscita" if tipo_voce == "Uscita" else "entrata"
            values = (cat, tipo_voce, f"{imp:,.2f} €", n_volte, volte_passate, data_inizio_str, data_fine, f"{importo_totale:,.2f} €", f"{importo_gia_pagato:,.2f} €", f"{importo_rimasto:,.2f} €", id_ricorrenza)
            tree.insert("", "end", iid=id_ricorrenza, values=values, tags=(tag,))
            if ric_periodo.lower() == "ogni mese":
                bilancio_mensile += imp if tipo_voce == "Entrata" else -imp
        summary_frame = ttk.Frame(main_frame, padding=(0, 10))
        summary_frame.pack(fill="x", expand=False)
        bilancio_colore = "darkgreen" if bilancio_mensile >= 0 else "darkred"
        ttk.Label(summary_frame, text="Impatto Mensile Stimato (su base 'Mese'):", font=("Arial", 10)).pack(side="left")
        ttk.Label(summary_frame, text=f"{bilancio_mensile:,.2f} €", font=("Arial", 11, "bold"), foreground=bilancio_colore).pack(side="left", padx=5)
        button_frame = ttk.Frame(main_frame, padding=(0, 10))
        button_frame.pack(fill="x", expand=False)
        cancel_button = ttk.Button(button_frame, text="❌ Cancella Selezionate", command=_delete_selected_ricorrenze, style="Verde.TButton")
        cancel_button.pack(side="left", padx=5)
        close_button = ttk.Button(button_frame, text="✅ Chiudi", command=lista_window.destroy, style="Giallo.TButton")
        close_button.pack(side="right", padx=5)
        
    def set_tipo_spesa_editable(self, editable=True):
        if editable:
            self.btn_tipo_spesa.state(["!disabled"])
        else:
            self.btn_tipo_spesa.state(["disabled"])

    def _inserisci_importo_senza_validazione(self, imp_value):
        self.imp_entry.config(validate="none") 
        self.imp_entry.delete(0, tk.END)
        self.imp_entry.insert(0, imp_value)
        vcmd = self.imp_entry.cget('validatecommand')
        self.imp_entry.config(validate="key", validatecommand=vcmd)

    def on_table_click(self, event):
        self.label_smartcat.config(text="🛠️ SmartCat disattiva", foreground="green")
        self.aggiorna_bottone_spese_simili(visibile=False)
        mode = self.stats_mode.get()
        if mode != "giorno":
            return
        region = self.stats_table.identify("region", event.x, event.y)
        if region != "cell":
            return
        col = self.stats_table.identify_column(event.x)
        if col != "#6":
            return
        self.suggerimenti_attivi = False 
        rowid = self.stats_table.identify_row(event.y)
        if not rowid:
            return
        vals = self.stats_table.item(rowid, "values")
        giorno_str, cat, desc, imp, tipo, _ = vals
        giorno = datetime.datetime.strptime(giorno_str, "%d-%m-%Y").date()
        idx = self.stats_table.index(rowid)
        voce = self.spese[giorno][idx]
        self.modifica_idx = (giorno, idx)
        self.cat_sel.set(cat)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, desc)
        self.imp_entry.delete(0, tk.END)
        self.imp_entry.insert(0, imp)
        self.after(0, lambda: self._inserisci_importo_senza_validazione(imp))
        self.tipo_spesa_var.set(tipo)
        self.btn_tipo_spesa.config(text=tipo)
        self.btn_modifica["state"] = tk.NORMAL
        self.btn_aggiungi["state"] = tk.DISABLED
        self.btn_cancella["state"] = tk.NORMAL
        self.data_spesa_var.set(giorno.strftime("%d-%m-%Y"))
        self.btn_reset_form["state"] = tk.DISABLED
        #Modifica entrata uscita consentito
        self.set_tipo_spesa_editable(True)
        
        new_style = 'GreenOutline.TButton' if tipo == "Entrata" else 'RedOutline.TButton'
        self.btn_tipo_spesa.config(style=new_style)
        if len(voce) == 5:
            ric_id = voce[4]
            if ric_id in self.ricorrenze:
                ric = self.ricorrenze[ric_id]
                self.show_custom_info("Voce ricorrente", f"Questa voce è parte di una ricorrenza: {ric['tipo']} x{ric['n']} da {ric['data_inizio']}.\nPuoi cancellare tutta la ricorrenza dal pannello Ricorrenze sotto.\nIn alternativa puoi modificare la singola voce o cancellarla")

    def aggiorna_stile_tipo_spesa(self):
        tipo = self.tipo_spesa_var.get()
        btn_style = 'GreenOutline.TButton' if tipo == "Entrata" else 'RedOutline.TButton'
        
        self.btn_tipo_spesa.config(
            text=tipo,
            style=btn_style
        )

    def reset_modifica_form(self):
        self.suggerimenti_attivi = True  
        self.label_smartcat.config(text="🛠️ SmartCat attiva", foreground="red")
        self.modifica_idx = None
        self.btn_modifica["state"] = tk.DISABLED
        self.btn_aggiungi["state"] = tk.NORMAL
        self.btn_cancella["state"] = tk.DISABLED
        self.desc_entry.delete(0, tk.END)
        self.imp_entry.delete(0, tk.END)
        self.cat_sel.set("Generica")
        self.metodo_pagamento_var.set("")
        self.on_categoria_changed()
        self.set_tipo_spesa_editable(True)
        if not self.blocca_data_var.get():
         self.data_spesa_var.set(datetime.date.today().strftime("%d-%m-%Y"))
        self.categoria_bloccata = False  
        self.btn_reset_form["state"] = tk.NORMAL
        self.btn_aggiungi["state"] = tk.NORMAL
        
    def salva_modifica(self):
        if not self.modifica_idx:
            return
        old_dt, idx = self.modifica_idx
        new_data = self.data_spesa_var.get()
        new_dt = datetime.datetime.strptime(new_data, "%d-%m-%Y").date()
        cat = self.cat_sel.get()
        desc = self.desc_entry.get().strip()
        try:
            imp = float(self.imp_entry.get().replace(",", "."))
        except Exception:
            self.show_custom_warning("Errore", "Importo mancante o non valido.")
            return
        tipo = self.tipo_spesa_var.get()

        if old_dt not in self.spese or idx >= len(self.spese[old_dt]):
            self.show_custom_warning("Errore", "La voce selezionata non esiste più.")
            self.reset_modifica_form()
            return
        voce_old = self.spese[old_dt][idx]
        id_ric = voce_old[4] if len(voce_old) == 5 else None

        del self.spese[old_dt][idx]
        if not self.spese[old_dt]:
            del self.spese[old_dt]
        if new_dt not in self.spese:
            self.spese[new_dt] = []
        voce_new = (cat, desc, imp, tipo)
        if id_ric is not None:
            voce_new += (id_ric,)
        self.spese[new_dt].append(voce_new)
        self.save_db()
        self.refresh_gui()
        self.reset_modifica_form()
        self.suggerimenti_attivi = True 
        self.btn_aggiungi["state"] = tk.NORMAL
        
    def cancella_voce(self):
        if not self.modifica_idx:
            return
        dt, idx = self.modifica_idx
        if dt in self.spese and 0 <= idx < len(self.spese[dt]):
            del self.spese[dt][idx]
            if not self.spese[dt]:
                del self.spese[dt]
            self.save_db()
            self.refresh_gui()
        self.reset_modifica_form()
        self.colora_giorni_spese()
        self.suggerimenti_attivi = True 
        self.btn_aggiungi["state"] = tk.NORMAL
        
    def update_spese_mese_corrente(self):
        for i in self.spese_mese_tree.get_children():
            self.spese_mese_tree.delete(i)
        now = datetime.date.today()
        year, month = now.year, now.month
        spese_mese = []
        for d in sorted(self.spese.keys()):
            if d.year == year and d.month == month:
                for entry in self.spese[d]:
                    cat, desc, imp, tipo = entry[:4]
                    spese_mese.append((d, cat, desc, imp, tipo))
        for d, cat, desc, imp, tipo in spese_mese:
            tag = 'entrata' if tipo == 'Entrata' else 'uscita'
            self.spese_mese_tree.insert("", "end", values=(
                d.strftime("%d-%m-%Y"), cat, desc, f"{imp:.2f}", tipo
            ), tags=(tag,))

    def apply_estratto(self, forza_modalita=None):
        try:
            m = int(self.estratto_month_var.get().split(" - ")[0])
            y = int(self.estratto_year_var.get())
            d = datetime.date(y, m, 1)
            self.stats_refdate = d

            if forza_modalita:
                self.set_stats_mode(forza_modalita)

            self.update_totalizzatore_anno_corrente()
            self.update_totalizzatore_mese_corrente()
            self.update_spese_mese_corrente()
        except Exception:
            self.show_custom_warning("Errore", "Mese o anno non validi")

    def set_stats_mode(self, mode):
        self.stats_mode.set(mode)
        if mode == "giorno":
            try:
                data_corrente = self.cal.selection_get()
            except Exception:
                data_corrente = datetime.date.today()
            
            self.stats_label.config(text=f"Riepilogo Giornaliero - {data_corrente.strftime('%d-%m-%Y')}", foreground="purple",
    font=("Arial", 10, "bold"))

            self.stats_table["displaycolumns"] = ("A", "B", "C", "D", "E", "F")
            self.stats_table.column("A", width=80, anchor="center")
            self.stats_table.column("B", width=150, anchor="w")
            self.stats_table.column("C", width=240, anchor="w")
            self.stats_table.column("D", width=100, anchor="center")
            self.stats_table.column("E", width=80, anchor="center")
            self.stats_table.column("F", width=60, anchor="center")

            self.stats_table.heading("A", text="Data")
            self.stats_table.heading("B", text="Categoria")
            self.stats_table.heading("C", text="Descrizione")
            self.stats_table.heading("D", text="Importo (€)")
            self.stats_table.heading("E", text="Tipo")
            self.stats_table.heading("F", text="Modifica")

            self.update_stats()

        elif mode == "mese":
            ref = self.stats_refdate
            monthname = self.get_month_name(ref.month)
            self.stats_label.config(text=f"Riepilogo Mensile {monthname} {ref.year}", foreground="navy",
    font=("Arial", 10, "bold"))
            self.stats_table["displaycolumns"] = ("A","B","C")
            self.stats_table.column("A", width=300, anchor="w")
            self.stats_table.column("B", width=200, anchor="center")
            self.stats_table.column("C", width=150, anchor="center")
            self.stats_table.heading("A", text="Categoria")
            self.stats_table.heading("B", text="Totale Categoria (€)")
            self.stats_table.heading("C", text="Tipo")
        elif mode == "anno":
            ref = self.stats_refdate
            self.stats_label.config(text=f"Riepilogo Annuale {ref.year}", foreground="forest green",
    font=("Arial", 10, "bold"))
            self.stats_table["displaycolumns"] = ("A","B","C")
            self.stats_table.column("A", width=300, anchor="w")
            self.stats_table.column("B", width=200, anchor="center")
            self.stats_table.column("C", width=150, anchor="center")
            self.stats_table.heading("A", text="Categoria")
            self.stats_table.heading("B", text="Totale Categoria (€)")
            self.stats_table.heading("C", text="Tipo")
        else:
            self.stats_label.config(text="Riepilogo Categorie", foreground="firebrick",
    font=("Arial", 10, "bold"))
            self.stats_table["displaycolumns"] = ("A","B","C")
            self.stats_table.column("A", width=300, anchor="w")
            self.stats_table.column("B", width=200, anchor="center")
            self.stats_table.column("C", width=150, anchor="center")
            self.stats_table.heading("A", text="Categoria")
            self.stats_table.heading("B", text="Totale Categoria (€)")
            self.stats_table.heading("C", text="Tipo")
        self.update_stats()
        self.update_totalizzatore_anno_corrente()
        self.update_totalizzatore_mese_corrente()
        self.update_spese_mese_corrente()

    def treeview_sort_column(self, tv, col, reverse):
        items = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:  
            items.sort(key=lambda t: float(str(t[0]).replace(",", ".").replace("€", "")), reverse=reverse)
        except Exception:
            items.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(items):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def get_month_name(self, month):
        mesi = [
            "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
        ]
        return mesi[month-1] if 1 <= month <= 12 else str(month)

    def update_stats(self):
        for i in self.stats_table.get_children():
            self.stats_table.delete(i)

        mode = self.stats_mode.get()
        tot_entrate, tot_uscite = 0.0, 0.0
        oggi = datetime.date.today()
        ref = self.stats_refdate

        if mode == "giorno":
            try:
                giorno = datetime.datetime.strptime(self.cal.get_date(), "%d-%m-%Y").date()
            except Exception:
                giorno = oggi
            spese = self.spese.get(giorno, [])
            for idx, entry in enumerate(spese):
                cat, desc, imp, tipo = entry[:4]
                tag = "entrata" if tipo == "Entrata" else "uscita"
                self.stats_table.insert(
                    "", "end",
                    values=(giorno.strftime("%d-%m-%Y"), cat, desc, f"{imp:.2f}", tipo, "Modifica"),
                    tags=(f"{giorno.strftime('%d-%m-%Y')}|{idx}", tag)
                )
                if tipo == "Entrata":
                    tot_entrate += imp
                else:
                    tot_uscite += imp
        else:
  
            totali = {}
            for d, sp in self.spese.items():
                
                if mode == "mese":
                    if not (d.year == ref.year and d.month == ref.month):
                        continue
                elif mode == "anno":
                    if d.year != ref.year:
                        continue
                for entry in sp:
                    data_voce = d
                    if not self.considera_ricorrenze_var.get():
                        if mode == "totali":
                            if data_voce > oggi:
                                continue
                        elif mode == "anno":
                            if ref.year == oggi.year:
                                if data_voce > oggi:
                                    continue    
                        elif mode == "mese":
                            if ref.year == oggi.year and ref.month == oggi.month:
                                if data_voce > oggi:
                                    continue
                    cat, desc, imp, tipo = entry[:4]
                    if cat not in totali:
                        totali[cat] = {"Entrata": 0.0, "Uscita": 0.0}
                    totali[cat][tipo] += imp
                    
            for cat in sorted(totali.keys()):
                for tipo in ("Entrata", "Uscita"):
                    if totali[cat][tipo] > 0:
                        tag = "entrata" if tipo == "Entrata" else "uscita"
                        self.stats_table.insert(
                            "", "end",
                            values=(cat, f"{totali[cat][tipo]:.2f}", tipo),
                            tags=(tag,)
                        )
                        if tipo == "Entrata":
                            tot_entrate += totali[cat][tipo]
                        else:
                            tot_uscite += totali[cat][tipo]
        diff = tot_entrate - tot_uscite
        colore_fg = "blue" if diff >= 0 else "red" 
        txt_tot = f"Totale Entrate: {tot_entrate:.2f}    Totale Uscite: {tot_uscite:.2f}    Differenza: {diff:.2f}"
        self.totali_label.config(text=txt_tot, foreground=colore_fg, font=("Arial", 10, "bold"))

    def update_totalizzatore_anno_corrente(self):
        anno = datetime.date.today().year
        totale_entrate = 0.0
        totale_uscite = 0.0
        for d, sp in self.spese.items():
            if d.year == anno:
                for entry in sp:
                    if hasattr(self, "considera_ricorrenze_var") and not self.considera_ricorrenze_var.get() and len(entry) == 5:
                        if d > datetime.date.today():
                            continue
                    tipo = entry[3]
                    imp = entry[2]
                    if tipo == "Entrata":
                        totale_entrate += imp
                    else:
                        totale_uscite += imp
        differenza = totale_entrate - totale_uscite
        self.totalizzatore_entrate_label.config(text=f"{totale_entrate:.2f} €")
        self.totalizzatore_uscite_label.config(text=f"{totale_uscite:.2f} €")
        self.totalizzatore_diff_label.config(
            text=f"{differenza:.2f} €",
            foreground="blue" if differenza >= 0 else "red"
        )
     
    def update_totalizzatore_mese_corrente(self):
        now = datetime.date.today()
        year, month = now.year, now.month
        totale_entrate = 0.0
        totale_uscite = 0.0
        for d, sp in self.spese.items():
            if d.year == year and d.month == month:
                for entry in sp:
                    if hasattr(self, "considera_ricorrenze_var") and not self.considera_ricorrenze_var.get() and len(entry) == 5:
                        if d > now:
                            continue
                    tipo = entry[3]
                    imp = entry[2]
                    if tipo == "Entrata":
                        totale_entrate += imp
                    else:
                        totale_uscite += imp
        differenza = totale_entrate - totale_uscite
        self.totalizzatore_mese_entrate_label.config(text=f"{totale_entrate:.2f} €")
        self.totalizzatore_mese_uscite_label.config(text=f"{totale_uscite:.2f} €")
        self.totalizzatore_mese_diff_label.config(
            text=f"{differenza:.2f} €",
            foreground="blue" if differenza >= 0 else "red"
        )
 
    def show_reset_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Reset Database")
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.transient(self)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 600  
        window_height = 250 
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        dialog.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        dialog.bind("<Escape>", lambda e: dialog.destroy())

        label = tk.Label(dialog, text=(
            "Vuoi cancellare tutte le spese e/o le categorie?\n\n"
            "Scegli 'Sì' per cancellare tutto (spese + categorie, resterà solo la categoria di default)\n\n"
            "'No' per cancellare solo le spese.\n\n"
            "'Letture' per cancellare le letture delle utenze\n\n"
            "'Rubrica' per cancellare tutta la rubrica\n"
            "'Password' per cancellare la password\n"
        ), font=("Arial", 10), justify="left", padx=12, pady=10)
        label.pack()

        btns = tk.Frame(dialog)
        btns.pack(pady=(0, 10))
 
        def do_yes():
            dialog.destroy()
            self.spese = {}
            self.categorie = ["Generica"]
            self.categorie_tipi = {"Generica": "Uscita"}
            self.ricorrenze = {}
            self.cat_menu["values"] = self.categorie
            self.cat_mod_menu["values"] = self.categorie
            self.cat_sel.set(self.categorie[0])
            self.cat_mod_sel.set(self.categorie[0])
            self.save_db()
            self.update_stats()
            self.update_totalizzatore_anno_corrente()
            self.update_totalizzatore_mese_corrente()
            self.update_spese_mese_corrente()
            self.show_custom_warning("Spese", "Spese e categorie azzerate")
        def do_no():
            dialog.destroy()
            self.spese = {}
            self.ricorrenze = {}
            self.save_db()
            self.update_stats()
            self.update_totalizzatore_anno_corrente()
            self.update_totalizzatore_mese_corrente()
            self.update_spese_mese_corrente()
            self.show_custom_warning("Spese", "Spese azzerate")
        def do_letture():
            dialog.destroy()
            if os.path.exists(UTENZE_DB):
             os.remove(UTENZE_DB)
            if not os.path.exists(UTENZE_DB):
               with open(UTENZE_DB, "w") as file:
                 file.write("{\n}\n")  
                 self.show_custom_warning("Letture", "Letture utenze azzerate")
        def do_rubrica():
            dialog.destroy()
            if os.path.exists(DATI_FILE):
             os.remove(DATI_FILE)
            self.show_custom_warning("Rubrica", "Dati Rubrica azzerate")
        def do_password():
            dialog.destroy()
            if os.path.exists(PW_FILE):
             os.remove(PW_FILE)
            self.show_custom_warning("Password", "Password azzerata")
        def do_cancel():
            dialog.destroy()
            
        ttk.Button(btns, text="✅ Sì", command=do_yes, style="Rosso.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="❌ No", command=do_no, style="Rosso.TButton").grid(row=0, column=1, padx=5)
        ttk.Button(btns, text="📅 Letture", command=do_letture, style="Blu.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(btns, text="📅 Rubrica", command=do_rubrica, style="Blu.TButton").grid(row=0, column=3, padx=5)
        ttk.Button(btns, text="📅 Password", command=do_password, style="Blu.TButton").grid(row=0, column=4, padx=5)
        ttk.Button(btns, text="❌ Annulla", command=do_cancel, style="Giallo.TButton").grid(row=0, column=5, padx=5)

        btns.focus_set()
        dialog.bind("<Escape>", lambda e: do_cancel())
        dialog.bind("<Return>", lambda e: do_yes())
        dialog.bind("<KP_Enter>", lambda e: do_yes())

    def export_giorno_forzato(self):
        old_mode = self.stats_mode.get()
        self.stats_mode.set("giorno")
        self.export_stats()
        self.stats_mode.set(old_mode)

    def export_stats(self):
        mode = self.stats_mode.get()
        lines = []
 
        label_width = 20
        desc_width = 30
        value_width = 14
        tipo_width = 10

        tot_entrate, tot_uscite = 0.0, 0.0

        if mode == "giorno":
            try:
                giorno = datetime.datetime.strptime(self.cal.get_date(), "%d-%m-%Y").date()
            except Exception:
                giorno = datetime.date.today()

            spese = self.spese.get(giorno, []) or self.spese.get(giorno.strftime("%d-%m-%Y"), [])
            header = f"{'Categoria':<{label_width}} {'Descrizione':<{desc_width}} {'Importo (€)':>{value_width}}  {'Tipo':<{tipo_width}}"
            sep = "-" * len(header)

            lines.append("=" * len(header))
            lines.append(f"{('Riepilogo Giornaliero - ' + giorno.strftime('%d-%m-%Y')).center(len(header))}")
            lines.append("=" * len(header))
            lines.append("")
            lines.append(header)
            lines.append(sep)

            if not spese:
                lines.append("Nessuna spesa trovata per il giorno selezionato.")
            else:
                for entry in spese:
                    cat, desc, imp, tipo = entry[:4]
                    lines.append(f"{cat:<{label_width}.{label_width}} {desc:<{desc_width}.{desc_width}} {imp:>{value_width}.2f}  {tipo:<{tipo_width}}")
                    if tipo == "Entrata":
                        tot_entrate += imp
                    else:
                        tot_uscite += imp

            lines.append(sep)

        else:
            totali = {}
            tipo_cat = {}
            ref = self.stats_refdate

            if mode == "mese":
                year, month = ref.year, ref.month
                monthname = self.get_month_name(month)
                title = f"Riepilogo Mensile - {monthname} {year}"
            elif mode == "anno":
                year = ref.year
                title = f"Riepilogo Anno {year}"
            else:
                title = "Riepilogo Categorie"

            header = f"{'Categoria':<{label_width}} {'Totale (€)':>{value_width}}  {'Tipo':<{tipo_width}}"
            sep = "-" * len(header)

            lines.append("=" * len(header))
            lines.append(title.center(len(header)))
            lines.append("=" * len(header))
            lines.append("")
            lines.append(header)
            lines.append(sep)

            for d, sp in self.spese.items():
                try:
                    d2 = datetime.datetime.strptime(d, "%d-%m-%Y").date() if isinstance(d, str) else d
                except:
                    continue

                if (mode == "mese" and d2.year == year and d2.month == month) or \
                   (mode == "anno" and d2.year == year) or \
                   (mode == "totali"):
                    for entry in sp:
                        cat, desc, imp, tipo = entry[:4]
                        totali[cat] = totali.get(cat, 0.0) + imp
                        tipo_cat[cat] = self.categorie_tipi.get(cat, tipo)

            for cat in sorted(totali.keys()):
                val = totali[cat]
                tipo = tipo_cat.get(cat, "Uscita")
                lines.append(f"{cat:<{label_width}.{label_width}} {val:>{value_width}.2f}  {tipo:<{tipo_width}}")
                if tipo == "Entrata":
                    tot_entrate += val
                else:
                    tot_uscite += val

            lines.append(sep)

        diff = tot_entrate - tot_uscite
        lines.append(f"{'Totale Entrate:':<{label_width}} {tot_entrate:>{value_width}.2f}")
        lines.append(f"{'Totale Uscite:':<{label_width}} {tot_uscite:>{value_width}.2f}")
        lines.append(f"{'Differenza:':<{label_width}} {diff:>{value_width}.2f} €")
        lines.append("=" * max(len(header), label_width + value_width + tipo_width + 3))

        now = datetime.date.today()
        filename = ""

        if mode == "giorno":
            try:
                giorno = datetime.datetime.strptime(self.cal.get_date(), "%d-%m-%Y").date()
            except Exception:
                giorno = now
            filename = f"Riepilogo_Giorno_{giorno.strftime('%d-%m-%Y')}.txt"
        elif mode == "mese":
            monthname = self.get_month_name(ref.month)
            filename = f"Riepilogo_Mese_{monthname}_{ref.year}.txt"
        elif mode == "anno":
            filename = f"Riepilogo_Anno_{ref.year}.txt"
        else:
            filename = f"Riepilogo_Per_Categoria.txt"

        self.show_export_preview("\n".join(lines), default_filename=filename)

        
    def export_month_detail(self):
        ref = self.stats_refdate
        month = ref.month
        year = ref.year
        monthname = self.get_month_name(month)
        oggi = datetime.date.today()

        giorni_settimana = [
            "Lunedì", "Martedì", "Mercoledì", "Giovedì",
            "Venerdì", "Sabato", "Domenica"
        ]

        lines = []
        tot_entrate, tot_uscite = 0.0, 0.0

        lines.append("=" * 100)
        lines.append(f"{('Riepilogo Mensile ' + monthname + ' ' + str(year)).center(100)}")
        lines.append("=" * 100 + "\n")

        days_in_month = [
            d for d in sorted(self.spese.keys())
            if d.year == year and d.month == month
        ]

        if not days_in_month:
            lines.append("Nessuna spesa registrata in questo mese.\n")
        else:
            for d in days_in_month:
                giorno_it = giorni_settimana[d.weekday()]
                lines.append(f"{giorno_it:<10} {d.strftime('%d/%m/%Y')}")
                lines.append("-" * 100)
                lines.append(f"{'':2}{'Categoria':<20}{'Descrizione':<40}{'Tipo':<10}{'Importo (€)':>14}")
                ent_giorno, usc_giorno = 0.0, 0.0
                for entry in self.spese.get(d, []):
                    is_ricorrenza = len(entry) == 5
                    
                    if not self.considera_ricorrenze_var.get():
                        if d > oggi:
                            continue
                    if len(entry) >= 4:
                        cat, desc, imp, tipo = entry[:4]
                        lines.append(f"{'':2}{cat:<20.20}{desc:<40.40}{tipo:<10}{imp:14.2f}")
                        if tipo == "Entrata":
                            ent_giorno += imp
                            tot_entrate += imp
                        else:
                            usc_giorno += imp
                            tot_uscite += imp
                lines.append(f"\n{'':2}Totale giorno → Entrate: {ent_giorno:8.2f} €   Uscite: {usc_giorno:8.2f} €\n")

        lines.append("-" * 100)
        lines.append(f"{'Totale entrate mese:':<60}{tot_entrate:14.2f} €")
        lines.append(f"{'Totale uscite mese:':<60}{tot_uscite:14.2f} €")
        lines.append(f"{'Saldo finale:':<60}{(tot_entrate - tot_uscite):14.2f} €")

        now = datetime.date.today()
        month = now.strftime("%m-%Y")
        filename = f"Riepilogo_Mese_{month}.txt"
        self.show_export_preview("\n".join(lines), default_filename=filename)

    def show_export_preview(self, content, default_filename=None):
        preview = tk.Toplevel(self)
        preview.withdraw()  
        preview.title("Anteprima Esportazione Riepilogo")
        #preview.resizable(False, False)
        
        larghezza_finestra = 1300
        altezza_finestra = 600

        def centra_finestra():
                screen_width = preview.winfo_screenwidth()
                screen_height = preview.winfo_screenheight()
                x = (screen_width - larghezza_finestra) // 2
                y = (screen_height - altezza_finestra) // 2
                preview.geometry(f"{larghezza_finestra}x{altezza_finestra}+{x}+{y}")
                preview.deiconify()
                preview.lift()
                preview.focus_force()

        preview.after(0, centra_finestra)
        #preview.grab_set()
        
        preview.bind("<Escape>", lambda e: preview.destroy())

        text = tk.Text(preview, wrap="none", font=("Courier new", 10))
        text.insert("1.0", content)
        text.config(state="disabled")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def save_file():
            now = datetime.date.today()
            filename = default_filename or f"Riepilogo_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File txt", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=filename,
                title="Salva Riepilogo",
                confirmoverwrite=False,
                parent=preview)
            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return  

                with open(file, "w", encoding="utf-8") as f:
                    f.write(content)
                preview.destroy()
                self.show_custom_warning("Esportazione completata", f"Riepilogo esportato in {file}")

        btn_frame = ttk.Frame(preview)
        btn_frame.pack(fill=tk.X, pady=8)

        btn_salva = ttk.Button(btn_frame, text="💾 Salva", command=save_file, style="Verde.TButton")
        btn_salva.pack(side=tk.LEFT, padx=10)

        btn_chiudi = ttk.Button(btn_frame, text="❌ Chiudi", command=preview.destroy, style="Giallo.TButton")
        btn_chiudi.pack(side=tk.RIGHT, padx=10)

        preview.update() 
        
    def import_db(self):
        file = filedialog.askopenfilename(
            title="Importa Database",
            defaultextension=".json",
            initialdir=EXP_DB,
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        if file:
            try:
                with open(file, "r", encoding="utf-8") as fsrc:
                    dbdata = fsrc.read()
                with open(DB_FILE, "w", encoding="utf-8") as fdst:
                    fdst.write(dbdata)
                self.load_db()
                self.cat_menu["values"] = self.categorie
                self.cat_mod_menu["values"] = self.categorie
                if self.categorie:
                    self.cat_sel.set(self.categorie[0])
                    self.cat_mod_sel.set(self.categorie[0])
                self.update_stats()
                self.update_totalizzatore_anno_corrente()
                self.update_totalizzatore_mese_corrente()
                self.update_spese_mese_corrente()
                self.show_custom_warning("Importazione completata", f"Database importato da {file}")
            except Exception as e:
                self.show_custom_warning("Errore", f"Errore durante l'esportazione: {e}")

    def export_db(self):
        now = datetime.date.today()
        default_dir = EXP_DB
        default_filename = f"Export_Database{now.day:02d}-{now.month:02d}-{now.year}.json"
        file = filedialog.asksaveasfilename(
            title="Esporta Database",
            defaultextension=".json",
            initialdir=default_dir,
            initialfile=default_filename,
            confirmoverwrite=False,
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
        )
        if file:
            try:
                with open(DB_FILE, "r", encoding="utf-8") as fsrc:
                    dbdata = fsrc.read()
                with open(file, "w", encoding="utf-8") as fdst:
                    fdst.write(dbdata)
                self.show_custom_warning("Esportazione completata", f"Database esportato in {file}")
            except Exception as e:
                self.show_custom_warning("Errore", "Errore durante l'esportazione:", f"{e}")

    def export_anno_dettagliato(self):
        try:
            year = int(self.estratto_year_var.get())
        except Exception:
            year = datetime.date.today().year

        mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        label_width = 22

        categorie = sorted(
            set(
                entry[0]
                for sp in self.spese.values()
                for entry in sp
                if isinstance(entry, (list, tuple)) and len(entry) >= 4
            ).union(self.categorie)
        )

        tot_entrate_mese = [0.0] * 12
        tot_uscite_mese = [0.0] * 12
        cat_entrate = {cat: [0.0] * 12 for cat in categorie}
        cat_uscite = {cat: [0.0] * 12 for cat in categorie}
        tot_entrate_anno = 0.0
        tot_uscite_anno = 0.0

        oggi = datetime.date.today()

        def date_from_key(d):
            if isinstance(d, datetime.date):
                return d
            try:
                return datetime.datetime.strptime(d, "%d-%m-%Y").date()
            except:
                return None

        for d, sp in self.spese.items():
            d2 = date_from_key(d)
            if d2 and d2.year == year:
                m = d2.month - 1
                for entry in sp:
                    is_ricorrenza = len(entry) == 5
                    
                    if hasattr(self, "considera_ricorrenze_var") and not self.considera_ricorrenze_var.get():
                        if year == oggi.year:
                            if d2 > oggi:
                                continue
                        
                    if len(entry) >= 4:
                        cat, desc, imp, tipo = entry[:4]
                        if tipo == "Entrata":
                            tot_entrate_mese[m] += imp
                            tot_entrate_anno += imp
                            cat_entrate[cat][m] += imp
                        else:
                            tot_uscite_mese[m] += imp
                            tot_uscite_anno += imp
                            cat_uscite[cat][m] += imp

        def format_row(label, values):
            label_fmt = f"{label:<{label_width}.{label_width}}"
            numeri = "".join(f"{v:10.2f}" for v in values)
            return f"{label_fmt}{numeri}{sum(values):12.2f}"

        header = f"{'Categoria':<{label_width}}" + "".join(f"{m:>10}" for m in mesi) + f"{'Totale':>12}"

        sep = "-" * len(header)

        lines = []
        lines.append("=" * len(header))
        lines.append(f"{('RIEPILOGO ENTRATE/USCITE ANNO ' + str(year)).center(len(header))}")
        lines.append("=" * len(header))
        lines.append("")

        lines.append(header)
        lines.append(sep)
        lines.append("")

        lines.append("ENTRATE PER CATEGORIA:")
        lines.append(header)
        for cat in categorie:
            if any(cat_entrate[cat]):
                lines.append(format_row(cat, cat_entrate[cat]))
        lines.append(sep)
        lines.append(format_row("• Totale Entrate", tot_entrate_mese))
        lines.append(sep)
        lines.append("")

        lines.append("USCITE PER CATEGORIA:")
        lines.append(header)
        for cat in categorie:
            if any(cat_uscite[cat]):
                lines.append(format_row(cat, cat_uscite[cat]))
        lines.append("")

        lines.append(sep)
        lines.append(format_row("• Totale Uscite", tot_uscite_mese))
        lines.append("-" * len(header))
        saldo = tot_entrate_anno - tot_uscite_anno
        lines.append(f"{'SALDO FINALE:':<{label_width}}{saldo:>{len(header) - label_width}.2f} €")
        lines.append("=" * len(header))

        text = "\n".join(lines)
        
        now = datetime.date.today()
        self.show_export_preview(text, default_filename=f"Riepilogo_Anno_{year}.txt")

    def suggerisci_tipo_categoria(self, categoria):
        n_entrate = 0
        n_uscite = 0
        for voci in self.spese.values():
            for voce in voci:
                if len(voce) >= 4 and voce[0] == categoria:
                    tipo = voce[3]
                    if tipo == "Entrata":
                        n_entrate += 1
                    elif tipo == "Uscita":
                        n_uscite += 1
        totale = n_entrate + n_uscite
        if totale == 0:
            return ("Uscita", 0, 0)
        perc_entrate = int(n_entrate / totale * 100)
        perc_uscite = int(n_uscite / totale * 100)
        tipo_prevalente = "Entrata" if n_entrate >= n_uscite else "Uscita"
        return (tipo_prevalente, perc_entrate, perc_uscite)

    def open_analisi_categoria(self):
        popup = tk.Toplevel(self)
        popup.title("Analisi Categoria")
        popup.geometry("700x600")
        #popup.resizable(False, False)
        popup.transient(self)
        #popup.grab_set()

        popup.bind("<Escape>", lambda e: popup.destroy())

        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - 350
        y = self.winfo_rooty() + (self.winfo_height() // 2) - 300
        popup.geometry(f"+{x}+{y}")

        frame_top = ttk.Frame(popup)
        frame_top.pack(padx=18, pady=10, fill=tk.X)
        ttk.Label(frame_top, text="🔍 Seleziona modalità:").pack(side=tk.LEFT)
        mode_var = tk.StringVar(value="Giorno")
        mode_combo = ttk.Combobox(frame_top, values=["Giorno", "Mese", "Anno", "Totale"], textvariable=mode_var, state="readonly", width=10)
        mode_combo.pack(side=tk.LEFT, padx=10)

        frame_period = ttk.Frame(popup)
        frame_period.pack(padx=18, pady=2, fill=tk.X)

        months = [
            "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
        ]
        today = datetime.date.today()
    
        anni_presenti = sorted({d.year for d in self.spese.keys()}, reverse=True)
        if not anni_presenti:
            anni_presenti = [today.year]
    
        year_var_initial = str(anni_presenti[0]) if anni_presenti else str(today.year)
        year_var = tk.StringVar(value=year_var_initial)
    
        day_var = tk.StringVar(value=str(today.day))
        month_var = tk.StringVar(value=months[today.month - 1]) 

        def get_years_presenti():
            return [str(y) for y in anni_presenti]

        year_combo = ttk.Combobox(frame_period, values=get_years_presenti(), textvariable=year_var, state="readonly", width=8)
        month_combo = ttk.Combobox(frame_period, values=months, textvariable=month_var, state="readonly", width=16)
        day_combo = ttk.Combobox(frame_period, values=[str(d) for d in range(1, 32)], textvariable=day_var, state="readonly", width=4)
        year_combo_only = ttk.Combobox(frame_period, values=get_years_presenti(), textvariable=year_var, state="readonly", width=8)
        
        def update_days(*_):
            try:
                m = months.index(month_var.get()) + 1
                y = int(year_var.get())
            except Exception:
                m = today.month
                y = today.year
            n_days = calendar.monthrange(y, m)[1]
            days = [str(d) for d in range(1, n_days+1)]
            day_combo['values'] = days
            if day_var.get() not in days:
                day_var.set(days[-1])
        month_var.trace_add("write", update_days)
        year_var.trace_add("write", update_days)

        def reset_period():
            oggi = datetime.date.today()
            day_var.set(str(oggi.day))
            month_var.set(months[oggi.month - 1])
            year_var.set(str(oggi.year))

        def update_period_inputs(*_):
            for widget in frame_period.winfo_children():
                widget.pack_forget()
            mode = mode_var.get()
            reset_btn = ttk.Button(frame_period, text="↺", style='Yellow.TButton', command=reset_period)

            if mode == "Giorno":
                day_combo.pack(side=tk.LEFT)
                month_combo.pack(side=tk.LEFT, padx=(4,8))
                year_combo.pack(side=tk.LEFT)
                reset_btn.pack(side=tk.LEFT, padx=(10, 0))
                update_days()
            elif mode == "Mese":
                month_combo.pack(side=tk.LEFT, padx=(0,8))
                year_combo.pack(side=tk.LEFT)
                reset_btn.pack(side=tk.LEFT, padx=(10, 0))
            elif mode == "Anno":
                year_combo_only.pack(side=tk.LEFT)
                reset_btn.pack(side=tk.LEFT, padx=(10, 0))
        mode_combo.bind("<<ComboboxSelected>>", update_period_inputs)
        update_period_inputs()

        frame_cat = ttk.Frame(popup)
        frame_cat.pack(padx=18, pady=12, fill=tk.X)
        ttk.Label(frame_cat, text="Categoria:").pack(side=tk.LEFT)
        def get_catlist():
            return ["Tutte le categorie"] + sorted(self.categorie)
        cat_var = tk.StringVar(value="Tutte le categorie")
        cat_combo = ttk.Combobox(frame_cat, values=get_catlist(), textvariable=cat_var, state="readonly", width=25)
        cat_combo.pack(side=tk.LEFT, padx=10)

        main_result_frame = ttk.Frame(popup)
        main_result_frame.pack(padx=18, fill=tk.BOTH, expand=True)
        text_result = tk.Text(main_result_frame, height=22, width=90, font=("Arial", 10), wrap='none')
        text_result.pack(fill=tk.BOTH, expand=True)
        frame_buttons = ttk.Frame(main_result_frame)
        frame_buttons.pack(fill=tk.X, pady=8)
        export_btn = ttk.Button(frame_buttons, text="💾 Esporta", style='Verde.TButton')
        export_btn.pack(side=tk.LEFT, padx=4)
    
        close_btn = ttk.Button(frame_buttons, text="❌ Chiudi", command=popup.destroy, style='Giallo.TButton')
        close_btn.pack(side=tk.RIGHT, padx=4)

        def aggiorna_cat_combo():
            cat_combo['values'] = get_catlist()
            if cat_var.get() not in cat_combo['values']:
                cat_var.set("Tutte le categorie")
        aggiorna_cat_combo()

        def mostra_dettagli(*_):
            cat = cat_var.get()
            mode = mode_var.get()
            result_lines = []
            today = datetime.date.today()

            def calcola_totali(entries):
                entrate = sum(e[2] for _, e in filtered if "entrata" in e[3].lower())
                uscite = sum(e[2] for _, e in filtered if "entrata" not in e[3].lower())
                return entrate, uscite, entrate - uscite

            filtered = []
            label_intestazione = ""

            if mode == "Giorno":
                try:
                    m = months.index(month_var.get()) + 1
                    d = int(day_var.get())
                    y = int(year_var.get())
                    giorno = datetime.date(y, m, d)
                except Exception:
                    giorno = today
                spese = self.spese.get(giorno, [])
                filtered = [(giorno, e) for e in spese if cat == "Tutte le categorie" or e[0] == cat]
                label_intestazione = f"{'Entrate/Uscite' if cat == 'Tutte le categorie' else 'Spese ' + cat} per il giorno {giorno.strftime('%d-%m-%Y')}"

            elif mode == "Mese":
                try:
                    m = months.index(month_var.get()) + 1
                    y = int(year_var.get())
                except Exception:
                    m = today.month
                    y = today.year
                for d, sp in self.spese.items():
                    if d.year == y and d.month == m:
                        for e in sp:
                            if cat == "Tutte le categorie" or e[0] == cat:
                                filtered.append((d, e))
                label_intestazione = f"{'Entrate/Uscite' if cat == 'Tutte le categorie' else 'Spese ' + cat} per {self.get_month_name(m)} {y}"

            elif mode == "Anno":
                try:
                    y = int(year_var.get())
                except Exception:
                    y = today.year
                for d, sp in self.spese.items():
                    if d.year == y:
                        for e in sp:
                            if cat == "Tutte le categorie" or e[0] == cat:
                                filtered.append((d, e))
                label_intestazione = f"{'Entrate/Uscite' if cat == 'Tutte le categorie' else 'Spese ' + cat} per l'anno {y}"

            elif mode == "Totale":
                for d, sp in self.spese.items():
                    for e in sp:
                        if cat == "Tutte le categorie" or e[0] == cat:
                            filtered.append((d, e))
                label_intestazione = f"{'Entrate/Uscite' if cat == 'Tutte le categorie' else 'Spese ' + cat} totali"

            text_result.configure(font=("Courier New", 10))
            result_lines.clear()

            if not filtered:
                result_lines.append(f"Nessuna spesa per '{cat}'.")
            else:
                result_lines.append("=" * 80)
                result_lines.append(label_intestazione)
                result_lines.append("-" * 80)
                result_lines.append(f"{'Data':<12}  {'Categoria':<20}  {'Descrizione':<15}  {'Importo':>10}")
                result_lines.append("-" * 80)

                for d, e in sorted(filtered, key=lambda x: x[0], reverse=True):
                    valore = abs(e[2])
                    categoria = e[0][:20] if len(e[0]) > 12 else e[0]
                    descrizione = e[1][:15] if len(e[1]) > 25 else e[1]
                    
                    result_lines.append(
                        f"{d.strftime('%d-%m-%Y'):<12}  {categoria:<20}  {descrizione:<15}  {valore:>9.2f} € ({e[3]})"
                    )

                result_lines.append("-" * 80)
                entrate, uscite, saldo = calcola_totali([e for _, e in filtered])
                result_lines.append(f"{'Totale entrate':<54}  {entrate:>9.2f} €")
                result_lines.append(f"{'Totale uscite':<54}  {uscite:>9.2f} €")
                result_lines.append(f"{'Saldo finale':<54}  {saldo:+9.2f} €")
                result_lines.append("=" * 80)

            text_result.delete("1.0", tk.END)
            text_result.insert("end", "\n".join(result_lines))

        def esporta_analisi():
            contenuto = text_result.get("1.0", tk.END).strip()
            if not contenuto:
                self.show_custom_warning("Esporta", "Nulla da esportare.")
                return
            preview = tk.Toplevel(popup)
            preview.title("Preview esportazione")
            preview.geometry("800x500")
            preview.transient(popup)
            preview.grab_set()
            preview.focus_set()
            tx = tk.Text(preview, font=("Courier new", 10), wrap="none")
            tx.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            contenuto_preview = "\n".join(" " + l for l in contenuto.splitlines())

            tx.insert(tk.END, contenuto_preview)
            tx.config(state="disabled")
            frm = ttk.Frame(preview)
            frm.pack(fill=tk.X, padx=10, pady=8)
            def do_save():
                now = datetime.date.today()
                default_filename = f"Analisi_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
                file = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("File txt", "*.txt")],
                    initialdir=EXPORT_FILES,
                    title="Esporta Analisi Categoria",
                    initialfile=default_filename,
                    confirmoverwrite=False,
                    parent=preview)
                if file:
                    if os.path.exists(file):
                        conferma = self.show_custom_askyesno(
                            "Sovrascrivere file?",
                            f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                        )
                        if not conferma:
                            return  

                    with open(file, "w", encoding="utf-8") as f:
                        f.write(contenuto_preview)
                        self.show_custom_warning("Esporta", f"Analisi esportata in {file}")
                    preview.destroy()
            ttk.Button(frm, text="💾 Salva", command=do_save, style="Verde.TButton").pack(side=tk.LEFT, padx=6)
            ttk.Button(frm, text="❌ Chiudi", command=preview.destroy, style="Giallo.TButton").pack(side=tk.RIGHT, padx=6)

            preview.lift()
            preview.attributes('-topmost', True)
            preview.after(100, lambda: preview.attributes('-topmost', False))
        
            preview.bind("<Escape>", lambda e: preview.destroy())
        
        export_btn.config(command=esporta_analisi)

        mode_var.trace_add("write", mostra_dettagli)
        month_var.trace_add("write", mostra_dettagli)
        year_var.trace_add("write", mostra_dettagli)
        day_var.trace_add("write", mostra_dettagli)
        cat_var.trace_add("write", mostra_dettagli)
    
        mostra_dettagli()

    def open_saldo_conto(self):
        def valida_saldo(valore):
            if len(valore) > 8:
                return False
            if valore == "":
                return True
            return valore.isdigit()
        popup = tk.Toplevel(self)
        popup.title("Saldo Conto Corrente")
        popup.geometry("480x450")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()
        popup.bind("<Escape>", lambda e: popup.destroy())
        saldo_data = {"saldo": 0.0, "data": datetime.date.today().strftime("%d-%m-%Y")}
        if os.path.exists(SALDO_FILE):
            try:
                with open(SALDO_FILE, "r", encoding="utf-8") as f:
                    db = json.load(f)
                saldo_data["saldo"] = db.get("saldo", 0.0)
                saldo_data["data"] = db.get("saldo_data", saldo_data["data"])
            except Exception:
                pass
        frame = ttk.Frame(popup)
        frame.pack(padx=28, pady=18, fill=tk.BOTH, expand=True)
        lastframe = ttk.LabelFrame(frame, text="Ultimo saldo inserito", padding=10)
        lastframe.pack(fill=tk.X, padx=0, pady=(0, 18))
        last_saldo_var = tk.StringVar(value=f"{saldo_data['saldo']:.2f}")
        last_data_var = tk.StringVar(value=saldo_data["data"])
        ttk.Label(lastframe, text="💰 Ultimo saldo:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=(0,8), pady=2)
        ttk.Entry(lastframe, textvariable=last_saldo_var, width=15, font=("Arial", 11), state="readonly").grid(row=0, column=1, padx=(0,8), pady=2)
        ttk.Label(lastframe, text="€", font=("Arial", 11)).grid(row=0, column=2, sticky="w", pady=2)
        ttk.Label(lastframe, text="📅 Data inserimento:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=(0,8), pady=2)
        ttk.Entry(lastframe, textvariable=last_data_var, width=12, font=("Arial", 11), state="readonly").grid(row=1, column=1, pady=2, sticky="w")
        btmframe = ttk.LabelFrame(frame, text="🔄 Aggiorna saldo bancario", padding=10)
        btmframe.pack(fill=tk.X, padx=0, pady=(0, 0))
        try:
            default_dt = datetime.datetime.strptime(saldo_data["data"], "%d-%m-%Y").date()
        except Exception:
            default_dt = datetime.date.today()
        anni_spese = set()
        anno_corrente = datetime.date.today().year
        if hasattr(self, 'spese') and self.spese:
            for giorno in self.spese.keys():
                if hasattr(giorno, "year"):
                    anni_spese.add(giorno.year)
        anni_spese.add(anno_corrente)
        if anni_spese:
            anni = sorted(list(anni_spese))
        else:
            anni = [anno_corrente - 1, anno_corrente]
        mesi = list(range(1, 13))
        giorni = list(range(1, 32))
        ttk.Label(btmframe, text="Data saldo:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=(0,8), pady=2)
        day_var = tk.StringVar(value=f"{default_dt.day:02d}")
        month_var = tk.StringVar(value=f"{default_dt.month:02d}")
        year_var = tk.StringVar(value=str(default_dt.year))
        ttk.Combobox(btmframe, textvariable=day_var, values=[f"{g:02d}" for g in giorni], width=4, state="readonly").grid(row=0, column=1, sticky="w", padx=(0,2))
        ttk.Combobox(btmframe, textvariable=month_var, values=[f"{m:02d}" for m in mesi], width=4, state="readonly").grid(row=0, column=2, sticky="w", padx=(0,2))
        ttk.Combobox(btmframe, textvariable=year_var, values=[str(a) for a in anni], width=6, state="readonly").grid(row=0, column=3, sticky="w", padx=(0,6))
        ttk.Button(
            btmframe,
            text="↺",
            style='Yellow.TButton',
            command=lambda: [
                day_var.set(f"{datetime.date.today().day:02d}"),
                month_var.set(f"{datetime.date.today().month:02d}"),
                year_var.set(str(datetime.date.today().year))
            ]
        ).grid(row=0, column=4)
        ttk.Label(btmframe, text="Nuovo saldo:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=(14,2))
        saldo_var = tk.StringVar()
        vcmd = (popup.register(valida_saldo), "%P")
        ttk.Entry(
            btmframe,
            textvariable=saldo_var,
            width=15,
            font=("Arial", 11),
            validate="key",
            validatecommand=vcmd
        ).grid(row=1, column=1, columnspan=2, sticky="w", padx=4, pady=(14,2))
        ttk.Label(btmframe, text="€", font=("Arial", 11)).grid(row=1, column=3, sticky="w", pady=(14,2))
        data_var = tk.StringVar()
        
        def aggiorna_data_var(*_):
            data_var.set(f"{day_var.get()}-{month_var.get()}-{year_var.get()}")
        day_var.trace_add("write", aggiorna_data_var)
        month_var.trace_add("write", aggiorna_data_var)
        year_var.trace_add("write", aggiorna_data_var)
        aggiorna_data_var()
        lbl_saldo_mese = ttk.Label(frame, text="", font=("Arial", 11))
        lbl_saldo_anno = ttk.Label(frame, text="", font=("Arial", 11))
        lbl_saldo_tot = ttk.Label(frame, text="", font=("Arial", 11, "bold"))
        lbl_saldo_mese.pack(anchor="w", pady=(20, 0))
        lbl_saldo_anno.pack(anchor="w")
        lbl_saldo_tot.pack(anchor="w", pady=(0, 12))
    
        def get_selected_date():
            try:
                return datetime.datetime.strptime(data_var.get(), "%d-%m-%Y").date()
            except Exception:
                return datetime.date.today()

        def calcola_saldo(filtro):
            try:
                saldo = float(last_saldo_var.get())
            except Exception:
                saldo = 0.0
            data_saldo = get_selected_date()
            mese = data_saldo.month
            anno = data_saldo.year
            saldo_mese = saldo
            saldo_anno = saldo
            saldo_totale = saldo
            for d in sorted(self.spese.keys()):
                if d < data_saldo:
                    continue
                for entry in self.spese[d]:
                    imp = entry[2]
                    tipo = entry[3]
                    if tipo == "Entrata":
                        saldo_totale += imp
                        if d.year == anno:
                            saldo_anno += imp
                            if d.month == mese:
                                saldo_mese += imp
                    else:
                        saldo_totale -= imp
                        if d.year == anno:
                            saldo_anno -= imp
                            if d.month == mese:
                                saldo_mese -= imp
            return {"mese": saldo_mese, "anno": saldo_anno, "totale": saldo_totale}[filtro]
    
        def aggiorna_saldi(*_):
            lbl_saldo_mese.config(text=f"Saldo nel mese: {calcola_saldo('mese'):.2f} €")
            lbl_saldo_anno.config(text=f"Saldo nell'anno: {calcola_saldo('anno'):.2f} €")
            lbl_saldo_tot.config(text=f"Saldo totale    : {calcola_saldo('totale'):.2f} €")
        data_var.trace_add("write", aggiorna_saldi)
        aggiorna_saldi()
    
        def custom_warning(msg, parent):
            win = tk.Toplevel(parent)
            win.title("Avviso")
            win.configure(bg="#ffffcc")
            win.resizable(False, False)
            win.grab_set()
            win.geometry("420x140")
            ttk.Label(win, text=msg, background="#ffffcc", font=("Arial", 10)).pack(padx=20, pady=20)
            ttk.Button(win, text="OK", command=win.destroy, style='Verde.TButton').pack(pady=(0,16))
            win.transient(parent)
            win.lift()
            win.focus_force()
            win.attributes('-topmost', True)
            win.after(200, lambda: win.attributes('-topmost', False))
    
        def salva_saldo():
            try:
                nuovo_saldo = float(saldo_var.get().replace(",", "."))
                nuova_data = data_var.get()
                last_saldo_var.set(f"{nuovo_saldo:.2f}")
                last_data_var.set(nuova_data)
                db = {}
                if os.path.exists(SALDO_FILE):
                    try:
                        with open(SALDO_FILE, "r", encoding="utf-8") as f:
                            db = json.load(f)
                    except json.JSONDecodeError:
                        db = {}
                db["saldo"] = nuovo_saldo
                db["saldo_data"] = nuova_data
                with open(SALDO_FILE, "w", encoding="utf-8") as f:
                    json.dump(db, f, indent=2, ensure_ascii=False)
                saldo_var.set("")
                aggiorna_saldi()
                custom_warning("✅ Saldo aggiornato correttamente.", popup)
            except ValueError:
                self.show_custom_warning("Salvataggio", "❌ Inserisci un numero valido.")
                
        def esporta():
            sm = calcola_saldo("mese")
            sa = calcola_saldo("anno")
            st = calcola_saldo("totale")
            lines = [
                f"Saldo inserito il {last_data_var.get()}: {last_saldo_var.get()} €",
                f"Saldo nel mese: {sm:.2f} €",
                f"Saldo nell'anno: {sa:.2f} €",
                f"Saldo totale: {st:.2f} €",
            ]
            preview = tk.Toplevel(popup)
            preview.title("Esporta saldo")
            preview.geometry("420x200")
            preview.transient(popup)
            preview.grab_set()
            preview.bind("<Escape>", lambda e: preview.destroy())
    
            txt = tk.Text(preview, font=("Arial", 10), wrap="word", height=6)
            txt.insert("1.0", "\n".join(lines))
            txt.configure(state="disabled")
            txt.pack(fill="both", expand=True, padx=10, pady=10)
    
            def do_save():
                default_filename = f"Saldo_Export_{datetime.date.today().strftime('%d-%m-%Y')}.txt"
                path = filedialog.asksaveasfilename(
                    initialfile= default_filename,
                    initialdir=EXPORT_FILES,
                    defaultextension=".txt",
                    title="Salva Saldo",
                    confirmoverwrite=False,
                    filetypes=[("File di testo", "*.txt")],
                    parent=preview
                )
                if path:
                    if os.path.exists(path):
                        conferma = self.show_custom_askyesno(
                            "Sovrascrivere file?",
                            f"Il file '{os.path.basename(path)}' \nesiste già. Vuoi sovrascriverlo?"
                        )
                        if not conferma:
                            return  
                    with open(path, "w", encoding="utf-8") as f:
                        f.write("\n".join(lines))
                    custom_warning("✅ Esportazione completata.", preview)
                    preview.destroy()
            btns = ttk.Frame(preview)
            btns.pack(pady=10)
            ttk.Button(btns, text="💾 Salva", command=do_save, style="Verde.TButton").pack(side="left", padx=6)
            ttk.Button(btns, text="❌ Chiudi", command=preview.destroy, style="Giallo.TButton").pack(side="right", padx=6)
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=(12, 10))
        style = ttk.Style()
        ttk.Button(btn_frame, text="💾 Salva saldo", command=salva_saldo, style="Verde.TButton").pack(side="left", padx=6)
        ttk.Button(btn_frame, text="📄 Preview/Esporta", command=esporta, style="Arancio.TButton").pack(side="left", padx=6)
        ttk.Button(btn_frame, text="❌ Chiudi", command=popup.destroy, style="Giallo.TButton").pack(side="right", padx=6)
            
    def carica_saldo(self):
        self.saldo_iniziale = 0.0
        self.saldo_data = datetime.date.today()
        self.saldo_attuale = 0.0
        self.saldo_previsto = 0.0
        if os.path.exists(SALDO_FILE):
            try:
                with open(SALDO_FILE, "r", encoding="utf-8") as f:
                    saldo_db = json.load(f)
                self.saldo_iniziale = float(saldo_db.get("saldo", 0.0))
                self.saldo_data = datetime.datetime.strptime(
                    saldo_db.get("saldo_data", self.saldo_data.strftime("%d-%m-%Y")),
                    "%d-%m-%Y"
                ).date()
            except Exception as e:
                print("Errore caricamento saldo:", e)
        self.saldo_attuale = self.saldo_iniziale
        for d in sorted(self.spese.keys()):
            if d < self.saldo_data:
                continue
            for entry in self.spese[d]:
                imp = entry[2]
                tipo = entry[3]
                self.saldo_attuale += imp if tipo == "Entrata" else -imp
        oggi = datetime.date.today()
        fine_mese = datetime.date(oggi.year, oggi.month, 28)
        self.saldo_previsto = self.saldo_attuale
        for d in sorted(self.spese.keys()):
            if d <= oggi or d > fine_mese:
                continue
            for entry in self.spese[d]:
                imp = entry[2]
                tipo = entry[3]
                self.saldo_previsto += imp if tipo == "Entrata" else -imp

    def show_tooltip_saldo(self, event):
        self.carica_saldo()
        if hasattr(self, "tooltip_label"):
            self.tooltip_label.destroy()
        tooltip_text = (
            "💼 Saldo conto corrente\n\n"
            f"{'Saldo iniziale:':<18} € {self.saldo_iniziale:.2f}\n"
            f"{'Data saldo:':<18}   {self.saldo_data.strftime('%d-%m-%Y')}\n"
            f"{'Saldo attuale:':<18} € {self.saldo_attuale:.2f}\n"
            f"{'Saldo previsto:':<18} € {self.saldo_previsto:.2f}"
        )
        self.tooltip_label = tk.Label(
            self,
            text=tooltip_text,
            bg="lightyellow",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9),
            justify="left",
            wraplength=220
        )
        self.update_idletasks()
        x = self.winfo_width() - 250
        y = 20
        self.tooltip_label.place(x=x, y=y)

    def hide_tooltip_saldo(self,event):
        if hasattr(self, "tooltip_label"):
            self.tooltip_label.destroy()
            del self.tooltip_label
            
    def goto_today(self):
        today = datetime.date.today()
        if hasattr(self, "cal"):
            self.cal.selection_set(today)
            self.cal._sel_date = today
        self.stats_refdate = today
        mesi = [
            "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
        ]
        self.estratto_month_var.set(mesi[today.month - 1])
        self.estratto_year_var.set(str(today.year))
        self.set_stats_mode("giorno")
        self.after_idle(self.update_stats)
        self.update_totalizzatore_anno_corrente()
        self.update_totalizzatore_mese_corrente()
        self.update_spese_mese_corrente()
        self.stats_label.config(
            text=f"Riepilogo Giornaliero - {today.strftime('%d-%m-%Y')}", foreground="purple",
    font=("Arial", 10, "bold"))

    def open_compare_window(self):
        today = datetime.date.today()
        mese_oggi = f"{today.month:02d}"
        anno_oggi = str(today.year)
        compare_by_year = tk.BooleanVar(value=False)
        mostra_future_var = tk.BooleanVar(value=True)

        def parse_date(d):
            if isinstance(d, datetime.date):
                return d
            try:
                if len(d.split("-")[0]) == 4:
                    return datetime.datetime.strptime(d, "%Y-%m-%d").date()
                else:
                    return datetime.datetime.strptime(d, "%d-%m-%Y").date()
            except Exception:
                return None
    
        def get_rows(mese, anno, per_anno=False):
            rows = []
            oggi = datetime.date.today()
            for d_raw in sorted(self.spese):
                d = parse_date(d_raw)
                if not d:
                    continue
                if not mostra_future_var.get() and d > oggi:
                    continue
                if (per_anno and d.year == anno) or \
                   (not per_anno and d.month == mese and d.year == anno):
                    for voce in self.spese[d_raw]:
                        try:
                            
                            if len(voce) >= 4:
                                
                                if len(voce) == 5:
                                    cat, desc, imp, tipo, _ = voce 
                                else: 
                                    cat, desc, imp, tipo = voce

                                data_pagamento = d.strftime("%d-%m-%Y")
                                entrata = imp if tipo == "Entrata" else 0
                                uscita = imp if tipo == "Uscita" else 0
                            
                                rows.append((cat, data_pagamento, entrata, uscita))
                            else:
                                print(f"Skipping malformed row: {voce}")
                        except Exception as e:
                            print(f"Error processing row: {e} - Data was: {voce}")
                            continue
            return rows

        popup = tk.Toplevel(self)
        popup.withdraw()
        self.update_idletasks()
        main_x = self.winfo_rootx()
        main_y = self.winfo_rooty()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        popup_width = 1030   
        popup_height = 560
        center_x = main_x + (main_width // 2) - (popup_width // 2)
        center_y = main_y + (main_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup.transient(self)
        #popup.grab_set()
        popup.title("Confronta mesi/anni per categoria")
        popup.deiconify()
        popup.bind("<Escape>", lambda e: popup.destroy())

        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        anni_presenti_nel_db = set()
        for d_raw in self.spese.keys():
            d = parse_date(d_raw)
            if d:
                anni_presenti_nel_db.add(d.year)
        anni_correnti_e_db = sorted(list(anni_presenti_nel_db.union({today.year, today.year - 1, today.year + 1})), reverse=True) 
        anni_spese = {pd.year for d in self.spese.keys() if (pd := parse_date(d))}
        anno_corrente = today.year
        anni = anni_correnti_e_db 
        mesi = [f"{i:02d}" for i in range(1, 13)]

        mode_frame = ttk.Frame(frame)
        mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        tk.Label(mode_frame, text="Modalità confronto:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="Mese", variable=compare_by_year, value=False, command=lambda: update_tables()).pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Anno", variable=compare_by_year, value=True, command=lambda: update_tables()).pack(side=tk.LEFT)
        tk.Checkbutton(mode_frame, text="Includi movimenti futuri nei totali", bg="yellow", activebackground="gold", variable=mostra_future_var).pack(side=tk.LEFT, padx=(30, 0))

        left = ttk.Frame(frame)
        left.grid(row=2, column=0, sticky="nswe", padx=(0, 16))
        left_select_frame = ttk.Frame(frame)
        left_select_frame.grid(row=1, column=0, sticky="ew", padx=(0, 16), pady=(0, 6))
        tk.Label(left_select_frame, text="Mese/Anno 1", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        left_mese = tk.StringVar(value=mese_oggi)
        left_anno = tk.StringVar(value=anno_oggi)
        cb_lm = ttk.Combobox(left_select_frame, textvariable=left_mese, values=mesi, width=4, state="readonly", font=("Arial", 10))
        cb_la = ttk.Combobox(left_select_frame, textvariable=left_anno, values=[str(a) for a in anni], width=7, state="readonly", font=("Arial", 10))
        cb_lm.pack(side="left", padx=(0, 3))
        cb_la.pack(side="left")
        
        def reset_left():
            left_mese.set(mese_oggi)
            left_anno.set(anno_oggi)
        ttk.Button(left_select_frame, text="↺", command=reset_left, style='Yellow.TButton').pack(side="right", padx=7)
        left_tree = ttk.Treeview(left, columns=("Categoria", "Data", "Entrata", "Uscita"), show="headings", height=18)

        style = ttk.Style()

        left_tree.configure(style="Big.Treeview")
        left_tree.tag_configure('entrata', foreground='green')
        left_tree.tag_configure('uscita', foreground='red')

        for col, w, anchor in [("Categoria", 180, "center"), ("Data", 110, "center"), ("Entrata", 100, "center"), ("Uscita", 100, "center")]:
            left_tree.heading(col, text=col, anchor=anchor, command=lambda _col=col: treeview_sort_column(left_tree, _col, False))
            left_tree.column(col, width=w, anchor=anchor, stretch=False)
        left_tree.pack(fill=tk.BOTH, expand=True)

        left_diff_frame = ttk.Frame(left)
        left_diff_frame.pack(pady=(4, 0), fill=tk.X, expand=True)
        
        tk.Label(left_diff_frame, text="Entrate:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        left_total_ent_lbl = tk.Label(left_diff_frame, text="", font=("Arial", 10, "bold"))
        left_total_ent_lbl.pack(side=tk.LEFT, padx=(2, 10))

        tk.Label(left_diff_frame, text="Uscite:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        left_total_usc_lbl = tk.Label(left_diff_frame, text="", font=("Arial", 10, "bold"))
        left_total_usc_lbl.pack(side=tk.LEFT, padx=(2, 10))

        tk.Label(left_diff_frame, text="Differenza:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        left_diff_val_lbl = tk.Label(left_diff_frame, text="", font=("Arial", 10, "bold"))
        left_diff_val_lbl.pack(side=tk.LEFT, padx=(2, 0))

        right = ttk.Frame(frame)
        right.grid(row=2, column=1, sticky="nswe")
        right_select_frame = ttk.Frame(frame)
        right_select_frame.grid(row=1, column=1, sticky="ew", pady=(0, 6))
        tk.Label(right_select_frame, text="Mese/Anno 2", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        right_mese = tk.StringVar(value=mese_oggi)
        right_anno = tk.StringVar(value=anno_oggi)
        cb_rm = ttk.Combobox(right_select_frame, textvariable=right_mese, values=mesi, width=4, state="readonly", font=("Arial", 10))
        cb_ra = ttk.Combobox(right_select_frame, textvariable=right_anno, values=[str(a) for a in anni], width=7, state="readonly", font=("Arial", 10))
        cb_rm.pack(side="left", padx=(0, 3))
        cb_ra.pack(side="left")
        
        def reset_right():
            right_mese.set(mese_oggi)
            right_anno.set(anno_oggi)
        ttk.Button(right_select_frame, text="↺", command=reset_right, style='Yellow.TButton').pack(side="right", padx=7)
        right_tree = ttk.Treeview(right, columns=("Categoria", "Data", "Entrata", "Uscita"), show="headings", height=18)
        right_tree.configure(style="Big.Treeview")
        right_tree.tag_configure('entrata', foreground='green')
        right_tree.tag_configure('uscita', foreground='red')

        for col, w, anchor in [("Categoria", 180, "center"), ("Data", 110, "center"), ("Entrata", 100, "center"), ("Uscita", 100, "center")]:
            right_tree.heading(col, text=col, anchor=anchor, command=lambda _col=col: treeview_sort_column(right_tree, _col, False))
            right_tree.column(col, width=w, anchor=anchor, stretch=False)
        right_tree.pack(fill=tk.BOTH, expand=True)

        right_diff_frame = ttk.Frame(right)
        right_diff_frame.pack(pady=(4, 0), fill=tk.X, expand=True)

        tk.Label(right_diff_frame, text="Entrate:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        right_total_ent_lbl = tk.Label(right_diff_frame, text="", font=("Arial", 10, "bold"))
        right_total_ent_lbl.pack(side=tk.LEFT, padx=(2, 10))

        tk.Label(right_diff_frame, text="Uscite:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        right_total_usc_lbl = tk.Label(right_diff_frame, text="", font=("Arial", 10, "bold"))
        right_total_usc_lbl.pack(side=tk.LEFT, padx=(2, 10))

        tk.Label(right_diff_frame, text="Differenza:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        right_diff_val_lbl = tk.Label(right_diff_frame, text="", font=("Arial", 10, "bold"))
        right_diff_val_lbl.pack(side=tk.LEFT, padx=(2, 0))
        
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            if col == "Data":
                l.sort(key=lambda t: datetime.datetime.strptime(t[0], "%d-%m-%Y"), reverse=reverse)
            else:
                try:
                    l.sort(key=lambda t: float(t[0].replace('€', '').replace('.', '').replace(',', '.').strip()), reverse=reverse)
                except (ValueError, IndexError):
                    l.sort(key=lambda t: t[0].lower(), reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

        def update_month_visibility():
            is_annual = compare_by_year.get()
            for cb in [cb_lm, cb_rm]:
                if is_annual and cb.winfo_ismapped():
                    cb.pack_forget()
                elif not is_annual and not cb.winfo_ismapped():
                    cb.pack(side="left", padx=(0, 3))
                    
        def update_tables():
            update_month_visibility()
            per_anno = compare_by_year.get()
            a1, a2 = int(left_anno.get()), int(right_anno.get())
            m1 = int(left_mese.get()) if not per_anno else 1
            m2 = int(right_mese.get()) if not per_anno else 1

            rows1, rows2 = get_rows(m1, a1, per_anno), get_rows(m2, a2, per_anno)
            
            left_tree.delete(*left_tree.get_children())
            right_tree.delete(*right_tree.get_children())

            tot_ent1, tot_usc1 = 0, 0
            for cat, data, ent, usc in sorted(rows1, key=lambda x: x[0].lower()):
                tag = 'entrata' if ent > 0 else ('uscita' if usc > 0 else '')
                left_tree.insert("", "end", values=(cat, data, f"{ent:,.2f} €", f"{usc:,.2f} €"), tags=(tag,))
                tot_ent1, tot_usc1 = tot_ent1 + ent, tot_usc1 + usc
            
            diff1 = tot_ent1 - tot_usc1
            
            left_total_ent_lbl.config(text=f"{tot_ent1:,.2f} €", fg="green")
            left_total_usc_lbl.config(text=f"{tot_usc1:,.2f} €", fg="red")
            left_diff_val_lbl.config(
                text=f"{diff1:,.2f} €",
                fg="green" if diff1 >= 0 else "red"
            )

            tot_ent2, tot_usc2 = 0, 0
            for cat, data, ent, usc in sorted(rows2, key=lambda x: x[0].lower()):
                tag = 'entrata' if ent > 0 else ('uscita' if usc > 0 else '')
                right_tree.insert("", "end", values=(cat, data, f"{ent:,.2f} €", f"{usc:,.2f} €"), tags=(tag,))
                tot_ent2, tot_usc2 = tot_ent2 + ent, tot_usc2 + usc
                
            diff2 = tot_ent2 - tot_usc2

            right_total_ent_lbl.config(text=f"{tot_ent2:,.2f} €", fg="green")
            right_total_usc_lbl.config(text=f"{tot_usc2:,.2f} €", fg="red")
            right_diff_val_lbl.config(
                text=f"{diff2:,.2f} €",
                fg="green" if diff2 >= 0 else "red"
            )

        for var in [left_mese, left_anno, right_mese, right_anno, compare_by_year, mostra_future_var]:
            var.trace_add("write", lambda *a: update_tables())

        update_tables()

        def do_preview_export():
            per_anno = compare_by_year.get()
            a1, a2 = int(left_anno.get()), int(right_anno.get())
            m1 = int(left_mese.get()) if not per_anno else 1
            m2 = int(right_mese.get()) if not per_anno else 1
            rows1, rows2 = get_rows(m1, a1, per_anno), get_rows(m2, a2, per_anno)
            label1 = f"{m1:02d}/{str(a1)[-2:]}" if not per_anno else str(a1)
            label2 = f"{m2:02d}/{str(a2)[-2:]}" if not per_anno else str(a2)
            lines = [f"Confronto tra {label1} e {label2}\n"]
            lines.append(f"{'Categoria':<20} {'Data':<12} {'Entrate ' + label1:>12} {'Uscite ' + label1:>12} | {'Entrate ' + label2:>12} {'Uscite ' + label2:>12} | {'Δ Entrate':>12} {'Δ Uscite':>12}")
            lines.append("-" * 130)
            data1 = {}
            for cat, _, ent, usc in rows1:
                prev_ent, prev_usc = data1.get(cat, (0.0, 0.0))
                data1[cat] = (prev_ent + ent, prev_usc + usc)
            data2 = {}
            for cat, _, ent, usc in rows2:
                prev_ent, prev_usc = data2.get(cat, (0.0, 0.0))
                data2[cat] = (prev_ent + ent, prev_usc + usc)
            tutte_le_categorie = sorted(set(data1.keys()) | set(data2.keys()))
            for cat in tutte_le_categorie:
                ent1, usc1 = data1.get(cat, (0.0, 0.0))
                ent2, usc2 = data2.get(cat, (0.0, 0.0))
                diff_ent, diff_usc = ent2 - ent1, usc2 - usc1
                lines.append(f"{cat:<20.20} {'':<12} {ent1:12,.2f} {usc1:12,.2f} | {ent2:12,.2f} {usc2:12,.2f} | {diff_ent:12,.2f} {diff_usc:12,.2f}")
            tot_ent1, tot_usc1 = sum(v[0] for v in data1.values()), sum(v[1] for v in data1.values())
            diff1 = tot_ent1 - tot_usc1
            tot_ent2, tot_usc2 = sum(v[0] for v in data2.values()), sum(v[1] for v in data2.values())
            diff2 = tot_ent2 - tot_usc2
            diff_ent_tot, diff_usc_tot = tot_ent2 - tot_ent1, tot_usc2 - tot_usc1
            lines.append("-" * 130)
            lines.append(f"{'Totali':<20} {'':<12}{tot_ent1:12,.2f} {tot_usc1:12,.2f} | {tot_ent2:12,.2f} {tot_usc2:12,.2f} | {diff_ent_tot:12,.2f} {diff_usc_tot:12,.2f}")
            lines.append(f"{'Differenza':<33}{diff1:12,.2f}{'':15}{diff2:12,.2f}")
            text = "\n".join(lines)
            prev = tk.Toplevel(popup)
            prev.title("Preview/Esporta confronto")
            prev.geometry("1100x580")
            prev.transient(popup)
            #prev.resizable(False, False)
            prev.bind("<Escape>", lambda e: prev.destroy())
            t = tk.Text(prev, font=("Courier New", 10), wrap="none")
            t.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
            t.insert(tk.END, text)
            t.config(state="disabled")
            def do_save():
                now = datetime.date.today()
                default_filename = f"Confronto_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
                file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("File txt", "*.txt")], initialdir=EXPORT_FILES, initialfile=default_filename, title="Esporta confronto", confirmoverwrite=False, parent=prev)
                if file:
                    if os.path.exists(file) and not self.show_custom_askyesno("Sovrascrivere file?", f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"):
                        return
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(text)
                    if hasattr(self, "show_custom_warning"):
                        self.show_custom_warning("Esportazione completata", f"Tabella confronti esportata in:\n{file}")
            frm = ttk.Frame(prev)
            frm.pack(fill=tk.X, padx=10, pady=8)
            ttk.Button(frm, text="💾 Salva", command=do_save, style="Verde.TButton").pack(side=tk.LEFT, padx=6)
            ttk.Button(frm, text="❌ Chiudi", command=prev.destroy, style="Giallo.TButton").pack(side=tk.RIGHT, padx=6)
            prev.lift()
            prev.focus_force()
            prev.attributes('-topmost', True)
            prev.after(100, lambda: prev.attributes('-topmost', False))

        btnframe = ttk.Frame(popup)
        btnframe.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 7))
        ttk.Button(btnframe, text="📄 Preview/Esporta", command=do_preview_export, style="Verde.TButton").pack(side=tk.LEFT, padx=8)
        ttk.Button(btnframe, text="❌ Chiudi", command=popup.destroy, style="Giallo.TButton").pack(side=tk.RIGHT, padx=8)

    def scadenze_mese(self):
        def ordina_colonna(treeview, col, reverse):
            def converti(valore):
                if col in ("data", "scadenza"):
                    try:
                        return datetime.datetime.strptime(valore, "%d-%m-%Y")
                    except:
                        return datetime.datetime.max
                elif col == "importo":
                    try:
                        return float(valore.replace("€", "").replace(".", "").replace(",", ".").strip())
                    except:
                        return 0
                else:
                    return valore.lower() if isinstance(valore, str) else valore

            dati = [(treeview.set(k, col), k) for k in treeview.get_children("")]
            dati.sort(key=lambda t: converti(t[0]), reverse=reverse)

            for index, (val, k) in enumerate(dati):
                treeview.move(k, "", index)

            treeview.heading(col, command=(lambda c=col: lambda: ordina_colonna(treeview, c, not reverse))())

        oggi = datetime.date.today()
        mese_corrente = oggi.month
        anno_corrente = oggi.year

        mesi_italiani = [
            "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
        ]
        mese_nome = mesi_italiani[mese_corrente - 1]

        popup_mensile = tk.Toplevel(self)
        popup_mensile.title(f"Scadenze di {mese_nome} {anno_corrente}")
        popup_mensile.geometry("1000x420")
        popup_mensile.transient(self)
        popup_mensile.focus_force()
        popup_mensile.resizable(False, False)
        popup_mensile.bind("<Escape>", lambda e: popup_mensile.destroy())

        colonne = ("data", "categoria", "descrizione", "importo", "tipo_voce", "scadenza", "pagato", "progressione")
        tree_mensile = ttk.Treeview(popup_mensile, columns=colonne, show="headings")
        tree_mensile.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        tree_mensile.bind("<Double-1>", self.on_scadenza_doppio_click)

        for col in colonne:
            tree_mensile.heading(col, text=col.capitalize(), command=(lambda c=col: lambda: ordina_colonna(tree_mensile, c, False))())

        tree_mensile.column("data", width=80, anchor="center", stretch=False)
        tree_mensile.column("categoria", width=180, anchor="center", stretch=False)
        tree_mensile.column("descrizione", width=307, anchor="w", stretch=False)
        tree_mensile.column("importo", width=100, anchor="e", stretch=False)
        tree_mensile.column("tipo_voce", width=80, anchor="center", stretch=False)
        tree_mensile.column("scadenza", width=80, anchor="center", stretch=False)
        tree_mensile.column("pagato", width=60, anchor="center", stretch=False)
        tree_mensile.column("progressione", width=90, anchor="center", stretch=False)

        tree_mensile.tag_configure("verde", foreground="darkgreen")
        tree_mensile.tag_configure("rosso", foreground="darkred")
        tree_mensile.tag_configure("grigio", foreground="gray")

        for item_id, dati in self.ricorrenze.items():
            try:
                ric_type = dati.get("tipo", "").lower()
                n = dati.get("n", 0)
                data_inizio = datetime.datetime.strptime(dati.get("data_inizio", ""), "%d-%m-%Y").date()
                categoria = dati.get("cat", "N/D")
                descrizione_base = dati.get("desc", "—")
                tipo_voce = dati.get("tipo_voce", "N/D")
                importo_base = float(str(dati.get("imp", "0")).replace(",", "."))

                date_nel_mese = []
                for i in range(n):
                    if ric_type == "ogni mese":
                        mese = (data_inizio.month - 1 + i) % 12 + 1
                        anno = data_inizio.year + (data_inizio.month - 1 + i) // 12
                        giorno = min(
                            data_inizio.day,
                            [31, 29 if anno % 4 == 0 and (anno % 100 != 0 or anno % 400 == 0) else 28,
                             31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mese - 1]
                        )
                        data_movimento = datetime.date(anno, mese, giorno)
                    elif ric_type == "ogni anno":
                        data_movimento = data_inizio.replace(year=data_inizio.year + i)
                    else:
                        data_movimento = data_inizio + datetime.timedelta(days=i)

                    if data_movimento.month == mese_corrente and data_movimento.year == anno_corrente:
                        date_nel_mese.append((i + 1, data_movimento))

                for indice, data_movimento in date_nel_mese:
                    voce_trovata = False
                    importo_effettivo = importo_base

                    if data_movimento in self.spese:
                        for voce in self.spese[data_movimento]:
                            if len(voce) == 5 and voce[4] == item_id:
                                importo_effettivo = voce[2]
                                voce_trovata = True
                                break

                    valore_importo = f"{importo_effettivo:,.2f} €" if voce_trovata else "—"
                    pagato = "✔️" if data_movimento <= oggi and voce_trovata else "❌"
                    progressione = f"{indice}/{n}"
                    descrizione = descrizione_base
                    tag = "rosso" if tipo_voce == "Uscita" else "verde" if voce_trovata else "grigio"
                    data_scadenza = date_nel_mese[-1][1].strftime("%d-%m-%Y") if date_nel_mese else "N/D"

                    tree_mensile.insert(
                        "",
                        "end",
                        values=(
                            data_movimento.strftime("%d-%m-%Y"),
                            categoria,
                            descrizione,
                            valore_importo,
                            tipo_voce,
                            data_scadenza,
                            pagato,
                            progressione
                        ),
                        tags=(tag,)
                    )

            except Exception as e:
                print(f"Errore nella ricorrenza con ID {item_id}: {e}")
                continue

        fine_mese = datetime.date(anno_corrente, mese_corrente, 28)
        while True:
            try:
                fine_mese = fine_mese.replace(day=fine_mese.day + 1)
            except ValueError:
                break

        for data_voce in sorted(self.spese.keys()):
            if oggi <= data_voce <= fine_mese:
                for voce in self.spese[data_voce]:
                    if len(voce) < 5 or voce[4] not in self.ricorrenze:
                        try:
                            categoria, descrizione, importo, tipo_voce = voce[:4]
                            valore_importo = f"{importo:,.2f} €"
                            pagato = "✔️" if data_voce <= oggi else "❌"
                            progressione = "—"
                            data_scadenza = data_voce.strftime("%d-%m-%Y")
                            tag = "rosso" if tipo_voce == "Uscita" else "verde"

                            tree_mensile.insert(
                                "",
                                "end",
                                values=(
                                    data_voce.strftime("%d-%m-%Y"),
                                    categoria,
                                    descrizione,
                                    valore_importo,
                                    tipo_voce,
                                    data_scadenza,
                                    pagato,
                                    progressione
                                ),
                                tags=(tag,)
                            )
                        except Exception as e:
                            print(f"Errore nella voce normale del {data_voce}: {e}")
                            continue

        ordina_colonna(tree_mensile, "data", False)

        button_frame = ttk.Frame(popup_mensile)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="🔄 Calcola Mancanti", command=self.calcola_mancanti, style='Verde.TButton').pack(side="left", padx=20, pady=5)
        ttk.Button(button_frame, text="❌ Chiudi", command=popup_mensile.destroy, style='Giallo.TButton').pack(side="right", padx=20, pady=5)
 
    def on_scadenza_doppio_click(self, event):
        tree = event.widget
        item_id = tree.focus()
        if not item_id:
            return
        valori = tree.item(item_id, "values")
        if not valori or len(valori) < 1:
            return
        data_str = valori[0]  
        try:
            giorno = datetime.datetime.strptime(data_str, "%d-%m-%Y").date()
        except Exception:
            return
        self.set_stats_mode("giorno")
        if hasattr(self, "cal"):
            self.cal.selection_set(giorno)
            self.cal._sel_date = giorno
            self.stats_refdate = giorno

        self.update_stats()
        self.estratto_month_var.set(f"{giorno.month:02d}")
        self.estratto_year_var.set(str(giorno.year))
        self.stats_label.config(text=f"Riepilogo Giornaliero - {giorno.strftime('%d-%m-%Y')}", foreground="purple",
    font=("Arial", 10, "bold"))

    def aggiorna(self, url, nome_file):
        try:
            
            if os.path.exists(nome_file):
                nome_backup = f"{nome_file}.bak"
                try:
                    shutil.copy2(nome_file, nome_backup)
                    print(f"Backup creato: {nome_backup}")
                except Exception as backup_err:
                    print(f"Errore durante la creazione del backup: {backup_err}")
                    self.show_custom_warning("Attenzione", "⚠️ Impossibile creare il backup. Aggiornamento annullato.")
                    return

            
            urllib.request.urlretrieve(url, nome_file)
            print(f"Download completato! {nome_file} è stato aggiornato.")
            
            if self.show_custom_askyesno(
                "Conferma chiusura",
                "✅ L'aggiornamento è stato eseguito correttamente!\n\n🔒 Vuoi chiudere il programma adesso?"
            ):
                if APRI_BROWSER:
                    webbrowser.open(URL_QST) #Questionario
                    APRI_BROWSER = False

                self.save_db()
                self._on_close_lock()
                self.destroy()
            return

        except Exception as e:
            print(f"Errore durante il download: {str(e)}")
            self.show_custom_warning("Attenzione", "❌ Aggiornamento NON completato ! \n\n Sembra ci sia stato un problema. 😕")
            return
 
    def calcolo_mutuo_prestito(self):
        def popola_piano(tree_widget, capitale_iniziale, anni, mesi, rata_base, spese_mensili, tasso_mensile, title_label, ammortamento_extra=0):
            if capitale_iniziale is None or anni is None or mesi is None:
                for row in tree_widget.get_children():
                    tree_widget.delete(row)
                title_label.config(text="Nessun dato disponibile")
                return
            for row in tree_widget.get_children():
                tree_widget.delete(row)
            debito_res = capitale_iniziale
            if ammortamento_extra > 0:
                debito_res -= ammortamento_extra
            capitale_res_dopo_extra = debito_res
            try:
                if tasso_mensile > 0:
                    rata_base_nuova = capitale_res_dopo_extra * (tasso_mensile * (1 + tasso_mensile) ** mesi) / ((1 + tasso_mensile) ** mesi - 1)
                else:
                    rata_base_nuova = capitale_res_dopo_extra / mesi
            except (ZeroDivisionError, OverflowError):
                rata_base_nuova = 0

            totale_capitale = ammortamento_extra
            totale_interessi = 0
            for mese in range(1, mesi + 1):
                interessi_rata = debito_res * tasso_mensile
                capitale_rata = rata_base_nuova - interessi_rata
                debito_res -= capitale_rata
                totale_capitale += capitale_rata
                totale_interessi += interessi_rata
                tree_widget.insert("", "end", values=(
                    mese,
                    f"{rata_base_nuova + spese_mensili:,.2f} €",
                    f"{capitale_rata:,.2f} €",
                    f"{interessi_rata:,.2f} €",
                    f"{debito_res if debito_res > 0.005 else 0.0:,.2f} €"
                ))
            totale_rata_pagata = totale_capitale + totale_interessi + (spese_mensili * mesi)
            riepilogo_text = (
                f"Capitale: {capitale_iniziale:,.2f} €\n"
                f"Durata: {anni} anni ({mesi} mesi)\n"
                f"Tasso: {tasso_mensile * 100 * 12:,.2f} %\n"
                f"Ammortamento Extra: {ammortamento_extra:,.2f} €\n"
                f"Importo Totale Restituito: {totale_rata_pagata:,.2f} €\n"
                f"Interessi Totali: {totale_interessi:,.2f} €"
            )
            title_label.config(text=riepilogo_text, wraplength=1000)
            tree_widget.insert("", "end", values=("TOTALE", f"{totale_rata_pagata:,.2f} €", f"{totale_capitale:,.2f} €", f"{totale_interessi:,.2f} €", "-"), tags=('total_row',))
            tree_widget.tag_configure('total_row', font=('Arial', 10, 'bold'))

        def crea_tab_piano_ammortamento(notebook_widget, title):
            frame = ttk.Frame(notebook_widget, padding=10)
            notebook_widget.add(frame, text=title)
            title_label = ttk.Label(frame, text="Nessun dato disponibile", font=("Arial", 9, "bold"))
            title_label.pack(pady=10, fill=tk.X)
            tree_frame = ttk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            tree = ttk.Treeview(tree_frame, columns=("Rata", "Rata Mensile", "Quota Capitale", "Quota Interessi", "Debito Residuo"), show="headings")
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)
            tree.heading("Rata", text="Rata")
            tree.heading("Rata Mensile", text="Rata Mensile")
            tree.heading("Quota Capitale", text="Quota Capitale")
            tree.heading("Quota Interessi", text="Quota Interessi")
            tree.heading("Debito Residuo", text="Debito Residuo")            
            tree.column("Rata", width=50, anchor="center")
            tree.column("Rata Mensile", width=120, anchor="center")
            tree.column("Quota Capitale", width=120, anchor="center")
            tree.column("Quota Interessi", width=120, anchor="center")
            tree.column("Debito Residuo", width=120, anchor="center")            
            return tree, title_label

        def calcola_scenario_singolo(capitale_iniziale, anni_simulazione, tasso_annuo, spese_mensili, ammortamento_extra=0):
            try:
                if ammortamento_extra > capitale_iniziale:
                    raise ValueError("L'ammortamento extra non può essere maggiore del capitale.")
                tasso_mensile = tasso_annuo / 100 / 12
                mesi_simulazione = anni_simulazione * 12
                if mesi_simulazione <= 0:
                    return {
                        "rata_mensile_totale": 0,
                        "interessi_totali": 0,
                        "importo_totale": ammortamento_extra,
                        "capitale": capitale_iniziale,
                        "anni": 0,
                        "mesi": 0,
                        "rata_base": 0,
                        "spese_mensili": spese_mensili,
                        "tasso_mensile": tasso_mensile,
                        "tasso_annuo": tasso_annuo,
                        "ammortamento_extra": ammortamento_extra
                    }
                debito_res = capitale_iniziale - ammortamento_extra
                if debito_res <= 0:
                    return {
                        "rata_mensile_totale": 0,
                        "interessi_totali": 0,
                        "importo_totale": ammortamento_extra,
                        "capitale": capitale_iniziale,
                        "anni": 0,
                        "mesi": 0,
                       "rata_base": 0,
                        "spese_mensili": spese_mensili,
                        "tasso_mensile": tasso_mensile,
                        "tasso_annuo": tasso_annuo,
                        "ammortamento_extra": ammortamento_extra
                    }
                if tasso_mensile > 0:
                    rata_base = debito_res * (tasso_mensile * (1 + tasso_mensile) ** mesi_simulazione) / ((1 + tasso_mensile) ** mesi_simulazione - 1)
                else:
                    rata_base = debito_res / mesi_simulazione
                interessi_totali_nuovi = (rata_base * mesi_simulazione) - debito_res
                importo_totale_nuovo = debito_res + interessi_totali_nuovi + (spese_mensili * mesi_simulazione) + ammortamento_extra
                return {
                    "rata_mensile_totale": rata_base + spese_mensili,
                    "interessi_totali": interessi_totali_nuovi,
                    "importo_totale": importo_totale_nuovo,
                    "capitale": capitale_iniziale,
                    "anni": anni_simulazione,
                    "mesi": mesi_simulazione,
                    "rata_base": rata_base,
                    "spese_mensili": spese_mensili,
                    "tasso_mensile": tasso_mensile,
                    "tasso_annuo": tasso_annuo,
                    "ammortamento_extra": ammortamento_extra
                }
            except (ValueError, OverflowError):
                return None

        def aggiorna_simulazione_singola(i):
            campi_input = [entry.get().replace(",", ".").strip() for entry in entry_scenari[i]]
            
            if not campi_input[0] or not campi_input[1] or not campi_input[2]:
                for lbl in lbl_scenari_risultati[i]: lbl.config(text="N/A", foreground='black')
                popola_piano(trees_piani[i], None, None, None, None, None, None, labels_piani[i])
                self.tutti_i_risultati[i] = None
                return
            try:
                capitale_simulazione = float(campi_input[0])
                anni_simulazione = int(campi_input[1])
                tasso_annuo = float(campi_input[2])
                spese = float(campi_input[3] or 0)
                ammortamento_extra = float(campi_input[4] or 0)
                if (capitale_simulazione <= 0 or anni_simulazione <= 0 or tasso_annuo < 0 or
                    capitale_simulazione > 500000 or anni_simulazione > 35 or tasso_annuo > 35):
                    self.show_custom_warning("Attenzione", "Assicurati che siano positivi e rientrino in un intervallo ragionevole.\ncapitale_simulazione > 500000 or anni_simulazione > 35 or tasso_annuo > 35")
                    raise ValueError("Uno o più valori non sono validi. Assicurati che siano positivi e rientrino in un intervallo ragionevole.")
                if ammortamento_extra > capitale_simulazione:
                    self.show_custom_warning("Attenzione", "L'ammortamento extra non può essere maggiore del capitale.")
                    raise ValueError("L'ammortamento extra non può essere maggiore del capitale.")
                risultati_scenario = calcola_scenario_singolo(capitale_simulazione, anni_simulazione, tasso_annuo, spese, ammortamento_extra)
                if risultati_scenario is not None:
                    self.tutti_i_risultati[i] = risultati_scenario
                    risultati_principali = self.tutti_i_risultati[0]
                    lbl_scenari_risultati[i][0].config(text=f"{risultati_scenario['mesi']}")
                    lbl_scenari_risultati[i][1].config(text=f"{risultati_scenario['tasso_mensile'] * 100:,.4f} %")
                    lbl_scenari_risultati[i][2].config(text=f"{risultati_scenario['rata_mensile_totale']:,.2f} €")
                    lbl_scenari_risultati[i][3].config(text=f"{risultati_scenario['interessi_totali']:,.2f} €")
                    costo_totale_cap_int = risultati_scenario['capitale'] + risultati_scenario['interessi_totali']
                    lbl_scenari_risultati[i][4].config(text=f"{costo_totale_cap_int:,.2f} €")
                    if risultati_principali:
                        risparmio = risultati_principali["interessi_totali"] - risultati_scenario["interessi_totali"]
                        lbl_scenari_risultati[i][5].config(text=f"{risparmio:,.2f} €", foreground='green' if risparmio > 0 else ('#E53935' if risparmio < 0 else 'black'))
                    else:
                        lbl_scenari_risultati[i][5].config(text="N/A", foreground='black')
                    popola_piano(
                        trees_piani[i], risultati_scenario["capitale"], risultati_scenario["anni"],
                        risultati_scenario["mesi"], risultati_scenario["rata_base"],
                        risultati_scenario["spese_mensili"], risultati_scenario["tasso_mensile"],
                        labels_piani[i], risultati_scenario["ammortamento_extra"]
                    )
                else:
                    for lbl in lbl_scenari_risultati[i]: lbl.config(text="N/A", foreground='black')
                    popola_piano(trees_piani[i], None, None, None, None, None, None, labels_piani[i])
                    self.tutti_i_risultati[i] = None
            except ValueError as ve:
                for lbl in lbl_scenari_risultati[i]: lbl.config(text="N/A", foreground='black')
                popola_piano(trees_piani[i], None, None, None, None, None, None, labels_piani[i])
                self.tutti_i_risultati[i] = None
        def calcola_tutte_simulazioni():
            self.tutti_i_risultati = [None] * 6
            for i in range(6):
                aggiorna_simulazione_singola(i)
            aggiorna_tab_analisi(self.tutti_i_risultati)
        def aggiorna_tab_analisi(risultati):
            for row in tree_analisi.get_children():
                tree_analisi.delete(row)
            risultati_principali = risultati[0] if risultati and risultati[0] else None
            for i, res in enumerate(risultati):
                if res:
                    risparmio = 0.0
                    if risultati_principali:
                        risparmio = risultati_principali["interessi_totali"] - res["interessi_totali"]
                    tree_analisi.insert("", "end", values=(
                        f"Simulazione {i+1}", 
                        f"{res['capitale']:,.2f} €",
                        f"{res['anni']} anni ({res['mesi']} rate)", 
                        f"{res['tasso_annuo']:,.2f} %",
                        f"{res['ammortamento_extra']:,.2f} €",
                        f"{res['rata_mensile_totale']:,.2f} €", 
                        f"{res['importo_totale']:,.2f} €",
                        f"{res['interessi_totali']:,.2f} €",
                        f"{risparmio:,.2f} €"
                    ), tags=('all_rows',))
            tree_analisi.tag_configure('all_rows', font=('Arial', 10, 'bold'))
            
        def resetta_tutti_i_campi_simulazione():
            for i in range(6):
                for entry_widget in entry_scenari[i]:
                    entry_widget.delete(0, tk.END)
                for lbl in lbl_scenari_risultati[i]:
                    lbl.config(text="N/A", foreground='black')
                popola_piano(trees_piani[i], None, None, None, None, None, None, labels_piani[i])
                self.tutti_i_risultati[i] = None
            aggiorna_tab_analisi(self.tutti_i_risultati)
            
        def esporta_dati_con_preview():
            if not hasattr(self, 'tutti_i_risultati') or not any(self.tutti_i_risultati):
                self.show_custom_warning("Dati mancanti", "Esegui prima almeno una simulazione per poter esportare i dati.")
                return
            preview_window = tk.Toplevel(root)
            preview_window.title("Anteprima Esportazione")
            screen_width = preview_window.winfo_screenwidth()
            screen_height = preview_window.winfo_screenheight()
            window_width = 1200
            window_height = 600
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            preview_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
            preview_window.transient(root)
            preview_window.bind("<Escape>", lambda e: preview_window.destroy())
            contenuto_testo = (
                "=====================================================================================================================\n"
                "          REPORT SIMULAZIONI MUTUO/PRESTITO - RIEPILOGO STATISTICHE\n"
                "=====================================================================================================================\n"
                "CATEGORIA            | Simulazione 1 | Simulazione 2 | Simulazione 3 | Simulazione 4 | Simulazione 5 | Simulazione 6\n"
                "---------------------+---------------+---------------+---------------+---------------+---------------+---------------\n"
            )
            
            sim_data = {
            "Capitale (€)": [], "Durata (anni)": [], "N° Rate": [], "Tasso (%)": [], "Spese Incasso (€)": [], "Ammort. Extra (€)": [],
            "Rata Mensile (€)": [], "Interessi Totali (€)": [], "Costo Totale (€)": [],
            "Risparmio Int. (€)": []
            }
            risultati_principali = self.tutti_i_risultati[0] if self.tutti_i_risultati and self.tutti_i_risultati[0] else None
            for i, res in enumerate(self.tutti_i_risultati):
                if res:
                    sim_data["Capitale (€)"].append(f"{res['capitale']:,.2f}")
                    sim_data["Durata (anni)"].append(f"{res['anni']}")
                    sim_data["N° Rate"].append(f"{res['mesi']}")  
                    sim_data["Tasso (%)"].append(f"{res['tasso_annuo']:,.2f}")
                    sim_data["Spese Incasso (€)"].append(f"{res['spese_mensili']:,.2f}")
                    sim_data["Ammort. Extra (€)"].append(f"{res['ammortamento_extra']:,.2f}")
                    sim_data["Rata Mensile (€)"].append(f"{res['rata_mensile_totale']:,.2f}")
                    sim_data["Interessi Totali (€)"].append(f"{res['interessi_totali']:,.2f}")
                    sim_data["Costo Totale (€)"].append(f"{res['capitale'] + res['interessi_totali']:,.2f}")

                    risparmio = 0.0
                    if risultati_principali and i > 0:
                        risparmio = risultati_principali["interessi_totali"] - res["interessi_totali"]
                    sim_data["Risparmio Int. (€)"].append(f"{risparmio:,.2f}")
                    
                else:
                    for key in sim_data:
                        sim_data[key].append("")

            max_len_cat = max(len(cat) for cat in sim_data.keys())
            for cat, values in sim_data.items():
                formatted_cat = f"{cat}{' ' * (max_len_cat - len(cat))}"
                formatted_values = " | ".join(f"{val:<13}" for val in values)
                contenuto_testo += f"{formatted_cat} | {formatted_values}\n"

                if cat in ["Ammort. Extra (€)", "Costo Totale (€)", "Risparmio Int. (€)"]:
                    contenuto_testo += "---------------------+---------------+---------------+---------------+---------------+---------------+---------------\n"
            
            contenuto_testo += f"\nData Esportazione: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            text_frame = ttk.Frame(preview_window, padding=10)
            text_frame.pack(fill=tk.BOTH, expand=True)
            txt_preview = tk.Text(text_frame, wrap=tk.WORD, height=20, width=70, font=('Courier New', 10))
            txt_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=txt_preview.yview)
            scrollbar.pack(side=tk.RIGHT, fill='y')
            txt_preview.config(yscrollcommand=scrollbar.set)
            txt_preview.insert(tk.END, contenuto_testo)
            txt_preview.config(state="disabled")

            def salva_effettivamente():
                now = datetime.date.today()
                default_filename = f"Mutuo_Prestito_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
                file = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("File txt", "*.txt")],
                    initialdir=EXPORT_FILES,
                    initialfile=default_filename,
                    title="Salva Preview",
                    confirmoverwrite=False,
                    parent=preview_window
                )
                if file:
                    if os.path.exists(file):
                        conferma = self.show_custom_askyesno(
                            "Sovrascrivere file?",
                            f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                        )
                        if not conferma:
                            return 
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(contenuto_testo)
                    self.show_custom_warning("Esportazione completata", f"Riepilogo esportato in\n{file}")
                    
            button_frame = ttk.Frame(preview_window, padding=(10, 0, 10, 10))
            button_frame.pack()  
            ttk.Button(button_frame, text="💾 Salva", command=salva_effettivamente, style='Verde.TButton').pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="❌ Chiudi", command=preview_window.destroy, style='Giallo.TButton').pack(side=tk.LEFT, padx=5)

        root = tk.Toplevel()
        root.title("Gestore Finanziario - Calcolo Finanziamento e Simulazioni")
        root.geometry("1200x600")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1200
        window_height = 600
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        root.bind("<Escape>", lambda e: root.destroy())
        self.tutti_i_risultati = [None] * 6
    
        style = ttk.Style() 

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        simulazioni_frame = ttk.Frame(notebook, padding=10)
        notebook.add(simulazioni_frame, text="Simulazioni")

        titoli_simulazioni = ["Scenario", "Capitale (€)", "Durata (anni)", "Tasso (%)", "Spese Incasso (€)", "Ammort. Extra (€)", "N° Rate", "Tasso Mensile", "Rata Mensile", "Interessi Totali", "Costo Totale", "Risparmio Interessi"]
        for i, titolo in enumerate(titoli_simulazioni):
            ttk.Label(simulazioni_frame, text=titolo, font=("Arial", 9, "bold")).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
        entry_scenari, lbl_scenari_risultati = [], []
        for i in range(6):
            entry_row, lbl_row = [], []
            ttk.Label(simulazioni_frame, text=f"Simulazione {i+1}").grid(row=i+1, column=0, pady=5, sticky="w")
            
            entry_capitale_scen = ttk.Entry(simulazioni_frame, width=9); entry_capitale_scen.grid(row=i+1, column=1, padx=5); entry_row.append(entry_capitale_scen)
            entry_durata_scen = ttk.Entry(simulazioni_frame, width=9); entry_durata_scen.grid(row=i+1, column=2, padx=5); entry_row.append(entry_durata_scen)
            entry_tasso_scen = ttk.Entry(simulazioni_frame, width=5); entry_tasso_scen.grid(row=i+1, column=3, padx=5); entry_row.append(entry_tasso_scen)
            entry_spese_scen = ttk.Entry(simulazioni_frame, width=9); entry_spese_scen.grid(row=i+1, column=4, padx=5); entry_row.append(entry_spese_scen)
            entry_ammortamento_extra_scen = ttk.Entry(simulazioni_frame, width=9); entry_ammortamento_extra_scen.grid(row=i+1, column=5, padx=5); entry_row.append(entry_ammortamento_extra_scen)
            
            lbl_rate_scen = ttk.Label(simulazioni_frame, text="N/A", width=5, anchor="w"); lbl_rate_scen.grid(row=i+1, column=6, padx=5); lbl_row.append(lbl_rate_scen)
            lbl_tasso_mensile_scen = ttk.Label(simulazioni_frame, text="N/A", width=9, anchor="w"); lbl_tasso_mensile_scen.grid(row=i+1, column=7, padx=5); lbl_row.append(lbl_tasso_mensile_scen)
            lbl_rata_scen = ttk.Label(simulazioni_frame, text="N/A", width=12, anchor="w"); lbl_rata_scen.grid(row=i+1, column=8, padx=5); lbl_row.append(lbl_rata_scen)
            lbl_interessi_scen = ttk.Label(simulazioni_frame, text="N/A", width=12, anchor="w"); lbl_interessi_scen.grid(row=i+1, column=9, padx=5); lbl_row.append(lbl_interessi_scen)
            lbl_costo_totale = ttk.Label(simulazioni_frame, text="N/A", width=12, anchor="w"); lbl_costo_totale.grid(row=i+1, column=10, padx=5); lbl_row.append(lbl_costo_totale)
            lbl_risparmiati_scen = ttk.Label(simulazioni_frame, text="N/A", width=15, anchor="w", font=("Arial", 9, "bold")); lbl_risparmiati_scen.grid(row=i+1, column=11, padx=5); lbl_row.append(lbl_risparmiati_scen)
            
            entry_scenari.append(entry_row)
            lbl_scenari_risultati.append(lbl_row)

        btn_calcola_simulazioni = ttk.Button(simulazioni_frame, text="📄 Calcola Tutte le Simulazioni", command=calcola_tutte_simulazioni, style='Verde.TButton')
        btn_calcola_simulazioni.grid(row=7, column=0, columnspan=11, pady=10)

        btn_reset_simulazioni = ttk.Button(
            simulazioni_frame,
            text="↺",
            command=resetta_tutti_i_campi_simulazione,
            style='Giallo.TButton'
        )
        btn_reset_simulazioni.grid(row=7, column=7, pady=10, padx=5, sticky="ew")

        analisi_frame = ttk.Frame(notebook, padding=10)
        notebook.add(analisi_frame, text="Riepilogo Analisi")
        tree_analisi = ttk.Treeview(analisi_frame, columns=("Scenario", "Capitale", "Durata", "Tasso", "Ammortamento Extra", "Rata Mensile", "Importo Totale", "Interessi Totali", "Risparmio Interessi"), show="headings")
        tree_analisi.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        headings = {"Scenario": 120, "Capitale": 120, "Durata": 150, "Tasso": 80, "Ammortamento Extra": 140, "Rata Mensile": 120, "Importo Totale": 150, "Interessi Totali": 120, "Risparmio Interessi": 140}
        for col, width in headings.items():
            tree_analisi.heading(col, text=col)
            tree_analisi.column(col, width=width, anchor="center")
        trees_piani, labels_piani = [], []
        for i in range(6):
            tree, label = crea_tab_piano_ammortamento(notebook, f"Simulazione {i+1}")
            trees_piani.append(tree); labels_piani.append(label)
        common_button_frame = ttk.Frame(root, padding=10)
        common_button_frame.pack()  
    
        ttk.Button(common_button_frame, text="📄 Esporta Riepilogo", command=esporta_dati_con_preview, style='Verde.TButton').pack(side=tk.LEFT, padx=5)  
        ttk.Button(common_button_frame, text="❌ Chiudi", command=root.destroy, style='Giallo.TButton').pack(side=tk.LEFT, padx=5)
        
    def on_stats_table_right_click(self, event):
        try:
            item_id = self.stats_table.identify_row(event.y)
            selezioni_correnti = self.stats_table.selection()
            if item_id and item_id not in selezioni_correnti:
                self.stats_table.selection_set(item_id)
            final_selections = self.stats_table.selection()
            if not final_selections:
                return
            self.after(1, lambda: self.crea_grafico_categorie(final_selections))
        except Exception as e:
            print(f"Errore durante l'elaborazione del click destro: {e}")

    def crea_grafico_categorie(self, id_righe_selezionate):
        anno_filtro = None
        mese_filtro = None
        giorno_filtro = None
        entrate_count = 0
        uscite_count = 0
        tipo_transazione_ricercato = "saldo"
        colore_barra_base = None
        stats_mode = getattr(self, 'stats_mode', tk.StringVar(value="totali")).get() 
        stats_refdate = getattr(self, 'stats_refdate', None) 
        categorie_da_elaborare = []
        for item_id in id_righe_selezionate:
            try:
                cat_name_raw = str(self.stats_table.item(item_id, "values")[0]).strip()
                cat_name = ' '.join(cat_name_raw.split()) 
                if cat_name not in categorie_da_elaborare:
                    categorie_da_elaborare.append(cat_name)
            except:
                continue
        if not categorie_da_elaborare:
            self.show_custom_info("Errore", "Nessuna categoria valida trovata.")
            return
        if stats_mode == "giorno" and stats_refdate:
            anno_filtro = str(stats_refdate.year)
            mese_filtro = str(stats_refdate.month).zfill(2)
            giorno_filtro = str(stats_refdate.day).zfill(2)
        elif stats_mode == "mese" and stats_refdate:
            anno_filtro = str(stats_refdate.year)
            mese_filtro = str(stats_refdate.month).zfill(2)
        elif stats_mode == "anno" and stats_refdate:
            anno_filtro = str(stats_refdate.year)
        for data_oggetto, entries in self.spese.items():
            data_anno_str = str(data_oggetto.year)
            data_mese_pad = str(data_oggetto.month).zfill(2)
            if anno_filtro and data_anno_str != anno_filtro: continue
            if mese_filtro and data_mese_pad != mese_filtro: continue
            for entry in entries:
                if len(entry) < 4: continue 
                cat_raw, desc, imp, tipo = entry[:4]
                cat = ' '.join(str(cat_raw).strip().split())
                tipo_lower = str(tipo).lower()
                if cat in categorie_da_elaborare:
                    if "entrata" in tipo_lower:
                        entrate_count += 1
                    elif "uscita" in tipo_lower:
                        uscite_count += 1
        if entrate_count > 0 and uscite_count > 0:
            tipo_transazione_ricercato = "misto"
        elif entrate_count > 0:
            tipo_transazione_ricercato = "entrata"
            colore_barra_base = "#28A745"
        else:
            tipo_transazione_ricercato = "uscita"
            colore_barra_base = "#DC3545"
        spese_combinate = defaultdict(lambda: {
            'Entrata': 0.0, 
            'Uscita': 0.0,
            'Dettaglio_Entrata': defaultdict(float),
            'Dettaglio_Uscita': defaultdict(float)
        })
        saldo_aggregato_totale = 0.0
        for data_objeto, entries in self.spese.items():
            try:
                data_anno_str = str(data_objeto.year)
                data_mese_pad = str(data_objeto.month).zfill(2)
                data_giorno_pad = str(data_objeto.day).zfill(2)
            except:
                continue
            if anno_filtro and data_anno_str != anno_filtro: continue
            if mese_filtro and data_mese_pad != mese_filtro: continue
            if giorno_filtro and data_giorno_pad != giorno_filtro: continue
            if stats_mode == "giorno" or stats_mode == "mese":
                  chiave_aggregazione = f"{data_giorno_pad}/{data_mese_pad}/{data_anno_str}"
            else:
                  chiave_aggregazione = f"{data_anno_str}-{data_mese_pad}"
            for entry in entries:
                if len(entry) < 4: continue
                cat_raw, desc, imp, tipo = entry[:4]
                cat = ' '.join(str(cat_raw).strip().split())
                tipo_lower = str(tipo).lower()
                if cat in categorie_da_elaborare:
                    try:
                        importo_numerico = float(imp)
                        if tipo_transazione_ricercato == "misto":
                            if "entrata" in tipo_lower:
                                spese_combinate[chiave_aggregazione]['Entrata'] += importo_numerico
                                spese_combinate[chiave_aggregazione]['Dettaglio_Entrata'][cat] += importo_numerico
                                saldo_aggregato_totale += importo_numerico
                            elif "uscita" in tipo_lower:
                                spese_combinate[chiave_aggregazione]['Uscita'] += abs(importo_numerico)
                                spese_combinate[chiave_aggregazione]['Dettaglio_Uscita'][cat] += abs(importo_numerico)
                                saldo_aggregato_totale -= abs(importo_numerico)
                        elif tipo_transazione_ricercato == "entrata" and "entrata" in tipo_lower:
                            spese_combinate[chiave_aggregazione]['Entrata'] += importo_numerico
                            spese_combinate[chiave_aggregazione]['Dettaglio_Entrata'][cat] += importo_numerico
                            saldo_aggregato_totale += importo_numerico
                        elif tipo_transazione_ricercato == "uscita" and "uscita" in tipo_lower:
                            spese_combinate[chiave_aggregazione]['Uscita'] += abs(importo_numerico)
                            spese_combinate[chiave_aggregazione]['Dettaglio_Uscita'][cat] += abs(importo_numerico)
                            saldo_aggregato_totale -= abs(importo_numerico)
                    except (ValueError, TypeError):
                        continue
        dati_filtrati_non_zero = {}
        for k, v in spese_combinate.items():
            if tipo_transazione_ricercato == "misto":
                 if v['Entrata'] != 0.0 or v['Uscita'] != 0.0:
                     dati_filtrati_non_zero[k] = v
            else:
                 if v['Entrata'] != 0.0 or v['Uscita'] != 0.0:
                     valore_unico = v['Entrata'] + v['Uscita']
                     if tipo_transazione_ricercato == "entrata":
                          dati_filtrati_non_zero[k] = {'Totale': valore_unico, 'Dettaglio': v['Dettaglio_Entrata']}
                     else:
                          dati_filtrati_non_zero[k] = {'Totale': valore_unico, 'Dettaglio': v['Dettaglio_Uscita']}
        if not dati_filtrati_non_zero:
             self.show_custom_info("Nessun Dato", "Nessun dato di transazione con importo non zero trovato per il filtro e il periodo selezionati.")
             return
        dati_ordinati = sorted(dati_filtrati_non_zero.items())
        dati_per_grafico = list(reversed(dati_ordinati)) 
        if tipo_transazione_ricercato == "misto":
            totale_aggregato = saldo_aggregato_totale
        else:
            totale_aggregato = sum(d['Totale'] for _, d in dati_per_grafico)
        if tipo_transazione_ricercato == "misto":
            tipo_transazione_base = "Entrate vs Uscite"
            totale_copertura_desc_saldo = "Saldo Netto"
        elif tipo_transazione_ricercato == "entrata":
            tipo_transazione_base = "Entrate"
            totale_copertura_desc_saldo = "Totale Entrate"
        else:
            tipo_transazione_base = "Uscite"
            totale_copertura_desc_saldo = "Totale Uscite"
        if len(categorie_da_elaborare) > 1:
            tipo_titolo = "Combinata"
        else:
            tipo_titolo = "Categoria"
        if stats_mode == "giorno" and stats_refdate: 
            data_str = stats_refdate.strftime('%d/%m/%Y')
            etichetta_tempo = "Giornaliero"
            filtro_titolo = f" - Giorno {data_str}"
            totale_copertura_desc = f"{totale_copertura_desc_saldo} Giorno {data_str}"
        elif stats_mode == "mese" and anno_filtro and mese_filtro: 
            etichetta_tempo = "Giornalieri"
            filtro_titolo = f" - Mese {mese_filtro}/{anno_filtro}"
            totale_copertura_desc = f"{totale_copertura_desc_saldo} Mese {mese_filtro} / {anno_filtro}"
        elif stats_mode == "anno" and anno_filtro: 
            etichetta_tempo = "Mensili" 
            filtro_titolo = f" - Anno {anno_filtro}"
            totale_copertura_desc = f"{totale_copertura_desc_saldo} Anno {anno_filtro}"
        else:
            etichetta_tempo = "Mensili" 
            filtro_titolo = " - Totale"
            totale_copertura_desc = f"{totale_copertura_desc_saldo} Totale"

        #titolo_grafico = f"{tipo_transazione_base} {tipo_titolo} {etichetta_tempo}: {', '.join(categorie_da_elaborare)}{filtro_titolo}"
        # Nuovo Titolo (senza lista categorie)
        titolo_grafico = f"{tipo_transazione_base} {tipo_titolo} {etichetta_tempo}{filtro_titolo}"

        popup_width, popup_height = 1200, 600 
        popup_grafico = tk.Toplevel(self)
        popup_grafico.title(f"📊 {titolo_grafico}")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - popup_width/2)
        center_y = int(screen_height/2 - popup_height/2)
        popup_grafico.geometry(f'{popup_width}x{popup_height}+{center_x}+{center_y}')
        popup_grafico.bind('<Escape>', lambda e: popup_grafico.destroy())
        main_frame = ttk.Frame(popup_grafico)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(main_frame, text=titolo_grafico, font=("Arial", 12, "bold")).pack(pady=10)
        canvas_frame_scroll = ttk.Frame(main_frame)
        canvas_frame_scroll.pack(fill="both", expand=True)
        scrollbar_h = ttk.Scrollbar(canvas_frame_scroll, orient="horizontal")
        canvas = tk.Canvas(
            canvas_frame_scroll, 
            bg="white",
            xscrollcommand=scrollbar_h.set 
        )
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar_h.config(command=canvas.xview)
        canvas.bind("<Configure>", lambda e: disegna_barre_scroll(canvas, dati_per_grafico))

        def disegna_barre_scroll(c, dati_tuple):
            c.delete("all")
            LARGHEZZ_STANDARD = 100
            LARGHEZZ_MISTA = 140 
            BAR_FACTOR = 0.7 
            margine_superiore = 40
            margine_inferiore = 90 
            SPAZIO_EXTRA_MINIMO = 200 
            tooltip_window_local = None

            def hide_tooltip_local(event=None):
                nonlocal tooltip_window_local
                if tooltip_window_local:
                    tooltip_window_local.destroy()
                    tooltip_window_local = None

            def show_tooltip_local(event, text):
                nonlocal tooltip_window_local
                hide_tooltip_local() 
                root_x = c.winfo_rootx()
                root_y = c.winfo_rooty()
                screen_x = root_x + event.x + 10
                screen_y = root_y + event.y + 10
                tooltip_window_local = tk.Toplevel(c)
                tooltip_window_local.wm_overrideredirect(True)
                tooltip_window_local.wm_geometry(f"+{screen_x}+{screen_y}")
                label = tk.Label(tooltip_window_local, 
                                 text=text, 
                                 background="#FFFFEA", 
                                 relief="solid", 
                                 borderwidth=1,
                                 font=("Arial", 9),
                                 justify=tk.LEFT,
                                 anchor='w')
                label.pack(padx=1, pady=1)
            altezza = c.winfo_height() 
            canvas_larghezza = c.winfo_width() 
            if altezza <= 50 or canvas_larghezza <= 50: 
                hide_tooltip_local()
                return
            y_base = altezza - margine_inferiore
            importi_entrate = []
            importi_uscite = []
            for _, val in dati_tuple:
                if isinstance(val, dict):
                    if 'Totale' in val:
                         if tipo_transazione_ricercato == "entrata":
                             importi_entrate.append(val.get('Totale', 0))
                         else:
                             importi_uscite.append(abs(val.get('Totale', 0)))
                    else:
                         importi_entrate.extend([val.get('Entrata', 0), 0])
                         importi_uscite.extend([val.get('Uscita', 0), 0])
                else:
                    if tipo_transazione_ricercato == "entrata":
                        importi_entrate.append(val)
                    else:
                        importi_uscite.append(abs(val))

            def calculate_capped_max(abs_importi):
                if not abs_importi or max(abs_importi) == 0: return 0
                abs_importi_sorted = sorted([i for i in abs_importi if i > 0], reverse=True)
                if len(abs_importi_sorted) <= 1: return abs_importi_sorted[0]
                valore_base = abs_importi_sorted[1] 
                max_val_cap = valore_base * 2 
                if abs_importi_sorted[0] / max_val_cap > 2.5: return max_val_cap
                else: return abs_importi_sorted[0]
            max_e = calculate_capped_max(importi_entrate)
            max_u = calculate_capped_max(importi_uscite)
            max_val = max(max_e, max_u)
            altezza_utilizzabile = altezza - (margine_superiore + margine_inferiore) 
            scala = altezza_utilizzabile / max(max_val * 1.05, 0.01)
            y_zero = y_base
            x_current = margine_inferiore
            dati_posizioni = []
            for periodo, dati_valore in dati_tuple:
                is_misto = isinstance(dati_valore, dict) and 'Entrata' in dati_valore and 'Uscita' in dati_valore and 'Totale' not in dati_valore
                barra_width = LARGHEZZ_MISTA if is_misto else LARGHEZZ_STANDARD
                if stats_mode == "giorno":
                    larghezza_gruppo = LARGHEZZ_STANDARD
                else:
                    larghezza_gruppo = barra_width
                dati_posizioni.append({
                    'periodo': periodo,
                    'dati_valore': dati_valore,
                    'x_start': x_current,
                    'barra_width': barra_width
                })
                x_current += larghezza_gruppo
            if dati_tuple:
                larghezza_contenuto_barre = x_current + margine_inferiore
            else:
                larghezza_contenuto_barre = canvas_larghezza 
            if stats_mode == "giorno":
                larghezza_contenuto = canvas_larghezza
            else:
                larghezza_contenuto = max(larghezza_contenuto_barre, canvas_larghezza + SPAZIO_EXTRA_MINIMO) 
            c.config(scrollregion=(0, 0, larghezza_contenuto, altezza))
            c.create_line(margine_inferiore/2, y_zero, larghezza_contenuto, y_zero, fill="gray", dash=(4, 2))
            c.bind("<Leave>", hide_tooltip_local) 

            def formatta_dettaglio(dettagli_dict):
                if not dettagli_dict:
                    return "  Nessun dettaglio categoria."
                dettaglio_lines = []
                dati_ordinati = sorted(dettagli_dict.items(), key=lambda item: item[0], reverse=False)
                for cat, importo in dati_ordinati:
                     if importo > 0:
                         importo_f = f"{importo:,.2f}" 
                         dettaglio_lines.append(f"  {cat}: {importo_f} €")
                return "\n".join(dettaglio_lines)
            for item in dati_posizioni:
                periodo = item['periodo']
                dati_valore = item['dati_valore']
                LARGHEZZA_BARRA_DINAMICA = item['barra_width']
                x_start_base = item['x_start']
                x_start = x_start_base
                if stats_mode == "giorno":
                    x_center = canvas_larghezza / 2 
                    bar_group_width = LARGHEZZA_BARRA_DINAMICA * BAR_FACTOR
                    x_start = x_center - (bar_group_width / 2)
                is_misto = isinstance(dati_valore, dict) and 'Entrata' in dati_valore and 'Uscita' in dati_valore and 'Totale' not in dati_valore
                if is_misto:
                    valore_e = dati_valore.get('Entrata', 0)
                    valore_u = dati_valore.get('Uscita', 0)
                    dettaglio_e = dati_valore.get('Dettaglio_Entrata', {})
                    dettaglio_u = dati_valore.get('Dettaglio_Uscita', {})
                    barra_singola_w = (LARGHEZZA_BARRA_DINAMICA * BAR_FACTOR) / 2
                    if valore_e > 0:
                        valore_e_scalato = min(valore_e, max_val) 
                        altezza_barra_e = valore_e_scalato * scala
                        x0_e, x1_e = x_start, x_start + barra_singola_w
                        rect_e = c.create_rectangle(x0_e, y_zero - altezza_barra_e, x1_e, y_zero, fill="#28A745")
                        testo_etichetta = f"{valore_e:,.2f}".replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
                        c.create_text(
                            (x0_e + x1_e) / 2, y_zero - altezza_barra_e - 6, 
                            text=testo_etichetta, font=("Arial", 9), fill="#28A745"
                        )
                        dettaglio_cat_e = formatta_dettaglio(dettaglio_e)
                        tooltip_text_e = (
                            f"Totale Entrata: {valore_e:,.2f} €\n"
                            f"\n"
                            #f"--- Dettaglio Categorie Selezionate ---\n"
                            f"{dettaglio_cat_e}"
                        ).replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
                        c.tag_bind(rect_e, "<Enter>", lambda e, t=tooltip_text_e: show_tooltip_local(e, t))
                        c.tag_bind(rect_e, "<Leave>", hide_tooltip_local)
                        filter_data = self.get_filter_data(periodo, 'Entrata', categorie_da_elaborare, stats_mode)
                        c.tag_bind(rect_e, "<Double-1>", lambda e, f=filter_data: self.mostra_transazioni_popup(f, f"Entrate aggregate {periodo}"))
                    if valore_u > 0:
                        valore_u_scalato = min(valore_u, max_val)
                        altezza_barra_u = valore_u_scalato * scala
                        x0_u, x1_u = x_start + barra_singola_w, x_start + barra_singola_w * 2
                        rect_u = c.create_rectangle(x0_u, y_zero - altezza_barra_u, x1_u, y_zero, fill="#DC3545")
                        testo_etichetta = f"{valore_u:,.2f}".replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
                        c.create_text(
                            (x0_u + x1_u) / 2, y_zero - altezza_barra_u - 6, 
                            text=testo_etichetta, font=("Arial", 9), fill="#DC3545"
                        )
                        dettaglio_cat_u = formatta_dettaglio(dettaglio_u)
                        tooltip_text_u = (
                            f"Totale Uscita: {valore_u:,.2f} €\n"
                            f"\n"
                            #f"--- Dettaglio Categorie Selezionate ---\n"
                            f"{dettaglio_cat_u}"
                        ).replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
                        c.tag_bind(rect_u, "<Enter>", lambda e, t=tooltip_text_u: show_tooltip_local(e, t))
                        c.tag_bind(rect_u, "<Leave>", hide_tooltip_local)
                        filter_data = self.get_filter_data(periodo, 'Uscita', categorie_da_elaborare, stats_mode)
                        c.tag_bind(rect_u, "<Double-1>", lambda e, f=filter_data: self.mostra_transazioni_popup(f, f"Uscite aggregate {periodo}"))
                    x_center_text = x_start + (LARGHEZZA_BARRA_DINAMICA * BAR_FACTOR) / 2
                else:
                    if isinstance(dati_valore, dict):
                        valore = dati_valore.get('Totale', 0)
                        dettaglio = dati_valore.get('Dettaglio', {})
                    else:
                        valore = dati_valore 
                        dettaglio = {}
                    colore_barra = "#28A745" if tipo_transazione_ricercato == "entrata" else "#DC3545"
                    valore_scalato = min(abs(valore), max_val)
                    altezza_barra_pix = valore_scalato * scala
                    x0 = x_start
                    x1 = x0 + LARGHEZZA_BARRA_DINAMICA * BAR_FACTOR
                    rect = c.create_rectangle(x0, y_zero - altezza_barra_pix, x1, y_zero, fill=colore_barra)
                    importo_formattato = f"{valore:,.2f} €".replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
                    c.create_text((x0 + x1) / 2, y_zero - altezza_barra_pix - 6, text=importo_formattato, font=("Arial", 9), fill=colore_barra)
                    x_center_text = (x0 + x1) / 2
                    tipo_testo = "Entrata" if tipo_transazione_ricercato == "entrata" else "Uscita"
                    dettaglio_cat = formatta_dettaglio(dettaglio)
                    tooltip_text = (
                        f"Totale {tipo_testo}: {valore:,.2f} €\n"
                        f"\n"
                        #f"--- Dettaglio Categorie Selezionate ---\n"
                        f"{dettaglio_cat}"
                    ).replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
                    c.tag_bind(rect, "<Enter>", lambda e, t=tooltip_text: show_tooltip_local(e, t))
                    c.tag_bind(rect, "<Leave>", hide_tooltip_local)
                    tipo_bind = tipo_transazione_ricercato.capitalize()
                    filter_data = self.get_filter_data(periodo, tipo_bind, categorie_da_elaborare, stats_mode)
                    c.tag_bind(rect, "<Double-1>", lambda e, f=filter_data: self.mostra_transazioni_popup(f, f"{tipo_transazione_base} aggregate {periodo}"))
                label_y = altezza - margine_inferiore + 40 
                if stats_mode == "giorno": label_y = altezza - 20
                c.create_text(
                    x_center_text, 
                    label_y, 
                    text=periodo, 
                    font=("Arial", 8), 
                    angle=45 if stats_mode != "giorno" else 0
                )
            
        self.get_filter_data = lambda periodo, tipo, categories, mode: self._build_filter_data(periodo, tipo, categories, mode)
        if stats_mode == "giorno":
             scrollbar_h.pack_forget()
        else:
             scrollbar_h.pack(side="bottom", fill="x")
        popup_grafico.update_idletasks()
        disegna_barre_scroll(canvas, dati_per_grafico)
        popup_grafico.after(3000, esegui_disegno_ritardato) 
        popup_grafico.transient(self)
        if stats_mode != "giorno":
            popup_grafico.after(10, lambda: canvas.xview_moveto(0)) 

        def chiudi_popup():
            popup_grafico.destroy()
        totale_formattato = f"{totale_aggregato:,.2f} €".replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
        colore_totale = "black"
        if tipo_transazione_ricercato == "misto":
              if totale_aggregato > 0:
                  colore_totale = "#28A745"
              elif totale_aggregato < 0:
                  colore_totale = "#DC3545"
              else:
                  colore_totale = "gray"
        elif tipo_transazione_ricercato == "entrata":
            colore_totale = "#28A745"
        elif tipo_transazione_ricercato == "uscita":
            colore_totale = "#DC3545"
        totale_frame = ttk.Frame(main_frame)
        totale_frame.pack(fill='x', pady=(10, 5), padx=20) 
        tk.Label(
            totale_frame, 
            text=f"{totale_copertura_desc}:",
            font=("Arial", 10),
            anchor="w"
        ).pack(side="left")
        tk.Label(
            totale_frame, 
            text=totale_formattato,
            font=("Arial", 10, "bold"),
            anchor="w", 
            padx=5,
            fg=colore_totale 
        ).pack(side="left") 
        ttk.Button(
            main_frame, 
            text="✖ Chiudi", 
            command=chiudi_popup,
            style="Giallo.TButton"
        ).pack(pady=10)
        popup_grafico.bind("<Escape>", lambda event: chiudi_popup())

    def _build_filter_data(self, periodo, tipo, categories_to_elaborate, stats_mode):
        anno_bind = None
        mese_bind = None
        giorno_bind = None
        try:
            if '/' in periodo and len(periodo.split('/')) == 3:
                g, m, a = periodo.split('/')
                anno_bind = a
                mese_bind = int(m)
                giorno_bind = int(g)
            elif '-' in periodo and len(periodo.split('-')) == 2:
                a, m = periodo.split('-')
                anno_bind = a
                mese_bind = int(m)
                giorno_bind = None 
        except Exception as e:
            pass
        return {
            "anno": anno_bind, 
            "mese": mese_bind, 
            "giorno": giorno_bind, 
            "tipo": tipo, 
            "categorie": categories_to_elaborate
        }
        

    def mostra_analisi_grafici(self):
        def disegna_barre(canvas, dati, colori, mostra_anno=False, mostra_tipo=False, centro=False):
            canvas.delete("all")
            canvas.update_idletasks()
            larghezza = canvas.winfo_width()
            altezza = canvas.winfo_height()
            margine = 50
            if isinstance(dati, dict):
                elementi = list(dati.items())
            else:
                elementi = dati
            max_val = max(abs(val) for _, val in elementi) if elementi else 1
            scala = (altezza - margine * 2) / (max_val * 1.5)
            larghezza_barra = (larghezza - margine * 2) // max(len(elementi), 1)
            y_base = altezza // 2 if centro else altezza - margine
            anno_selezionato = selettore_anno1.get()
            
            for i, (etichetta, valore) in enumerate(elementi):
                x0 = margine + i * larghezza_barra
                x1 = x0 + larghezza_barra * 0.6
                colore = colori.get(etichetta, "gray")
                parts = etichetta.split(" ")
                tipo = parts[-1] if mostra_tipo else None 
                if anno_selezionato == "Tutti":
                    anno = parts[0] 
                    mese = None
                else:
                    anno = anno_selezionato
                    mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
                    try:
                        mese = mesi.index(parts[0]) + 1
                    except ValueError:
                        mese = None
                filter_data = {"anno": anno, "mese": mese, "tipo": tipo}
                title_text = f"Transazioni {tipo} per {anno_selezionato}" if anno_selezionato != "Tutti" else f"Transazioni {tipo} per l'anno {anno}"
                if valore >= 0:
                    y1 = y_base - valore * scala
                    rect = canvas.create_rectangle(x0, y_base, x1, y1, fill=colore)
                    canvas.create_text((x0 + x1) / 2, y1 - 10, text=f"{int(valore)}", font=("Arial", 8))
                else:
                    y1 = y_base + abs(valore) * scala
                    rect = canvas.create_rectangle(x0, y_base, x1, y1, fill=colore)
                    canvas.create_text((x0 + x1) / 2, y1 + 10, text=f"{int(valore)}", font=("Arial", 8))
                canvas.tag_bind(
                    rect, 
                    "<Double-1>", 
                    lambda e, f=filter_data, t=title_text: self.mostra_transazioni_popup(f, t)
                )
                if mostra_tipo and " " in etichetta:
                    tipo_label = etichetta.split(" ")[1]
                    canvas.create_text((x0 + x1) / 2, y_base + 15, text=tipo_label, font=("Arial", 8))
                if not mostra_anno and " " in etichetta:
                    mese_label = etichetta.split(" ")[0]
                    canvas.create_text((x0 + x1) / 2, y_base + 30, text=mese_label, font=("Arial", 8))
                elif mostra_anno:
                    anno_label = etichetta.split(" ")[0] if " " in etichetta else etichetta
                    canvas.create_text((x0 + x1) / 2, y_base + 30, text=anno_label, font=("Arial", 8))

        def disegna_barre_categorie(canvas, dati, colori):
            if hasattr(canvas, "tooltip") and canvas.tooltip:
                canvas.tooltip.destroy()
                canvas.tooltip = None
            canvas.delete("all")
            canvas.update_idletasks()
            LARGHEZZA_BARRA_FISSA = 80 
            margine = 50
            larghezza_visualizzata = canvas.winfo_width()
            altezza = canvas.winfo_height()
            y_base = altezza - margine
            totale = sum(val for _, val in dati) if dati else 1
            max_val = max(val for _, val in dati) if dati else 1
            scala = (altezza - margine * 2) / (max_val * 1.2)
            numero_barre = max(len(dati), 1)
            larghezza_contenuto = margine * 2 + numero_barre * LARGHEZZA_BARRA_FISSA
            x_offset = max(0, (larghezza_visualizzata - larghezza_contenuto) // 2)
            anno_selezionato = canvas.anno_corrente
            for i, (categoria, valore) in enumerate(dati):
                x0 = x_offset + margine + i * LARGHEZZA_BARRA_FISSA
                x1 = x0 + LARGHEZZA_BARRA_FISSA * 0.6
                y1 = y_base - valore * scala
                colore = colori.get(categoria, "#888888")
                rect = canvas.create_rectangle(x0, y_base, x1, y1, fill=colore)
                anno = anno_selezionato
                filter_data = {"anno": anno, "categoria": categoria, "tipo": "Uscita"}
                title_text = f"Spese Categoria '{categoria}' (Anno: {anno})"
                canvas.tag_bind(
                    rect, 
                    "<Double-1>", 
                    lambda e, f=filter_data, t=title_text: self.mostra_transazioni_popup(f, t)
                )
                percentuale = int((valore / totale) * 100)
                canvas.create_text((x0 + x1) / 2, y1 - 12, text=f"{int(valore)} €", font=("Arial", 9))
                canvas.create_text((x0 + x1) / 2, y1 - 26, text=f"{percentuale}%", font=("Arial", 8), fill="gray")
                limite = 10
                nome_visualizzato = categoria if len(categoria) <= limite else categoria[:limite] + "..."
                canvas.create_text((x0 + x1) / 2, y_base + 20, text=nome_visualizzato, font=("Arial", 9))
                
                def show_tooltip(event, text=categoria):
                    if hasattr(canvas, "tooltip") and canvas.tooltip:
                        canvas.tooltip.destroy()
                        canvas.tooltip = None
                    canvas.tooltip = tk.Toplevel(canvas)
                    canvas.tooltip.wm_overrideredirect(True)
                    canvas.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
                    label = tk.Label(canvas.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 9))
                    label.pack(ipadx=4)
                
                def hide_tooltip(event):
                    if hasattr(canvas, "tooltip") and canvas.tooltip:
                        canvas.tooltip.destroy()
                        canvas.tooltip = None
                canvas.tag_bind(rect, "<Enter>", show_tooltip)
                canvas.tag_bind(rect, "<Leave>", hide_tooltip)
            canvas.create_text(
                larghezza_visualizzata // 2,
                y_base + 40,
                text=f"Totale uscite: € {totale:,.2f}",
                font=("Arial", 10, "bold"),
                fill="black"
            )
            canvas.config(scrollregion=(0, 0, larghezza_contenuto, altezza))

        def mostra_legenda_categorie(canvas_master, categorie_dati, colori):
            if hasattr(canvas_master, "legenda_frame"):
                canvas_master.legenda_frame.destroy()
            categorie_ordinate = sorted(categorie_dati, key=lambda x: x[1], reverse=True)
            legenda_frame = ttk.Frame(canvas_master, relief="groove", borderwidth=1)
            legenda_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10)) 
            canvas_master.legenda_frame = legenda_frame
            tk.Label(legenda_frame, text="Legenda Categorie", font=("Arial", 10, "bold")).pack(pady=5)
            scroll_container = ttk.Frame(legenda_frame)
            scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
            scrollbar = ttk.Scrollbar(scroll_container, orient="vertical")
            scrollbar.pack(side="right", fill="y")
            canvas_legenda = tk.Canvas(scroll_container, borderwidth=0, highlightthickness=0, yscrollcommand=scrollbar.set)
            canvas_legenda.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=canvas_legenda.yview)
            inner_frame = ttk.Frame(canvas_legenda)
            
            def on_frame_configure(event):
                bbox = canvas_legenda.bbox("all")
                if bbox and (bbox[3] - bbox[1] < event.height):
                    altezza_forzata = event.height + 1
                    nuova_scrollregion = (bbox[0], bbox[1], bbox[2], altezza_forzata)
                    canvas_legenda.configure(scrollregion=nuova_scrollregion)
                else:
                    canvas_legenda.configure(scrollregion=bbox)
                canvas_legenda.itemconfig(canvas_legenda_window, width=event.width)
            canvas_legenda.bind('<Configure>', on_frame_configure)
            canvas_legenda_window = canvas_legenda.create_window((0, 0), window=inner_frame, anchor="nw")
            
            for categoria, valore in categorie_ordinate:
                colore = colori.get(categoria, "#888888")
                voce_frame = ttk.Frame(inner_frame)
                voce_frame.pack(fill="x", padx=2, pady=1)
                quadrato = tk.Canvas(voce_frame, width=10, height=10, bg=colore, highlightthickness=0)
                quadrato.pack(side="left", padx=(5, 5))
                testo = f"{categoria}: € {int(valore):,}"
                tk.Label(voce_frame, text=testo, anchor="w", font=("Arial", 8)).pack(side="left", fill="x", expand=True)
            inner_frame.update_idletasks()
            canvas_legenda.config(scrollregion=canvas_legenda.bbox("all"))
            canvas_legenda.event_generate('<Configure>')


        def disegna_barre_saldo(canvas, dati):
            canvas.delete("all")
            canvas.update_idletasks()
            larghezza = canvas.winfo_width()
            altezza = canvas.winfo_height()
            margine = 50
            mesi_ordinati = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
            chiavi = mesi_ordinati if set(mesi_ordinati).issubset(dati.keys()) else list(dati.keys())
            max_val = max(abs(dati[k]) for k in chiavi) if dati else 1
            scala = (altezza - margine * 2) / (max_val * 1.5)
            larghezza_barra = (larghezza - margine * 2) // max(len(chiavi), 1)
            y_base = altezza - margine
            for i, etichetta in enumerate(chiavi):
                valore = dati.get(etichetta, 0)
                x0 = margine + i * larghezza_barra
                x1 = x0 + larghezza_barra * 0.6
                if abs(valore) < 0.01:
                    y1 = y_base
                else:
                    y1 = y_base - abs(valore) * scala 
                colore = "green" if valore >= 0 else "red"
                segno = "+" if valore >= 0 else "−"
                canvas.create_rectangle(x0, y_base, x1, y1, fill=colore)
                testo_y = y1 - 10 
                canvas.create_text(
                    (x0 + x1) / 2, 
                    testo_y, 
                    text=f"{segno}{int(abs(valore))}", 
                    font=("Arial", 9)
                )
                canvas.create_text((x0 + x1) / 2, y_base + 20, text=etichetta, font=("Arial", 9))

        def aggiorna_tab3(event=None):
            selezione = selettore_anno3.get()
            entrate = defaultdict(float)
            uscite = defaultdict(float)
            for data, voci in self.spese.items():
                anno = data.year
                mese = data.month
                if selezione != "Tutti" and str(anno) != selezione:
                    continue
                for voce in voci:
                    tipo = voce[3].strip().lower()
                    importo = voce[2]
                    if selezione == "Tutti":
                        chiave = str(anno)
                    else:
                        chiave = mese
                    if tipo == "entrata":
                        entrate[chiave] += importo
                    elif tipo == "uscita":
                        uscite[chiave] += importo 
            total_entrate = sum(entrate.values())
            total_uscite = sum(uscite.values())
            saldo_totale = total_entrate - total_uscite
            self.lbl_entrate_tab3.config(text=f"Entrate: € {total_entrate:,.2f}")
            self.lbl_uscite_tab3.config(text=f"Uscite: € {total_uscite:,.2f}")
            if saldo_totale >= 0:
                self.lbl_saldo_tab3.config(text=f"Saldo: € {saldo_totale:,.2f}", fg="green")
            else:
                self.lbl_saldo_tab3.config(text=f"Saldo: € {saldo_totale:,.2f}", fg="red")
            saldo_per_grafico = defaultdict(float)
            for chiave, importo in entrate.items():
                saldo_per_grafico[chiave] += importo
            for chiave, importo in uscite.items():
                saldo_per_grafico[chiave] -= importo 
            if selezione == "Tutti":
                grafico = {str(a): saldo_per_grafico.get(a, 0) for a in sorted(saldo_per_grafico)}
            else:
                mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
                grafico = {mesi[m - 1]: saldo_per_grafico.get(m, 0) for m in range(1, 13)}
            disegna_barre_saldo(canvas3, grafico)
            
        def aggiorna_tab2(event=None):
            anno = selettore_anno2.get()
            canvas2.anno_corrente = anno
            if hasattr(tab2, "bottone_indietro"):
                tab2.bottone_indietro.destroy()
            if hasattr(tab2, "label_altro"):
                tab2.label_altro.destroy()
            canvas_frame_scroll.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0, 10)) 
            categories = defaultdict(float)
            for data, voci in self.spese.items():
                if anno == "Tutti" or str(data.year) == anno:
                    for voce in voci:
                        if voce[3].strip().lower() == "uscita":
                            categories[voce[0]] += float(voce[2])
            
            tutte_categorie = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            
            colori = {}
            for cat, _ in tutte_categorie:
                colori[cat] = f'#{random.randint(50,200):02x}{random.randint(50,200):02x}{random.randint(50,200):02x}'
            canvas2.delete("all")
            canvas2.update_idletasks()
            disegna_barre_categorie(canvas2, tutte_categorie, colori)
            mostra_legenda_categorie(tab2, tutte_categorie, colori)

        def aggiorna_tab1(event=None):
            anno_selezionato = selettore_anno1.get()
            entrate = defaultdict(float)
            uscite = defaultdict(float)
            for data, voci in self.spese.items():
                anno = data.year
                mese = data.month
                if anno_selezionato != "Tutti" and str(anno) != anno_selezionato:
                    continue
                for voce in voci:
                    tipo = voce[3].strip().lower()
                    importo = voce[2]
                    if anno_selezionato == "Tutti":
                        chiave = str(anno)
                    else:
                        chiave = mese
                    if tipo == "entrata":
                        entrate[chiave] += importo
                    elif tipo == "uscita":
                        uscite[chiave] += importo
            total_entrate = sum(entrate.values())
            total_uscite = sum(uscite.values())
            saldo = total_entrate - total_uscite
            lbl_entrate.config(text=f"Entrate: € {total_entrate:,.2f}")
            lbl_uscite.config(text=f"Uscite: € {total_uscite:,.2f}")
            if saldo >= 0:
                lbl_saldo.config(text=f"Saldo: € {saldo:,.2f}", fg="green")
            else:
                lbl_saldo.config(text=f"Saldo: € {saldo:,.2f}", fg="red")
            grafico = {}
            colore = {}
            if anno_selezionato == "Tutti":
                for anno in sorted(set(entrate.keys()) | set(uscite.keys())):
                    grafico[f"{anno} Entrata"] = entrate[anno]
                    grafico[f"{anno} Uscita"] = uscite[anno]
                    colore[f"{anno} Entrata"] = "green"
                    colore[f"{anno} Uscita"] = "red"
                disegna_barre(canvas1, grafico, colore, mostra_anno=True, mostra_tipo=True, centro=False)
            else:
                mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
                for m in range(1, 13):
                    nome_mese = mesi[m - 1]
                    grafico[f"{nome_mese} Entrata"] = entrate.get(m, 0)
                    grafico[f"{nome_mese} Uscita"] = uscite.get(m, 0)
                    colore[f"{nome_mese} Entrata"] = "green"
                    colore[f"{nome_mese} Uscita"] = "red"
                disegna_barre(canvas1, grafico, colore, mostra_anno=False, mostra_tipo=True, centro=False)

        larghezza_finestra = 1200
        altezza_finestra = 600
        larghezza_schermo = self.winfo_screenwidth()
        altezza_schermo = self.winfo_screenheight()
        x = (larghezza_schermo // 2) - (larghezza_finestra // 2)
        y = (altezza_schermo // 2) - (altezza_finestra // 2)
        popup = tk.Toplevel(self)
        popup.title("Grafico Analisi Spese")
        popup.geometry(f"{larghezza_finestra}x{altezza_finestra}+{x}+{y}")
        popup.bind("<Escape>", lambda e: popup.destroy())
        notebook = ttk.Notebook(popup)
        notebook.pack(fill="both", expand=True)
        anni = sorted({d.year for d in self.spese.keys()}, reverse=True)
        anno_corrente = str(datetime.date.today().year)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Entrate/Uscite")
        frame_totali = ttk.Frame(tab1)
        frame_totali.pack(side="bottom", pady=10)
        lbl_entrate = tk.Label(frame_totali, text="Entrate: € 0.00", fg="green", font=("Arial", 10, "bold"))
        lbl_entrate.pack(side="left", padx=10)
        lbl_uscite = tk.Label(frame_totali, text="Uscite: € 0.00", fg="red", font=("Arial", 10, "bold"))
        lbl_uscite.pack(side="left", padx=10)
        lbl_saldo = tk.Label(frame_totali, text="Saldo: € 0.00", font=("Arial", 10, "bold"))
        lbl_saldo.pack(side="left", padx=10)
        tk.Label(tab1, text="■ Seleziona periodo *Dettaglio (Clicca 🖱️)*", fg="green", font=("Arial", 10)).pack(side="top", padx=10)
        selettore_anno1 = ttk.Combobox(tab1, values=["Tutti"] + [str(a) for a in anni], state='readonly')
        selettore_anno1.set("Tutti")
        selettore_anno1.pack(pady=10)
        selettore_anno1.bind("<<ComboboxSelected>>", aggiorna_tab1)
        canvas1 = tk.Canvas(tab1, bg="white")
        canvas1.pack(fill="both", expand=True, padx=10, pady=10)
        canvas1.bind("<Configure>", lambda e: aggiorna_tab1())

        tab2 = ttk.Frame(notebook)
        tab2.grid_columnconfigure(0, weight=4) 
        tab2.grid_columnconfigure(1, weight=1) 
        tab2.grid_rowconfigure(1, weight=1) 
        notebook.add(tab2, text="Categorie")
        tk.Label(tab2, text="■ Seleziona periodo *Dettaglio (Clicca 🖱️)*", fg="green", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        selettore_anno2 = ttk.Combobox(tab2, values=["Tutti"] + [str(a) for a in anni], state='readonly')
        selettore_anno2.set(anno_corrente if anno_corrente in [str(a) for a in anni] else "Tutti") 
        selettore_anno2.grid(row=0, column=0, sticky="n", pady=10) 
        selettore_anno2.bind("<<ComboboxSelected>>", aggiorna_tab2)
        canvas_frame_scroll = ttk.Frame(tab2)
        canvas_frame_scroll.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=(0, 10)) 
        scrollbar_h = ttk.Scrollbar(canvas_frame_scroll, orient="horizontal")
        scrollbar_h.pack(side="bottom", fill="x")
        canvas2 = tk.Canvas(
            canvas_frame_scroll, 
            bg="white",
            xscrollcommand=scrollbar_h.set 
        )
        canvas2.pack(side="top", fill="both", expand=True)
        scrollbar_h.config(command=canvas2.xview)
        
        canvas2.tooltip = None
        canvas2.anno_corrente = selettore_anno2.get()
        canvas2.bind("<Configure>", lambda e: aggiorna_tab2())
        aggiorna_tab2() 
        
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Saldo Mensile/Annuale")
        frame_totali_tab3 = ttk.Frame(tab3)
        frame_totali_tab3.pack(side="bottom", pady=10)
        self.lbl_entrate_tab3 = tk.Label(frame_totali_tab3, text="Entrate: € 0.00", fg="green", font=("Arial", 10, "bold"))
        self.lbl_entrate_tab3.pack(side="left", padx=10)
        self.lbl_uscite_tab3 = tk.Label(frame_totali_tab3, text="Uscite: € 0.00", fg="red", font=("Arial", 10, "bold"))
        self.lbl_uscite_tab3.pack(side="left", padx=10)
        self.lbl_saldo_tab3 = tk.Label(frame_totali_tab3, text="Saldo: € 0.00", font=("Arial", 10, "bold"))
        self.lbl_saldo_tab3.pack(side="left", padx=10)
        tk.Label(tab3, text="■ Seleziona periodo", fg="green", font=("Arial", 10)).pack(side="top", padx=10)
        selettore_anno3 = ttk.Combobox(tab3, values=["Tutti"] + [str(a) for a in anni], state='readonly')
        selettore_anno3.set(anno_corrente if anno_corrente in [str(a) for a in anni] else "Tutti")
        selettore_anno3.pack(pady=10)
        selettore_anno3.bind("<<ComboboxSelected>>", aggiorna_tab3)
        canvas3 = tk.Canvas(tab3, bg="white")
        canvas3.pack(fill="both", expand=True, padx=10, pady=10)
        canvas3.bind("<Configure>", lambda e: aggiorna_tab3())
        aggiorna_tab3()

    def mostra_transazioni_popup(self, data_filter, title):

        anno = data_filter.get("anno")
        mese = data_filter.get("mese")
        categoria = data_filter.get("categoria")
        tipo = data_filter.get("tipo")
        spese_filtrate = []
        for data, voci in self.spese.items():
            if anno and anno != "Tutti" and str(data.year) != anno:
                continue
            if mese and anno != "Tutti" and data.month != mese:
                continue
            for entry in voci:
                try:
                    cat, desc, imp, entry_tipo = entry[:4]
                    entry_imp = float(imp)
                    entry_tipo = entry_tipo.strip()
                except Exception:
                    continue
                if categoria and cat != categoria:
                    continue
                if tipo and entry_tipo != tipo:
                    continue
                spese_filtrate.append((data, cat, desc, entry_imp, entry_tipo))
        if not spese_filtrate:
            self.show_custom_info("Nessuna transazione", f"Nessuna transazione trovata per {title}.")
            return
        
        popup_width, popup_height = 800, 450
        popup = tk.Toplevel(self)
        popup.title(f"Dettaglio Transazioni - {title}")
        popup.resizable(True, True)
        popup.withdraw() 
        self.update_idletasks()
        main_x = self.winfo_rootx()
        main_y = self.winfo_rooty()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        center_x = main_x + (main_width // 2) - (popup_width // 2)
        center_y = main_y + (main_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup.transient(self)
        popup.deiconify() 
        popup.lift()
        popup.focus_force()
        popup.bind("<Escape>", lambda event: popup.destroy()) 
        tk.Label(popup, text=title, font=("Arial", 12, "bold")).pack(pady=10)
        columns = ("Data", "Categoria", "Descrizione", "Importo", "Tipo")
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=10)
        tree.pack(fill="both", expand=True, padx=10, pady=6)
        widths = (90, 150, 250, 100, 100)
        anchors = ("center", "w", "w", "e", "center")
        for col, w, a in zip(columns, widths, anchors):
            initial_reverse = True if col == "Data" else False
            tree.heading(
                col, 
                text=col, 
                command=lambda c=col: self.treeview_sort_column(tree, c, initial_reverse)
            )
            tree.column(col, width=w, anchor=a)
        tot_entrate = tot_uscite = 0.0
        for d, cat, desc, imp, tipo in sorted(spese_filtrate, key=lambda x: x[0], reverse=True):
            tag_name = "green_row" if tipo == "Entrata" else "red_row"
            tree.insert("", "end", values=(d.strftime("%d-%m-%Y"), cat, desc, f"{imp:.2f} €", tipo), tags=(tag_name,))
            if tipo == "Entrata":
                tot_entrate += imp
            else:
                tot_uscite += imp
        tree.tag_configure("green_row", foreground="green")
        tree.tag_configure("red_row", foreground="red")
        saldo = tot_entrate - tot_uscite
        lbl = tk.Label(popup, font=("Arial", 10, "bold"))
        lbl.pack(pady=5)
        saldo_color = "green" if saldo >= 0 else "red"
        lbl.config(text=f"Totale Entrate: {tot_entrate:,.2f} € | Totale Uscite: {tot_uscite:,.2f} € | Saldo: {saldo:,.2f} €", fg=saldo_color)
        tree.bind("<Double-1>", lambda evt: self.goto_day_from_popup(tree, popup))
        ttk.Button(popup, text="❌ Chiudi", command=popup.destroy, style="Giallo.TButton").pack(pady=10)


    def mostra_help(self):
        if hasattr(self, '_filter_help_popup') and self._filter_help_popup.winfo_exists():
            self._filter_help_popup.destroy()
        popup_aiuto = tk.Toplevel(self)
        popup_aiuto.title("❓ Aiuto: Filtri, Tabelle e Grafici")
        popup_aiuto.geometry("1200x600") 
        popup_aiuto.resizable(False, False)
        popup_aiuto.transient(self)
        self._filter_help_popup = popup_aiuto
        stile = ttk.Style()
        main_frame = ttk.Frame(popup_aiuto, padding="15")
        main_frame.pack(fill="both", expand=True)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        tk.Label(
            content_frame, 
            text="Filtri Temporali: Controllano l'Aggregazione dei Dati nella Tabella Statistiche.",
            font=("Arial", 11, "bold"),
            anchor='w'
        ).pack(pady=(5, 15), fill='x')
        help_content = [
            ("Totali ", "Aggrega e mostra il totale per categoria per TUTTO il periodo storico disponibile."),
            ("Anno ", "Aggrega i dati dell'ANNO selezionato, mostrando le singole categorie totalizzate"),
            ("Mese ", "Aggrega i dati del MESE selezionato, mostrando le singole categorie totalizzate "),
            ("Giorno (Punto Singolo)", "Mostra le spese solo per il GIORNO selezionato."),
        ]
        for title, description in help_content:
            title_label = tk.Label(
                content_frame, 
                text=f"• Filtro {title}:",
                font=("Arial", 10, "bold"),
                justify=tk.LEFT,
                anchor='w'
            )
            title_label.pack(fill='x', pady=(5, 0))
            desc_label = tk.Label(
                content_frame, 
                text=f"{description}",
                font=("Arial", 9),
                justify=tk.LEFT,
                anchor='w',
                wraplength=1150
            )
            desc_label.pack(fill='x', padx=15, pady=(0, 5))
        tk.Label(
            content_frame, 
            text="\nInterazioni con le Tabelle Dati (Treeview):",
            font=("Arial", 11, "bold"),
            anchor='w'
        ).pack(pady=(10, 5), fill='x')
        tk.Label(
            content_frame,
            text="• **Scroll e Navigazione:** Utilizza la **Rotella del Mouse** per scorrere verticalmente in qualsiasi Treeview o area.\n"
                 "• **Ordinamento (Sort):** Clicca sull'intestazione di qualsiasi colonna per ordinare i dati in base a quella colonna. Clicca di nuovo per invertire (crescente/decrescente).",
            font=("Arial", 9),
            justify=tk.LEFT,
            anchor='w'
        ).pack(fill='x', padx=5, pady=(0, 5))
        tk.Label(
            content_frame,
            text="• **Dettaglio Transazioni:**\n"
                 "  1. Doppio Clic sulla riga (Treeview Statistiche): Apre il pop-up con il **Dettaglio** di tutte le transazioni aggregate.\n"
                 "  2. Doppio Clic sulla riga (Popup Dettaglio): **Seleziona la riga** della transazione e ti reindirizza automaticamente alla transazione corrispondente nella Treeview principale.",
            font=("Arial", 9),
            justify=tk.LEFT,
            anchor='w'
        ).pack(fill='x', padx=5, pady=(0, 5))
        tk.Label(
            content_frame, 
            text="\nAvvio e Interazioni del Grafico a Barre:",
            font=("Arial", 11, "bold"),
            anchor='w'
        ).pack(pady=(10, 5), fill='x')
        tk.Label(
            content_frame,
            text="• **Navigazione Grafici Treeview :** Usa le **Frecce Destra/Sinistra** per scorrere tra le diverse visualizzazioni (Tabella, Grafico, Mensile, Saldo). Premi **ESC** per tornare alla Treeview\n""• **Dettaglio Spesa (Drill-Down):** Doppio Clic su una barra del grafico per aprire il dettaglio delle transazioni relative a quel periodo (Giorno/Mese).\n""• **Avvio Grafico Multiplo :** Dopo aver selezionato una o più categorie dalla Treeview (usando **CTRL/SHIFT**), clicca con il **Tasto Destro** del mouse sulle righe selezionate per avviare il grafico.\n"
     "• **Dettaglio Grafico (Tooltip):** Passa il mouse sopra una barra per visualizzare un **Tooltip** che mostra il totale e il **dettaglio delle singole categorie** aggregate in quella barra.\n"
     "• **Dettaglio Spesa (Drill-Down):** Doppio Clic su una barra del grafico per aprire il dettaglio delle transazioni relative a quel periodo (Giorno/Mese). Da questo pop-up, un ulteriore\n   **Doppio Clic** sulla transazione ti porta alla spesa nella Treeview principale e imposta il giorno nel Calendario.",
            font=("Arial", 9),
            justify=tk.LEFT,
            anchor='w'
        ).pack(fill='x', padx=5)
        bottom_frame = ttk.Frame(popup_aiuto)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 15), padx=15) 
        
        ttk.Button(
            bottom_frame, 
            text="Ho Capito (OK)", 
            command=popup_aiuto.destroy,
            style="Giallo.TButton" 
        ).pack(pady=5, padx=10) 
        popup_aiuto.bind("<Escape>", lambda e: popup_aiuto.destroy())

    def show_info_app(self):
        
        def apri_email(event):
            webbrowser.open("mailto:helpcasafacilepro@gmail.com")

        def apri_link_python(event):
            webbrowser.open("https://www.python.org/downloads/")

        info_win = tk.Toplevel(self)
        info_win.title("Informazioni sull'applicazione e Interazioni")
        info_win.resizable(False, False)

        text = tk.Text(info_win, wrap="word", bg="white", font=("Courier New", 10))
        text.pack(fill="both", expand=True, padx=20, pady=10)
        text.insert("end", f"{NAME}  ", "titolo")
        text.insert("end", f"Versione v.{VERSION}\n", "versione")
        text.insert("end", "© 2025 Casa Facile Pro - Sviluppo Python/Tkinter (2023-2025)    ")
        text.insert("end", "Email Supporto: ")
        text.insert("end", "helpcasafacilepro@gmail.com\n", "email")
        text.insert("end", "Progetto Python: ")
        text.insert("end", "https://www.python.org/downloads/\n", "link")
        text.insert("end", "\n──────────────── FUNZIONALITÀ PRINCIPALI ────────────────\n", "sezione")
        text.insert("end", "• Inserimento, modifica e cancellazione di spese ed entrate per categoria.\n")
        text.insert("end", "• Gestione Categorie personalizzate e Ricorrenze (spese/entrate ripetute).\n")
        text.insert("end", "• Riepilogo e Analisi: Giornaliere, Mensili, Annuali, Totali, Grafici, Bonus Time Machine, e Confronta.\n")
        text.insert("end", "• Esportazione Dati e Riepilogo dettagliato in formato stampabile (Giorno, Mese, Anno, Utenze).\n")
        text.insert("end", "• Strumenti Integrati: Saldo Conto, Calcolatrice, Rubrica, Gestione Utenze, Cerca, Report Finanziamenti.\n")
        text.insert("end", "• Database: Backup (Automatico e Manuale) , Import/Export database e Reset.\n")
        text.insert("end", "• L'applicazione integra un WebServer sulla porta 8081 per consentire l'accesso remoto ai dati.\n")
        text.insert("end", "  Questo accesso è protetto da password per garantirne la sicurezza, consentendo la gestione dell'app tramite\n  browser (PC, SMARTPHONE) solo agli utenti autorizzati.\n")
        text.insert("end", "• Calendario interattivo con caselle colorate che indicano l'attività del giorno.\n")
        text.insert("end", "\nIl tasto Esc chiude istantaneamente qualsiasi finestra secondaria aperta.\n" "Dopo 5 minuti di inattività, la finestra principale viene iconizzata e un popup di notifica appare ogni 5 minuti; ")
        text.insert("end", "\npassando il mouse sull'icona o sul popup, l'applicazione si riapre.\n")
        text.insert("end", "\n──────────────── INTERAZIONE TABELLE DATI ────────────────\n", "sezione")
        text.insert("end", "Le tabelle che mostrano le tue operazioni (Treeview) sono progettate per l'efficienza:\n\n")
        text.insert("end", "1. Ordinamento delle Colonne (Sortby):\n", "sottosezione")
        text.insert("end", "   • Clicca sull'intestazione di qualsiasi colonna (Data, Importo, Categoria, tipo, descrizione) per ordinare i dati.\n")
        text.insert("end", "   • L'ordinamento gestisce correttamente date e numeri, e alterna la direzione (Ascendente/Discendente).\n\n")
        text.insert("end", "   • Funzione Universale (Dettaglio): Fai doppio click su una riga in **Qualsiasi Treeview**\n     (es. Ricorrenze, Report Mese Dettagliato, Mese/Anno Totali, Grafici, etc.) per ottenere l'azione di dettaglio logica\n     per quel contesto. Ad esempio, aprire il dettaglio del record in un *sottomenu* o visualizzare la sua posizione\n     nel Treeview principale.\n")
        text.insert("end", "2. Scorrimento con Mouse (Scroll):\n", "sottosezione")
        text.insert("end", "   • Tutte le tabelle e le aree di testo scorribili supportano lo scorrimento **ovunque** tramite la rotella del mouse,\n     senza la necessità di cliccare prima sulla barra di scorrimento.\n\n")
        text.tag_config("titolo", foreground="darkblue", font=("Courier New", 12, "bold"))
        text.tag_config("versione", foreground="blue", font=("Courier New", 10, "italic"))
        text.tag_config("sezione", foreground="darkgreen", font=("Courier New", 10, "bold"))
        text.tag_config("sottosezione", foreground="darkorange", font=("Courier New", 10, "bold"))
        
        text.tag_config("email", foreground="blue", underline=1)
        text.tag_bind("email", "<Button-1>", apri_email)
        
        text.tag_config("link", foreground="blue", underline=1)
        text.tag_bind("link", "<Button-1>", apri_link_python)

        text.config(state="disabled")    

        btn_aggiorna = ttk.Button(info_win, text="🔄 Aggiorna Software", command=lambda: self.aggiorna(GITHUB_FILE_URL, NOME_FILE), style='Verde.TButton')
        btn_aggiorna.pack(side="left", padx=100, pady=10)

        btn_chiudi = ttk.Button(info_win, text="❌ Chiudi", command=info_win.destroy, style='Giallo.TButton')
        btn_chiudi.pack(side="right", padx=100, pady=10)

        info_win.withdraw()
        info_win.update_idletasks()
        min_w, min_h = 1160, 650
        w = max(info_win.winfo_width(), min_w)
        h = max(info_win.winfo_height(), min_h)
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (h // 2)
        info_win.geometry(f"{w}x{h}+{x}+{y}")
        #info_win.grab_set()
        info_win.transient(self)
        info_win.focus_set()
        info_win.deiconify()
        
        info_win.bind("<Escape>", lambda e: info_win.destroy())
        
    def save_db_and_notify(self):
            self.save_db()
            self.show_custom_warning("Attenzione", "Dati Salvati correttamente !")
          
    def check_UTENZE_DB(self):
         if not os.path.exists(UTENZE_DB):
            with open(UTENZE_DB, "w") as file:
                file.write("")  
                self.utenze()

    def update_file_date(self):
            now_timestamp = datetime.datetime.now().timestamp()
            os.utime(UTENZE_DB, (now_timestamp, now_timestamp))  

    def utenze(self):
        self.check_UTENZE_DB()
        def get_consumi_per_anno(anno):
            return {
                "Acqua": [(f"{m:02d}/{anno}", 0.0, 0.0, 0.0) for m in range(1, 13)],
                "Luce":  [(f"{m:02d}/{anno}", 0.0, 0.0, 0.0) for m in range(1, 13)],
                "Gas":   [(f"{m:02d}/{anno}", 0.0, 0.0, 0.0) for m in range(1, 13)],
            }

        utenze = ["Acqua", "Luce", "Gas"]

        def carica_db():
            if os.path.exists(UTENZE_DB):
                try:
                    with open(UTENZE_DB, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    letture = data.get("letture_salvate", {u: {} for u in utenze})
                    for utenza, per_anno in letture.items():
                        for anno, righe in per_anno.items():
                            letture_norm = []
                            for r in righe:
                                if len(r) == 4:
                                   mese, prec, att, _ = r
                                   try:
                                       consumo = max(0.0, float(att) - float(prec))
                                   except:
                                       prec, att, consumo = 0.0, 0.0, 0.0
                                       letture_norm.append((mese, prec, att, consumo))
                                else:
                                   letture_norm.append(tuple(r))
                                   letture[utenza][anno] = letture_norm

                    anagrafiche = data.get("anagrafiche", {u: {
                        "Ragione sociale": "",
                        "Telefono": "",
                        "Email": "",
                        "Numero contratto": "",
                        "POD": "",
                        "Note": ""
                    } for u in utenze})
                    for utenza in utenze:
                        if utenza not in anagrafiche:
                            anagrafiche[utenza] = {
                                "Ragione sociale": "",
                                "Telefono": "",
                                "Email": "",
                                "Numero contratto": "",
                                "POD": "",
                                "Note": ""
                            }
                        else:
                            for campo in ["Ragione sociale", "Telefono", "Email", "Numero contratto", "POD", "Note"]:
                                if campo not in anagrafiche[utenza]:
                                    anagrafiche[utenza][campo] = ""
                    return letture, anagrafiche
                except Exception as e:
                  
                    return {u: {} for u in utenze}, {u: {
                        "Ragione sociale": "",
                        "Telefono": "",
                        "Email": "",
                        "Numero contratto": "",
                        "POD": "",
                        "Note": ""
                    } for u in utenze}
            else:
                return {u: {} for u in utenze}, {u: {
                    "Ragione sociale": "",
                    "Telefono": "",
                    "Email": "",
                    "Numero contratto": "",
                    "POD": "",
                    "Note": ""
                } for u in utenze}


        def scrivi_db():
            try:
                data = {
                    "letture_salvate": {
                        u: {a: [list(r) for r in anni] for a, anni in letture_salvate[u].items()}
                        for u in utenze
                    },
                    "anagrafiche": anagrafiche
                }
                with open(UTENZE_DB, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=1, ensure_ascii=False)
            except Exception as e:
                 self.show_custom_warning("Errore", "Errore scrittura dati")
 
        letture_salvate, anagrafiche = carica_db()
        self.letture_salvate_utenze = letture_salvate
        self.anagrafiche_salvate_utenze = anagrafiche

        anno_corrente = str(datetime.datetime.now().year)
        year_current = int(anno_corrente)
        
        anni = [str(a) for a in range(year_current, year_current-11, -1)]

        consumi = get_consumi_per_anno(anno_corrente)

        win = tk.Toplevel(self)
        win.withdraw() 
        larghezza = 1200
        altezza = 660
        self.update_idletasks()
        self_x = self.winfo_rootx()
        self_y = self.winfo_rooty()
        self_width = self.winfo_width()
        self_height = self.winfo_height()
        x = self_x + (self_width // 2) - (larghezza // 2)
        y = self_y + (self_height // 2) - (altezza // 2)
        win.geometry(f"{larghezza}x{altezza}+{x}+{y}")
        win.title("Gestione Consumi Utenze")
        #win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        win.deiconify() 

        menu_win = tk.Menu(win, background="black", foreground="white")
        # Menu "Opzioni"
        menu_funzioni = tk.Menu(menu_win, tearoff=0)
        menu_funzioni.add_command(label="📂 Esporta Preview", command=lambda: esporta_preview())
        menu_funzioni.add_command(label="⚙️ Analizza", command=lambda: crea_tabella_consumi(win, UTENZE_DB))
        menu_funzioni.add_separator()
        menu_funzioni.add_command(label="❌ Chiudi", command=win.destroy)
        menu_win.add_cascade(label="📂 Opzioni", menu=menu_funzioni)

        # Menu "Database"
        menu_database = tk.Menu(menu_win, tearoff=0)
        menu_database.add_command(label="📤 Esporta DB", command=lambda: esporta_letture_data(UTENZE_DB))
        menu_database.add_command(label="📥 Importa DB", command=lambda: importa_letture_data(letture_salvate, anagrafiche))
        menu_win.add_cascade(label="🗄️ Database", menu=menu_database)

        win.config(menu=menu_win)

        win.bind("<Escape>", lambda e: win.destroy())

        top_controls = ttk.Frame(win)
        top_controls.pack(pady=(0, 6))
        ttk.Label(top_controls, text="Gestione Consumi Utenze", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=(0, 25))
        ttk.Label(top_controls, text="Anno: ").pack(side=tk.LEFT)
        anno_var = tk.StringVar(value=anno_corrente)

        def salva_letture_preview(txt, preview_win):
            now = datetime.date.today()
            default_filename = f"Letture_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
            preview_win.wm_attributes('-topmost', 1)
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File txt", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=default_filename,
                title="Salva Preview",
                confirmoverwrite=False,
                parent=preview_win)
            preview_win.wm_attributes('-topmost', 0)
            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return 

                with open(file, "w", encoding="utf-8") as f:
                    lines = txt.get("1.0", tk.END)
                    f.write(lines)
                preview_win.destroy()
                self.show_custom_warning("Esportazione completata", f"Riepilogo esportate in\n{file}")
        
        def esporta_preview():
            preview_win = tk.Toplevel(win)
            preview_win.title("Preview Esportazione")
            preview_win.geometry("1050x600")
            screen_width = preview_win.winfo_screenwidth()
            screen_height = preview_win.winfo_screenheight()
            x = (screen_width - 1050) // 2
            y = (screen_height - 600) // 2
            preview_win.geometry(f"1050x600+{x}+{y}")
            preview_win.after(10, lambda: preview_win.focus_force())

            txt = tk.Text(preview_win, font=("Courier New", 10), wrap="none")
            txt.pack(fill=tk.BOTH, expand=True)

            anno_x = anno_var.get()
            txt.insert(tk.END, f"Consumi utenze per anno {anno_x}\n\n")

            header = f"{'Mese':<10}"
            for utenza in utenze:
                header += f"{utenza:^30}"
            txt.insert(tk.END, header + "\n")

            sub_header = f"{'':<10}"
            for _ in utenze:
                sub_header += f"{'Prec':>8}{'Att':>10}{'Cons':>10}  "
            txt.insert(tk.END, sub_header + "\n")
            txt.insert(tk.END, "-" * len(header) + "\n")

            mesi = [self.trees[utenze[0]].item(iid)['values'][0] for iid in self.trees[utenze[0]].get_children()]
            for i, mese in enumerate(mesi):
                riga = f"{mese:<10}"
                for utenza in utenze:
                    values = self.trees[utenza].item(self.trees[utenza].get_children()[i])['values']
                    prec, att, cons = float(values[1]), float(values[2]), float(values[3])
                    riga += f"{prec:8.2f}{att:10.2f}{cons:10.2f}  "
                txt.insert(tk.END, riga + "\n")

            txt.insert(tk.END, "-" * len(header) + "\n")

            tot_riga = f"{'Totale':<10}"
            for utenza in utenze:
                somma = sum(float(self.trees[utenza].item(iid)['values'][3]) for iid in self.trees[utenza].get_children())
                tot_riga += f"{'':8}{'':10}{somma:10.2f}  "
            txt.insert(tk.END, tot_riga + "\n")

            txt.config(state="disabled")

            btn_frame = ttk.Frame(preview_win)
            btn_frame.pack(fill=tk.X, pady=12)
            ttk.Button(btn_frame, text="💾 Salva", command=lambda: salva_letture_preview(txt, preview_win), style="Verde.TButton").pack(side=tk.LEFT, padx=10)
            ttk.Button(btn_frame, text="❌ Chiudi", command=preview_win.destroy, style="Giallo.TButton").pack(side=tk.RIGHT, padx=10)

            preview_win.lift()
            preview_win.attributes('-topmost', True)
            preview_win.after(200, lambda: preview_win.attributes('-topmost', False))

            preview_win.bind("<Escape>", lambda e: preview_win.destroy())

        def chiudi():
            win.destroy()

        def cambia_anno(*args):
            nonlocal consumi
            for utenza in utenze:
                if self.trees[utenza].get_children():
                    anno_attuale = self.trees[utenza].item(self.trees[utenza].get_children()[0])['values'][0].split("/")[1]
                    letture_salvate[utenza][anno_attuale] = [
                        tuple(self.trees[utenza].item(iid)['values']) for iid in self.trees[utenza].get_children()
                    ]
            scrivi_db()
            for utenza in utenze:
                self.trees[utenza].delete(*self.trees[utenza].get_children())
            anno_sel = anno_var.get()
            consumi = get_consumi_per_anno(anno_sel)
            for utenza in utenze:
                if (anno_sel not in letture_salvate[utenza]) or (not letture_salvate[utenza][anno_sel]):
                    letture_salvate[utenza][anno_sel] = [
                        (f"{m:02d}/{anno_sel}", 0.0, 0.0, 0.0) for m in range(1, 13)
                    ]
                righe = letture_salvate[utenza][anno_sel]
                righe_norm = []
                for r in righe:
                    if len(r) == 4:
                        mese, prec, att, consumo = r
                        consumo = max(0.0, float(att) - float(prec))
                        righe_norm.append((mese, float(prec), float(att), float(consumo)))
                    else:
                        righe_norm.append(tuple(r))
                letture_salvate[utenza][anno_sel] = righe_norm
                for mese, prec, att, consumo in righe_norm:
                    self.trees[utenza].insert("", "end", values=(mese, float(prec), float(att), float(consumo)))

        anno_cb = ttk.Combobox(top_controls, values=anni, textvariable=anno_var, state="readonly", width=8)
        anno_cb.pack(side=tk.LEFT)
        
        def reset_anno():
            anno_var.set(anno_corrente)
        style = ttk.Style()

        ttk.Button(top_controls, text="🔄", style="Giallo.TButton", width=2, command=reset_anno).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_controls, text="❌ Chiudi", style="Giallo.TButton", command=chiudi).pack(side=tk.LEFT, padx=7)
        anno_var.trace_add("write", cambia_anno)

        main_frame = ttk.Frame(win)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=6)
        for c in range(len(utenze)):
            main_frame.grid_columnconfigure(c, weight=1)

        colori = {"Acqua": "#ccefff", "Luce": "#fff9cc", "Gas": "#ffe0cc"}
        self.trees = {}
        anag_entries = {}

        def importa_letture_data(letture_salvate, anagrafiche):
            now = datetime.date.today()
            default_dir = EXP_DB
            default_filename = f"Letture_import_{now.day:02d}-{now.month:02d}-{now.year}.json"
            file = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("File JSON", "*.json")],
                initialdir=default_dir,
                initialfile=default_filename,
                title="Importa utenze",
            )
            if file:
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    letture = data.get("letture_salvate", {})
                    anagrafiche = data.get("anagrafiche", {})
                    self.letture_salvate_utenze.update(letture)
                    self.anagrafiche_salvate_utenze.update(anagrafiche)
                    self.show_custom_warning("Importazione riuscita", "Utenze importate correttamente!")
                except Exception as e:
                    self.show_custom_warning("Errore", f"Errore durante l'importazione:\n{e}")

        def esporta_letture_data(UTENZE_DB):
            now = datetime.date.today()
            default_dir = EXP_DB
            default_filename = f"Letture_Export_{now.day:02d}-{now.month:02d}-{now.year}.json"
            file = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("File JSON", "*.json")],
                initialdir=default_dir,
                initialfile=default_filename,
                confirmoverwrite=False,
                title="Esporta utenze",
            )
            
            if file:
                try:
                    data = {
                        "letture_salvate": self.letture_salvate_utenze,
                        "anagrafiche": self.anagrafiche_salvate_utenze
                    }
                    with open(file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    self.show_custom_warning("Esportazione completata", f"Database utenze salvato in:\n{file}")
                except Exception as e:
                    self.show_custom_warning("Errore", f"Errore durante l'esportazione:\n{e}")

        def crea_tabella_consumi(parent, UTENZE_DB):
            try:
                with open(UTENZE_DB, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    letture_salvate = data.get("letture_salvate", {})
            except Exception as e:
                print(f"❌ Errore lettura file: {e}")
                return

            utenze = ["Acqua", "Luce", "Gas"]
            win = tk.Toplevel(parent)
            win.bind("<Escape>", lambda e: win.destroy())

            win.title("Consumi Utenze - Anteprima")
            win.geometry("1150x600")
            win.transient(parent)
            win.grab_set()

            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()
            x_coordinate = (screen_width - 1150) // 2
            y_coordinate = (screen_height - 600) // 2
            win.geometry(f"1150x600+{x_coordinate}+{y_coordinate}")

            frame_principale = ttk.Frame(win)
            frame_principale.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            canvas = tk.Canvas(frame_principale)
            scrollbar = ttk.Scrollbar(frame_principale, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            frame_interno = ttk.Frame(canvas)
            canvas_window = canvas.create_window((0, 0), window=frame_interno, anchor="nw")

            def aggiorna_scrollregion(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=canvas.winfo_width())

            frame_interno.bind("<Configure>", aggiorna_scrollregion)

            for utenza in utenze:
                frame_tabella = ttk.Frame(frame_interno)
                frame_tabella.pack(fill=tk.BOTH, expand=True, pady=10)

                ttk.Label(
                    frame_tabella,
                    text=f"Consumi {utenza}",
                    font=("Arial", 12, "bold")
                ).pack(pady=5)

                colonne = [
                    "Anno", "Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                    "Lug", "Ago", "Set", "Ott", "Nov", "Dic", "Totale"
                ]
                tree = ttk.Treeview(
                    frame_tabella,
                    columns=colonne,
                    show="headings",
                    height=4
                )

                for col in colonne:
                    tree.heading(col, text=col)
                    tree.column(col, width=80, anchor="center")

                tree.pack(fill=tk.BOTH, expand=True)

                for anno in sorted(letture_salvate.get(utenza, {}).keys(), reverse=True):
                    row = [anno]
                    tot_consumi = 0.0
                    for mese in range(1, 13):
                        mese_str = f"{mese:02d}/{anno}"
                        consumo = sum(
                            float(r[3])
                            for r in letture_salvate.get(utenza, {}).get(anno, [])
                            if r[0] == mese_str
                        )
                        row.append(consumo)
                        tot_consumi += consumo
                    row.append(tot_consumi)
                    tree.insert("", tk.END, values=row)

            frame_bottoni = ttk.Frame(win)
            frame_bottoni.pack(fill=tk.X, padx=10, pady=10)
            ttk.Button(frame_bottoni, text="💾 Salva", style="Verde.TButton", command=lambda: salva_dati_letture(letture_salvate)).pack(side=tk.LEFT, padx=10)
            ttk.Button(frame_bottoni, text="❌ Chiudi", style="Giallo.TButton", command=win.destroy).pack(side=tk.RIGHT, padx=10)
            

        def salva_dati_letture(letture_salvate):
            win.focus_force()
            now = datetime.date.today()
            default_filename = f"Letture_anno_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File txt", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=default_filename,
                confirmoverwrite=False,
                title="Salva i dati dei consumi"
               )

            if file_path:
                if os.path.exists(file_path):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file_path)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return

            if not file_path:
                return

            mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    for utenza, anni in letture_salvate.items():
                        f.write(f"Consumi {utenza}:\n")
                        intestazione = f"{'Anno':>6} " + "".join([f"{mese:>8}" for mese in mesi]) + f"{'Totale':>10}\n"
                        f.write(intestazione)
                        f.write("-" * len(intestazione) + "\n")

                        for anno in sorted(anni.keys(), reverse=True):
                            valori_mensili = {r[0]: float(r[3]) for r in anni[anno]}
                            riga = f"{anno:>6} "
                            totale = 0.0
                            for m in range(1, 13):
                                mese_str = f"{m:02d}/{anno}"
                                consumo = valori_mensili.get(mese_str, 0.0)
                                riga += f"{consumo:8.2f}"
                                totale += consumo
                            riga += f"{totale:10.2f}\n"
                            f.write(riga)

                        f.write("\n")

                self.show_custom_warning("Esportazione", f"Riepilogo esportato correttamente in:\n{file_path}")
            except Exception as e:
                self.show_custom_warning("Errore", f"Errore durante il salvataggio:\n{e}")

        def centra_su_padre(finestra, padre):
            padre.update_idletasks()
            larghezza = finestra.winfo_reqwidth()
            altezza = finestra.winfo_reqheight()
            px = padre.winfo_rootx() + (padre.winfo_width() // 2) - (larghezza // 2)
            py = padre.winfo_rooty() + (padre.winfo_height() // 2) - (altezza // 2)
            finestra.geometry(f"+{px}+{py}")

        def salva_letture_utenza(utenza):
            anno_sel = anno_var.get()
            letture_salvate[utenza][anno_sel] = [
                tuple(self.trees[utenza].item(iid)['values']) for iid in self.trees[utenza].get_children()
            ]
            scrivi_db()

        def salva_anagrafica_utenza(utenza):
            for field, ent in anag_entries[utenza].items():
                if field == "Note":
                    anagrafiche[utenza][field] = ent.get("1.0", "end-1c")
                else:
                    anagrafiche[utenza][field] = ent.get()
            scrivi_db()

        def on_tree_double_click(event, utenza):
            tree = self.trees[utenza]
            item_id = tree.identify_row(event.y)
            if item_id:
                tree.selection_set(item_id)
                tree.focus(item_id)
                apri_modale(utenza)

        def on_tree_right_click(event, utenza):
            tree = self.trees[utenza]
            item_id = tree.identify_row(event.y)
            if not item_id:
                return
            tree.selection_set(item_id)
            tree.focus(item_id)
            apri_modale_solo_totale(utenza)
    
        def apri_modale_solo_totale(utenza):
            selected = self.trees[utenza].focus()
            if not selected:
                self.show_custom_warning("Errore", "Seleziona un mese dalla tabella")
                return

            item = self.trees[utenza].item(selected)
            mese, prec, att, consumo = item['values']

            try:
                consumo = float(consumo)
            except:
                consumo = 0.0
    
            modal = tk.Toplevel(win)
            modal.title(f"Consumo {utenza}")
            modal.geometry("300x140")
            modal.resizable(False, False)
            modal.transient(win)
            centra_su_padre(modal, win)
            modal.after_idle(modal.grab_set)

            def only_numeric_8char(val):
                if len(val) > 8:
                    return False
                if val == "":
                    return True
                if val.count(".") > 1:
                    return False
                return all(c.isdigit() or c == "." for c in val)

            vcmd = modal.register(only_numeric_8char)

            tk.Label(modal, text=f"{utenza} - {mese}", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(modal, text="Consumo:").pack()

            consumo_var = tk.DoubleVar(value=consumo)
            e_cons = tk.Entry(modal, textvariable=consumo_var, font=("Arial", 10), width=15,
                      validate="key", validatecommand=(vcmd, "%P"))
            e_cons.pack()
            e_cons.focus_set()
            modal.bind("<Return>", lambda event: salva()) 
            modal.bind("<KP_Enter>", lambda event: salva()) 

            def salva():
                val = e_cons.get().strip()
                if not val:
                    self.show_custom_warning("Campo vuoto", "Inserisci il valore del consumo.")
                    return
                try:
                    cons = float(consumo_var.get())
                    if cons < 0:
                        self.show_custom_warning("Errore", "Consumo non può essere negativo.")
                        return
                    nuovo_att = float(prec) + cons
                    self.trees[utenza].item(selected, values=(mese, prec, nuovo_att, cons))
                    anno_sel = anno_var.get()
                    righe = [
                        tuple(self.trees[utenza].item(iid)['values'])
                        for iid in self.trees[utenza].get_children()
                    ]
                    letture_salvate[utenza][anno_sel] = righe
                    scrivi_db()
                    modal.destroy()
                except ValueError:
                    self.show_custom_warning("Errore", "Valore non valido.")

            btn_frame = tk.Frame(modal)
            btn_frame.pack(fill="x", pady=10, padx=10)

            btn_salva = ttk.Button(btn_frame, text="💾 Salva", command=salva, style="Verde.TButton")
            btn_salva.pack(side=tk.LEFT, padx=(0,10))

            btn_chiudi = ttk.Button(btn_frame, text="❌ Chiudi", command=modal.destroy, style="Giallo.TButton")
            btn_chiudi.pack(side=tk.RIGHT, padx=(10,0))
            modal.bind("<Escape>", lambda e: modal.destroy())

        def apri_modale(utenza):
            selected = self.trees[utenza].focus()
            if not selected:
                self.show_custom_warning("Errore", "Seleziona un mese dalla tabella")
                return

            item = self.trees[utenza].item(selected)
            mese, prec, att, _ = item['values']

            items = self.trees[utenza].get_children()
            idx = items.index(selected)
            if idx > 0:
                prev_item = self.trees[utenza].item(items[idx - 1])
                try:
                    prec = float(prev_item['values'][2])
                except:
                    prec = 0.0

            try:
                prec = float(prec)
            except:
                prec = 0.0

            try:
                att = float(att)
            except:
                att = 0.0

            modal = tk.Toplevel(win)
            modal.title(f"Letture {utenza}")
            modal.geometry("300x180")
            modal.resizable(False, False)
            modal.transient(win)
            centra_su_padre(modal, win)
            modal.after_idle(modal.grab_set)
            modal.bind("<Return>", lambda e: salva())
            modal.bind("<KP_Enter>", lambda e: salva())
            
            def only_numeric_8char(val):
                if len(val) > 8:
                    return False
                if val == "":
                    return True
                if val.count(".") > 1:
                    return False
                return all(c.isdigit() or c == "." for c in val)

            vcmd = modal.register(only_numeric_8char)
    
            tk.Label(modal, text=f"{utenza} - {mese}", font=("Arial", 12, "bold")).pack(pady=10)

            tk.Label(modal, text="Lettura precedente:").pack()
            prec_var = tk.DoubleVar(value=prec)
            e_prec = tk.Entry(modal, textvariable=prec_var, font=("Arial", 10), width=22,
                      validate="key", validatecommand=(vcmd, "%P"))
            e_prec.pack()

            tk.Label(modal, text="Lettura attuale:").pack()
            att_var = tk.DoubleVar(value=att)
            e_att = tk.Entry(modal, textvariable=att_var, font=("Arial", 10), width=22,
                     validate="key", validatecommand=(vcmd, "%P"))
            e_att.pack()

            modal.e_prec = e_prec
            modal.e_att = e_att
            modal.prec_var = prec_var
            modal.att_var = att_var
            modal.mese = mese
            modal.utenza = utenza
            
            def salva():
                try:
                
                    if not e_prec.get().strip() or not e_att.get().strip():
                        self.show_custom_warning("Campo vuoto", "Compila entrambi i campi prima di salvare.")
                        return

                    p = float(prec_var.get())
                    a = float(att_var.get())
                    if a < p:
                        conferma = tk.Toplevel(modal)
                        conferma.title("Conferif att_var.get() == 0.0 and e_att.get().strip() == "":ma Forzatura")
                        conferma.geometry("350x120")
                        conferma.resizable(False, False)
                        conferma.transient(modal)
                        conferma.grab_set()
                        centra_su_padre(conferma, modal)
                        fnt = ("Arial", 9, "bold")
                        msg = tk.Label(conferma,
                                       text="La lettura attuale è minore della precedente.\nVuoi forzare l'inserimento?",
                                       font=fnt, fg="red")
                        msg.pack(pady=15)
                        btn_frame = ttk.Frame(conferma)
                        btn_frame.pack()
                        def ok():
                            consumo = round(max(0.0, a - p), 2)
                            self.trees[utenza].item(selected, values=(mese, p, a, consumo))
                            if idx + 1 < len(items):
                                next_item = self.trees[utenza].item(items[idx + 1])
                                next_mese, _, next_att, _ = next_item['values']
                                next_att_f = float(next_att)
                                next_cons = round(next_att_f - a, 2)
                                self.trees[utenza].item(items[idx + 1], values=(next_mese, a, next_att_f, next_cons))
                            conferma.destroy()
                            modal.destroy()
                            salva_letture_utenza(utenza)
                        def annulla():
                            conferma.destroy()
                        ttk.Button(btn_frame, text="Forza", style="Arancio.TButton", width=10, command=ok).pack(side=tk.LEFT, padx=12)
                        ttk.Button(btn_frame, text="Annulla", style="Giallo.TButton", width=10, command=annulla).pack(side=tk.LEFT, padx=12)
                        return
                    consumo = round(a - p, 2)
                    self.trees[utenza].item(selected, values=(mese, p, a, consumo))
                    if idx + 1 < len(items):
                        next_item = self.trees[utenza].item(items[idx + 1])
                        next_mese, _, next_att, _ = next_item['values']
                        next_att_f = float(next_att)
                        next_cons = max(0.0, next_att_f - a)
                        self.trees[utenza].item(items[idx + 1], values=(next_mese, a, next_att_f, next_cons))
                    modal.destroy()
                    salva_letture_utenza(utenza)
                except ValueError:
                    self.show_custom_warning("Errore", "Valori non validi")

            ttk.Button(modal, text="💾 Salva", command=salva, style="Verde.TButton").pack(side=tk.LEFT, padx=10)
            ttk.Button(modal, text="❌ Chiudi", command=modal.destroy, style="Giallo.TButton").pack(side=tk.RIGHT, padx=10)
            modal.bind("<Escape>", lambda e: modal.destroy())
            
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        for utenza in utenze:
                tab = ttk.Frame(notebook)
                notebook.add(tab, text=f"{'💧' if utenza=='Acqua' else '💡' if utenza=='Luce' else '🔥'} {utenza}")
 
                colore_bg = colori[utenza]
                frame = tk.Frame(tab, bg=colore_bg, bd=2, relief="groove")
                frame.pack(fill="both", expand=True, padx=8, pady=8)

                top_btn_fr = tk.Frame(frame, bg=colore_bg)
                top_btn_fr.pack(fill="x", padx=4, pady=(2, 0))

                ttk.Button(top_btn_fr,text="📥 Modifica Letture" , style="Rosso.TButton", command=lambda u=utenza: apri_modale(u)).pack(side=tk.LEFT, padx=5, pady=2)

                ttk.Button(top_btn_fr,text="🟢 Modifica Consumo", style="Verde.TButton", command=lambda u=utenza: apri_modale_solo_totale(u)).pack(side=tk.LEFT, padx=5, pady=2)

               
                bg_utenza = colori.get(utenza, "#f0f0f0")  

                tk.Label(
                    top_btn_fr,
                    text="🖱️ 2 Click sx: Mod.letture | Click dx: Mod.consumo",
                    font=("Arial", 9, "bold"),
                    fg="black",
                    bg=bg_utenza
                ).pack(side=tk.LEFT, padx=10, pady=2)


                tree = ttk.Treeview(frame, columns=("Mese", "Prec", "Att", "Consumo"), show="headings", height=12)
                for col in ("Mese", "Prec", "Att", "Consumo"):
                        tree.heading(col, text=col)
                        tree.column(col, anchor="center", width=80)
                tree.pack(padx=8, pady=6, fill="both", expand=True)

                anno_sel = anno_var.get()
                if (anno_sel not in letture_salvate[utenza]) or (not letture_salvate[utenza][anno_sel]):
                        letture_salvate[utenza][anno_sel] = [(f"{m:02d}/{anno_sel}", 0.0, 0.0, 0.0) for m in range(1, 13)]
                righe = letture_salvate[utenza][anno_sel]
                righe_norm = []
                for r in righe:
                        if len(r) == 4:
                                mese, prec, att, consumo = r
                                consumo = max(0.0, float(att) - float(prec))
                                righe_norm.append((mese, float(prec), float(att), float(consumo)))
                        else:
                                righe_norm.append(tuple(r))
                letture_salvate[utenza][anno_sel] = righe_norm
                for mese, prec, att, consumo in righe_norm:
                        tree.insert("", "end", values=(mese, float(prec), float(att), float(consumo)))

                self.trees[utenza] = tree
                tree.bind("<Double-1>", lambda event, utenza=utenza: on_tree_double_click(event, utenza))
                tree.bind("<Button-3>", lambda event, utenza=utenza: on_tree_right_click(event, utenza))

                anag_frame = tk.LabelFrame(frame, text="Dati Anagrafici", bg=colore_bg)
                anag_frame.pack(fill="x", padx=8, pady=8)

                anag_frame.grid_columnconfigure(3, weight=1)
                anag_frame.grid_columnconfigure(4, weight=0)

                anag_entries[utenza] = {}
                campi = [("Ragione sociale", 40), ("Telefono", 40), ("Email", 40), ("Numero contratto", 40), ("POD", 40)]
                for row, (label, width) in enumerate(campi):
                    tk.Label(anag_frame, text=label+":", bg=colore_bg).grid(row=row, column=0, sticky="e", padx=5, pady=2)
                    ent = tk.Entry(anag_frame, width=width)
                    ent.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                    ent.insert(0, anagrafiche[utenza][label])
                    ent.config(state="readonly")
                    anag_entries[utenza][label] = ent

                tk.Label(anag_frame, text="Note:", bg=colore_bg).grid(row=0, column=2, sticky="ne", padx=5, pady=2)
                note_txt = tk.Text(anag_frame, width=60, height=8, wrap="word")
                note_txt.grid(row=0, column=3, rowspan=6, sticky="nsew", padx=5, pady=2)
                note_txt.insert("1.0", anagrafiche[utenza]["Note"])
                note_txt.config(state="disabled")
                anag_entries[utenza]["Note"] = note_txt

                btns = ttk.Frame(anag_frame)
                btns.grid(row=0, column=4, rowspan=6, sticky="n", padx=(5,10), pady=2)

                def set_editable(editable, u=utenza):
                    for k, ent in anag_entries[u].items():
                        if k == "Note":
                            ent.config(state="normal" if editable else "disabled")
                        else:
                            ent.config(state="normal" if editable else "readonly")

                def salva_dati(u=utenza):
                    for field, ent in anag_entries[u].items():
                        if field == "Note":
                            anagrafiche[u][field] = ent.get("1.0", "end-1c")
                        else:
                            anagrafiche[u][field] = ent.get()
                    set_editable(False, u)
                    scrivi_db()
                    self.show_custom_warning("Attenzione", f"Dati {u} Salvati correttamente !")

                def modifica_dati(u=utenza):
                    set_editable(True, u)

                ttk.Button(btns,text="💾 Salva",width=10,command=lambda u=utenza: salva_dati(u), style="Verde.TButton").pack(pady=(0, 5))

                ttk.Button(btns,text="📄 Modifica",width=10,command=lambda u=utenza: modifica_dati(u), style="Giallo.TButton").pack()

    def apri_cancella_spese_treeview_unica(self):
        
        NOMI_MESI_ITALIANO = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
                              "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
        if not hasattr(self, 'spese') or not isinstance(self.spese, dict):
            self.spese = {} 
        self.filtri_cancellazione = {} 
        if not hasattr(self, 'selezionate_iid'):
            self.selezionate_iid = set()
        self.selezionate_iid.clear() 

        def sort_treeview_column(tree, col, reverse, data_type='string'):
            items_to_sort = []
            for k in tree.get_children(''):
                value = tree.set(k, col)
                if value in ("—", ""): continue 
                items_to_sort.append((value, k))
            def get_sort_key(item):
                value = item[0]
                try:
                    if data_type == 'float':
                        return float(value.replace(' €', '').replace(',', '.'))
                    elif data_type == 'date':
                        return datetime.datetime.strptime(value, '%d/%m/%Y')
                    else: 
                        return value.lower()
                except Exception:
                    return value
            items_to_sort.sort(key=get_sort_key, reverse=reverse)
            for index, (val, k) in enumerate(items_to_sort):
                tree.move(k, '', index)
            tree.heading(col, command=lambda: sort_treeview_column(tree, col, not reverse, data_type))

        def toggle_selection_treeview(event):
            row_id = self.spese_treeview.identify_row(event.y)
            if not row_id or row_id in ("EMPTY_MSG", "FILTER_MSG"): return
            
            is_selected = row_id in self.selezionate_iid
            current_tags = list(self.spese_treeview.item(row_id, 'tags'))
            type_tag = [t for t in current_tags if t in ('entrata', 'uscita')] 
            
            if is_selected:
                self.selezionate_iid.remove(row_id)
                self.spese_treeview.item(row_id, tags=type_tag, text="[ ]") 
            else:
                self.selezionate_iid.add(row_id)
                new_tags = type_tag + ['selezionata']
                self.spese_treeview.item(row_id, tags=new_tags, text="[X]") 

        def esegui_cancellazione_azione(): 
            if not self.selezionate_iid:
                self.show_custom_warning("Attenzione", "Seleziona almeno una spesa da cancellare.")
                return

            num_selezionate = len(self.selezionate_iid)
            testo_messaggio = f"\nSei sicuro di voler cancellare {num_selezionate} selezionate?\nL'azione è irreversibile."
            response = self.show_custom_askyesno("Conferma Cancellazione", testo_messaggio)
            
            if not response: return
            spese_da_mantenere = {}
            for giorno_obj in self.spese.keys():
                giorno_interno = str(giorno_obj)
                spese_mantenute_giorno = []
                for indice, voce in enumerate(self.spese.get(giorno_obj, [])):
                    iid = f"{giorno_interno}_{indice}"
                    if iid not in self.selezionate_iid:
                        spese_mantenute_giorno.append(voce)
                
                if spese_mantenute_giorno:
                    spese_da_mantenere[giorno_obj] = spese_mantenute_giorno

            self.spese = spese_da_mantenere
            self.selezionate_iid.clear() 
            popola_treeview_spese()
            if hasattr(self, 'refresh_gui'): self.refresh_gui()
            if hasattr(self, 'save_db'): self.save_db()
            self.show_custom_warning("Successo", f"✅ {num_selezionate} spese sono state cancellate.")

        def popola_treeview_spese():

            self.spese_treeview.delete(*self.spese_treeview.get_children())
            
            if not self.spese:
                self.spese_treeview.insert("", "end", iid="EMPTY_MSG", 
                                           text="", 
                                           values=("—", "⚠️ Dati spese non trovati o database vuoto.", "", "", ""),
                                           tags=('empty',))
                return
            
            filtri = self.filtri_cancellazione
            items_inserted = 0
            filtro_testo_globale = filtri.get("descrizione", "").lower()
            filtro_categoria_esatta = filtri.get("categoria")
            filtro_tipo = filtri.get("tipo")
            filtro_anno = filtri.get("anno")
            filtro_mese_nome = filtri.get("mese")
            filtro_mese_numero = ""
            if filtro_mese_nome and filtro_mese_nome != "—":
                try:
                    mese_index = NOMI_MESI_ITALIANO.index(filtro_mese_nome) + 1
                    filtro_mese_numero = f"{mese_index:02d}"
                except ValueError:
                    pass 
            try:
                giorni_ordinati = sorted(self.spese.keys(), 
                                         key=lambda d: d if isinstance(d, datetime.date) else datetime.datetime.strptime(str(d), '%Y-%m-%d').date(), 
                                         reverse=True) 
            except Exception:
                 giorni_ordinati = sorted(self.spese.keys(), reverse=True)
            
            for giorno_obj in giorni_ordinati:
                d = None
                giorno_interno = str(giorno_obj)
                giorno_visualizzato = str(giorno_obj)
                try:
                    if isinstance(giorno_obj, datetime.date):
                        d = giorno_obj
                    else:
                        d = datetime.datetime.strptime(str(giorno_obj), '%Y-%m-%d').date()
                    
                    giorno_interno = d.strftime('%Y-%m-%d')
                    giorno_visualizzato = d.strftime('%d/%m/%Y')
                except Exception:
                    pass 

                lista_voci = self.spese.get(giorno_obj, [])
                
                for indice, voce in enumerate(lista_voci): 
                    try:
                        categoria, descrizione, importo = voce[0], voce[1], voce[2]
                        tipo = voce[3].capitalize() if len(voce) > 3 else "N/A" 
                        filtro_icona = filtri.get("icona")
                        if filtro_icona not in ["", "—"] and filtro_icona not in descrizione:
                            continue
                        matches = True
                        if filtro_testo_globale:
                            testo_da_cercare = f"{descrizione} {categoria}".lower()
                            if filtro_testo_globale not in testo_da_cercare: 
                                matches = False
                        if matches and filtro_categoria_esatta not in ["", "—"] and categoria != filtro_categoria_esatta: matches = False
                        if matches and filtro_tipo not in ["", "—"] and tipo != filtro_tipo: matches = False
                        if matches and filtro_anno not in ["", "—"] and d and str(d.year) != filtro_anno: matches = False
                        if matches and filtro_mese_numero and d:
                            if d.strftime('%m') != filtro_mese_numero:
                                matches = False
                        try:
                            da = float(filtri.get("da", "") or "0")
                            a = float(filtri.get("a", "") or "999999999")
                            if matches and not (da <= float(importo) <= a): matches = False 
                        except (ValueError, TypeError): pass
                        if matches:
                            importo_formattato = f"{float(importo):.2f} €"
                            iid = f"{giorno_interno}_{indice}" 
                            is_selected = iid in self.selezionate_iid
                            color_tag = 'entrata' if tipo == 'Entrata' else 'uscita'
                            tags = [color_tag]
                            if is_selected:
                                tags.append('selezionata')
                            checkbox_text = "[X]" if is_selected else "[ ]" 
                            self.spese_treeview.insert(
                                "", "end", iid=iid,
                                text=checkbox_text,
                                values=(giorno_visualizzato, categoria, descrizione, tipo, importo_formattato),
                                tags=tags
                            )
                            items_inserted += 1
                    except Exception:
                        continue
            if items_inserted == 0 and self.spese:
                self.spese_treeview.insert("", "end", iid="FILTER_MSG", 
                                           text="", 
                                           values=("—", "Nessun risultato.", "", "", ""),
                                           tags=('empty',))
        def aggiorna_stato_filtri():
            attivi = {k: v for k, v in self.filtri_cancellazione.items() if v and v != "—"}
            if not attivi:
                lbl_filtri_attivi.config(text="Nessun filtro attivo. Attiva un Filtro Avanzato.", fg="gray")
            else:
                testo_formattato = []
                for k, v in attivi.items():
                    if k == 'descrizione':
                        testo_formattato.append(f"Testo Globale: {v}")
                    else:
                        testo_formattato.append(f"{k.capitalize()}: {v}")
                testo = ", ".join(testo_formattato)
                lbl_filtri_attivi.config(text=f"Filtri attivi: {testo}", fg="blue")

        def apri_filtri_avanzati():
            filtro_win = tk.Toplevel(popup)
            filtro_win.title("⚙️ Filtri Avanzati di Cancellazione")
            filtro_win.geometry("400x320") 
            filtro_win.transient(popup)
            filtro_win.grab_set()
            descrizione_var = tk.StringVar(value=self.filtri_cancellazione.get("descrizione", ""))
            categoria_var = tk.StringVar(value=self.filtri_cancellazione.get("categoria", "—"))
            tipo_var = tk.StringVar(value=self.filtri_cancellazione.get("tipo", "—"))
            anno_var = tk.StringVar(value=self.filtri_cancellazione.get("anno", "—"))
            mese_var = tk.StringVar(value=self.filtri_cancellazione.get("mese", "—"))
            da_var = tk.StringVar(value=self.filtri_cancellazione.get("da", ""))
            a_var = tk.StringVar(value=self.filtri_cancellazione.get("a", ""))
            icona_var = tk.StringVar(value=self.filtri_cancellazione.get("icona", "—"))

            def crea_riga(testo, var, values=None):
                f = tk.Frame(filtro_win); f.pack(fill="x", padx=12, pady=5)
                tk.Label(f, text=testo, width=16, anchor="w").pack(side="left") 
                if values:
                    ttk.Combobox(f, textvariable=var, values=values, state="readonly", width=20).pack(side="left")
                else:
                    tk.Entry(f, textvariable=var, width=22).pack(side="left")

            tutte_cat = ["—"] + sorted(list(self.categorie_tipi.keys()))
            anni = ["—"]
            for giorno_obj in self.spese.keys():
                try:
                    d = giorno_obj if isinstance(giorno_obj, datetime.date) else datetime.datetime.strptime(str(giorno_obj), "%Y-%m-%d").date()
                    anni.append(str(d.year))
                except Exception: continue
            anni = sorted(list(set(anni)), reverse=True)
            nomi_mesi_dropdown = ["—"] + NOMI_MESI_ITALIANO
            crea_riga("Testo Globale:", descrizione_var)
            crea_riga("Categoria:", categoria_var, tutte_cat)
            crea_riga("Tipo voce:", tipo_var, ["—", "Entrata", "Uscita"]) 
            crea_riga("Anno:", anno_var, anni)
            crea_riga("Mese:", mese_var, nomi_mesi_dropdown)
            crea_riga("Simbolo:", icona_var, ["—", "💰", "🔄", "🏦", "💎", "💳"])
            crea_riga("Importo da (€):", da_var)
            crea_riga("Importo a (€):", a_var)

            def applica():
                self.filtri_cancellazione = {
                    "descrizione": descrizione_var.get(),
                    "categoria": categoria_var.get(),
                    "tipo": tipo_var.get(),
                    "anno": anno_var.get(),
                    "mese": mese_var.get(), 
                    "da": da_var.get(),
                    "a": a_var.get(),
                    "icona": icona_var.get()
                }
                filtro_win.destroy()
                self.selezionate_iid.clear() 
                aggiorna_stato_filtri()
                popola_treeview_spese()

            def cancella_filtri():
                self.filtri_cancellazione = {}
                filtro_win.destroy()
                self.selezionate_iid.clear() 
                aggiorna_stato_filtri()
                popola_treeview_spese()

            f_btn = tk.Frame(filtro_win); f_btn.pack(pady=10)
            ttk.Button(f_btn, text="✅ Applica Filtri", command=applica, style="Verde.TButton").pack(side="left", padx=10)
            ttk.Button(f_btn, text="🎛 Cancella Filtri", command=cancella_filtri, style="Giallo.TButton").pack(side="right", padx=10)

        def seleziona_tutto_azione():
            all_children = self.spese_treeview.get_children()
            self.selezionate_iid.clear()
            items_to_select = []
            for iid in all_children:
                if iid in ("EMPTY_MSG", "FILTER_MSG", "NO_DATA"):
                    continue
                self.selezionate_iid.add(iid)
                items_to_select.append(iid)
            popola_treeview_spese()
        popup = tk.Toplevel(self.master)
        popup.title("🗑️ Cancella Spese Multiple")
        
        larg, alt = 800, 600
        x = self.winfo_x() + (self.winfo_width() // 2) - (larg // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (alt // 2)
        popup.geometry(f"{larg}x{alt}+{x}+{y}")
        popup.transient(self.master) 
        
        tk.Label(popup, text="Seleziona le spese da cancellare:", font=("Arial", 12, "bold")).pack(pady=(10, 5))

        filter_control_frame = tk.Frame(popup)
        filter_control_frame.pack(fill='x', padx=10, pady=5)
        
        lbl_filtri_attivi = tk.Label(filter_control_frame, text="", fg="gray")
        lbl_filtri_attivi.pack(side="left", fill='x', expand=True)
        
        ttk.Button(
            filter_control_frame,
            text="⚙️ Filtri Avanzati",
            command=apri_filtri_avanzati, 
            style='Blu.TButton' 
        ).pack(side="right")
        
        tree_frame = tk.Frame(popup)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5) 

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        self.spese_treeview = ttk.Treeview(
            tree_frame,
            columns=("Giorno", "Categoria", "Descrizione", "Tipo", "Importo"), 
            show=("tree", "headings"), 
            yscrollcommand=scrollbar.set,
            height=15
        )
        self.spese_treeview.pack(side="left", fill="both", expand=True) 
        
        scrollbar.config(command=self.spese_treeview.yview)

        self.spese_treeview.heading("#0", text="Sel.", anchor="center") 
        self.spese_treeview.heading("Giorno", text="Giorno", anchor="center", 
                                    command=lambda: sort_treeview_column(self.spese_treeview, "Giorno", True, data_type='date')) 
        self.spese_treeview.heading("Categoria", text="Categoria", anchor="center", 
                                    command=lambda: sort_treeview_column(self.spese_treeview, "Categoria", False, data_type='string'))
        self.spese_treeview.heading("Descrizione", text="Descrizione", anchor="center", 
                                    command=lambda: sort_treeview_column(self.spese_treeview, "Descrizione", False, data_type='string'))
        self.spese_treeview.heading("Tipo", text="Tipo", anchor="center", 
                                    command=lambda: sort_treeview_column(self.spese_treeview, "Tipo", False, data_type='string'))
        self.spese_treeview.heading("Importo", text="Importo", anchor="center", 
                                    command=lambda: sort_treeview_column(self.spese_treeview, "Importo", False, data_type='float'))

        self.spese_treeview.column("#0", width=40, anchor="center", stretch=False) 
        self.spese_treeview.column("Giorno", width=90, anchor="w", stretch=False)
        self.spese_treeview.column("Categoria", width=150, anchor="w", stretch=False)
        self.spese_treeview.column("Descrizione", width=200, anchor="w", stretch=True)
        self.spese_treeview.column("Tipo", width=60, anchor="center", stretch=False) 
        self.spese_treeview.column("Importo", width=100, anchor="e", stretch=False)
        self.spese_treeview.tag_configure('selezionata', background='#FFEBCC') 
        self.spese_treeview.tag_configure('entrata', foreground='green')
        self.spese_treeview.tag_configure('uscita', foreground='red') 
        self.spese_treeview.tag_configure('empty', foreground='gray', font=('Arial', 10, 'italic')) 
        
        self.spese_treeview.bind('<Button-1>', toggle_selection_treeview)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10) 

        ttk.Button(
            btn_frame,
            text="🗑️ Cancella Selezionate",
            command=esegui_cancellazione_azione,
            style='Rosso.TButton' 
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame, 
            text="✅ Seleziona Tutto", 
            command=seleziona_tutto_azione, 
            style='Verde.TButton'
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="🔄 Deseleziona Tutto",
            command=lambda: [self.selezionate_iid.clear(), popola_treeview_spese()], 
            style='Giallo.TButton' 
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="❌ Chiudi",
            command=popup.destroy,
            style='Giallo.TButton' 
        ).pack(side="left", padx=5)
        
        aggiorna_stato_filtri() 
        popola_treeview_spese()
        sort_treeview_column(self.spese_treeview, "Giorno", True, data_type='date') 
        
        popup.grab_set()


    def cerca_operazioni(self):
        larghezza, altezza = 900, 600
        x = self.winfo_screenwidth() // 2 - larghezza // 2
        y = self.winfo_screenheight() // 2 - altezza // 2

        finestra = tk.Toplevel(self)
        finestra.title("Ricerca operazioni")
        finestra.geometry(f"{larghezza}x{altezza}+{x}+{y}")
        finestra.transient(self)
        finestra.bind("<Escape>", lambda e: finestra.destroy())
        
        frame_superiore = tk.Frame(finestra)
        frame_superiore.pack(fill="x", pady=10, padx=10)

        tk.Label(frame_superiore, text="🔎 Ricerca generale:").pack(side="left")
        campo_input = tk.Entry(frame_superiore, width=30)
        campo_input.pack(side="left", padx=8)
        campo_input.focus_set()

        mostra_futuro_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_superiore, text="Includi futuri", variable=mostra_futuro_var).pack(side="left", padx=10)

        frame_risultati = tk.Frame(finestra)
        frame_risultati.pack(fill="both", expand=True, padx=10)

        columns = ("Data", "Categoria", "Descrizione", "Tipo", "Importo")
        tree = ttk.Treeview(frame_risultati, columns=columns, show="headings")
        tree.pack(side="left", fill="both", expand=True)

        tree.bind("<Double-1>", self.cerca_doppio_click)

        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: sort_by_column(tree, c, False))
            if col == "Importo":
                tree.column(col, anchor="e")
            else:
                tree.column(col, anchor="w")

        tree.column("Data", width=90, stretch=False)
        tree.column("Categoria", width=120, stretch=False)
        tree.column("Descrizione", width=300, stretch=True)
        tree.column("Tipo", width=80, stretch=False)
        tree.column("Importo", width=100, stretch=False)
        
        scroll = ttk.Scrollbar(frame_risultati, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        
        tree.tag_configure("entrata_tag", foreground="green")
        tree.tag_configure("uscita_tag", foreground="red")
        tree.tag_configure("neutro_tag", foreground="gray")

        frame_totali = tk.Frame(finestra)
        frame_totali.pack(fill="x", pady=10, padx=10)
        
        lbl_risultati = tk.Label(frame_totali, text="", anchor="w", font=("Arial", 10))
        lbl_risultati.pack(fill="x")
        
        lbl_totali = tk.Label(frame_totali, text="", anchor="w", font=("Arial", 10, "bold"))
        lbl_totali.pack(fill="x")
        
        def esegui_ricerca(event=None):
            parola = campo_input.get().strip().lower()
            filtri = getattr(self, "filtri_avanzati", {})
            
            if parola:
                filtri = {}
            
            for item in tree.get_children():
                tree.delete(item)

            risultati = []
            oggi = datetime.date.today()
            mostra_futuro = mostra_futuro_var.get()
            
            for data_key in sorted(self.spese.keys(), reverse=True):
                try:
                    d = data_key if isinstance(data_key, datetime.date) else datetime.datetime.strptime(data_key, "%d-%m-%Y").date()
                except ValueError:
                    d = datetime.datetime.strptime(data_key, "%Y-%m-%d").date()
                
                if not mostra_futuro and d > oggi:
                    continue

                for voce in self.spese[data_key]:
                    categoria = str(voce[0]).lower()
                    descrizione = str(voce[1]).lower()
                    importo_voce = voce[2]
                    tipo = str(voce[3]).lower()
                    
                    matches = True
                    
                    if parola:
                        if not any(parola in str(campo).lower() for campo in [categoria, descrizione, tipo, str(importo_voce)]):
                            matches = False
                    
                    elif filtri:
                        if filtri.get("descrizione") and filtri["descrizione"].lower() not in descrizione:
                            matches = False
                        if filtri.get("categoria") not in ["", "—"] and categoria != filtri["categoria"].lower():
                            matches = False
                        if filtri.get("tipo") not in ["", "—"] and tipo != filtri["tipo"].lower():
                            matches = False
                        if filtri.get("icona") not in ["", "—"]:
                            icona = filtri["icona"]
                            if icona not in descrizione:
                                matches = False

                        if filtri.get("anno") not in ["", "—"] and str(d.year) != filtri["anno"]:
                            matches = False
                        if filtri.get("mese") not in ["", "—"]:
                            mesi_nomi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                                         "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
                            mesi_map = {m: i+1 for i, m in enumerate(mesi_nomi)}
                            if d.month != mesi_map.get(filtri["mese"], 0):
                                matches = False
                        
                        try:
                            da = float(filtri.get("da", "") or "0")
                            a = float(filtri.get("a", "") or "999999999")
                            if not (da <= float(importo_voce) <= a):
                                matches = False
                        except (ValueError, TypeError):
                            pass
                    
                    if matches:
                        risultati.append({
                            "data": d.strftime('%d/%m/%Y'),
                            "categoria": voce[0],
                            "descrizione": voce[1],
                            "importo": importo_voce,
                            "tipo": tipo.capitalize()
                        })

            risultati.sort(key=lambda x: datetime.datetime.strptime(x['data'], '%d/%m/%Y'), reverse=True)
            
            tot_entrate = sum(r['importo'] for r in risultati if r['tipo'] == "Entrata")
            tot_uscite = sum(r['importo'] for r in risultati if r['tipo'] == "Uscita")
            
            testo_filtri = ""
            if parola:
                testo_filtri = f"Parola chiave: '{parola}'"
            elif filtri:
                testo_filtri = ", ".join([f"{k.capitalize()}: {v}" for k, v in filtri.items() if v not in ["", "—"]])
            
            lbl_risultati.config(text=f"📊 Operazioni trovate: {len(risultati)} | Filtri attivi: {testo_filtri or 'Nessuno'}")
            
            netto = tot_entrate - tot_uscite
            lbl_totali.config(text=f"✅ Entrate: {tot_entrate:,.2f} € | ❌ Uscite: {tot_uscite:,.2f} € | 🧮 Saldo: {netto:,.2f} €")
            
            if not risultati:
                lbl_risultati.config(text=f"🔍 Nessuna corrispondenza per la ricerca attuale.", fg="gray")
                lbl_totali.config(text="", fg="gray")
            else:
                lbl_risultati.config(fg="black")
                lbl_totali.config(fg="black")

            for riga in risultati:
                tipo = riga['tipo'].lower()
                tag = "entrata_tag" if tipo == "entrata" else "uscita_tag" if tipo == "uscita" else "neutro_tag"
                tree.insert("", "end", values=(riga['data'], riga['categoria'], riga['descrizione'], riga['tipo'], f"{riga['importo']:,.2f} €"), tags=(tag,))

        campo_input.bind("<Return>", esegui_ricerca)
        campo_input.bind("<KP_Enter>", esegui_ricerca)
        
        def resetta_campo():
            campo_input.delete(0, tk.END)
            self.filtri_avanzati = {}
            for item in tree.get_children():
                tree.delete(item)
            lbl_risultati.config(text="🔍 Nessuna corrispondenza per la ricerca attuale.", fg="gray")
            lbl_totali.config(text="")

        ttk.Button(frame_superiore, text="↺", command=resetta_campo, style="Yellow.TButton").pack(side="left", padx=5)

        def apri_filtri_avanzati():
            self.filtri_avanzati = {"descrizione": ""}
            parola_chiave = campo_input.get().strip()
            campo_input.delete(0, tk.END)
            self.filtri_avanzati = {}
            if parola_chiave:
                self.filtri_avanzati = {"descrizione": ""}
            filtro_win = tk.Toplevel(finestra)
            filtro_win.title("⚙️ Filtri avanzati")
            filtro_win.geometry("400x320")
            filtro_win.transient(finestra)
            filtro_win.grab_set()
            descrizione_var = tk.StringVar(value=self.filtri_avanzati.get("descrizione", ""))
            categoria_var = tk.StringVar(value=self.filtri_avanzati.get("categoria", "—"))
            tipo_var = tk.StringVar(value=self.filtri_avanzati.get("tipo", "—"))
            anno_var = tk.StringVar(value=self.filtri_avanzati.get("anno", "—"))
            mese_var = tk.StringVar(value=self.filtri_avanzati.get("mese", "—"))
            da_var = tk.StringVar(value=self.filtri_avanzati.get("da", ""))
            a_var = tk.StringVar(value=self.filtri_avanzati.get("a", ""))
            icona_var = tk.StringVar(value=self.filtri_avanzati.get("icona", "—"))
            
            def crea_riga(testo, var, values=None):
                f = tk.Frame(filtro_win); f.pack(fill="x", padx=12, pady=5)
                tk.Label(f, text=testo, width=14, anchor="w").pack(side="left")
                if values:
                    ttk.Combobox(f, textvariable=var, values=values, state="readonly", width=22).pack(side="left")
                else:
                    tk.Entry(f, textvariable=var, width=24).pack(side="left")

            tutte_cat = sorted(list(self.categorie_tipi.keys()))
            anni = sorted(set(str(d.year if isinstance(d, datetime.date)else datetime.datetime.strptime(d, "%d-%m-%Y").year) for d in self.spese), reverse=True)
            mesi_nomi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                         "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
            crea_riga("Descrizione:", descrizione_var)
            crea_riga("Categoria:", categoria_var, ["—"] + tutte_cat)
            crea_riga("Tipo voce:", tipo_var, ["—", "Entrata", "Uscita"])
            crea_riga("Anno:", anno_var, ["—"] + anni)
            crea_riga("Mese:", mese_var, ["—"] + mesi_nomi)
            icone_simboli = ["—", "💰", "🔄", "🏦", "💎", "💳"]
            crea_riga("Simbolo:", icona_var, icone_simboli)

            crea_riga("Importo da:", da_var)
            crea_riga("Importo a:", a_var)

            def applica():
                self.filtri_avanzati = {
                    "descrizione": descrizione_var.get(),
                    "categoria": categoria_var.get(),
                    "tipo": tipo_var.get(),
                    "anno": anno_var.get(),
                    "mese": mese_var.get(),
                    "da": da_var.get(),
                    "a": a_var.get(),
                    "icona": icona_var.get()
                }
                filtro_win.destroy()
                esegui_ricerca()

            def cancella():
                self.filtri_avanzati = {}
                filtro_win.destroy()
                esegui_ricerca()

            f_btn = tk.Frame(filtro_win); f_btn.pack(pady=10)
            ttk.Button(f_btn, text="✅ Applica", command=applica, style="Verde.TButton").pack(side="left", padx=10)
            ttk.Button(f_btn, text="🎛 Cancella filtri", command=cancella, style="Giallo.TButton").pack(side="right", padx=10)

        def esporta_risultato():
            contenuto = "Data,Categoria,Descrizione,Tipo,Importo\n"
            for item in tree.get_children():
                values = tree.item(item, "values")
                values_cleaned = [str(v).replace(" €", "") for v in values]
                contenuto += ",".join(values_cleaned) + "\n"
                
            if not contenuto.strip():
                self.show_custom_warning("Esportazione", "⚠️ Nessun contenuto da salvare.")
                return

            nome_file = f"Risultati_Ricerca_{datetime.date.today():%d_%m_%Y}.txt"
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File di testo", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=nome_file,
                title="Salva risultati ricerca",
                confirmoverwrite=False,
                parent=finestra
            )
            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return
                try:
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(contenuto)
                    self.show_custom_warning("Esportazione completata", f"✅ Risultati salvati:\n{file}")
                except Exception as e:
                    self.show_custom_warning("Errore", f"❌ Salvataggio fallito:\n{e}")

        def sort_by_column(tv, col, reverse):
            cols = list(tv["columns"])
            try:
                col_index = cols.index(col)
            except ValueError:
                return
            def converti_importo(s):
                s = str(s).strip()
                s = s.replace('€', '').strip()
                if s.count(',') == 1 and s.count('.') == 0:
                    s = s.replace(',', '.')
                s = s.replace('.', '').replace(',', '')
                try:
                    return float(s)
                except ValueError:
                    return float('-inf')
            def converti_data(s):
                try:
                    return datetime.datetime.strptime(str(s), '%d/%m/%Y')
                except ValueError:
                    return datetime.datetime.min
            l = []
            for k in tv.get_children(''):
                item_values = tv.item(k, 'values')
                if item_values and len(item_values) > col_index:
                    if col == "Importo":
                        sort_value = converti_importo(item_values[col_index])
                    elif col == "Data":
                        sort_value = converti_data(item_values[col_index])
                    else:
                        sort_value = item_values[col_index]
                    l.append((sort_value, k))
                else:
                    l.append(('', k))
            l.sort(key=lambda t: t[0], reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: sort_by_column(tv, col, not reverse))
            
        frame_bottoni = tk.Frame(finestra)
        frame_bottoni.pack(pady=(0, 12))

        ttk.Button(frame_bottoni, text="🔍 Cerca", command=esegui_ricerca, style="Verde.TButton").pack(side="left", padx=6)
        ttk.Button(frame_bottoni, text="📄 Esporta", command=esporta_risultato, style="Arancio.TButton").pack(side="left", padx=6)
        ttk.Button(frame_bottoni, text="⚙️ Filtri avanzati", command=apri_filtri_avanzati, style="Blu.TButton").pack(side="left", padx=6)
        ttk.Button(frame_bottoni, text="↺ Reset", command=resetta_campo, style="Giallo.TButton").pack(side="left", padx=6)
        ttk.Button(frame_bottoni, text="❌ Chiudi", command=finestra.destroy, style="Giallo.TButton").pack(side="left", padx=6)


    def cerca_doppio_click(self, event):
        tree = event.widget
        item_id = tree.focus()
        if not item_id:
            return
        vals = tree.item(item_id, "values")
        if not vals or len(vals) < 1:
            return
        data_str = vals[0]  
        try:
            giorno = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
        except Exception:
            return
        self.set_stats_mode("giorno")
        if hasattr(self, "cal"):
            self.cal.selection_set(giorno)
            self.cal._sel_date = giorno
            self.stats_refdate = giorno
        self.update_stats()
        self.estratto_month_var.set(f"{giorno.month:02d}")
        self.estratto_year_var.set(str(giorno.year))
        self.stats_label.config(text=f"Riepilogo Giornaliero - {giorno.strftime('%d-%m-%Y')}", foreground="purple",
    font=("Arial", 10, "bold"))

    def rubrica_app(self):
        root = tk.Toplevel()
        root.title("Rubrica Contatti")
        window_width, window_height = 800, 530
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
        #root.resizable(False, False)
        
        contatti = []

        def salva_su_json():
            with open(DATI_FILE, "w", encoding="utf-8") as f:
                json.dump(contatti, f, indent=2, ensure_ascii=False)

        def carica_da_json():
            if os.path.exists(DATI_FILE):
                with open(DATI_FILE, "r", encoding="utf-8") as f:
                    try:
                        dati = json.load(f)
                        contatti.clear()
                        contatti.extend(dati)
                        aggiorna_lista()
                    except:
                        self.show_custom_warning("Attenzione", "File rubrica non valido !")

        def aggiorna_lista():
            lista_contatti.delete(0, tk.END)
            for c in contatti:
                lista_contatti.insert(tk.END, c["nome"])

        def aggiungi_contatto():
            nome = entry_nome.get().strip()
            telefono = entry_telefono.get().strip()
            email = entry_email.get().strip()
            note = entry_note.get("1.0", tk.END).strip()
            
            if len(nome) > 43 or len(telefono) > 43 or len(email) > 43 or len(note) > 100:
               self._show_custom_message("Limite superato", "Hai superato il limite massimo di caratteri:\n\n"
                                "- Nome: 43\n- Telefono: 43\n- Email: 43\n- Note:100",
                                "#fff3cd", "#856404")
               return
               
            if nome:
                contatti.append({"nome": nome, "telefono": telefono, "email": email, "note": note})
                salva_su_json()
                aggiorna_lista()
                pulisci_campi()
                self.show_custom_warning("Attenzione", "Contatto aggiunto correttamente !")
                
        def modifica_contatto():
            idx = lista_contatti.curselection()
            if not idx: return
            i = idx[0]
            contatti[i] = {
                "nome": entry_nome.get(),
                "telefono": entry_telefono.get(),
                "email": entry_email.get(),
                "note": entry_note.get("1.0", tk.END).strip()
            }
            salva_su_json()
            aggiorna_lista()
            self.show_custom_warning("Attenzione", "Contatto modificato correttamente !")
            
        def cancella_contatto():
            idx = lista_contatti.curselection()
            if not idx: return
            contatti.pop(idx[0])
            salva_su_json()
            aggiorna_lista()
            pulisci_campi()
            self.show_custom_warning("Attenzione", "Contatto cancellato con successo !")
            
        def esporta_txt():
            now = datetime.date.today()
            if not contatti:
                self.show_custom_warning("Attenzione", "Nessun Contatto. Rubrica vuota")
                return
            default_filename = f"Rubrica_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File txt", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=default_filename,
                title="Salva Rubrica",
                confirmoverwrite=False,
                parent=root)
 
            if path:
                if os.path.exists(path):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(path)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return 
                        
                with open(path, "w", encoding="utf-8") as f:
                    for c in contatti:
                        f.write(f"Nome: {c['nome']}   Telefono: {c['telefono']}   Email: {c['email']}\nNote: {c['note']}\n\n")
                    self.show_custom_warning("Attenzione", f"Rubrica esportata con successo in {path}")
                        
        def esporta_rubrica():
            now = datetime.date.today()
            default_dir = EXP_DB
            default_filename = f"Rubrica_Export_{now.day:02d}-{now.month:02d}-{now.year}.json"
            if not contatti:
                self.show_custom_warning("Attenzione", "Nessun contatto, la rubrica e' vuota !")
                return
            path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("File JSON", "*.json")],
                initialdir=default_dir,
                initialfile=default_filename,
                title="Salva Rubrica .json",
                confirmoverwrite=False,
                parent=root
            )
            if path:
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(contatti, f, indent=2, ensure_ascii=False)
                    self.show_custom_warning("Attenzione", f"Rubrica salvata con successo in {path}")
                except Exception as e:
                    self.show_custom_warning("Attenzione", f"Impossibile salvare la rubrica:\n{e}")
        
        def importa_rubrica():
            default_dir = EXP_DB
            path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("File JSON", "*.json")],
                initialdir=EXP_DB,
                parent=root
            )
            if path:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        dati_importati = json.load(f)
                        if isinstance(dati_importati, list):
                            contatti.clear()
                            contatti.extend(dati_importati)
                            aggiorna_lista()
                            self.show_custom_warning("Importazione riuscita", "Rubrica importata correttamente!")
                        else:
                            self.show_custom_warning("Errore", "Il file selezionato non contiene una rubrica valida.")
                except Exception as e:
                            self.show_custom_warning("Errore", f"Impossibile importare la rubrica:\n{e}")
                   
        def seleziona_contatto(event):
            idx = lista_contatti.curselection()
            if not idx: return
            c = contatti[idx[0]]
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, c["nome"])
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, c["telefono"])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, c["email"])
            entry_note.delete("1.0", tk.END)
            entry_note.insert("1.0", c["note"])

        def cerca_contatto(event=None):
            query = entry_cerca.get().lower()
            lista_contatti.delete(0, tk.END)
            for c in contatti:
                if query in c["nome"].lower():
                    lista_contatti.insert(tk.END, c["nome"])

        def pulisci_campi():
            entry_nome.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_note.delete("1.0", tk.END)
            lista_contatti.selection_clear(0, tk.END)

        frame_input = ttk.Frame(root)
        frame_input.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(frame_input, text="Nome:").grid(row=0, column=0, sticky="e")
        entry_nome = ttk.Entry(frame_input, width=45)
        entry_nome.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_input, text="Telefono:").grid(row=1, column=0, sticky="e")
        entry_telefono = ttk.Entry(frame_input, width=45)
        entry_telefono.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_input, text="Email:").grid(row=2, column=0, sticky="e")
        entry_email = ttk.Entry(frame_input, width=45)
        entry_email.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame_input, text="Note:").grid(row=3, column=0, sticky="ne")
        entry_note = tk.Text(frame_input, width=45, height=5)
        entry_note.grid(row=3, column=1, padx=5, pady=2)

        frame_cerca = ttk.Frame(root)
        frame_cerca.pack(padx=10, pady=(5, 10), fill=tk.X)
        ttk.Label(frame_cerca, text="      Cerca:  ").pack(side=tk.LEFT)
        entry_cerca = ttk.Entry(frame_cerca, width=30)
        entry_cerca.pack(side=tk.LEFT, padx=5)
        entry_cerca.bind("<Return>", cerca_contatto)
        entry_cerca.bind("<KP_Enter>", cerca_contatto)
        lista_contatti = tk.Listbox(root, width=85, height=10)
        lista_contatti.pack(padx=10, pady=10)
        lista_contatti.bind("<<ListboxSelect>>", seleziona_contatto)
        
        frame_btn = ttk.Frame(root)
        frame_btn.pack(pady=10)

        ttk.Button(frame_btn, text="👤 Aggiungi", command=aggiungi_contatto, style="Verde.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="🔄 Modifica", command=modifica_contatto, style="Arancio.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="❌ Cancella", command=cancella_contatto, style="Rosso.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="ℹ️ Esporta stampa", command=esporta_txt, style="Verde.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="📂 Esporta Rubrica", command=esporta_rubrica, style="Rosso.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="📂 Importa Rubrica", command=importa_rubrica, style="Rosso.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(frame_btn, text="❌ Chiudi", command=root.destroy, style="Giallo.TButton").pack(side=tk.LEFT, padx=4)
        
        carica_da_json()       
        root.bind("<Escape>", lambda e: root.destroy())  
        root.mainloop()

    def mostra_calendario_popup(self, entry_widget, var_data):
 
        if hasattr(self, "popup_calendario") and self.popup_calendario and self.popup_calendario.winfo_exists():
            self.popup_calendario.destroy()
            self.popup_calendario = None
            self.unbind_all('<Button-1>')
            self.unbind_all('<Escape>')
            return
        entry_widget.update_idletasks()
        x = entry_widget.winfo_rootx()
        y = entry_widget.winfo_rooty()
        w = entry_widget.winfo_width()

        self.popup_calendario = tk.Toplevel(self)
        self.popup_calendario.withdraw() 
        self.popup_calendario.title("Seleziona una Data")
        #self.popup_calendario.wm_overrideredirect(True)
        self.popup_calendario.geometry(f"{w+250}x180+{x}+{y - 220}")

        self.bind_all('<Button-1>', self.check_click_outside_calendar)
        self.bind_all('<Escape>', self.check_click_outside_calendar)
        
        cal = Calendar(
            self.popup_calendario,
            showothermonthdays=False,
            date_pattern="dd-mm-yyyy",
            locale="it_IT",
            font=("Arial", 10),
            selectbackground="blue",
            weekendbackground="lightblue",
            weekendforeground="darkblue"
        )
        cal.pack(fill="both", expand=True)

        oggi = datetime.date.today()
        cal.calevent_create(oggi, "Oggi", "today")
        cal.tag_config("today", background="gold", foreground="black")

        try:
            cal._header_month.config(font=("Arial", 12, "bold"))
            cal._header_year.config(font=("Arial", 12, "bold"))
        except:
            pass
            
        def select_date(event):
            var_data.set(cal.selection_get().strftime("%d-%m-%Y"))
            self.popup_calendario.destroy()
            self.popup_calendario = None
            self.unbind_all('<Button-1>')
            self.unbind_all('<Escape>')

        cal.bind("<<CalendarSelected>>", select_date)
        self.popup_calendario.deiconify()
    def check_click_outside_calendar(self, event):
 
        if event.keysym == 'Escape':
            if hasattr(self, 'popup_calendario') and self.popup_calendario and self.popup_calendario.winfo_exists():
                self.popup_calendario.destroy()
                self.popup_calendario = None
                self.unbind_all('<Button-1>')
                self.unbind_all('<Escape>')
            return

        if not (hasattr(self, 'popup_calendario') and self.popup_calendario and self.popup_calendario.winfo_exists()):
            return
            
        x_cal = self.popup_calendario.winfo_rootx()
        y_cal = self.popup_calendario.winfo_rooty()
        w_cal = self.popup_calendario.winfo_width()
        h_cal = self.popup_calendario.winfo_height()
        
        if not (x_cal <= event.x_root <= x_cal + w_cal and y_cal <= event.y_root <= y_cal + h_cal):
            self.popup_calendario.destroy()
            self.popup_calendario = None
            self.unbind_all('<Button-1>')
            self.unbind_all('<Escape>')
       
        def select_date(event):
            var_data.set(cal.selection_get().strftime("%d-%m-%Y"))
            self.popup_calendario.destroy()
            self.popup_calendario = None
            self.unbind_all('<Button-1>')

        cal.bind("<<CalendarSelected>>", select_date)

        def seleziona_data(event=None):
            var_data.set(cal.get_date())
            chiudi_popup_calendario()

        def chiudi_se_fuori(event=None):
            x, y = self.popup_calendario.winfo_pointerxy()
            widget_sotto = self.popup_calendario.winfo_containing(x, y)
            if widget_sotto is None or not str(widget_sotto).startswith(str(self.popup_calendario)):
                chiudi_popup_calendario()

        def chiudi_popup_calendario():
             if self.popup_calendario and self.popup_calendario.winfo_exists():
                 self.popup_calendario.destroy()
                 self.popup_calendario = None

        cal.bind("<<CalendarSelected>>", seleziona_data)
        self.popup_calendario.bind("<FocusOut>", lambda e: self.popup_calendario.after(150, chiudi_se_fuori))
        cal.focus_set()
        self.popup_calendario.bind("<Escape>", lambda e: chiudi_popup_calendario())

    def anteprima_e_stampa_txt(self):
        now = datetime.date.today()
        default_dir = EXPORT_FILES
        default_filename = ""
        path = filedialog.askopenfilename(
               filetypes=[("File txt", "*.txt")],
               initialdir=default_dir,
               initialfile=default_filename,
               title="Stampa Testi"
               )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            contenuto = f.read()

        anteprima = tk.Toplevel()
        anteprima.withdraw()
        anteprima.title(f"Anteprima stampa: {os.path.basename(path)}")
        anteprima.resizable(False, False)  
        
        larghezza_finestra = 1300
        altezza_finestra = 600

        def centra_finestra():
            larghezza_schermo = anteprima.winfo_screenwidth()
            altezza_schermo = anteprima.winfo_screenheight()
            x = (larghezza_schermo // 2) - (larghezza_finestra // 2)
            y = (altezza_schermo // 2) - (altezza_finestra // 2)
            anteprima.geometry(f"{larghezza_finestra}x{altezza_finestra}+{x}+{y}")
            anteprima.deiconify()
            anteprima.lift()
            anteprima.focus_force()
        anteprima.after(0, centra_finestra)
            
        txt = tk.Text(anteprima, wrap="word", font=("Courier new", 10))
        txt.insert("1.0", contenuto)
        txt.config(state="disabled")
        txt.pack(padx=10, pady=10, fill="both", expand=True)

        def stampa():
            try:
                sistema = platform.system()

                if not os.path.exists(path):
                    raise FileNotFoundError("File non trovato per la stampa")

                if sistema == "Windows":
                    import win32print
                    import win32ui
                    import win32con

                    printer_name = win32print.GetDefaultPrinter()

                    hprinter = win32print.OpenPrinter(printer_name)
                    properties = win32print.GetPrinter(hprinter, 2)
                    devmode = properties["pDevMode"]
                    devmode.Orientation = 2  # 2 = Landscape
                    win32print.ClosePrinter(hprinter)

                    pdc = win32ui.CreateDC()
                    pdc.CreatePrinterDC(printer_name)
                    pdc.SetMapMode(win32con.MM_TEXT)
                    if hasattr(pdc, "ResetDC"):
                          pdc.ResetDC(devmode)
                    else:
                          print("⚠️ Attenzione: ResetDC non disponibile su questo oggetto DC")                                       

                    HORZRES = pdc.GetDeviceCaps(win32con.HORZRES)  
                    VERTRES = pdc.GetDeviceCaps(win32con.VERTRES)  

                    font = win32ui.CreateFont({
                         "name": "Courier New",     
                         "height": -int(VERTRES / 60),  
                         "width": int(HORZRES / 160),  
                    })
                    pdc.SelectObject(font)

                    pdc.StartDoc("Stampa compatibile")
                    pdc.StartPage()
                    margin_x = 100  # Margine sinistro
                    margin_y = 100  # Margine superiore
                    line_height = int(VERTRES / 70)     #60 righe circa dal fondo def.
                    with open(path, "r", encoding="utf-8") as file:
                        y = margin_y
                        for line in file:
                            pdc.TextOut(margin_x, y, line.rstrip())
                            y += line_height
                            if y + line_height > VERTRES:
                        
                                   pdc.EndPage()
                                   pdc.StartPage()
                                   y = margin_y

                    
                    pdc.EndPage()
                    pdc.EndDoc()
                    pdc.DeleteDC()

                elif sistema in ["Linux", "Darwin"]:
                    subprocess.run([
                        "lp",
                        "-o", "orientation-requested=4",
                        "-o", "fit-to-page",
                        "-o", "cpi=17",
                        "-o", "lpi=8",
                        path
                    ], check=True)

                else:
                    raise OSError(f"Sistema non supportato: {sistema}")

                self.show_custom_warning("Stampa Avviata", f"Inviato alla stampante predefinita ({sistema})")

            except subprocess.CalledProcessError as e:
                self.show_custom_warning("Stampa Errore", f"Errore di stampa: {e}")
            except Exception as ex:
                self.show_custom_warning("Errore imprevisto", str(ex))
            
        frame_bottoni = tk.Frame(anteprima)
        frame_bottoni.pack(pady=10, fill="x")
        ttk.Button(frame_bottoni, text="🖨️ Stampa ora", style="Arancio.TButton", command=stampa).pack(side="left", padx=20)
        ttk.Button(frame_bottoni, text="❌ Chiudi", style="Giallo.TButton", command=anteprima.destroy).pack(side="right", padx=20)


    def gruppo_categorie(self):
        popup = tk.Toplevel(self)
        popup.title("📂 Analisi per categorie selezionate")
        popup.geometry("800x650") 
        popup.withdraw() 
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        popup_width = 800
        popup_height = 650
        center_x = main_x + (main_width // 2) - (popup_width // 2)
        center_y = main_y + (main_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup.transient(self)
        popup.update_idletasks()
        popup.deiconify()
        popup.update()  
        #popup.grab_set() 

        main_frame = ttk.Frame(popup, padding=10)
        main_frame.pack(fill="both", expand=True)

        bottom_buttons = ttk.Frame(popup)
        bottom_buttons.pack(fill="x", pady=10)

        today = datetime.date.today()
        mesi = ["Tutti"] + ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
        mese_var = tk.StringVar(value="Tutti")
        anno_var = tk.StringVar(value=str(today.year))

        mostra_future_var = tk.BooleanVar(value=True)

        top_bar = ttk.Frame(main_frame)
        top_bar.pack(fill="x", pady=(0, 10))

        ttk.Label(top_bar, text="Mese:").pack(side="left", padx=(0, 5))
        ttk.Combobox(top_bar, values=mesi, textvariable=mese_var, state="readonly", width=12).pack(side="left")

        anni = sorted({
            d.year if not isinstance(d, str) else datetime.datetime.strptime(d, "%d-%m-%Y").year
            for d in self.spese
        }, reverse=True)

        ttk.Label(top_bar, text="Anno:").pack(side="left", padx=(10, 5))
        ttk.Combobox(top_bar, values=[str(a) for a in anni], textvariable=anno_var, state="readonly", width=8).pack(side="left")
       
        ttk.Button(top_bar,text="↺", style="Yellow.TButton", command=lambda: [mese_var.set("Tutti"),anno_var.set(str(today.year))]).pack(side="left", padx=(10, 0))

        tk.Checkbutton(
            top_bar,
            text="Includi movimenti futuri nei totali",
            bg="yellow",
           activebackground="gold",
            variable=mostra_future_var
        ).pack(side="left", padx=(20,0))

        valori_combo = ["— Nessuna —"] + sorted(list(self.categorie_tipi.keys()))
        
        selettori_box = ttk.LabelFrame(main_frame, text="🎯 Seleziona fino a 10 categorie da analizzare")
        selettori_box.pack(fill="x", pady=(5, 15))

        sx = ttk.Frame(selettori_box)
        dx = ttk.Frame(selettori_box)
        sx.pack(side="left", fill="both", expand=True, padx=(0, 10))
        dx.pack(side="right", fill="both", expand=True)

        combo_vars = []
        for i in range(10):
            var = tk.StringVar(value="— Nessuna —")
            cb = ttk.Combobox(sx if i < 5 else dx, values=valori_combo, textvariable=var, state="readonly", width=35, height=15)
            cb.pack(anchor="w", pady=2)
            combo_vars.append(var)

        ttk.Label(main_frame, text="📊 Risultato:", font=("Arial", 10, "bold")).pack(anchor="w")
        text_output = tk.Text(main_frame, height=18, wrap="word", font=("Courier New", 10))
        scroll = ttk.Scrollbar(main_frame, command=text_output.yview)
        text_output.config(yscrollcommand=scroll.set)
        text_output.pack(side="left", fill="both", expand=True, pady=(5, 10))
        scroll.pack(side="right", fill="y")

        def analizza():
            text_output.delete("1.0", "end")
            try:
                anno = int(anno_var.get())
            except:
                self.show_custom_warning("Errore", "Anno non valido.")
                return

            selezionato = mese_var.get()
            if selezionato not in mesi:
                self.show_custom_warning("Errore", "Mese non valido.")
                return

            scelte = {v.get().strip().title() for v in combo_vars if v.get() != "— Nessuna —"}
            risultato = {}
            oggi = datetime.date.today()

            for d, sp in self.spese.items():
                if isinstance(d, str):
                    d = datetime.datetime.strptime(d, "%d-%m-%Y").date()
                if not mostra_future_var.get() and d > oggi:
                    continue
                if d.year == anno and (selezionato == "Tutti" or d.month == mesi.index(selezionato)):
                    for voce in sp:
                        if len(voce) >= 4:
                            cat = voce[0].strip().title()
                            imp = voce[2]
                            tipo = voce[3]
                            if cat in scelte:
                                if cat not in risultato:
                                    risultato[cat] = {"num": 0, "uscite": 0.0, "entrate": 0.0}
                                risultato[cat]["num"] += 1
                                if tipo == "Uscita":
                                    risultato[cat]["uscite"] += imp
                                elif tipo == "Entrata":
                                    risultato[cat]["entrate"] += imp

            righe = [f"📅 Analisi categorie – {mese_var.get()} {anno}\n"]
            righe.append(f"{'Categoria':<30} {'Num':>4}   {'Uscite (€)':>12}   {'Entrate (€)':>12}   {'Saldo (€)':>12}")
            righe.append("-" * 80)
            totale = 0.0
            for cat, dati in sorted(risultato.items(), key=lambda x: -(x[1]["entrate"] - x[1]["uscite"])):
                saldo = dati["entrate"] - dati["uscite"]
                righe.append(f"{cat:<30} {dati['num']:>4}   {dati['uscite']:>12.2f}   {dati['entrate']:>12.2f}   {saldo:>12.2f}")
                totale += saldo
            righe.append("-" * 80)
            righe.append(f"💰 Totale gruppo categorie (Entrate - Uscite): {totale:.2f} €")
            text_output.insert("1.0", "\n".join(righe))

        def reset_campi():
            mese_var.set("Tutti")
            anno_var.set(str(today.year))
            mostra_future_var.set(True)
            for var in combo_vars:
                var.set("— Nessuna —")
            text_output.delete("1.0", "end")

        def salva():
            contenuto = text_output.get("1.0", "end").strip()
            if not contenuto:
                self.show_custom_warning("Nessun dato", "Nessun risultato da salvare.")
                return
            now = datetime.date.today()
            nome_file = f"Analisi_Categorie_{now:%d_%m_%Y}.txt"
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File di testo", "*.txt")],
                initialfile=nome_file,
                initialdir=EXPORT_FILES,
                title="Esporta risultati",
                confirmoverwrite=False,
                parent=popup
            )
            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return

                with open(file, "w", encoding="utf-8") as f:
                    f.write(contenuto)
                self.show_custom_warning("Esportazione completata", f"File salvato:\n{file}")

        mostra_future_var.trace_add("write", lambda *a: analizza())

        ttk.Button(bottom_buttons, text="📥 Analizza", command=analizza, style="Verde.TButton").pack(side="left", padx=10)
        ttk.Button(bottom_buttons, text="💾 Esporta", command=salva, style="Arancio.TButton").pack(side="left", padx=10)
        ttk.Button(bottom_buttons, text="🟨 Reset campi", command=reset_campi, style="Giallo.TButton").pack(side="left", padx=10)
        ttk.Button(bottom_buttons, text="❌ Chiudi", command=popup.destroy, style="Giallo.TButton").pack(side="right", padx=10)
        popup.bind("<Escape>", lambda e: popup.destroy())

    def calcola_mancanti(self):
        from datetime import datetime, timedelta
        popup = tk.Toplevel()
        popup.withdraw()
        popup.title("📋 Controllo Categorie Ricorrenti")
        w, h = 950, 600
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.resizable(True, True)
        popup.deiconify()
        mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        oggi = datetime.today().date()
        def converti_data(d):
            if isinstance(d, str):
                try:
                    return datetime.strptime(d, "%d-%m-%Y").date()
                except:
                    return None
            elif isinstance(d, datetime):
                return d.date()
            return d

        anni_disponibili = sorted({
            converti_data(d).year for d in self.spese
            if converti_data(d)
        }, reverse=True)

        anno_var = tk.StringVar(value=str(oggi.year))

        top_bar = ttk.Frame(popup, padding=10)
        top_bar.pack(fill="x")
        ttk.Label(top_bar, text="Anno di Analisi:").pack(side="left", padx=6)
        anno_combo = ttk.Combobox(top_bar, textvariable=anno_var,
                                 values=[str(a) for a in anni_disponibili], state="readonly", width=6)
        anno_combo.pack(side="left", padx=6)
        anno_combo.bind("<<ComboboxSelected>>", lambda event: analizza())
        ttk.Button(
            top_bar,
            text="↺ Ricarica Anno",
            style='Yellow.TButton',
            command=lambda: [
                anno_var.set(str(oggi.year)),
                analizza() 
            ]
        ).pack(side="left", padx=2)
        ttk.Label(top_bar, text="Clicca sull'intestazione per ordinare. ✔/✖ = Mese con/senza spese.").pack(side="right", padx=6)

        cols = ["Categoria", "Totale (€)", "Media (€)", "Cadenza"] + mesi
        self.tree = ttk.Treeview(popup, columns=cols, show='headings', selectmode='browse')
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0,8))

        for col in cols:

            self.tree.heading(col, 
                              text=col.replace(" (€)", ""), 
                              anchor="center", 
                              command=lambda c=col: self.treeview_sort_column(self.tree, c, False))

            if col == "Categoria":
                width_val = 150
            elif col == "Totale (€)":
                width_val = 75
            elif col == "Media (€)":
                width_val = 75
            elif col == "Cadenza":
                width_val = 100 
            else:
                width_val = 35 

            if col == "Categoria":
                anchor_data = "w"  
            elif col in ("Totale (€)", "Media (€)"):
                anchor_data = "e"     
            else:
                anchor_data = "center" 
                
            self.tree.column(col, width=width_val, anchor=anchor_data)

        self.tree.tag_configure("mese_presente", foreground="green", font=("Arial", 8, "bold"))
        self.tree.tag_configure("mese_assente", foreground="red")
        self.tree.tag_configure("cadenza_mensile", background="#E6FFE6", foreground="#004C00")
        self.tree.tag_configure("cadenza_regolare", background="#F0FFF0", foreground="#333333")
        self.tree.tag_configure("cadenza_bimestrale", background="#FFFFE0", foreground="#CC9900")
        self.tree.tag_configure("cadenza_trimestrale", background="#FFF0E0", foreground="#FF6600")
        self.tree.tag_configure("cadenza_irregolare", background="#FFEEEE", foreground="#CC0000")
        self.tree.tag_configure("intestazione", background="#CCCCCC", foreground="black", font=("Arial", 10, "bold"))
        
        def analizza():
            dati_mensili = {} 

            for i in self.tree.get_children():
                self.tree.delete(i)
            try:
                anno = int(anno_var.get())
            except ValueError:
                self.show_custom_warning("Errore", "Anno non valido.")
                return
            risultati = {}
            importi_categoria = {}
            conteggio_categoria = {}
            for d, sp in self.spese.items():
                dd = converti_data(d)
                if not dd or dd.year != anno:
                    continue
                mese = dd.month
                for voce in sp:
                    if len(voce) < 1 or not voce[0].strip():
                        continue
                    cat = voce[0].strip().title()
                    importo = voce[2] if len(voce) > 2 and isinstance(voce[2], (int, float)) else 0
                    tipo = voce[3].strip().title() if len(voce) > 3 else "Uscita"
                    importi_categoria[cat] = importi_categoria.get(cat, 0) + importo
                    conteggio_categoria[cat] = conteggio_categoria.get(cat, 0) + 1
                    risultati.setdefault(cat, set()).add(mese)
                    dati_mensili.setdefault(cat, {}).setdefault(mese, {"Entrata": 0, "Uscita": 0})
                    if tipo == "Entrata":
                        dati_mensili[cat][mese]["Entrata"] += importo
                    else:
                        dati_mensili[cat][mese]["Uscita"] += importo
            count = 0

            for cat, mesi_presenti in sorted(risultati.items()):
                if len(mesi_presenti) < 2: 
                    continue
                spesa_totale = importi_categoria.get(cat, 0)
                n_elementi = conteggio_categoria.get(cat, 1)
                media_spesa = spesa_totale / n_elementi
                sorted_months = sorted(list(mesi_presenti))
                avg_interval = 0
                if len(sorted_months) > 1:
                    intervals = [(sorted_months[i] - sorted_months[i-1]) for i in range(1, len(sorted_months))]
                    avg_interval = sum(intervals) / len(intervals)
                if len(mesi_presenti) == 12:
                    cadenza = "Mensile"
                    tag_riga = "cadenza_mensile" 
                elif 0.8 <= avg_interval <= 1.2:
                    cadenza = "Mensile Reg."
                    tag_riga = "cadenza_regolare" 
                elif 1.5 <= avg_interval <= 2.5:
                    cadenza = "Bimestrale"
                    tag_riga = "cadenza_bimestrale" 
                elif 2.5 < avg_interval <= 3.5:
                    cadenza = "Trimestrale"
                    tag_riga = "cadenza_trimestrale" 
                else:
                    cadenza = "Irregolare"
                valori_riga = [
                    cat,
                    f"€{spesa_totale:.2f}",
                    f"€{media_spesa:.2f}",
                    cadenza
                ]
                tags = []
                for mese_idx in range(1, 13):
                    tag = "mese_assente"
                    simbolo = "✖"
                    if mese_idx in mesi_presenti:
                        simbolo = "✔"
                        tag = "mese_presente"
                        
                    if mese_idx == oggi.month and anno == oggi.year:
                        simbolo = f"[{simbolo}]" 
                    valori_riga.append(simbolo)
                    tags.append(tag)
                self.tree.insert("", "end", iid=cat, values=valori_riga, tags=(tag_riga,))
                count += 1
            if count == 0:
                self.tree.insert("", "end", values=("Nessuna categoria ricorrente trovata.", "", "", ""), tags=("intestazione",))
        def on_tree_select(event):
            selected_item = self.tree.focus()
            if not selected_item:
                return
            valori = self.tree.item(selected_item, 'values')
            categoria_selezionata = valori[0]
            if categoria_selezionata.startswith("Nessuna"):
                return
            anno_selezionato = anno_var.get()
            data_filter = {
                "anno": anno_selezionato,
                "mese": None, 
                "categoria": categoria_selezionata,
                "tipo": None
            }
            title = f"Movimenti Ricorrenti: {categoria_selezionata} ({anno_selezionato})"
            self.mostra_transazioni_popup(data_filter, title)
        self.tree.bind("<<TreeviewSelect>>", on_tree_select)
        self.tree.bind("<Double-1>", on_tree_select)
        style = ttk.Style() 
        legenda_frame = ttk.Frame(popup, padding=(10, 5, 10, 5))
        legenda_frame.pack(fill="x")

        ttk.Label(legenda_frame, text="Legenda Cadenza: ", font=("Arial", 8, "bold")).pack(side="left", padx=(0, 10))

        colori_cadenza = [
            ("Mensile", "#E6FFE6", "#004C00", "mensile"),
            ("Regolare", "#F0FFF0", "#333333", "regolare"),
            ("Bimestrale", "#FFFFE0", "#CC9900", "bimestrale"),
            ("Trimestrale", "#FFF0E0", "#FF6600", "trimestrale"),
            ("Irregolare", "#FFEEEE", "#CC0000", "irregolare"),
        ]
        for testo, bg_color, fg_color, alias_name in colori_cadenza:
            stile_legenda = f"Legenda.{alias_name}.TLabel"
            style.configure(stile_legenda, 
                            background=bg_color, 
                            foreground=fg_color, 
                            border=1, 
                            relief="flat") 
            ttk.Label(legenda_frame, text=testo, style=stile_legenda, padding=3).pack(side="left", padx=2)
        ttk.Label(legenda_frame, text=" | Simboli Mese: ", font=("TkDefaultFont", 8, "bold")).pack(side="left", padx=(10, 10))
        ttk.Label(legenda_frame, text="✔ Presente", foreground="green", font=("TkDefaultFont", 8, "bold")).pack(side="left", padx=5)
        ttk.Label(legenda_frame, text="✖ Assente", foreground="red").pack(side="left", padx=5)
        ttk.Label(legenda_frame, text="[ ] Mese Corrente", foreground="#555555").pack(side="left", padx=5)
        bottom_buttons = ttk.Frame(popup)
        bottom_buttons.pack(pady=8)
        ttk.Button(bottom_buttons, text="✖ Chiudi", command=popup.destroy, style="Giallo.TButton").pack(side="right", padx=10)
        popup.bind("<Escape>", lambda e: popup.destroy())
        analizza()

    def time_machine(self):
        popup = tk.Toplevel()
        popup.title("🕰️ Time Machine – Simulazione per categoria")
        popup.geometry("880x650")
        popup.withdraw()
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        popup_width = 880
        popup_height = 650
        center_x = main_x + (main_width // 2) - (popup_width // 2)
        center_y = main_y + (main_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup.transient(self)
        popup.update_idletasks()
        popup.deiconify()
        popup.update()
        # popup.grab_set()

        main = ttk.Frame(popup, padding=10)
        main.pack(fill="both", expand=True)

        anni_disponibili = sorted({datetime.datetime.strptime(str(d), "%d-%m-%Y").year
                                   if isinstance(d, str) else d.year for d in self.spese}, reverse=True)
        anno_var = tk.IntVar(value=datetime.date.today().year)
        mostra_future_var = tk.BooleanVar(value=True)

        top_bar = ttk.Frame(main)
        top_bar.pack(fill="x", pady=(0, 10))
        ttk.Label(top_bar, text="Anno:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        anno_combo = ttk.Combobox(top_bar, textvariable=anno_var, values=anni_disponibili, state="readonly", width=8)
        anno_combo.pack(side="left")
        ttk.Button(
            top_bar,
            text="↺",
            style='Yellow.TButton',
            command=lambda: [anno_var.set(datetime.date.today().year)]
        ).pack(side="left", padx=(5, 0))

        tk.Checkbutton(
            top_bar,
            text="Includi movimenti futuri nei totali",
            bg="yellow",
            activebackground="gold",
            variable=mostra_future_var
        ).pack(side="left", padx=(30, 0))

        colonne = ttk.Frame(main)
        colonne.pack(fill="x", padx=5)

        sinistra = ttk.Frame(colonne)
        destra = ttk.Frame(colonne)
        sinistra.pack(side="left", fill="both", expand=True, padx=(0, 40))
        destra.pack(side="right", fill="both", expand=True)

        ttk.Label(sinistra, text="🎯 Selezione manuale", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 6))
        destra_label = ttk.Label(destra, text="📊 Top 10 categorie per risparmio", font=("Arial", 10, "bold"))
        destra_label.pack(anchor="w", pady=(0, 6))

        combo_vars = []
        combo_widgets = []
        for _ in range(10):
            var = tk.StringVar()
            cbx = ttk.Combobox(sinistra, textvariable=var, state="readonly", width=30)
            cbx.set("— Nessuna —")
            cbx.pack(pady=2, anchor="w")
            combo_vars.append(var)
            combo_widgets.append(cbx)

        selezioni = {}

        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=14)
        ttk.Label(main, text="💡 Risultato della simulazione:", font=("Arial", 10, "bold")).pack(anchor="w", padx=5)
        text_output = tk.Text(main, height=10, wrap="word")
        text_output.pack(fill="both", expand=False, padx=5, pady=(0, 10))
        text_output.configure(font=("Courier New", 10))

        def aggiorna_categorie():
            anno = anno_var.get()
            contatori = {}
            oggi = datetime.date.today()
            for d, sp in self.spese.items():
                try:
                    if isinstance(d, str):
                        d_conv = datetime.datetime.strptime(d, "%d-%m-%Y").date()
                    else:
                        d_conv = d
                except:
                    continue
                if not mostra_future_var.get() and d_conv > oggi:
                    continue
                if d_conv.year != anno:
                    continue
                for voce in sp:
                    if len(voce) < 4:
                        continue
                    cat, _, imp, tipo = voce[:4]
                    key = cat.strip().lower()
                    if key not in contatori:
                        contatori[key] = {"count": 0, "uscite": 0.0, "entrate": 0.0}
                    contatori[key]["count"] += 1
                    if tipo == "Uscita":
                        contatori[key]["uscite"] += imp
                    elif tipo == "Entrata":
                        contatori[key]["entrate"] += imp

            for key in contatori:
                contatori[key]["risparmio"] = contatori[key]["uscite"] - contatori[key]["entrate"]
            return contatori

        def aggiorna_interfaccia(*_):
            contatori = aggiorna_categorie()

            tutte_categorie_da_spese = [k.lower() for k in contatori.keys()]
            tutte_categorie_principali = [k.lower() for k in self.categorie_tipi.keys()]
            
            tutte_categorie = sorted(list(set(tutte_categorie_da_spese) | set(tutte_categorie_principali)))
            
            valori_combo = ["— Nessuna —"] + tutte_categorie

            for var, cb in zip(combo_vars, combo_widgets):
                cb["values"] = valori_combo
                if var.get().strip().lower() not in tutte_categorie:
                    var.set("— Nessuna —")

            for w in destra.winfo_children():
                if w != destra_label:
                    w.destroy()

            top_cat = sorted(contatori.items(), key=lambda x: -x[1]["risparmio"])[:10]
            selezioni.clear()
            for cat, dati in top_cat:
                var = tk.BooleanVar(value=False)
                selezioni[cat] = (var, dati)
                txt = f"{cat.title()} – {dati['count']}×, Risparmio: {dati['risparmio']:.2f} € (Uscite: {dati['uscite']:.2f} - Entrate: {dati['entrate']:.2f})"
                chk = tk.Checkbutton(destra, text=txt, variable=var)
                chk.pack(anchor="w", pady=2)

        def esegui_simulazione():
            contatori = aggiorna_categorie()
            text_output.delete("1.0", tk.END)
            lines = [f"🕰️ Time Machine – Anno {anno_var.get()}\n"]
            totale = 0.0
            scelte = set()

            for cat, (var, _) in selezioni.items():
                if var.get():
                    scelte.add(cat)

            for var in combo_vars:

                val = var.get().strip().lower()
                if val and val != "— nessuna —" and val in contatori:
                    scelte.add(val)

            risultati = []
            for cat in scelte:
                dati = contatori.get(cat)
                if dati:
                    risultati.append((cat, dati["count"], dati["uscite"], dati["entrate"], dati["risparmio"]))

            risultati.sort(key=lambda x: -x[4])

            lines.append(f"💭 Proiezione del risparmio ottenibile nel {anno_var.get()}, escludendo le categorie selezionate: ➤\n")
            lines.append(f"{'Categoria':<25} {'Num':>4}   {'Uscite (€)':>12}   {'Entrate (€)':>12}   {'Risparmio (€)':>14}")
            lines.append("-" * 77)
            for cat, n, usc, ent, risp in risultati:
                lines.append(f"{cat.title():<25} {n:>4}   {usc:>12.2f}   {ent:>12.2f}   {risp:>14.2f}")
                totale += risp
            lines.append("-" * 77)
            lines.append(f"\n💰 Risparmio totale teorico: {totale:.2f} € (Uscite - Entrate delle categorie selezionate)")
            text_output.insert("1.0", "\n".join(lines))

        def reset_tutto():
            anno_var.set(datetime.date.today().year)
            mostra_future_var.set(True)
            for var in combo_vars:
                var.set("— Nessuna —")
            for var, _ in selezioni.values():
                var.set(False)
            text_output.delete("1.0", tk.END)
            aggiorna_interfaccia()

        def salva_file():
            content = text_output.get("1.0", "end").strip()
            if not content:
                self.show_custom_warning("Nessun dato", "Non c'è nessuna simulazione da salvare.")
                return
            now = datetime.date.today()
            default_filename = f"Time_Machine_{now.day:02d}_{now.month:02d}_{now.year}.txt"
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File txt", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=default_filename,
                title="Esporta risultato simulazione",
                confirmoverwrite=False,
                parent=popup)

            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return
                with open(file, "w", encoding="utf-8") as f:
                    f.write(content)
                self.show_custom_warning("Esportazione completata", f"Simulazione salvata in:\n{file}")

        anno_combo.bind("<<ComboboxSelected>>", lambda e: aggiorna_interfaccia())
        mostra_future_var.trace_add("write", lambda *a: aggiorna_interfaccia())
        aggiorna_interfaccia()
        pulsanti = ttk.Frame(main)
        pulsanti.pack(pady=5)
        ttk.Button(pulsanti, text="🟥 Simula Risparmio", command=esegui_simulazione, style="Verde.TButton").pack(side="left", padx=10)
        ttk.Button(pulsanti, text="💾 Esporta", command=salva_file, style="Arancio.TButton").pack(side="left", padx=10)
        ttk.Button(pulsanti, text="🔄 Reset campi", command=reset_tutto, style="Giallo.TButton").pack(side="left", padx=10)
        ttk.Button(pulsanti, text="✖ Chiudi", command=popup.destroy, style="Giallo.TButton").pack(side="left", padx=10)
        popup.bind("<Escape>", lambda e: popup.destroy())
        
    def on_spese_mese_tree_double_click(self, event):
        item_id = self.spese_mese_tree.identify_row(event.y)
        if not item_id:
            return
        values = self.spese_mese_tree.item(item_id, "values")
        if not values:
            return
        data_str = str(values[0]).strip()
        try:
            giorno = datetime.datetime.strptime(data_str, "%d-%m-%Y").date()
        except Exception:
            try:
                giorno = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
            except Exception:
                return
        self.set_stats_mode("giorno")
        if hasattr(self, "cal"):
            self.cal.selection_set(giorno)
            self.cal._sel_date = giorno
        self.update_stats()
        self.stats_label.config(text=f"Riepilogo Giornaliero - {giorno.strftime('%d-%m-%Y')}", foreground="purple",
    font=("Arial", 10, "bold"))

    def on_stats_table_double_click(self, event):
        mode = self.stats_mode.get()
        if mode not in ("mese", "anno", "totali"):
            return
        item_id = self.stats_table.identify_row(event.y)
        if not item_id:
            return
        values = self.stats_table.item(item_id, "values")
        if not values or len(values) < 1:
            return

        categoria = str(values[0]).strip()
        spese_categoria = []

        if mode == "mese":
            ref = self.stats_refdate
            mese, anno = ref.month, ref.year
            for d, sp in self.spese.items():
                if d.month == mese and d.year == anno:
                    for entry in sp:
                        cat, desc, imp, tipo = entry[:4]
                        if cat == categoria:
                            spese_categoria.append((d, desc, imp, tipo))
            titolo_periodo = f"{mese:02d}-{anno}"
            testo_periodo = f"il mese {mese:02d}-{anno}"
        elif mode == "anno":
            ref = self.stats_refdate
            anno = ref.year
            for d, sp in self.spese.items():
                if d.year == anno:
                    for entry in sp:
                        cat, desc, imp, tipo = entry[:4]
                        if cat == categoria:
                            spese_categoria.append((d, desc, imp, tipo))
            titolo_periodo = f"{anno}"
            testo_periodo = f"l'anno {anno}"
        elif mode == "totali":
            for d, sp in self.spese.items():
                for entry in sp:
                    cat, desc, imp, tipo = entry[:4]
                    if cat == categoria:
                        spese_categoria.append((d, desc, imp, tipo))
            titolo_periodo = "Tutte le annualità"
            testo_periodo = "tutti gli anni"

        if not spese_categoria:
            self.show_custom_info("Nessuna spesa", f"Nessuna spesa per la categoria '{categoria}' nel periodo selezionato.")
            return

        style = ttk.Style()

        popup = tk.Toplevel(self)
        popup.title(f"Dettaglio spese - {categoria} ({titolo_periodo})")
        popup.geometry("650x400")
        popup.withdraw()
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        popup_width = 650
        popup_height = 400
        center_x = main_x + (main_width // 2) - (popup_width // 2)
        center_y = main_y + (main_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
        popup.transient(self)
        popup.update_idletasks()
        popup.deiconify()
        popup.update()
        popup.grab_set()

        label = tk.Label(
            popup,
            text=f"Spese categoria '{categoria}' per {testo_periodo}",
            font=("Arial", 11)
        )
        label.pack(pady=8)

        columns = ("Data", "Descrizione", "Importo", "Tipo")
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=10)
        tree.pack(fill="both", expand=True, padx=10, pady=6)

        def ordina_colonna(treeview, colonna, inverti):
            dati = [(treeview.set(k, colonna), k) for k in treeview.get_children("")]

            try:
                if colonna == "Data":
                    dati.sort(
                        key=lambda t: datetime.datetime.strptime(t[0], "%d-%m-%Y"),
                        reverse=inverti
                    )
                elif colonna == "Importo":
                    dati.sort(
                        key=lambda t: float(t[0].replace(",", ".").replace("€", "")),
                        reverse=inverti
                    )
                else:
                    dati.sort(key=lambda t: t[0].lower(), reverse=inverti)
            except Exception as e:
                print("Errore ordinamento:", e)

            for index, (_, k) in enumerate(dati):
                treeview.move(k, "", index)

            treeview.heading(colonna, command=lambda: ordina_colonna(treeview, colonna, not inverti))

        for col, w in zip(columns, (90, 230, 100, 80)):
            anchor = "w" if col == "Descrizione" else "center"
            tree.heading(col, text=col, command=lambda c=col: ordina_colonna(tree, c, False))
            tree.column(col, width=w, anchor=anchor)

        tot_entrate = tot_uscite = 0.0
        for d, desc, imp, tipo in sorted(spese_categoria, key=lambda x: x[0], reverse=True):
            tag_name = f"row_{d.strftime('%Y%m%d%H%M%S')}_{len(tree.get_children(''))}"
            tree.insert("", "end", values=(d.strftime("%d-%m-%Y"), desc, f"{imp:.2f} €", tipo), tags=(tag_name,))
            if tipo == "Entrata":
                tree.tag_configure(tag_name, foreground="green")
            else:
                tree.tag_configure(tag_name, foreground="red")
            if tipo == "Entrata":
                tot_entrate += imp
            else:
                tot_uscite += imp
        saldo = tot_entrate - tot_uscite
        lbl = tk.Text(popup, height=1, borderwidth=0, font=("Arial", 10, "bold"), wrap="none", background=popup.cget("background"))
        lbl.pack(pady=7)
        lbl.tag_config("entrate_color", foreground="green")
        lbl.tag_config("uscite_color", foreground="red")
        lbl.tag_config("saldo_pos_color", foreground="green")
        lbl.tag_config("saldo_neg_color", foreground="red")
        text_full = f"Totale entrate: {tot_entrate:.2f} €   Totale uscite: {tot_uscite:.2f} €   Saldo: {saldo:.2f} €"
        lbl.config(state="normal")
        lbl.insert("end", text_full)
        entrate_start = text_full.find(f"{tot_entrate:.2f} €")
        entrate_end = entrate_start + len(f"{tot_entrate:.2f} €")
        lbl.tag_add("entrate_color", f"1.{entrate_start}", f"1.{entrate_end}")

        uscite_start = text_full.find(f"{tot_uscite:.2f} €")
        uscite_end = uscite_start + len(f"{tot_uscite:.2f} €")
        lbl.tag_add("uscite_color", f"1.{uscite_start}", f"1.{uscite_end}")

        saldo_start = text_full.find(f"{saldo:.2f} €")
        saldo_end = saldo_start + len(f"{saldo:.2f} €")
        if saldo >= 0:
            lbl.tag_add("saldo_pos_color", f"1.{saldo_start}", f"1.{saldo_end}")
        else:
            lbl.tag_add("saldo_neg_color", f"1.{saldo_start}", f"1.{saldo_end}")
        lbl.config(state="disabled")
        tree.bind("<Double-1>", lambda evt: self.goto_day_from_popup(tree, popup))
        
        ttk.Button(popup, text="✖ Chiudi", style="Giallo.TButton", command=popup.destroy).pack(pady=4)

    def goto_day_from_popup(self, tree, popup):
        if self.stats_view_mode.get() != "tabella":
            self.mostra_treeview_statistiche()

        item_id = tree.focus()
        if not item_id:
            return
        vals = tree.item(item_id, "values")
        if not vals or len(vals) < 1:
            return
        data_str = vals[0]
        try:
            giorno = datetime.datetime.strptime(data_str, "%d-%m-%Y").date()
        except Exception:
            return
        self.set_stats_mode("giorno")
        if hasattr(self, "cal"):
            self.cal.selection_set(giorno)
            self.cal._sel_date = giorno
        self.stats_refdate = giorno
        self.estratto_month_var.set(f"{giorno.month:02d}")
        self.estratto_year_var.set(str(giorno.year))
        self.stats_label.config(text=f"Riepilogo Giornaliero - {giorno.strftime('%d-%m-%Y')}", foreground="purple",
    font=("Arial", 10, "bold"))
        self.after_idle(self.update_stats)
        try:
            popup.destroy()
        except Exception:
            pass

    def on_blocca_data_changed(self):
        if not self.blocca_data_var.get():
            self.data_spesa_var.set(datetime.date.today().strftime("%d-%m-%Y"))
            
    def gestione_login(self):
        def hash_pw(pw):
                return hashlib.sha256(pw.encode()).hexdigest()
        def salva_hash(pw):
                with open(PW_FILE, "w") as f:
                        json.dump({"hash": hash_pw(pw)}, f)
        def leggi_hash():
                if not os.path.exists(PW_FILE):
                        return None
                with open(PW_FILE) as f:
                        return json.load(f).get("hash")
        login_riuscito = [False]
        args = sys.argv

        def crea_campo_password(parent, etichetta=""):
                if etichetta:
                        tk.Label(parent, text=f"\n{etichetta}:", bg="black", fg="white", font=("Arial", 8, "bold")).pack()
                frame_pw = tk.Frame(parent, bg="black")
                frame_pw.pack()
                visibile = tk.BooleanVar(value=False)
                entry_pw = tk.Entry(frame_pw, show="*", width=22, bg="#333333", fg="white", insertbackground="white")
                entry_pw.pack(side="left", padx=(0, 5))
                def toggle_visibilita():
                        if visibile.get():
                                entry_pw.config(show="*")
                                lbl_occhio.config(text="👁")
                                visibile.set(False)
                        else:
                                entry_pw.config(show="")
                                lbl_occhio.config(text="🔒")
                                visibile.set(True)
                lbl_occhio = tk.Label(
                        frame_pw, text="👁", font=("Arial", 10), bg="black", fg="white", cursor="hand2"
                )
                lbl_occhio.pack(side="left")
                lbl_occhio.bind("<Button-1>", lambda e: toggle_visibilita())
                return entry_pw 

        def cambia_password():
                win = tk.Toplevel(self) 
                win.title("🔁 Cambia password")
                win.resizable(False, False)
                w_win, h_win = 380, 260
                x_win = self.winfo_screenwidth() // 2 - w_win // 2
                y_win = self.winfo_screenheight() // 2 - h_win // 2
                win.geometry(f"{w_win}x{h_win}+{x_win}+{y_win}")
                win.grab_set()
                win.configure(bg="black")
                win.focus_force()
                mess = tk.Label(win, text="", fg="red", bg="black")
                entry_attuale = crea_campo_password(win, "Vecchia password")
                entry_nuova = crea_campo_password(win, "Nuova password")
                entry_conferma = crea_campo_password(win, "Conferma nuova password")
                entry_attuale.focus()
                mess.pack()
                def conferma_cambio():
                        attuale = entry_attuale.get()
                        nuova = entry_nuova.get()
                        conferma = entry_conferma.get()
                        def reset_campi():
                                entry_attuale.delete(0, tk.END)
                                entry_nuova.delete(0, tk.END)
                                entry_conferma.delete(0, tk.END)
                                entry_attuale.focus()
                        if hash_pw(attuale) != leggi_hash():
                                mess.config(text="❌ Password attuale errata.", fg="red")
                                reset_campi()
                                return
                        if not nuova:
                                salva_hash(nuova)
                                mess.config(text="✅ Password disattivata.", fg="lightgreen")
                                win.after(1000, win.destroy)
                                return
                        if nuova != conferma:
                                mess.config(text="❌ Le Password non corrispondono.", fg="red")
                                entry_nuova.delete(0, tk.END)
                                entry_conferma.delete(0, tk.END)
                                entry_nuova.focus()
                        else:
                                salva_hash(nuova)
                                mess.config(text="✅ Password aggiornata.", fg="lightgreen")
                                win.after(1000, win.destroy)
                tk.Button(
                        win, text="💾 Salva", command=conferma_cambio, font=("Arial", 8, "bold"),
                        bg="#4CAF50", fg="white", activebackground="#45A049", relief="raised"
                ).pack(pady=8)
                win.wait_window() 

        def mostra_finestra_login():
                login = tk.Toplevel(self)
                login.title(f"🔐 Login {NAME}")
                login.resizable(False, False)
                login.configure(bg="black")
                def chiusura():
                        self._on_close_lock()
                        self.quit()
                        self.destroy()
                login.protocol("WM_DELETE_WINDOW", chiusura)
                w, h = 380, 230
                x = self.winfo_screenwidth() // 2 - w // 2
                y = self.winfo_screenheight() // 2 - h // 2
                login.geometry(f"{w}x{h}+{x}+{y}")
                login.deiconify()
                login.lift()
                login.focus_force()
                login.grab_set()

                if os.path.exists(PW_FILE):
                        tk.Label(login, text=f"Utente:► {current_folder} \n\n🔑 Inserisci la password: ↵\n",
                                 font=("Arial", 8, "bold"), bg="black", fg="white").pack(pady=(15, 5))
                else:
                        tk.Label(login, text=f"🆕 PRIMO ACCESSO \n\n Utente:► {current_folder} \n\n🔐 Crea una nuova password per proteggere i tuoi dati. ↵\n ", 
                                 font=("Arial", 8, "bold"), bg="black", fg="white").pack(pady=(15, 5))

                entry_pw = crea_campo_password(login) 
                entry_pw.focus()
                messaggio_errore = tk.Label(login, text="", fg="red", font=("Arial", 8), bg="black")
                messaggio_errore.pack()
                
                def conferma_login():
                        inserita = entry_pw.get()
                        salvata = leggi_hash()
                        if not salvata:
                                salva_hash(inserita)
                                messaggio_errore.config(text="✅ Password creata con successo.", fg="lightgreen")
                                login_riuscito[0] = True
                                login.after(1500, login.destroy)
                        elif hash_pw(inserita) == salvata:
                                login_riuscito[0] = True
                                login.destroy()
                        else:
                                entry_pw.delete(0, tk.END)
                                messaggio_errore.config(text="❌ Password errata.")
                tk.Button(
                        login, text="Login", command=conferma_login, font=("Arial", 8, "bold"),
                        bg="#4CAF50", fg="white", activebackground="#45A049", activeforeground="white", relief="raised"
                ).pack(pady=7)

                entry_pw.bind("<Return>", lambda e: conferma_login())
                entry_pw.bind("<KP_Enter>", lambda e: conferma_login())
                login.bind("<Escape>", lambda e: login.destroy())

                if os.path.exists(PW_FILE):
                        tk.Button(
                                login, text="🔁 Cambia password", command=cambia_password,
                                bg="#2196F3", fg="white", activebackground="#1976D2", activeforeground="white",
                                relief="raised", font=("Arial", 8, "bold"), cursor="hand2"
                        ).pack(pady=(2, 8))

                login.wait_window()

        if "noweb" not in args:
                threading.Thread(target=self.start_web_server, daemon=True).start()
                print("🌐 Server web avviato di default (nessun 'noweb' tra gli argomenti).")
        else:
                print("🛑 Server web disattivato da 'noweb'.")

        if "auto" in args:
                index = args.index("auto")
                arg_password = args[index + 1] if len(args) > index + 1 else ""
                salvata = leggi_hash()
                if salvata and hash_pw(arg_password) == salvata:
                        print("✅ Login automatico riuscito.")
                        login_riuscito[0] = True
                        self.after(3000, self._iconizza_finestra_startup)
                        return login_riuscito[0]
                else:
                        print("❌ Password da argomento non valida. Apro GUI...")
        if not login_riuscito[0]:
                mostra_finestra_login()
        return login_riuscito[0]
        
    def apri_finestra_importa(self):
        win = tk.Toplevel(self)
        win.title("Importa Spese")
        larghezza, altezza = 300, 160
        x = (win.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (win.winfo_screenheight() // 2) - (altezza // 2)
        win.geometry(f"{larghezza}x{altezza}+{x}+{y}")

        win.resizable(False, False)
        win.grab_set()
        win.configure(bg="#F9F9D1") 

        tk.Label(win, text="Seleziona la banca:", font=("Arial", 10), bg="#F9F9D1").pack(pady=(10, 4))

        banca_var = tk.StringVar()
        banca_combo = ttk.Combobox(win, textvariable=banca_var, state="readonly", values=["-- Nessuna --", "UniCredit", "Intesa", "Fineco", "Altra..."])
        banca_combo.set("-- Nessuna --")  
        banca_combo.pack()

        frame_bottoni = tk.Frame(win, bg="#F9F9D1")
        frame_bottoni.pack(pady=10)

        style = ttk.Style()

        btn_icc = ttk.Button(frame_bottoni, text="💳 ICC", width=10, style="Verde.TButton", command=lambda: [win.destroy(), self.importa_spese_csv_unicredit()])
        btn_ccv = ttk.Button(frame_bottoni, text="🏦 CCV", width=10, style="Verde.TButton", command=lambda: [win.destroy(), self.importa_spese_cc_csv_unicredit()])
        btn_icc.pack(side="left", padx=8)
        btn_ccv.pack(side="right", padx=8)
        btn_icc.pack_forget()
        btn_ccv.pack_forget()
        
        messaggio_var = tk.StringVar()
        label_messaggio = tk.Label(win, textvariable=messaggio_var, font=("Arial", 9), bg="#F9F9D1", fg="gray25")
        label_messaggio.pack(pady=(6, 2))

        def mostra_bottoni(event=None):
            banca = banca_var.get()
            if banca == "UniCredit":
                messaggio_var.set("✅ Importazione disponibile per UniCredit:")
                btn_icc.pack(side="left", padx=8)
                btn_ccv.pack(side="right", padx=8)
            else:
                btn_icc.pack_forget()
                btn_ccv.pack_forget()
                messaggio_var.set(f"⚠️ Importazione da {banca} non ancora disponibile.")

        banca_combo.bind("<<ComboboxSelected>>", mostra_bottoni)

    def importa_spese_csv_unicredit(self):
        from datetime import datetime
        path = filedialog.askopenfilename(
            title="Seleziona Estratto CARTA UNICREDIT",
            filetypes=[("File CSV", "*.csv")]
        )
        if not path:
            return

        movimenti = []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    try:
                        data = datetime.strptime(row["Data Registrazione"], "%d/%m/%Y").date()
                        descrizione = row["Descrizione"].strip()
                        importo = float(row["Importo"].replace(",", "."))
                        movimenti.append({"data": data, "descrizione": descrizione, "importo": importo})
                    except Exception as e:
                        print("Errore riga:", row, "→", e)
        except Exception as e:
            self.show_custom_warning("Errore apertura CSV", str(e))
            return

        if not movimenti:
            self.show_custom_warning("Importazione", "Nessuna spesa valida trovata.")
            return

        movimenti.sort(key=lambda m: m["data"])

        if not hasattr(self, "memoria_descrizioni_categoria"):
            self.memoria_descrizioni_categoria = {}
        memoria = self.memoria_descrizioni_categoria
    
        win = tk.Toplevel(self)
        win.resizable(False, False)
        win.title("Importa da Unicredit Credit Card")
        larghezza, altezza = 820, 600
        x = (win.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (win.winfo_screenheight() // 2) - (altezza // 2)
        win.geometry(f"{larghezza}x{altezza}+{x}+{y}")
        win.update_idletasks()
        win.grab_set()

        contenitore = tk.Frame(win)
        contenitore.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenitore, highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenitore, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        area_dati = tk.Frame(canvas)
        canvas.create_window((0, 0), window=area_dati, anchor="nw")

        area_dati.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        pannello_aggiungi_cat = tk.Frame(area_dati)
        pannello_aggiungi_cat.pack(anchor="w", pady=(6, 6), padx=4)

        tk.Label(pannello_aggiungi_cat, text="➕ Nuova categoria:", foreground="green").pack(side="left", padx=(0, 4))

        var_nuova_cat = tk.StringVar()
        entry_nuova_cat = ttk.Entry(pannello_aggiungi_cat, textvariable=var_nuova_cat, width=20)
        entry_nuova_cat.pack(side="left")

        def aggiungi_categoria_csv():
            nome = var_nuova_cat.get().strip()
            if not nome:
                self.show_custom_warning("Attenzione", "Il nome categoria è vuoto.")
                return
            if nome in self.categorie:
                self.show_custom_warning("Attenzione", "Categoria già esistente.")
                return

            self.categorie.append(nome)
            self.categorie_tipi[nome] = "Uscita"
            memoria[nome.strip().upper()] = nome
            var_nuova_cat.set("")

            for _, _, combo in righe:
                combo["values"] = self.categorie
            self.aggiorna_combobox_categorie()
            self.show_custom_info("Categoria creata", f"Categoria '{nome}' aggiunta.")
        style = ttk.Style()

        btn_aggiungi_cat = ttk.Button(
            pannello_aggiungi_cat,
            text="Aggiungi",
            command=aggiungi_categoria_csv,
            style="Verde.TButton"
        )

        btn_aggiungi_cat.pack(side="left", padx=6)

        entry_nuova_cat.bind("<Return>", lambda e: aggiungi_categoria_csv())
        entry_nuova_cat.bind("<KP_Enter>", lambda e: aggiungi_categoria_csv())
        
        righe = []
        seleziona_tutti_var = tk.BooleanVar(value=True)

        def toggle_tutti():
            for _, var_check, _ in righe:
                var_check.set(seleziona_tutti_var.get())

        tk.Checkbutton(area_dati, text="✔ Seleziona tutto", variable=seleziona_tutti_var, command=toggle_tutti).pack(anchor="w", pady=(5, 2))

        header = tk.Frame(area_dati)
        header.pack(anchor="w")
        tk.Label(header, text="✔", width=2).grid(row=0, column=0)
        tk.Label(header, text="Data", width=10).grid(row=0, column=1)
        tk.Label(header, text="Descrizione", width=40, anchor="w").grid(row=0, column=2)
        tk.Label(header, text="Importo", width=12, anchor="e").grid(row=0, column=3)
        tk.Label(header, text="Categoria", width=20).grid(row=0, column=4)
        for mov in movimenti:
            riga = tk.Frame(area_dati)
            riga.pack(anchor="w", pady=1)
            var = tk.BooleanVar(value=True)
            tk.Checkbutton(riga, variable=var).grid(row=0, column=0)

            tk.Label(riga, text=mov["data"].strftime("%d/%m/%Y"), width=10).grid(row=0, column=1)
            tk.Label(riga, text=mov["descrizione"], width=40, anchor="w").grid(row=0, column=2)
            tk.Label(riga, text=f"{mov['importo']:.2f} €", width=12, anchor="e").grid(row=0, column=3)

            chiave = mov["descrizione"].strip().upper()
            categoria = memoria.get(chiave, "Generica")

            combo = ttk.Combobox(riga, values=self.categorie, state="readonly", width=20)
            combo.set(categoria)
            combo.grid(row=0, column=4, padx=4)

            righe.append((mov, var, combo))

        bottoni = tk.Frame(win)
        bottoni.pack(pady=10)

        def salva():
            count = 0
            duplicati = 0

            for mov, var, combo in righe:
                if var.get():
                    giorno = mov["data"]
                    descr = mov["descrizione"]
                    imp = abs(mov["importo"])
                    tipo = "Entrata" if mov["importo"] >= 0 else "Uscita"
                    cat = combo.get() or "Generica"
                    voce = (cat, descr, imp, tipo)
                    gia_presente = None
                    for voce_esistente in self.spese.get(giorno, []):
                        cat_es, desc_es, imp_es, tipo_es = voce_esistente
                        if (
                            cat_es == cat and
                            tipo_es == tipo and
                            round(imp_es) == round(imp)
                        ):
                            gia_presente = voce_esistente
                            break

                    if gia_presente:
                        if self.conferma_sostituzione_spesa(giorno, cat, imp_es, imp):
                                self.spese[giorno].remove(gia_presente)
                        else:
                                duplicati += 1
                                continue

                    self.spese.setdefault(giorno, []).append(voce)
                    memoria[descr.strip().upper()] = cat
                    count += 1

            self.save_db()
            self.refresh_gui()
            
            messaggio = f"{count} spese importate/salvate."

            if duplicati > 0:
                messaggio += f"\n⚠️ {duplicati} duplicate/ignorate."

            self.show_custom_warning("Completato", messaggio)
            #win.destroy()

        def chiudi():
            win.destroy()
            self.show_custom_warning("Annullato", "Importazione interrotta.")
                 
        ttk.Button(bottoni, text="💾 Salva", style="Verde.TButton", width=12, command=salva).pack(side="left", padx=10)
        ttk.Button(bottoni, text="✖ Chiudi", style="Giallo.TButton", width=12, command=chiudi).pack(side="right", padx=10)

    
    def importa_spese_cc_csv_unicredit(self):
        from datetime import datetime
        path = filedialog.askopenfilename(
            title="Seleziona Estratto Conto UNICREDIT",
            filetypes=[("File CSV", "*.csv")]
        )
        if not path:
            return

        movimenti = []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    try:
                        data_str = row["Data Registrazione"].strip()
                        try:
                            data = datetime.strptime(data_str, "%d/%m/%Y").date()
                        except ValueError:
                            data = datetime.strptime(data_str, "%d.%m.%Y").date()

                        descrizione = row["Descrizione"].strip()

                        importo_str = row["Importo (EUR)"].strip().replace(".", "").replace(",", ".")
                        importo = float(importo_str)

                        movimenti.append({"data": data, "descrizione": descrizione, "importo": importo})
                    except Exception as e:
                        print("Errore riga:", row, "→", e)
        except Exception as e:
            self.show_custom_warning("Errore apertura CSV", str(e))
            return

        if not movimenti:
            self.show_custom_warning("Importazione", "Nessuna spesa valida trovata.")
            return

        movimenti.sort(key=lambda m: m["data"])

        if not hasattr(self, "memoria_descrizioni_categoria"):
            self.memoria_descrizioni_categoria = {}
        memoria = self.memoria_descrizioni_categoria

        win = tk.Toplevel(self)
        win.resizable(False, False)
        win.title("Importa da Unicredit C/C")
        larghezza, altezza = 820, 600
        x = (win.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (win.winfo_screenheight() // 2) - (altezza // 2)
        win.geometry(f"{larghezza}x{altezza}+{x}+{y}")
        win.update_idletasks()
        win.grab_set()

        contenitore = tk.Frame(win)
        contenitore.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenitore, highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenitore, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        area_dati = tk.Frame(canvas)
        canvas.create_window((0, 0), window=area_dati, anchor="nw")

        area_dati.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        pannello_aggiungi_cat = tk.Frame(area_dati)
        pannello_aggiungi_cat.pack(anchor="w", pady=(6, 6), padx=4)

        tk.Label(pannello_aggiungi_cat, text="➕ Nuova categoria:", foreground="green").pack(side="left", padx=(0, 4))

        var_nuova_cat = tk.StringVar()
        entry_nuova_cat = ttk.Entry(pannello_aggiungi_cat, textvariable=var_nuova_cat, width=20)
        entry_nuova_cat.pack(side="left")

        def aggiungi_categoria_csv():
            nome = var_nuova_cat.get().strip()
            if not nome:
                self.show_custom_warning("Attenzione", "Il nome categoria è vuoto.")
                return
            if nome in self.categorie:
                self.show_custom_warning("Attenzione", "Categoria già esistente.")
                return

            self.categorie.append(nome)
            self.categorie_tipi[nome] = "Uscita"
            memoria[nome.strip().upper()] = nome
            var_nuova_cat.set("")

            for _, _, combo in righe:
                combo["values"] = self.categorie
            self.aggiorna_combobox_categorie()
            self.show_custom_info("Categoria creata", f"Categoria '{nome}' aggiunta.")
            
        style = ttk.Style()

        btn_aggiungi_cat = ttk.Button(
            pannello_aggiungi_cat,
            text="Aggiungi",
            command=aggiungi_categoria_csv,
            style="Verde.TButton"
        )
        
        btn_aggiungi_cat.pack(side="left", padx=6)

        entry_nuova_cat.bind("<Return>", lambda e: aggiungi_categoria_csv())
        entry_nuova_cat.bind("<KP_Enter>", lambda e: aggiungi_categoria_csv())
        
        righe = []
        seleziona_tutti_var = tk.BooleanVar(value=True)

        def toggle_tutti():
            for _, var_check, _ in righe:
                var_check.set(seleziona_tutti_var.get())

        tk.Checkbutton(area_dati, text="✔ Seleziona tutto", variable=seleziona_tutti_var, command=toggle_tutti).pack(anchor="w", pady=(5, 2))

        intest = tk.Frame(area_dati)
        intest.pack(anchor="w")
        tk.Label(intest, text="✔", width=2).grid(row=0, column=0)
        tk.Label(intest, text="Data", width=10).grid(row=0, column=1)
        tk.Label(intest, text="Descrizione", width=40, anchor="w").grid(row=0, column=2)
        tk.Label(intest, text="Importo", width=12, anchor="e").grid(row=0, column=3)
        tk.Label(intest, text="Categoria", width=20).grid(row=0, column=4)

        for mov in movimenti:
            riga = tk.Frame(area_dati)
            riga.pack(anchor="w", pady=1)

            var = tk.BooleanVar(value=True)
            tk.Checkbutton(riga, variable=var).grid(row=0, column=0)

            tk.Label(riga, text=mov["data"].strftime("%d/%m/%Y"), width=10).grid(row=0, column=1)
            tk.Label(riga, text=mov["descrizione"], width=40, anchor="w").grid(row=0, column=2)
            tk.Label(riga, text=f"{mov['importo']:.2f} €", width=12, anchor="e").grid(row=0, column=3)

            chiave = mov["descrizione"].strip().upper()
            categoria = memoria.get(chiave, "Generica")

            combo = ttk.Combobox(riga, values=self.categorie, state="readonly", width=20)
            combo.set(categoria)
            combo.grid(row=0, column=4, padx=4)

            righe.append((mov, var, combo))

        bottoni = tk.Frame(win)
        bottoni.pack(pady=10)

        def salva():
            count = 0
            duplicati = 0
            for mov, var, combo in righe:
                if var.get():
                    giorno = mov["data"]
                    descr = mov["descrizione"]
                    imp = abs(mov["importo"])
                    tipo = "Entrata" if mov["importo"] >= 0 else "Uscita"
                    cat = combo.get() or "Generica"
                    voce = (cat, descr, imp, tipo)

                    if voce in self.spese.get(giorno, []):
                        duplicati += 1
                        continue

                    self.spese.setdefault(giorno, []).append(voce)
                    memoria[descr.strip().upper()] = cat
                    count += 1

            self.save_db()
            self.refresh_gui()
            try:
                with open("memoria_categorie.json", "w", encoding="utf-8") as f:
                    json.dump(memoria, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print("⚠️ Impossibile salvare memoria categorie:", e)

            messaggio = f"{count} spese importate/salvate."
            if duplicati > 0:
                messaggio += f"\n⚠️ {duplicati} duplicate/ignorate."

            self.show_custom_warning("Completato", messaggio)

        def chiudi():
            win.destroy()
            self.show_custom_warning("Annullato", "Importazione interrotta.")
            
        ttk.Button(bottoni, text="💾 Salva", style="Verde.TButton", command=salva).pack(side="left", padx=10)
        ttk.Button(bottoni, text="❌ Chiudi", style="Giallo.TButton", command=chiudi).pack(side="right", padx=10)

    def conferma_sostituzione_spesa(self, giorno, categoria, imp_esistente, imp_nuovo):
        popup = tk.Toplevel(self)
        popup.title("Sostituisci spesa?")
        popup.resizable(False, False)
        width, height = 400, 160
        popup.withdraw()
        popup.update_idletasks()

        x = self.winfo_rootx() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.configure(bg="#FFFACD")
        popup.deiconify()
        popup.grab_set()

        msg = (
            f"Esiste già una spesa nella categoria “{categoria}” il {giorno.strftime('%d/%m/%Y')} "
            f"da €{imp_esistente:.2f}.\n\nVuoi sostituirla con la nuova da €{imp_nuovo:.2f}?"
        )

        label = tk.Label(
            popup,
            text=msg,
            font=("Arial", 10),
            justify="center",
            wraplength=360,
            bg="#FFFACD"
        )
        label.pack(pady=12, padx=16)

        frame = tk.Frame(popup, bg="#FFFACD")
        frame.pack(pady=4)

        result = {"ok": False}

        def conferma():
            result["ok"] = True
            popup.destroy()

        def annulla():
            popup.destroy()
        ttk.Button(frame, text="Sostituisci", style="Verde.TButton", width=12, command=conferma).pack(side="left", padx=10)
        ttk.Button(frame, text="Annulla", style="Giallo.TButton", width=12, command=annulla).pack(side="right", padx=10)

        self.wait_window(popup)
        return result["ok"]

    def calcola_statistiche_annuali(self):
        from datetime import date
        oggi = date.today()
        anno_corr = oggi.year
        anno_prec = anno_corr - 1
        mese_corr = oggi.month

        tot_mese_corr, tot_mese_prec = 0.0, 0.0
        tot_anno_corr, tot_anno_prec = 0.0, 0.0

        for giorno, voci in self.spese.items():
            for voce in voci:
                if len(voce) < 4:
                    continue
                categoria, descrizione, importo, tipo = voce[:4]
                if tipo != "Uscita":
                    continue

                if giorno.year == anno_corr and giorno.month == mese_corr:
                    tot_mese_corr += importo
                if giorno.year == anno_prec and giorno.month == mese_corr:
                    tot_mese_prec += importo
                if giorno.year == anno_corr and giorno <= oggi:
                    tot_anno_corr += importo
                if giorno.year == anno_prec and giorno <= oggi.replace(year=anno_prec):
                    tot_anno_prec += importo

        giorni_passati_corr = (oggi - date(anno_corr, 1, 1)).days + 1
        giorni_totali_corr = 365  # Anni non bisestili
        perc_corr = giorni_passati_corr / giorni_totali_corr
        stima_2025 = tot_anno_corr / perc_corr if perc_corr else tot_anno_corr
        stima_2024 = 0.0
        for giorno, voci in self.spese.items():
            if giorno.year == anno_prec:
                for voce in voci:
                    if len(voce) >= 4 and voce[3] == "Uscita":
                        stima_2024 += voce[2]
            if tot_mese_prec:
                variazione_mese_pct = (tot_mese_corr - tot_mese_prec) / tot_mese_prec * 100
            else:
                variazione_mese_pct = 0.0  
        differenza = stima_2024 - stima_2025
        report = f"""
        
    📊 REPORT PROIEZIONE SPESE – {oggi.strftime('%d/%m/%Y')}
    
    ─────────────────────────────────────────────────────────────────────────────────
    📅 Mese corrente: {mese_corr:02}/{anno_corr}
    ▸ Uscite attuali {anno_corr}     : € {tot_mese_corr:>10,.2f}
    ▸ Stesso mese {anno_prec}        : € {tot_mese_prec:>10,.2f}
    
    ▸ Variazione rispetto a {mese_corr:02}/{anno_prec} : {variazione_mese_pct:+.1f}%
    
    ─────────────────────────────────────────────────────────────────────────────────
    📆 Da inizio anno (01/01 → oggi)
    ▸ Totale uscite {anno_corr}      : € {tot_anno_corr:>10,.2f}
    ▸ Stesso periodo {anno_prec}     : € {tot_anno_prec:>10,.2f}

    ─────────────────────────────────────────────────────────────────────────────────
    📈 Spesa a confronto annuale
    ▸ Spesa effettiva {anno_prec}    : € {stima_2024:>10,.2f}
    ▸ Proiezione {anno_corr}         : € {stima_2025:>10,.2f}   (basata su {perc_corr:.1%} dell’anno trascorso)

    ─────────────────────────────────────────────────────────────────────────────────

    """

        if differenza > 0:
            report += f"\n📉 Risparmio previsto: € {differenza:,.2f} se mantieni l’andamento attuale ✨💰✨ "
        else:
            report += f"\n⚠️ Spesa stimata superiore di € {abs(differenza):,.2f} rispetto al {anno_prec} 📉🪙"

        self.mostra_report_popup(report.strip())

    def mostra_report_popup(self, testo):
   
        preview = tk.Toplevel(self)
        preview.withdraw() 
        preview.title("📊 Report Proiezione Annuale")
        width, height = 860, 500

        self.update_idletasks()
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
        preview.geometry(f"{width}x{height}+{x}+{y}")
        preview.deiconify()  
        preview.configure(bg="#FDFEE0")
        #preview.grab_set()
        preview.bind("<Escape>", lambda e: preview.destroy())
        text_area = tk.Text(preview, font=("Courier New", 10), bg="#FFFFF5", wrap="word")
        text_area.insert("1.0", testo)
        text_area.config(state="disabled")
        text_area.pack(fill="both", expand=True, padx=10, pady=10)

        def save_file():
            now = datetime.date.today()
            default_filename = f"Report_Export_{now.day:02d}-{now.month:02d}-{now.year}.txt"
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File txt", "*.txt")],
                initialdir=EXPORT_FILES,
                initialfile=default_filename,
                title="Salva Report",
                confirmoverwrite=False,
                parent=preview
            )
            if file:
                if os.path.exists(file):
                    conferma = self.show_custom_askyesno(
                        "Sovrascrivere file?",
                        f"Il file '{os.path.basename(file)}' \nesiste già. Vuoi sovrascriverlo?"
                    )
                    if not conferma:
                        return 
                        
                with open(file, "w", encoding="utf-8") as f:
                    f.write(testo)
                preview.destroy()
                self.show_custom_warning("Esportazione completata", f"Report esportato in:\n{file}")

        frame_bottoni = tk.Frame(preview, bg="#FDFEE0")
        frame_bottoni.pack(fill="x", padx=8, pady=8)

        ttk.Button(frame_bottoni, text="📄 Esporta", style="Arancio.TButton", command=save_file).pack(side="left")
        ttk.Button(frame_bottoni, text="❌ Chiudi", style="Giallo.TButton", width=12, command=preview.destroy).pack(side="right")
        preview.bind("<Escape>", lambda e: preview.destroy())

    def apri_cancella_multiplo(self):
        popup = tk.Toplevel(self)
        popup.title("Cancella Categorie")
        popup.resizable(True, True)

        larghezza, altezza = 400, 500
        x = self.winfo_x() + (self.winfo_width() // 2) - (larghezza // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (altezza // 2)
        popup.geometry(f"{larghezza}x{altezza}+{x}+{y}")
        popup.grab_set()

        tk.Label(
            popup,
            text="Seleziona le categorie da cancellare:",
            font=("Arial", 10, "bold")
        ).pack(pady=(10, 5))
        self.elimina_spese_var = tk.BooleanVar()

        tk.Checkbutton(
            popup,
            text="Elimina anche le spese associate",
            variable=self.elimina_spese_var,
            anchor="w",
            bg="yellow",       
            activebackground="gold"  
        ).pack(fill="x", padx=15, pady=(5, 0))

        contenitore = tk.Frame(popup)
        contenitore.pack(fill="both", expand=True, padx=10, pady=5)
        canvas = tk.Canvas(contenitore)
        scrollbar = tk.Scrollbar(contenitore, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        scroll_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def aggiorna_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", aggiorna_scroll)
        self.checkbox_vars = {}
        for cat in sorted(set(self.categorie), key=lambda c: c.lower()):

            if cat not in ("Generica", self.CATEGORIA_RIMOSSA):
                var = tk.BooleanVar()
                chk = tk.Checkbutton(scroll_frame, text=cat, variable=var, anchor="w")
                chk.pack(fill="x", padx=5, pady=2)
                self.checkbox_vars[cat] = var
        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Elimina Selezionate",
            style="Rosso.TButton",
            command=lambda: self.cancella_categorie_checkbox(popup)
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="❌ Chiudi",
            style="Giallo.TButton",
            command=popup.destroy
        ).pack(side="left", padx=5)
        
    def cancella_categorie_checkbox(self, popup):
        selezionate = [cat for cat, var in self.checkbox_vars.items() if var.get()]
        if not selezionate:
            self.show_custom_warning("Attenzione", "Seleziona almeno una categoria da cancellare.")
            return
        testo_conferma = f"Sei sicuro di voler cancellare le seguenti categorie?\n\n"
        conferma = self.show_custom_askyesno("Eliminazione Multipla", testo_conferma)
        if not conferma:
            return

        for cat in selezionate:
            if cat in self.categorie:
                self.categorie.remove(cat)
            if cat in self.categorie_tipi:
                del self.categorie_tipi[cat]

            for giorno in list(self.spese.keys()):
                nuove_spese = []
                for voce in self.spese[giorno]:
                    voce_cat = voce[0]
                    if voce_cat == cat:
                         if not self.elimina_spese_var.get():
                             nuove_spese.append((self.CATEGORIA_RIMOSSA,) + voce[1:])
                    else:
                        nuove_spese.append(voce)
                self.spese[giorno] = nuove_spese
                
        self.show_custom_warning("Successo", f"✅ {len(selezionate)} categorie sono state cancellate.")
        popup.destroy()
        self.save_db()
        self.refresh_gui()
        self.aggiorna_combobox_categorie()
               
    def apri_categorie_suggerite(self):
        CATEGORIE_SUGGERITE = [
            # 🏠 Casa & Famiglia
            "🏠 Casa",
            "🏠 Affitto Immobile",
            "🏠 Mutuo Immobile",
            "🏡 Manutenzione casa",
            "💡 Utenze (Luce)",
            "🔥 Utenze (Gas)",
            "🚿 Utenze (Acqua)",
            "♨️ Caldaia",
            "🌰 Pellet",
            "🗑️ Tassa Rifiuti",
            "🏠 Pulizie domestiche",
            "🛋️ Arredamento",
            "🐾 Animali domestici",
            "🏠 Assicurazione Immobile",

            # 🍽️ Alimentari & Consumi
            "🍽️ Alimentari & Consumi",
            "🛒 Spesa supermercato",
            "🍞 Spesa Discount",
            "☕ Colazioni / Caffè fuori",
            "🍽️ Pranzi / Ristoranti",
            "🍕 Asporto / Fast food",

            # 🚗 Veicoli & Trasporti
            "🚗 Veicoli & Trasporti",
            "⛽ Carburante",
            "🛠️ Manutenzione auto",
            "📅 Bollo auto",
            "🏥 Assicurazione veicoli",
            "🚇 Trasporti pubblici",
            "🚕 Taxi / Car sharing",

            # 💡 Bollette & Abbonamenti
            "💡 Bollette & Abbonamenti",
            "📱 Telefonia / Internet",
            "📱 Telefonia / Cellulari",
            "💻 Streaming (Netflix, Prime...)",
            "🔐 Servizi cloud / backup",
            "🎮 Abbonamenti digitali",

            # 🩺 Salute & Benessere
            "🩺 Salute & Benessere",
            "💊 Farmaci",
            "👨‍⚕️ Visite mediche",
            "🏥 Dentista",
            "🧘‍♂️ Wellness / Spa",
            "🏋️‍♀️ Palestra / Fitness",

            # 🎓 Istruzione & Lavoro
            "🎓 Istruzione & Lavoro",
            "📚 Libri / Materiali",
            "🧑‍🏫 Corsi / Formazione",
            "💻 Software",
            "🗂️ Utenze professionali / Partita IVA",

            # 🎉 Tempo libero & Spese personali
            "🎉 Tempo libero & Spese personali",
            "🎁 Regali",
            "🎬 Cinema / Eventi",
            "🎮 Videogiochi",
            "🎮 Computer",
            "🧥 Abbigliamento",
            "🎁 Tabacchi",
            "💇 Parrucchiere / Estetica",
            "✈️ Viaggi / Hotel",

            # 💸 Finanza & Risparmio
            "💸 Stipendio",
            "💸 Pensione",
            "💸 Entrate Extra",
            "💸 Finanza & Risparmio",
            "🏦 Conto corrente",
            "💳 Rate / Finanziamenti",
            "💰 Commercialista",

            # 📤 Uscite straordinarie
            "📤 Uscite straordinarie",
            "🏥 Emergenze",
            "🛠️ Riparazioni impreviste",
            "📦 Spese non ricorrenti"
        ]

        TIPO_SUGGERITI = {
            "Casa": "Uscita",
            "Affitto Immobile": "Uscita",
            "Mutuo Immobile": "Uscita",
            "Manutenzione casa": "Uscita",
            "Utenze (Luce)": "Uscita",
            "Utenze (Gas)": "Uscita",
            "Utenze (Acqua)": "Uscita",
            "Caldaia": "Uscita",
            "Pellet": "Uscita",
            "Tassa Rifiuti": "Uscita",
            "Pulizie domestiche": "Uscita",
            "Arredamento": "Uscita",
            "Animali domestici": "Uscita",
            "Assicurazione Immobile": "Uscita",
            "Alimentari & Consumi": "Uscita",
            "Spesa supermercato": "Uscita",
            "Spesa Discount": "Uscita",
            "Colazioni / Caffè fuori": "Uscita",
            "Pranzi / Ristoranti": "Uscita",
            "Asporto / Fast food": "Uscita",
            "Veicoli & Trasporti": "Uscita",
            "Carburante": "Uscita",
            "Manutenzione auto": "Uscita",
            "Bollo auto": "Uscita",
            "Assicurazione veicoli": "Uscita",
            "Trasporti pubblici": "Uscita",
            "Taxi / Car sharing": "Uscita",
            "Bollette & Abbonamenti": "Uscita",
            "Telefonia / Internet": "Uscita",
            "Telefonia / Cellulari": "Uscita",
            "Streaming (Netflix, Prime...)": "Uscita",
            "Servizi cloud / backup": "Uscita",
            "Abbonamenti digitali": "Uscita",
            "Salute & Benessere": "Uscita",
            "Farmaci": "Uscita",
            "Visite mediche": "Uscita",
            "Dentista": "Uscita",
            "Wellness / Spa": "Uscita",
            "Palestra / Fitness": "Uscita",
            "Istruzione & Lavoro": "Uscita",
            "Libri / Materiali": "Uscita",
            "Corsi / Formazione": "Uscita",
            "Software": "Uscita",
            "Utenze professionali / Partita IVA": "Uscita",
            "Tempo libero & Spese personali": "Uscita",
            "Regali": "Uscita",
            "Cinema / Eventi": "Uscita",
            "Videogiochi": "Uscita",
            "Computer": "Uscita",
            "Abbigliamento": "Uscita",
            "Tabacchi": "Uscita",
            "Parrucchiere / Estetica": "Uscita",
            "Viaggi / Hotel": "Uscita",
            "Stipendio": "Entrata",
            "Pensione": "Entrata",
            "Entrate Extra": "Entrata",
            "Finanza & Risparmio": "Uscita",
            "Conto corrente": "Uscita",
            "Rate / Finanziamenti": "Uscita",
            "Commercialista": "Uscita",
            "Uscite straordinarie": "Uscita",
            "Emergenze": "Uscita",
            "Riparazioni impreviste": "Uscita",
            "Spese non ricorrenti": "Uscita"
        }

        finestra = tk.Toplevel(self)
        finestra.title("Categorie suggerite")
        finestra.configure(bg="white")
        #finestra.resizable(False, False)
        finestra.bind("<Escape>", lambda e: finestra.destroy())
        finestra.geometry("500x480") 
        larghezza, altezza = 500, 480
        x = (finestra.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (finestra.winfo_screenheight() // 2) - (altezza // 2)
        finestra.geometry(f"{larghezza}x{altezza}+{x}+{y}")

        tk.Label(
            finestra,
            text="✨ Scegli categorie da aggiungere:",
            bg="white", font=("Arial", 10, "bold")
        ).pack(pady=(10, 5))

        container = tk.Frame(finestra, bg="white")
        container.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg="white")
        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def aggiorna_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))
        scroll_frame.bind("<Configure>", aggiorna_scroll_region)

        selezioni = {}

        toggle_var = tk.BooleanVar(value=False)

        def seleziona_tutto():
            stato = toggle_var.get()
            for var in selezioni.values():
                var.set(stato)

        toggle_chk = tk.Checkbutton(
            scroll_frame,
            text="✔️ Seleziona Tutte / Nessuna",
            variable=toggle_var,
            command=seleziona_tutto,
            bg="white",
            activebackground="white",
            highlightthickness=0,
            anchor="w",
            font=("Arial", 9, "bold")
        )
        toggle_chk.pack(anchor="w", pady=(6, 6), padx=4)

        for nome in CATEGORIE_SUGGERITE:
            var = tk.BooleanVar()
            nome_pulito = nome.split(" ", 1)[1] if " " in nome else nome
            tipo = TIPO_SUGGERITI.get(nome_pulito, "Uscita")
            etichetta = f"{nome} [{tipo}]"

            chk = tk.Checkbutton(
                scroll_frame,
                text=etichetta,
                variable=var,
                bg="white",
                activebackground="white",
                highlightthickness=0,
                anchor="w"
            )

            chk.pack(anchor="w", pady=2, padx=4)
            selezioni[nome] = var

        def aggiungi_categorie_scelte():
            nuove = [nome for nome, var in selezioni.items() if var.get()]
            pulite = [nome.split(" ", 1)[1] if " " in nome else nome for nome in nuove]
            
            if not pulite:
               self.show_custom_warning("Nessuna selezione", "⚠️ Seleziona almeno una categoria da aggiungere.")
               return
    
            for cat in pulite:
                tipo = TIPO_SUGGERITI.get(cat, "Uscita")
                if cat not in self.categorie:
                    self.categorie.append(cat)
                self.categorie_tipi[cat] = tipo
                
            self.categorie.sort()
            self.aggiorna_combobox_categorie()
            self.save_db()
            self.show_custom_warning("Aggiunta completata", "⚠️ Categorie aggiunte correttamente..")
            finestra.destroy()
        btn_frame = tk.Frame(finestra, bg="white")
        btn_frame.pack(pady=(0, 12))
        ttk.Button(btn_frame, text="➕ Aggiungi", style="Verde.TButton", command=aggiungi_categorie_scelte).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="❌ Chiudi", style="Giallo.TButton", command=finestra.destroy).pack(side="left", padx=8)

    def scarica_manuale(self):
        try:
            response = requests.get(URL_PDF)
            response.raise_for_status()
            temp_path = os.path.join(tempfile.gettempdir(), "manuale_casa_facile.pdf")
            with open(temp_path, "wb") as f:
                f.write(response.content)
            webbrowser.open(f"file://{temp_path}")
        except Exception as e:
            print("Errore nel download del manuale:", e)
            self.show_custom_warning("Attenzione", "❌ Download NON completato ! \n\n Sembra ci sia stato un problema. 😕")
            
    def apri_webserver(self):
        IP = self.get_ip_locale()
        webbrowser.open(f"http://{IP}:{PORTA}")

    def apri_webserver_port(self):
        finestra = tk.Toplevel()
        finestra.withdraw() 
        finestra.title("Cambio porta Webserver")
        finestra.resizable(False, False)
        finestra.grab_set()  
        larghezza, altezza = 320, 140
        finestra.update_idletasks()
        x = (finestra.winfo_screenwidth() // 2) - (larghezza // 2)
        y = (finestra.winfo_screenheight() // 2) - (altezza // 2)
        finestra.geometry(f"{larghezza}x{altezza}+{x}+{y}")  
        finestra.deiconify() 
        porta_corrente = "8081"  
        if os.path.exists(PORTA_DB):
            try:
                with open(PORTA_DB, "r") as file:
                    porta_corrente = str(json.load(file))
            except:
                pass
        vcmd = (finestra.register(lambda val: val.isdigit() or val == ""), "%P")
        ttk.Label(finestra, text="Porta Webserver:").pack(pady=(12, 4))
        entry_porta = ttk.Entry(finestra, justify="center", font=("Segoe UI", 12), validate="key", validatecommand=vcmd)
        entry_porta.insert(0, porta_corrente)
        entry_porta.pack(padx=20)
        btn_frame = ttk.Frame(finestra)
        btn_frame.pack(pady=16)
        def salva_porta():
            porta = entry_porta.get().strip()
            if porta.isdigit():
               with open(PORTA_DB, "w") as file:
                    json.dump(int(porta), file)
                    finestra.destroy()
        ttk.Button(btn_frame, text="💾 Salva", command=salva_porta, style='Verde.TButton').pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Chiudi", command=finestra.destroy, style='Giallo.TButton').pack(side="left", padx=5)

    def get_ip_locale(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP
   
    def start_web_server(self):
        server = HTTPServer(('0.0.0.0', PORTA), CasaFacileWebHandler)
        server.app = self  
        print(f"🌐 Web server pronto su http://localhost:{PORTA}")
        server.serve_forever()

    def html_login(self, path):
   
        folder = os.path.basename(os.getcwd())

        try:
            query = path.split("?", 1)[1]
            params = parse_qs(query)
            errore = "error" in params
        except:
            errore = False
        messaggio = ""
        if errore:
            messaggio = "<p style='color:red; text-align:center;'>❌ Password errata. Riprova.</p>"

        return f"""
        <!DOCTYPE html>
        <html><head><meta charset="utf-8">
        <title>🔐 Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body {{
            font-family: sans-serif;
            background: #f4f4f4;
            padding: 30px;
          }}
          form {{
            max-width: 400px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 6px rgba(0,0,0,0.1);
          }}
          h2 {{
            text-align: center;
            margin-bottom: 10px;
          }}
          input[type="password"], button {{
            display: block;
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            box-sizing: border-box;
            font-size: 16px;
          }}
          button {{
            background: #0078D4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          }}
        </style>
        </head><body>
        <form method="post" action="/check_login">
          <h2>🔐 Login {NAME}</h2>
          <h2>Versione v{VERSION} @ 2025</h2>
          <p style="text-align: center; font-size: 14px; color: #555; margin-top: -5px;">{folder}</p>
          {messaggio}
          <input type="password" name="password" placeholder="Password  ⏎" autofocus>
          <button type="submit">Accedi</button>
        </form>
        </body></html>
        """

    def leggi_hash(self):
        if not os.path.exists(PW_FILE):
            return None
        try:
            with open(PW_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("hash")
        except:
            return None

    def verifica_password(self, password):
        salvato = self.leggi_hash()
        if salvato is None:
            return False  
        inserito = hashlib.sha256(password.encode()).hexdigest()
        return salvato == inserito

    def pagina_risultati_avanzati(self, params):
        from datetime import datetime
        from collections import defaultdict 
        categoria = params.get("categoria", [""])[0].strip().lower()
        anno = params.get("anno", [""])[0].strip()
        mese = params.get("mese", [""])[0].strip()
        tipo = params.get("tipo", [""])[0].strip().lower()
        min_importo = float(params.get("min_importo", ["0"])[0] or 0)
        max_importo = float(params.get("max_importo", ["999999"])[0] or 999999)
        query = params.get("q", [""])[0].strip().lower()
        risultati_categorizzati = defaultdict(list)
        for data in sorted(self.spese.keys(), reverse=True):
            if anno and str(data.year) != anno:
                continue
            if mese and f"{data.month:02d}" != mese:
                continue
            for idx_voce, voce in enumerate(self.spese[data]):
                if len(voce) < 4:
                    continue
                cat, descrizione, importo, tipo_voce = voce[:4]
                if categoria and cat.strip().lower() != categoria:
                    continue
                if tipo and tipo_voce.strip().lower() != tipo:
                    continue
                if not (min_importo <= importo <= max_importo):
                    continue
                if query and not (
                    query in descrizione.lower()
                    or query in tipo_voce.lower()
                    or query in cat.lower()
                    or query in str(importo)
                ):
                    continue
                risultati_categorizzati[cat].append(
                    (
                        data.strftime("%d-%m-%Y"),
                        html_escape.escape(descrizione),
                        float(importo),
                        tipo_voce.strip(),
                        idx_voce,
                    )
                )

        entrate_totali = sum(
            v[2]
            for vlist in risultati_categorizzati.values()
            for v in vlist
            if v[3].lower() == "entrata"
        )
        uscite_totali = sum(
            v[2]
            for vlist in risultati_categorizzati.values()
            for v in vlist
            if v[3].lower() != "entrata"
        )
        saldo = entrate_totali - uscite_totali
        colore = "#3c763d" if saldo >= 0 else "#a94442"
        anno_corrente = datetime.now().year
        schede_html = ""
        for idx_cat, (cat, voci) in enumerate(sorted(risultati_categorizzati.items())):
            totale_cat = sum(
                imp if tipo_voce.lower() == "entrata" else -imp
                for _, _, imp, tipo_voce, _ in voci
            )
            voce_html = ""
            for data, descrizione, importo, tipo_voce, idx_voce in voci:
                simbolo = "+" if tipo_voce.lower() == "entrata" else "−"
                colore_tipo = "#007E33" if tipo_voce.lower() == "entrata" else "#D8000C"
                voce_html += f"""
                <li>
                    <form method="get" action="/modifica" style="display:inline;">
                        <input type="hidden" name="data" value="{data}">
                        <input type="hidden" name="idx" value="{idx_voce}">
                        <button type="submit" style="margin-right:4px;" title="Modifica">✏️</button>
                    </form>
                    <form onsubmit="
                        event.preventDefault();
                        fetch('/cancella', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                            body: 'data={data}&idx={idx_voce}'
                        }}).then(function() {{ window.location.reload(); }});
                    " style="display:inline;">
                        <button type="submit" style="margin-right:8px;color:#D8000C;" title="Cancella">❌</button>
                    </form>
                    {data} • {descrizione} 
                    <span style='color:#000; font-weight:bold;'>{simbolo}€{importo:.2f}</span>
                    <strong style='color:{colore_tipo};'>[{tipo_voce}]</strong>
                </li>
                """
            simbolo_totale = "➕" if totale_cat >= 0 else "➖"
            colore_totale = "#007E33" if totale_cat >= 0 else "#D8000C"
            schede_html += f"""
            <div class="categoria-blocco">
                <button class="toggle-btn" onclick="toggleCategoria(this)">
                    <span class="freccia">➤</span> <span class="etichetta">{html_escape.escape(cat)}</span>
                </button>

                <div class="riepilogo-riga" style="color:{colore_totale};">
                    {simbolo_totale} Totale: <strong>€{totale_cat:.2f}</strong> • Voci: <strong>{len(voci)}</strong>
                </div>
                <div class="categoria-contenuto" style="display:none;">
                    <ul>{voce_html}</ul>
                </div>
            </div>
            """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>📊 Risultati Avanzati</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                    margin: 0;
                }}
                header {{
                    background: #0078D4;
                    color: white;
                    padding: 20px 0;
                    position: relative;
                }}
                .header-title {{
                    text-align: center;
                    font-size: 1.5em;
                }}
                .menu-button {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    font-size: 1.6em;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                }}
                .dropdown {{
                    position: absolute;
                    top: 45px;
                    left: 10px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    display: none;
                    z-index: 999;
                }}
                .dropdown a {{
                    display: block;
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #0078D4;
                    font-weight: bold;
                }}
                .dropdown a:hover {{
                    background-color: #f0f0f0;
                }}
                h2 {{
                    text-align: center;
                    font-size: 1.5em;
                    color: #333;
                    margin-bottom: 20px;
                }}
                .categoria-blocco {{
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 6px rgba(0,0,0,0.1);
                    margin: 20px auto;
                    max-width: 600px;
                    padding: 10px;
                }}
                .toggle-btn {{
                    background: none;
                    border: none;
                    font-size: 1.1em;
                    font-weight: bold;
                    width: 100%;
                    text-align: left;
                    cursor: pointer;
                    padding: 8px 0;
                    color: #0078D4;
                }}
                .categoria-contenuto ul {{
                    list-style: none;
                    padding-left: 0;
                    margin-top: 10px;
                }}
                .categoria-contenuto li {{
                    font-size: 1em;
                    margin: 8px 0;
                }}
                ul.totali {{
                    background: #fff;
                    padding: 16px;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(0,0,0,0.1);
                    max-width: 600px;
                    margin: 0 auto 30px auto;
                    list-style: none;
                }}
                ul.totali li {{
                    font-size: 1.1em;
                    margin: 8px 0;
                }}
                .back {{
                    display: block;
                    text-align: center;
                    font-size: 1em;
                    text-decoration: none;
                    background: #0078D4;
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    max-width: 100%;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    margin-top: 20px;
                }}
                .back:hover {{
                    background-color: #005ea6;
                }}
                .riepilogo-riga {{
                    font-size: 0.95em;
                    color: #555;
                    margin-top: 6px;
                    margin-bottom: 10px;
                    text-align: left;
                    padding-left: 4px;
                }}
                .pulsanti-finali {{
                    max-width: 600px;
                    margin: 30px auto 0 auto;
                }}
            </style>
            <script>
                function toggleMenu() {{
                    const menu = document.getElementById("extraMenu");
                    menu.style.display = (menu.style.display === "block") ? "none" : "block";
                }}
                document.addEventListener("click", function(event) {{
                    const menu = document.getElementById("extraMenu");
                    const isClickInside = event.target.closest(".menu-button, #extraMenu");
                    if (!isClickInside) {{
                        menu.style.display = "none";
                    }}
                }});
                function toggleCategoria(btn) {{
                    const riepilogo = btn.nextElementSibling;
                    const content = riepilogo.nextElementSibling;
                    const isVisible = content.style.display === "block";
                    content.style.display = isVisible ? "none" : "block";
                    const freccia = btn.querySelector(".freccia");
                    freccia.textContent = isVisible ? "➤" : "▼";
                }}
            </script>
        </head>
        <body>
            <header>
                <button class="menu-button" onclick="toggleMenu()">☰</button>
                <div id="extraMenu" class="dropdown">
                    <a href="/">🏠 Torna alla Home</a>
                    <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
                    <a href="/lista">📈 Elenca/Modifica</a>
                    <a href="/stats">📊 Report Mese</a>
                    <a href="/report_annuo">📅 Report Annuale</a>
                    <a href="/menu_esplora">🔍 Esplora</a>
                    <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
                    <a href="/utenze?anno={anno_corrente}">💧 Utenze</a>
                    <a href="/logoff">🔓 Logout</a>
                </div>
                <div class="header-title">🔍 Risultati</div>
            </header>
            <h2>📊 Totali Esplorazione</h2>
            <ul class="totali">
                <li><strong>Entrate totali:</strong> €{entrate_totali:.2f}</li>
                <li><strong>Uscite totali:</strong> €{uscite_totali:.2f}</li>
                <li><strong style="color:{colore};">Saldo:</strong> €{saldo:.2f}</li>
            </ul>
            <h2>🔎 Risultati per Categoria</h2>
            {schede_html if schede_html else "<p style='text-align:center;'>Nessuna voce trovata per questi criteri.</p>"}
            <div class="pulsanti-finali">
                <form method="get" action="/menu_esplora">
                    <input type="submit" value="🔙 Torna al Menu Esplora"
                    style="background-color: #0078D4; color: white; border: none;
                    font-size: 1.1em; padding: 12px; border-radius: 6px;
                    cursor: pointer; width: 100%; margin-bottom: 10px;">
                </form>
                <form method="get" action="/">
                    <input type="submit" value="🏠 Torna alla Home"
                    style="background-color: #0078D4; color: white; border: none;
                    font-size: 1.1em; padding: 12px; border-radius: 6px;
                    cursor: pointer; width: 100%;">
                </form>
            </div>
        </body>
        </html>
        """
        return html

    def html_form(self):
        categorie_options = "\n".join(
            f"<option value='{c}'>{c}</option>" for c in self.categorie
        )
        today = datetime.date.today().isoformat()
        anno_corrente = datetime.date.today().year
        entrate_mese = 0.0
        uscite_mese = 0.0
        oggi = datetime.date.today()
        for data_spesa, voci in self.spese.items():
            if data_spesa.month == oggi.month and data_spesa.year == oggi.year:
                for voce in voci:
                    categoria, descrizione, importo, tipo = voce[:4]
                    if tipo == "Entrata":
                        entrate_mese += importo
                    else: 
                        uscite_mese += importo
        
        saldo_mese = entrate_mese - uscite_mese
        saldo_colore = "#3c763d" if saldo_mese >= 0 else "#c43b2e" 
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Casa Facile Web</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    margin: 0;
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f4f4f4;
                }}
                header {{
                    background: #0078D4;
                    color: white;
                    padding: 20px 0;
                    position: relative;
                }}
                .header-title {{
                    text-align: center;
                    font-size: 1.5em;
                }}
                .menu-button {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    font-size: 1.6em;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                }}
                .dropdown {{
                    position: absolute;
                    top: 45px;
                    left: 10px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    display: none;
                    z-index: 999;
                }}
                .dropdown a {{
                    display: block;
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #0078D4;
                    font-weight: bold;
                }}
                .dropdown a:hover {{
                    background-color: #f0f0f0;
                }}
                main {{
                    padding: 20px;
                    max-width: 600px;
                    margin: auto;
                }}
                form {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.05);
                }}
                label {{
                    display: block;
                    margin-top: 10px;
                    font-weight: bold;
                }}
                input, select {{
                    width: 100%;
                    padding: 10px;
                    margin-top: 5px;
                    margin-bottom: 15px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }}
                input[type="submit"] {{
                    background-color: #0078D4;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 1em;
                    border-radius: 6px;
                    padding: 12px;
                }}
                input[type="submit"]:hover {{
                    background-color: #005ea6;
                }}
                .input-errore {{
                    border: 2px solid red;
                }}
                .errore-msg {{
                    color: #a94442;
                    font-size: 0.95em;
                    display: none;
                    margin-top: -10px;
                    margin-bottom: 10px;
                }}
                input.input-errore + .errore-msg {{
                    display: block;
                }}
                .monthly-summary-container {{
                    background-color: #e6f2ff; 
                    border: 1px solid #b3d9ff; 
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .monthly-summary-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: pointer;
                    margin-bottom: 10px; 
                }}
                .monthly-summary-header h3 {{
                    margin: 0;
                    color: #005ea6; 
                    font-size: 1.0em; 
                }}
                .arrow {{
                    width: 0;
                    height: 0;
                    border-left: 8px solid transparent;
                    border-right: 8px solid transparent;
                    border-top: 8px solid #005ea6; 
                    transition: transform 0.3s ease; 
                }}
                .arrow.up {{
                    transform: rotate(180deg); 
                }}
                .monthly-summary-content {{
                    max-height: 0; 
                    overflow: hidden;
                    transition: max-height 0.3s ease-out, margin-top 0.3s ease-out;
                }}
                .monthly-summary-content.open {{
                    max-height: 200px; 
                    margin-top: 10px; 
                }}
                .monthly-summary-content p {{
                    margin: 5px 0;
                    font-size: 1.1em;
                    font-weight: bold;
                }}
                .income-value {{
                    color: #3c763d; 
                }}
                .expense-value {{
                    color: #c43b2e; 
                }}
                .balance-value {{
                    color: #0078D4; 
                }}
            </style>
            <script>
                function toggleMenu() {{
                    const menu = document.getElementById("extraMenu");
                    menu.style.display = (menu.style.display === "block") ? "none" : "block";
                }}
                document.addEventListener("click", function(event) {{
                    const menu = document.getElementById("extraMenu");
                    const isClickInside = event.target.closest(".menu-button, #extraMenu");
                    if (!isClickInside) {{
                        menu.style.display = "none";
                    }}
                }});
            </script>
            <script>
              document.addEventListener("DOMContentLoaded", function () {{
                const form = document.getElementById("spesaForm");
                const msg = document.getElementById("successMessage");
                const summaryHeader = document.getElementById("summaryHeader");
                const summaryContent = document.getElementById("summaryContent");
                const arrow = document.getElementById("summaryArrow");
                summaryContent.classList.remove("open");
                arrow.classList.remove("up");
                summaryHeader.style.marginBottom = "0"; 
                summaryHeader.addEventListener("click", function() {{
                    summaryContent.classList.toggle("open");
                    arrow.classList.toggle("up");
                    if (summaryContent.classList.contains("open")) {{
                        summaryHeader.style.marginBottom = "10px";
                    }} else {{
                        summaryHeader.style.marginBottom = "0";
                    }}
                }});
                form.addEventListener("submit", function () {{
                  const categoria = form.categoria.value;
                  const importo = form.importo.value;
                  msg.textContent = `✅ Inserita: ${{categoria}} €${{importo}}`;
                  msg.style.color = "black";
                  msg.style.display = "block";
                  setTimeout(() => {{
                    msg.style.display = "none";
                  }}, 8000);
                }});
              }});
            </script>
        </head>
        <body>
            <header>
                <button class="menu-button" onclick="toggleMenu()">☰</button>
                <div id="extraMenu" class="dropdown">
                    <a href="/">🏠 Torna alla Home</a>
                    <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
                    <a href="/lista">📈 Elenca/Modifica</a>
                    <a href="/stats">📊 Report Mese</a>
                    <a href="/report_annuo">📅 Report Annuale</a>
                    <a href="/menu_esplora">🔍 Esplora</a>
                    <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
                    <a href="/utenze?anno={anno_corrente}">💧 Utenze</a>
                    <a href="/logoff">🔓 Logout</a>
                </div>
                <div class="header-title">🏠 Casa Facile Web</div>
            </header>
            <main>
                <div id="successMessage" style="display:none; color:green;">✅ Inserito</div>
                <div class="monthly-summary-container">
                    <div class="monthly-summary-header" id="summaryHeader">
                        <h3>Riepilogo Mese Corrente</h3>
                        <div class="arrow" id="summaryArrow"></div>
                    </div>
                    <div class="monthly-summary-content" id="summaryContent">
                        <p>Entrate: <span class="income-value">€{entrate_mese:.2f}</span></p>
                        <p>Uscite: <span class="expense-value">€{uscite_mese:.2f}</span></p>
                        <p>Saldo: <span class="balance-value" style="color:{saldo_colore};">€{saldo_mese:.2f}</span></p>
                    </div>
                </div>
                <form method="post" action="/" id="spesaForm">
                    <label for="data">Data:</label>
                    <input name="data" type="date" value="{today}">
                    <label for="categoria">Categoria:</label>
                    <select name="categoria">{categorie_options}</select>
                    <label for="descrizione">Descrizione:</label>
                    <input name="descrizione" placeholder="Es: Pizza o bollette">
                    <label for="importo">Importo:</label>
                    <input
                        name="importo"
                        type="number"
                        step="0.01"
                        min="0.01"
                        required
                        placeholder="Es: 12.50"
                        oninvalid="this.classList.add('input-errore')"
                        oninput="this.classList.remove('input-errore')"
                    >
                    <span class="errore-msg">⚠️ Inserisci un importo valido</span>
                    <label for="tipo">Tipo:</label>
                    <select name="tipo">
                        <option value="Uscita">Uscita</option>
                        <option value="Entrata">Entrata</option>
                    </select>
                    <input type="submit" value="➕ Aggiungi Voce">
                </form>
            </main>
        </body>
        </html>
        """

    def genera_html_utenze(self, percorso_db, anno):
        from datetime import datetime
        utenze = ["Acqua", "Luce", "Gas"]
        if not os.path.exists(percorso_db):
            return """
            <!DOCTYPE html>
            <html>
            <head><title>Errore DB</title><meta charset="utf-8"></head>
            <body style='font-family:Arial; background:#fff; padding:20px;'>
              <h2 style='color:#b00;'>❌ Errore database</h2>
              <p style='font-size:3.2em;'>⚠️ Il file <strong>UTENZE_DB</strong> non esiste o è vuoto.</p>
              <a href='/' style='display:inline-block; margin-top:20px; font-size:3em; text-decoration:none; color:#0078D4;'>🔙 Torna alla Home</a>
            </body>
            </html>
            """
        try:
            with open(percorso_db, "r", encoding="utf-8") as f:
                contenuto = f.read().strip()
                if not contenuto:
                    return "<p style='font-size: 3.3em; font-weight: bold; color: #C00;'>⚠️ Il file database è vuoto.</p>"
                data = json.loads(contenuto)
        except Exception as e:
            return f"<p>❌ Errore nel file JSON: {e}</p>"
        letture = data.get("letture_salvate", {})
        anno_corrente = datetime.now().year
        anni_disponibili = [str(anno_corrente - i) for i in range(6)]
        select_html = "<form><label for='anno'>🗓️ Scegli anno:</label> "
        select_html += "<select id='anno' onchange=\"location.href='/utenze?anno=' + this.value\">"
        for a in anni_disponibili:
            selected = " selected" if a == str(anno) else ""
            select_html += f"<option value='{a}'{selected}>{a}</option>"
        select_html += "</select></form>"
        oggi = datetime.now()
        html = f"""<!DOCTYPE html>
    <html lang="it">
    <head>
      <meta charset="utf-8">
      <title>💧 Utenze — {anno}</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body {{
          margin: 0;
          font-family: 'Segoe UI', sans-serif;
          background-color: #f4f4f4;
        }}
        header {{
          background: #0078D4;
          color: white;
          padding: 20px 0;
          position: relative;
        }}
        .header-title {{
          text-align: center;
          font-size: 1.5em;
        }}
        .menu-button {{
          position: absolute;
          top: 10px;
          left: 10px;
          font-size: 1.6em;
          background: none;
          border: none;
          color: white;
          cursor: pointer;
        }}
        .dropdown {{
          position: absolute;
          top: 45px;
          left: 10px;
          background-color: white;
          box-shadow: 0 4px 8px rgba(0,0,0,0.15);
          border-radius: 4px;
          display: none;
          z-index: 999;
        }}
        .dropdown a {{
          display: block;
          padding: 10px 20px;
          text-decoration: none;
          color: #0078D4;
          font-weight: bold;
        }}
        .dropdown a:hover {{
          background-color: #f0f0f0;
        }}
        main {{
          padding: 20px;
          max-width: 600px;
          margin: auto;
        }}
        .utenza-title {{
          cursor: pointer;
          padding: 10px;
          background: #0078D4;
          color: white;
          border-radius: 4px;
          margin-top: 20px;
        }}
        .utenza-content {{
          display: none;
          background: white;
          padding: 10px;
          border-radius: 6px;
          box-shadow: 0 0 4px rgba(0,0,0,0.05);
          margin-bottom: 20px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          font-size: 0.9em;
        }}
        th, td {{
          border: 1px solid #ccc;
          padding: 8px;
          text-align: center;
        }}
        th {{
          background: #0078D4;
          color: white;
        }}
        .teardown {{
          background: #f9f9f9;
          margin-top: 10px;
          font-size: 0.9em;
          padding: 8px;
          border-radius: 4px;
        }}
        .back {{
          display: block;
          text-align: center;
          font-size: 1em;
          text-decoration: none;
          background: #0078D4;
          color: white;
          padding: 10px;
          border-radius: 4px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 20px auto;
          width: 200px;
        }}
        .back:hover {{
          background-color: #005ea6;
        }}
      </style>
      <script>
        function toggleMenu() {{
          const menu = document.getElementById("extraMenu");
          menu.style.display = (menu.style.display === "block") ? "none" : "block";
        }}
        function toggle(id) {{
          const el = document.getElementById(id);
          el.style.display = (el.style.display === "none") ? "block" : "none";
        }}
        document.addEventListener("click", function(event) {{
          const menu = document.getElementById("extraMenu");
          if (!event.target.closest(".menu-button, #extraMenu")) {{
            menu.style.display = "none";
          }}
        }});
      </script>
    </head>
    <body>
      <header>
        <button class="menu-button" onclick="toggleMenu()">☰</button>
        <div id="extraMenu" class="dropdown">
          <a href="/">🏠 Torna alla Home</a>
          <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
          <a href="/lista">📈 Elenca/Modifica</a>
          <a href="/stats">📊 Report Mese</a>
          <a href="/report_annuo">📅 Report Annuale</a>
          <a href="/menu_esplora">🔍 Esplora</a>
          <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
          <a href="/utenze?anno={anno_corrente}">💧 Utenze</a>
          <a href="/logoff">🔓 Logout</a>
        </div>
        <div class="header-title">💧 Utenze — Anno {anno}</div>
      </header>
      <main>
        {select_html}
    """

        for utenza in utenze:
            righe = letture.get(utenza, {}).get(str(anno), [])
            uid = f"utenza_{utenza.lower()}"
            html += f"<div class='utenza-title' onclick=\"toggle('{uid}')\">▶️ {utenza}</div><div id='{uid}' class='utenza-content'>"
            if righe:
                total = 0.0
                consumi = []
                html += "<table><tr><th>Mese</th><th>Prec</th><th>Att</th><th>Consumo</th></tr>"
                for riga in righe:
                    try:
                        mese, prec, att, cons = riga
                        prec, att, cons = float(prec), float(att), float(cons)
                        total += cons
                        consumi.append(cons)
                        html += f"<tr><td>{mese}</td><td>{prec:.2f}</td><td>{att:.2f}</td><td>{cons:.2f}</td></tr>"
                    except:
                        html += f"<tr><td colspan='4'>⚠️ Errore dati: {riga}</td></tr>"
                media = total / len(consumi) if consumi else 0
                variazioni = [consumi[i] - consumi[i - 1] for i in range(1, len(consumi))]
                ultima = variazioni[-1] if variazioni else 0
                html += "</table>"
                html += f"""
    <div class='teardown'>
    🔢 Totale: <strong>{total:.2f}</strong><br>
    📊 Media mensile: <strong>{media:.2f}</strong><br>
    📈 Ultima variazione: <strong>{ultima:+.2f}</strong><br>
    📅 Mesi registrati: <strong>{len(consumi)}</strong>
    </div>
    """
            else:
                html += "<p><i>Nessun dato disponibile.</i></p>"
            html += "</div>"

        html += f"""
        <a href="/" class="back">🏠 Torna alla Home</a>
      </main>
    </body>
    </html>
    """
        return html

    def genera_html_consultazione(self, file_selezionato=None):
        anno_corrente = datetime.datetime.now().year
        def inizializza_db_file(percorso_db, contenuto_iniziale="{}"):
            """Garantisce che la directory e il file DB esistano e siano stati inizializzati."""
            dir_path = os.path.dirname(percorso_db)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path) 
            if not os.path.exists(percorso_db):
                try:
                    with open(percorso_db, "w", encoding="utf-8") as f:
                        f.write(contenuto_iniziale)
                    return True
                except Exception as e:
                    print(f"Errore nella creazione automatica di {percorso_db}: {e}")
                    return False
            return True

        def get_file_list_internal():
            directory_esportazione = EXPORT_FILES
            if not os.path.isdir(directory_esportazione):
                try:
                    os.makedirs(directory_esportazione)
                except Exception:
                    pass
                return []
            list_files = os.listdir(directory_esportazione)
            lista_spesa_files = [f for f in list_files if f.startswith("Lista_Spesa_") and f.endswith(".txt")]
            try:
                lista_spesa_files.sort(key=lambda f: os.path.getmtime(os.path.join(directory_esportazione, f)), reverse=True)
            except Exception:
                pass
            return lista_spesa_files

        def leggi_lista_spesa_internal(nome_file):
            directory_esportazione = EXPORT_FILES
            file_path = os.path.join(directory_esportazione, nome_file)
            if not os.path.exists(file_path):
                return []
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Errore lettura file {nome_file}: {e}")
                return []
            return [{"raw_content": content}]
        lista_file_disponibili = get_file_list_internal() 
        file_visualizzato = lista_file_disponibili[0] if lista_file_disponibili else "Nessuna Lista Trovata"
        ultima_spesa_data = []
        if file_visualizzato != "Nessuna Lista Trovata":
            ultima_spesa_data = leggi_lista_spesa_internal(file_visualizzato)
        is_raw_content = ultima_spesa_data and 'raw_content' in ultima_spesa_data[0]
        percorso_db = SUPERMERCATI_DB
        dati_supermercati = {}
        if not inizializza_db_file(percorso_db):
             return f"""<!DOCTYPE html><html><head><title>Errore database</title><meta charset="utf-8"></head><body style='font-family:Arial; background:#fff; padding:20px;'><h2 style='color:#b00;'>❌ Errore database</h2><p style='font-size:1.5em;'>⚠️ Impossibile creare il file <strong>{percorso_db}</strong>.</p><a href='/' style='display:inline-block; margin-top:20px; font-size:1.5em; text-decoration:none; color:#0078D4;'>🔙 Torna alla Home</a></body></html>"""
        try:
            with open(percorso_db, "r", encoding="utf-8") as f:
                contenuto = f.read().strip()
                dati_supermercati = json.loads(contenuto) if contenuto else {}
        except Exception as e:
            return f"""<!DOCTYPE html><html><head><title>Errore JSON</title><meta charset="utf-8"></head><body style='font-family:Arial; background:#fff; padding:20px;'><h2 style='color:#b00;'>❌ Errore JSON</h2><p style='font-size:1.5em;'>Errore lettura database supermercati: {e}</p><a href='/' style='display:inline-block; margin-top:20px; font-size:1.5em; text-decoration:none; color:#0078D4;'>🔙 Torna alla Home</a></body></html>"""
        supermercati = sorted(dati_supermercati.keys())
        page_title = "🔍 Consultazione Cataloghi e Ultima Spesa"
        header_text = "Gestione Supermarket"
        emoji = ""
        html = f"""<!DOCTYPE html>
        <html lang="it">
        <head>
          <meta charset="utf-8">
          <title>{emoji} {page_title}</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body {{ margin: 0; font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; }}
            header {{ background: #0078D4; color: white; padding: 20px 0; position: relative; }}
            .header-title {{ text-align: center; font-size: 1.5em; }}
            .menu-button {{ position: absolute; top: 10px; left: 10px; font-size: 1.6em; background: none; border: none; color: white; cursor: pointer; }}
            .dropdown {{ position: absolute; top: 45px; left: 10px; background-color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.15); border-radius: 4px; display: none; z-index: 999; }}
            .dropdown a {{ display: block; padding: 10px 20px; text-decoration: none; color: #0078D4; font-weight: bold; }}
            .dropdown a:hover {{ background-color: #f0f0f0; }}
            main {{ padding: 20px; max-width: 800px; margin: auto; }}
            .section-title {{ 
              cursor: pointer; 
              padding: 12px; 
              background: #0078D4; 
              color: white; 
              border-radius: 4px; 
              margin-top: 20px; 
              font-weight: bold; 
              display: flex; 
              justify-content: space-between; 
              align-items: center; 
            }}
            .section-content {{ 
              display: block; 
              background: white; 
              padding: 15px; 
              border-radius: 6px; 
              box-shadow: 0 0 8px rgba(0,0,0,0.1); 
              margin-bottom: 20px; 
            }}
            /* OTTIMIZZAZIONI PER LE TABELLE DEI CATALOGHI */
            table {{ 
                width: 100%; 
                border-collapse: collapse; 
                font-size: 0.75em; 
                table-layout: fixed; /* Forza la larghezza del 100% per lo schermo */
            }}
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 4px; /* Ridotto il padding da 8px a 4px */
                text-align: left; 
                overflow: hidden; /* Nasconde il testo che eccede */
                text-overflow: ellipsis; /* Aggiunge i puntini di sospensione (utile per le descrizioni) */
            }}
            th {{ 
                background: #0078D4; 
                color: white; 
                text-align: center; 
                white-space: normal; /* Permette all'intestazione di andare a capo */
            }}
            /* FINE OTTIMIZZAZIONI */
            .promo {{ color: #d32f2f; font-weight: bold; }}
            .prezzo {{ text-align: right; white-space: nowrap; }}
            .categoria {{ font-style: italic; color: #777; }}
            .back {{ display: block; text-align: center; font-size: 1em; text-decoration: none; background: #0078D4; color: white; padding: 10px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px auto; width: 200px; }}
            .back:hover {{ background-color: #005ea6; }}
            pre {{ 
                white-space: pre-wrap; 
                word-wrap: break-word; 
                background:#fff3e0; 
                padding:15px; 
                border:1px solid #ffcc80; 
                border-left: 5px solid #ff9800; 
                overflow-x: auto; 
                font-size: 0.85em; /* RIDUZIONE FONT LISTA SPESA */
            }}
          </style>
          <script>
            function toggleMenu() {{
              const menu = document.getElementById("extraMenu");
              menu.style.display = (menu.style.display === "block") ? "none" : "block";
            }}
            function toggle(id) {{
              const el = document.getElementById(id);
              const icon = document.getElementById('icon_' + id);
              if (el.style.display === "none" || el.style.display === "") {{
                el.style.display = "block";
                icon.textContent = "▼";
              }} else {{
                el.style.display = "none";
                icon.textContent = "▶";
              }}
            }}
            document.addEventListener("click", function(event) {{
              const menu = document.getElementById("extraMenu");
              if (!event.target.closest(".menu-button, #extraMenu")) {{
                menu.style.display = "none";
              }}
            }});
          </script>
        </head>
        <body>
          <header>
            <button class="menu-button" onclick="toggleMenu()">☰</button>
            <div id="extraMenu" class="dropdown">
              <a href="/">🏠 Torna alla Home</a>
              <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
              <a href="/lista">📈 Elenca/Modifica</a>
              <a href="/stats">📊 Report Mese</a>
              <a href="/report_annuo">📅 Report Annuale</a>
              <a href="/menu_esplora">🔍 Esplora</a>
              <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
              <a href="/utenze">💧 Utenze</a>
              <a href="/logoff">🔓 Logout</a>
            </div>
            <div class="header-title">{emoji} {header_text}</div>
          </header>
          <main>
        """
        lista_id = "lista_spesa_contenuto"
        html += f"""
        <div class='section-title' style='margin-top: 0;' onclick="toggle('{lista_id}')">
            📋 Contenuto ULTIMA LISTA: {file_visualizzato}
            <span id='icon_{lista_id}'>▶</span>
        </div>
        """
        html += f"""
        <div id='{lista_id}' class='section-content' style='display: none;'>
        """
        if is_raw_content:
            raw_text = ultima_spesa_data[0]['raw_content']
            raw_text_safe = raw_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html += f"""
            <pre>{raw_text_safe}</pre>
            """
        else:
            html += f"""
            <p>❌ <strong>Impossibile visualizzare la lista spesa.</strong></p>
            <p>Assicurati che ci sia almeno un file 'Lista_Spesa_....txt' nella cartella 'export'.</p>
            """
        html += "</div>"
        html += f"<div class='section-title' onclick=\"toggle('cataloghi_sezione')\">🛒 Consultazione Cataloghi ({len(supermercati)}) <span id='icon_cataloghi_sezione'>▶</span></div><div id='cataloghi_sezione' class='section-content' style='display: none;'>"

        if supermercati:
            for superm in supermercati:
                articoli = dati_supermercati.get(superm, [])
                superm_id = f"catalogo_{superm.lower().replace(' ', '_')}"
                html += f"""
                <div class='section-title' style='margin-top:10px;' onclick=\"toggle('{superm_id}')\">
                    {superm} ({len(articoli)} articoli) 
                    <span id='icon_{superm_id}'>▶</span>
                </div>
                <div id='{superm_id}' class='section-content' style='padding:0; display: none;'>
                """ 
                if articoli:
                    #articoli_ordinati = sorted(articoli, key=lambda x: (x.get('categoria', ''), x.get('nome', '')))
                    articoli_ordinati = sorted(articoli, key=lambda x: x.get('nome', ''))
                    html += "<table><tr><th>Articolo</th><th>Descrizione</th><th>Categoria</th><th>Prezzo Normale (€)</th><th>Promo Attiva/Valore (€)</th></tr>"
                    for articolo in articoli_ordinati:
                        nome = articolo.get("nome", "N/D")
                        descrizione = articolo.get("descrizione", "N/D")
                        categoria = articolo.get("categoria", "Varie") 
                        prezzo_str = articolo.get("prezzo", "0.0")
                        prezzo_promo_str = articolo.get("prezzo_promo", "0.0")
                        promo_attiva = articolo.get("promo", False) 
                        try:
                            prezzo = float(prezzo_str)
                            prezzo_normale_fmt = f"{prezzo:.2f}"
                        except ValueError:
                            prezzo_normale_fmt = prezzo_str
                        try:
                            prezzo_promo = float(prezzo_promo_str)
                            prezzo_promo_fmt = f"{prezzo_promo:.2f}"
                        except ValueError:
                            prezzo_promo_fmt = prezzo_promo_str
                        
                        prezzo_normale_colonna = prezzo_normale_fmt
                        promo_colonna = 'No'
                        
                        if promo_attiva and prezzo_promo is not None and prezzo_promo > 0:
                            promo_colonna = f"<span class='promo'>{prezzo_promo_fmt}</span>"
                        
                        html += f"""
                        <tr>
                            <td>{nome}</td>
                            <td>{descrizione}</td>
                            <td class='categoria'>{categoria}</td>
                            <td class='prezzo'>{prezzo_normale_colonna}</td>
                            <td class='prezzo'>{promo_colonna}</td>
                        </tr>
                        """
                    html += "</table>"
                else:
                    html += "<p style='padding:15px;'><i>Nessun articolo registrato per questo supermercato.</i></p>"
                html += "</div>"  
        else:
            html += "<p>⚠️ Il database dei cataloghi è vuoto o non contiene supermercati registrati.</p>"
        html += "</div>" 
        html += f"""
            <a href="/" class="back">🏠 Torna alla Home</a>
          </main>
        </body>
        </html>
        """
        return html

    def pagina_menu_esplora(self):
        mesi_it_map = {
            "01": "Gennaio", "02": "Febbraio", "03": "Marzo",
            "04": "Aprile", "05": "Maggio", "06": "Giugno",
            "07": "Luglio", "08": "Agosto", "09": "Settembre",
            "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
        }
        mesi = [f"{m:02d} - {mesi_it_map[f'{m:02d}']}" for m in range(1, 13)]
        categorie = sorted(set(self.categorie))
        anno_corrente = datetime.date.today().year
        anni = [str(anno) for anno in range(anno_corrente, anno_corrente - 6, -1)] 
        html_code = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset='utf-8'>
            <title>🔎 Esplorazione Avanzata</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f4f4f4;
                    padding: 0;
                    margin: 0;
                }}
                header {{
                    background: #0078D4;
                    color: white;
                    padding: 20px 0; 
                    position: relative;
                }}
                .header-title {{
                    text-align: center;
                    font-size: 1.5em;
                }}
                .menu-button {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    font-size: 1.6em;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                }}
                .dropdown {{
                    position: absolute;
                    top: 45px;
                    left: 10px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    display: none;
                    z-index: 999;
                }}
                .dropdown a {{
                    display: block;
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #0078D4;
                    font-weight: bold;
                }}
                .dropdown a:hover {{
                    background-color: #f0f0f0;
                }}
                main {{
                    padding: 20px;
                    max-width: 600px;
                    margin: auto;
                }}
                form {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.08);
                }}
                label {{
                    font-weight: bold;
                    display: block;
                    margin-top: 15px;
                    margin-bottom: 8px;
                    color: #333;
                    font-size: 0.95em;
                }}
                input[type="text"], input[type="number"], select {{
                    width: 100%;
                    padding: 12px; 
                    font-size: 1em;
                    border: 1px solid #ccc;
                    border-radius: 6px; 
                    box-sizing: border-box;
                    background-color: #fff;
                    transition: border-color 0.2s ease, box-shadow 0.2s ease;
                }}
                input[type="text"]:focus, input[type="number"]:focus, select:focus {{
                    outline: none;
                    border-color: #0078D4;
                    box-shadow: 0 0 0 2px rgba(0,120,212,0.2);
                }}
                button[type="submit"] {{
                    margin-top: 30px; 
                    width: 100%;
                    background: #0078D4;
                    color: white;
                    padding: 15px; 
                    font-size: 1.1em;
                    border: none;
                    border-radius: 8px; 
                    cursor: pointer;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    transition: background-color 0.2s ease, box-shadow 0.2s ease;
                }}
                button[type="submit"]:hover {{
                    background: #005ea6;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                }}
                .collapsible-container {{ 
                    margin-top: 25px;
                    border-top: 1px solid #eee; 
                    padding-top: 15px;
                }}
                .collapsible-toggle {{
                    background: none;
                    border: none;
                    font-size: 1.05em; 
                    color: #0078D4;
                    display: flex;
                    align-items: center;
                    gap: 8px; 
                    font-weight: bold;
                    cursor: pointer;
                    width: 100%; 
                    padding: 10px 0; 
                    box-sizing: border-box;
                    text-align: left;
                }}
                .collapsible-toggle:hover {{
                    color: #005ea6;
                }}
                .arrow {{
                    transition: transform 0.3s ease;
                }}
                .collapsible-open .arrow {{
                    transform: rotate(90deg);
                }}
                .collapsible-content {{
                    display: none;
                    margin-top: 10px;
                    padding-top: 10px;
                }}
                .collapsible-open .collapsible-content {{
                    display: block;
                }}
                .back-button {{ 
                    display: block;
                    text-align: center;
                    font-size: 1em;
                    text-decoration: none;
                    background: #0078D4;
                    color: white;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin: 20px auto 0 auto; 
                    width: 200px;
                    transition: background-color 0.2s ease, box-shadow 0.2s ease;
                }}
                .back-button:hover {{
                    background-color: #005ea6;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                }}
                @media (max-width: 600px) {{
                    header {{
                        padding: 20px 0;
                    }}
                    .header-title {{
                        font-size: 1.3em;
                    }}
                    main {{
                        padding: 15px;
                    }}
                    form {{
                        padding: 15px;
                    }}
                    label {{
                        font-size: 0.9em;
                        margin-bottom: 5px;
                    }}
                    input, select, button {{
                        padding: 10px;
                        font-size: 0.95em;
                    }}
                    button[type="submit"] {{
                        margin-top: 25px;
                    }}
                    .back-button {{
                        width: 180px;
                        padding: 10px;
                        font-size: 0.95em;
                    }}
                    .collapsible-toggle {{
                        font-size: 1em;
                    }}
                }}
            </style>
            <script>
                function toggleMenu() {{
                    const menu = document.getElementById("extraMenu");
                    menu.style.display = (menu.style.display === "block") ? "none" : "block";
                }}
                document.addEventListener("click", function(event) {{
                    const menu = document.getElementById("extraMenu");
                    const isClickInside = event.target.closest(".menu-button, #extraMenu");
                    if (!isClickInside) {{
                        menu.style.display = "none";
                    }}
                }});
                function toggleCollapsible(button) {{
                    const container = button.parentNode;
                    container.classList.toggle('collapsible-open');
                }}
            </script>
        </head>
        <body>
            <header>
                <button class="menu-button" onclick="toggleMenu()">☰</button>
                <div id="extraMenu" class="dropdown">
                    <a href="/">🏠 Torna alla Home</a>
                    <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
                    <a href="/lista">📈 Elenca/Modifica</a>
                    <a href="/stats">📊 Report Mese</a>
                    <a href="/report_annuo">📅 Report Annuale</a>
                    <a href="/menu_esplora">🔍 Esplora</a>
                    <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
                    <a href="/utenze?anno={datetime.date.today().year}">💧 Utenze</a>
                    <a href="/logoff">🔓 Logout</a>
                </div>
                <div class="header-title">🔎 Esplorazione Avanzata</div>
            </header>
            <main>
                <form method='get' action='/cerca_avanzata'>
                    <label for='categoria'>Categoria:</label>
                    <select name='categoria'>
                        <option value=''>-- Qualsiasi --</option>
                        {''.join(f"<option value='{html.escape(str(cat))}'>{html.escape(str(cat))}</option>" for cat in categorie)}
                    </select>
                    <label for='tipo'>Tipo:</label>
                    <select name='tipo'>
                        <option value=''>-- Qualsiasi --</option>
                        <option value='Entrata'>Entrata</option>
                        <option value='Uscita'>Uscita</option>
                    </select>
                    <label for='anno'>Anno:</label>
                    <select name='anno'>
                        <option value=''>-- Tutti --</option>
                        {''.join(f"<option value='{html.escape(a)}'>{html.escape(a)}</option>" for a in anni)}
                    </select>
                    <label for='mese'>Mese:</label>
                    <select name='mese'>
                        <option value=''>-- Tutti --</option>
                        {''.join(f"<option value='{m.split(' - ')[0]}'>{m}</option>" for m in mesi)}
                    </select>
                    <div class="collapsible-container">
                        <button type="button" class="collapsible-toggle" onclick="toggleCollapsible(this)">
                            <span class="arrow">▶️</span> Filtri aggiuntivi
                        </button>
                        <div class="collapsible-content">
                            <label for='min_importo'>Importo minimo (€):</label>
                            <input type='number' name='min_importo' step='0.01' placeholder='es: 10.50'>
                            <label for='max_importo'>Importo massimo (€):</label>
                            <input type='number' name='max_importo' step='0.01' placeholder='es: 100.00'>
                            <label for='q'>Testo libero (descrizione):</label>
                            <input type='text' name='q' placeholder='es: pane, bolletta, abbonamento'>
                        </div>
                    </div>
                    <button type='submit'>🔍 Avvia Esplorazione</button>
                </form>
                <a href="/" class="back-button">🏠 Torna alla Home</a>
            </main>
        </body>
        </html>
        """
        return html_code

    def add_categoria_web(self, params):
        nome = params.get("nome_categoria", [""])[0].strip()
        tipo = params.get("tipo_categoria", ["Uscita"])[0]
        if not nome or nome in self.categorie or nome == self.CATEGORIA_RIMOSSA:
            print(f"Errore: Categoria '{nome}' già esistente o non valida.")
            return self.html_gestione_categorie()
        self.categorie.append(nome)
        self.categorie_tipi[nome] = tipo
        self.categorie.sort()
        self.save_db()
        self.refresh_categorie_web()
        
    def modifica_categoria_web(self, params):
        old_nome = params.get("categoria_selezionata", [""])[0]
        new_nome = params.get("nuovo_nome", [""])[0].strip()
        nuovo_tipo = params.get("nuovo_tipo", ["Uscita"])[0]
        if not old_nome or old_nome == "Generica":
            return
        if new_nome == old_nome:
            self.categorie_tipi[new_nome] = nuovo_tipo
        else:
            if not new_nome or new_nome in self.categorie:
                return 
            idx = self.categorie.index(old_nome)
            self.categorie[idx] = new_nome
            self.categorie_tipi[new_nome] = nuovo_tipo
            self.categorie_tipi.pop(old_nome, None)
            for d in self.spese:
                new_entries = []
                for entry in self.spese[d]:
                    if entry[0] == old_nome:
                        entry = (new_nome,) + entry[1:]
                    new_entries.append(entry)
                self.spese[d] = new_entries
            self.categorie.sort()
        self.save_db()
        self.refresh_categorie_web()
        
    def cancella_categoria_web(self, params):
        cat_da_cancellare = params.get("categoria_selezionata", [""])[0]
        if not cat_da_cancellare or cat_da_cancellare not in self.categorie or cat_da_cancellare == "Generica":
            return
        self.categorie.remove(cat_da_cancellare)
        self.categorie_tipi.pop(cat_da_cancellare, None)
        for d in self.spese:
            new_entries = []
            for entry in self.spese[d]:
                if entry[0] == cat_da_cancellare:
                    entry = (self.CATEGORIA_RIMOSSA,) + entry[1:]
                new_entries.append(entry)
            self.spese[d] = new_entries
        self.save_db()
        self.refresh_categorie_web()
        
    def refresh_categorie_web(self):
        self.after(100, self._esegui_aggiornamento_gui)
        
    def _esegui_aggiornamento_gui(self):
        self.load_db()
        self.aggiorna_combobox_categorie()
        self.carica_voci_treeview() 
        if hasattr(self, 'ricorrenza_popup') and self.ricorrenza_popup.winfo_exists():
            if hasattr(self, 'ric_cat_menu'):
                self.ric_cat_menu['values'] = sorted(self.categorie)
        self.refresh_gui()        
        
    def html_gestione_categorie(self):
        import datetime
        categorie_tipi_js = str(self.categorie_tipi).replace("'", '"')
        categorie_options = "".join(
            f"<option value='{cat}'>{cat}</option>" 
            for cat in sorted(self.categorie, key=lambda x: x.strip().lower())
        )
        anno_corrente = datetime.datetime.now().year
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Gestione Categorie - Casa Facile Web</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    margin: 0;
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f4f4f4;
                }}
                header {{
                    background: #0078D4;
                    color: white;
                    padding: 20px 0;
                    position: relative;
                }}
                .header-title {{
                    text-align: center;
                    font-size: 1.2em;
                }}
                .menu-button {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    font-size: 1.6em;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                }}
                .dropdown {{
                    position: absolute;
                    top: 45px;
                    left: 10px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    display: none;
                    z-index: 999;
                }}
                .dropdown a {{
                    display: block;
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #0078D4;
                    font-weight: bold;
                }}
                .dropdown a:hover {{
                    background-color: #f0f0f0;
                }}
                main {{
                    padding: 10px;
                    max-width: 400px;
                    margin: auto;
                }}
                .category-box {{
                    background: white;
                    padding: 15px 20px;
                    margin-bottom: 15px;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(0,0,0,0.05);
                }}
                details summary {{
                    cursor: pointer;
                    list-style: none;
                    padding: 5px 0;
                }}
                details summary::-webkit-details-marker {{
                    display: none;
                }}
                details summary:before {{
                    content: '▶️'; 
                    margin-right: 10px;
                    transition: transform 0.2s;
                }}
                details[open] summary:before {{
                    content: '🔽'; 
                    transform: rotate(90deg);
                }}
                label {{
                    display: block;
                    margin-top: 10px;
                    font-weight: bold;
                    font-size: 0.9em;
                }}
                input[type="text"], select {{
                    width: 100%;
                    padding: 8px;
                    margin-top: 5px;
                    margin-bottom: 12px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                    font-size: 0.9em;
                }}
                button[type="submit"] {{
                    background-color: #0078D4;
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 0.9em;
                    border-radius: 6px;
                    padding: 10px;
                    margin-top: 10px;
                    display: inline-block;
                    width: auto;
                }}
                button[type="submit"]:hover {{
                    background-color: #005ea6;
                }}
                .delete-button {{
                    background-color: #c43b2e;
                }}
                .delete-button:hover {{
                    background-color: #9c2e25;
                }}
            </style>
            <script>
                const CategorieTipi = {categorie_tipi_js};

                function toggleMenu() {{
                    const menu = document.getElementById("extraMenu");
                    menu.style.display = (menu.style.display === "block") ? "none" : "block";
                }}
                function aggiornaTipoCategoria() {{
                    const selector = document.getElementById("categoria_modifica");
                    const tipoSelect = document.getElementById("nuovo_tipo");
                    const selectedCat = selector.value;
                    
                    if (selectedCat && CategorieTipi[selectedCat]) {{
                        const tipoCorrente = CategorieTipi[selectedCat];
                        tipoSelect.value = tipoCorrente;
                    }} else {{
                        tipoSelect.value = 'Uscita';
                    }}
                }}
                document.addEventListener("click", function(event) {{
                    const menu = document.getElementById("extraMenu");
                    const isClickInside = event.target.closest(".menu-button, #extraMenu");
                    if (!isClickInside) {{
                        menu.style.display = "none";
                    }}
                }});
                document.addEventListener("DOMContentLoaded", function() {{
                    const categoriaModifica = document.getElementById("categoria_modifica");
                    if (categoriaModifica) {{
                        categoriaModifica.addEventListener("change", aggiornaTipoCategoria);
                        if (categoriaModifica.value) {{ 
                           aggiornaTipoCategoria();
                        }}
                    }}
                }});
            </script>
        </head>
        <body>
            <header>
                <button class="menu-button" onclick="toggleMenu()">☰</button>
                <div id="extraMenu" class="dropdown">
                    <a href="/">🏠 Torna alla Home</a>
                    <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
                    <a href="/lista">📈 Elenca/Modifica</a>
                    <a href="/stats">📊 Report Mese</a>
                    <a href="/report_annuo">📅 Report Annuale</a>
                    <a href="/menu_esplora">🔍 Esplora</a>
                    <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
                    <a href="/utenze?anno={anno_corrente}">💧 Utenze</a>
                    <a href="/logoff">🔓 Logout</a>
                </div>
                <div class="header-title">⚙️ Gestione Categorie</div>
            </header>
            <main>
                <details class="category-box">
                    <summary style="font-size: 1.1em; font-weight: bold; color: #0078D4;">
                        ➕ Aggiungi Categoria
                    </summary>
                    <form action="/salva_categoria" method="POST">
                        <input type="hidden" name="operazione" value="aggiungi">
                        <label for="nome_categoria">Nome:</label>
                        <input type="text" name="nome_categoria" required>
                        <label for="tipo_categoria">Tipo:</label>
                        <select name="tipo_categoria">
                            <option value="Uscita">Uscita</option>
                            <option value="Entrata">Entrata</option>
                        </select>
                        <button type="submit">➕ Aggiungi</button>
                    </form>
                </details>
                <details class="category-box">
                    <summary style="font-size: 1.1em; font-weight: bold; color: #0078D4;">
                        ⚙️ Modifica Categoria
                    </summary>
                    <form action="/salva_categoria" method="POST">
                        <input type="hidden" name="operazione" value="modifica">
                        <label for="categoria_selezionata">Seleziona:</label>
                        <select 
                            name="categoria_selezionata" 
                            id="categoria_modifica" 
                            required
                        >
                            {categorie_options} 
                        </select>
                        <label for="nuovo_nome">Nuovo Nome:</label>
                        <input type="text" name="nuovo_nome" placeholder="Lascia vuoto per modificare solo il tipo">
                        <label for="nuovo_tipo">Nuovo Tipo:</label>
                        <select name="nuovo_tipo" id="nuovo_tipo">
                            <option value="Uscita">Uscita</option>
                            <option value="Entrata">Entrata</option>
                        </select>
                        <button type="submit">⚙️ Modifica</button>
                    </form>
                </details>
                <details class="category-box" style="border: 1px solid #c43b2e;">
                    <summary style="font-size: 1.1em; font-weight: bold; color: #c43b2e;">
                        ❌ Cancella Categoria
                    </summary>
                    <form action="/cancella_categoria" method="POST">
                        <label for="categoria_selezionata">Seleziona:</label>
                        <select name="categoria_selezionata" required>
                            {categorie_options}
                        </select>
                        <button type="submit" class="delete-button">❌ Cancella</button>
                    </form>
                </details>
                <div style="background-color: #0078D4; text-align: center; margin-top: 20px; padding: 10px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <a href='/' style='font-size:0.9em; text-decoration:none; color:white; display: block; font-weight: bold;'>
                        🏠 Torna alla Home
                    </a>
                </div>
            </main>
        </body>
        </html>
        """
        return html

    def get_dati_entrate_uscite_tutti_gli_anni_json(self):
        totali_annuali = {}
        for giorno, voci in self.spese.items():
            try:
                anno = giorno.year
            except AttributeError:
                continue 
            if anno not in totali_annuali:
                totali_annuali[anno] = {'Entrate': 0.0, 'Uscite': 0.0}
            for voce in voci:
                if len(voce) < 4: continue
                raw_importo = voce[2]
                tipo = voce[3] 
                try:
                    importo_str = str(raw_importo).strip().replace(',', '.')
                    importo = float(importo_str)
                except (TypeError, ValueError):
                    continue 
                if tipo == "Entrata":
                    totali_annuali[anno]['Entrate'] += importo
                elif tipo == "Uscita":
                    totali_annuali[anno]['Uscite'] += importo
        anni_ordinati = sorted(totali_annuali.keys()) 
        data_entrate = [totali_annuali[anno]['Entrate'] for anno in anni_ordinati]
        data_uscite = [totali_annuali[anno]['Uscite'] for anno in anni_ordinati]
        dati_json = {
            "labels": [str(anno) for anno in anni_ordinati],
            "datasets": [
                {
                    "label": "Entrate",
                    "data": data_entrate,
                    "backgroundColor": "rgba(40, 167, 69, 0.7)"
                },
                {
                    "label": "Uscite",
                    "data": data_uscite,
                    "backgroundColor": "rgba(220, 53, 69, 0.7)"
                }
            ]
        }
        return json.dumps(dati_json)

    def pagina_statistiche_annuali_web(self):
        import re
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        anno_corrente_int = anno_corrente
        oggi_formattata = oggi.strftime('%d/%m/%Y')
        anno_corrente_format = str(anno_corrente)
        try:
            raw = self.calcola_statistiche_annuali_pura().strip()
            totale_entrate_match = re.search(r"Entrate Totali:.*?([€\s\d.,-]+)", raw, re.DOTALL)
            totale_uscite_match = re.search(r"Uscite Totali:.*?([€\s\d.,-]+)", raw, re.DOTALL)
            totale_entrate = totale_entrate_match.group(1).strip() if totale_entrate_match else None
            totale_uscite = totale_uscite_match.group(1).strip() if totale_uscite_match else None
            report_content = raw
            if totale_entrate:
                report_content = re.sub(r".*Entrate Totali:.*?\n", "", report_content, 1, re.DOTALL) 
            if totale_uscite:
                report_content = re.sub(r".*Uscite Totali:.*?\n", "", report_content, 1, re.DOTALL) 
            report_content = report_content.replace("\n", "<br>")
        except Exception as e:
            report_content = "⚠ Report Testuale: Dati non disponibili (Controlla calcola_statistiche_annuali_pura)."
            totale_entrate = None
            totale_uscite = None
        report_content = report_content.replace("🔹 Mese corrente", "<strong><span style='color:#c43b2e;'>🗓️ Mese corrente</span></strong>")
        report_content = report_content.replace("🔹 Da inizio anno", "<strong><span style='color:#d48300;'>📆 Da inizio anno</span></strong>")
        report_content = report_content.replace("🔹 Proiezione fine anno", "<strong><span style='color:#0078D4;'>📊 Proiezione fine anno</span></strong>")
        report_content = report_content.replace("✅ Risparmio previsto", "<strong><span style='color:green;'>💰 Risparmio previsto</span></strong>")
        report_content = report_content.replace("⚠️ Possibile extra spesa", "<strong><span style='color:red;'>📉 Possibile extra spesa</span></strong>")
        if totale_entrate is not None or totale_uscite is not None:
            entrate_display = totale_entrate if totale_entrate else "N/D"
            uscite_display = totale_uscite if totale_uscite else "N/D"
            report_summary_html = f"""
<div style="padding: 10px 20px; font-size: 1.1em; font-weight: bold; background: #fff; border-bottom: 2px solid #0078D4;">
    <p style="margin: 0;">💸 Riepilogo Totale Anno:</p>
    <p style="margin: 5px 0 0 0;">
        💰 Entrate: <span style='color:green;'>{entrate_display}</span> | 
        📉 Uscite: <span style='color:red;'>{uscite_display}</span>
    </p>
</div>
"""
        else:
            report_summary_html = ""
        fallback_storico = '{"labels": ["N/D"], "datasets": [{"label": "Dati non caricati", "data": [0], "backgroundColor": ["#ccc"]}]}'
        fallback_mensile = '{"labels": ["N/D"], "datasets": [{"label": "Dati non caricati", "data": [0], "backgroundColor": ["#ccc"]}]}'
        fallback_cat = '{"labels": ["N/D"], "datasets": [{"data": [1], "backgroundColor": ["#ccc"], "label": "Dati non caricati"}]}'
        fallback_saldo = '{"labels": ["N/D"], "datasets": [{"label": "Dati non caricati", "data": [0], "borderColor": "#ccc"}]}'
        fallback_cat_storico = '{"labels": ["N/D"], "datasets": [{"data": [1], "backgroundColor": ["#ccc"], "label": "Dati non caricati"}]}'
        fallback_saldo_annuale = '{"labels": ["N/D"], "datasets": [{"label": "Dati non caricati", "data": [0], "borderColor": "#ccc", "backgroundColor": ["#ccc"]}]}'
        try:
            dati_entrate_uscite_storici = self.get_dati_entrate_uscite_tutti_gli_anni_json()
        except Exception:
            dati_entrate_uscite_storici = fallback_storico
        try:
            dati_entrate_uscite_mensili = self.get_dati_entrate_uscite_json()
        except Exception:
            dati_entrate_uscite_mensili = fallback_mensile
        try:
            dati_categorie = self.get_dati_categorie_json()
        except Exception:
            dati_categorie = fallback_cat
        try:
            dati_saldo = self.get_dati_saldo_json()
        except Exception:
            dati_saldo = fallback_saldo
        try:
            dati_categorie_storiche = self.get_dati_categorie_storiche_json()
        except Exception as e:
            dati_categorie_storiche = fallback_cat_storico
        try:
            dati_saldo_annuale = self.get_dati_saldo_annuale_json()
        except Exception:
            dati_saldo_annuale = fallback_saldo_annuale
        try:
            data_storico = json.loads(dati_entrate_uscite_storici)
            totale_eu_storico_str = "Dati Non Trovati"
            if data_storico.get("datasets") and len(data_storico["datasets"]) == 2:
                entrate_storiche = sum(data_storico["datasets"][0].get("data", [0]))
                uscite_storiche = sum(data_storico["datasets"][1].get("data", [0]))
                saldo_storico = entrate_storiche - uscite_storiche
                totale_eu_storico_str = f"Entrate: {entrate_storiche:,.2f} | Uscite: {uscite_storiche:,.2f} | Saldo: {saldo_storico:,.2f}"
        except:
            totale_eu_storico_str = "Errore di calcolo"
        try:
            data_mensile = json.loads(dati_entrate_uscite_mensili)
            totale_eu_mensile_str = "Dati Non Trovati"
            if data_mensile.get("datasets") and len(data_mensile["datasets"]) == 2:
                entrate_mensili = sum(data_mensile["datasets"][0].get("data", [0]))
                uscite_mensili = sum(data_mensile["datasets"][1].get("data", [0]))
                saldo_mensile = entrate_mensili - uscite_mensili
                totale_eu_mensile_str = f"Entrate: {entrate_mensili:,.2f} | Uscite: {uscite_mensili:,.2f} | Saldo: {saldo_mensile:,.2f}"
        except:
            totale_eu_mensile_str = "Errore di calcolo"
        try:
            data_saldo = json.loads(dati_saldo)
            saldo_finale_str = "Dati Non Trovati"
            if data_saldo.get("datasets") and data_saldo["datasets"][0].get("data"):
                saldo_finale = data_saldo["datasets"][0]["data"][-1]
                saldo_finale_str = f"Saldo Finale: {saldo_finale:,.2f}"
        except:
            saldo_finale_str = "Errore di calcolo"
        try:
            data_saldo_annuale = json.loads(dati_saldo_annuale)
            totale_saldo_annuale_str = "Dati Non Trovati"
            if data_saldo_annuale.get("datasets") and data_saldo_annuale["datasets"][0].get("data"):
                somma_saldi = sum(data_saldo_annuale["datasets"][0]["data"])
                totale_saldo_annuale_str = f"Saldo Cumulativo: {somma_saldi:,.2f}"
        except:
            totale_saldo_annuale_str = "Errore di calcolo"
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>📊 Report Annuale — {oggi_formattata}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            font-size: 0.9em;
        }}
        header {{ background: #0078D4; color: white; padding: 20px 0; position: relative; }}
        .header-title {{ text-align: center; font-size: 1.5em; }}
        .menu-button {{ position: absolute; top: 10px; left: 10px; font-size: 1.6em; background: none; border: none; color: white; cursor: pointer; }}
        .dropdown {{ position: absolute; top: 45px; left: 10px; background-size: 100%; background-color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.15); border-radius: 4px; display: none; z-index: 999; }}
        .dropdown a {{ display: block; padding: 10px 20px; text-decoration: none; color: #0078D4; font-weight: bold; }}
        .dropdown a:hover {{ background-color: #f0f0f0; }}
        main {{ padding: 20px; max-width: 600px; margin: auto; }}
        .report-box {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 8px rgba(0,0,0,0.1); white-space: pre-wrap; word-break: break-word; font-size: 1em; line-height: 1.5em; font-weight: bold; }}
        .back {{ display: block; text-align: center; font-size: 1em; text-decoration: none; background: #0078D4; color: white; padding: 10px; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px auto; width: 200px; }}
        .back:hover {{ background-color: #005ea6; }}
        .accordion-header {{ background: #e0e0e0; color: #333; padding: 15px; border-radius: 6px; cursor: pointer; margin-top: 20px; display: flex; justify-content: space-between; align-items: center; font-size: 1.1em; font-weight: bold; }}
        .accordion-header:hover {{ background: #d0d0d0; }}
        .arrow {{ transition: transform 0.3s ease; font-size: 1.2em; }}
        .accordion-header.active .arrow {{ transform: rotate(90deg); }}
        .accordion-content {{
            padding: 0 15px;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 8px 8px;
            background: white;
        }}
        .tab-pane {{ padding-top: 15px; display: none; }}
        .tab-pane.active {{ display: block; }}
        .tab-container {{ 
            display: flex; 
            flex-wrap: wrap;
            border-bottom: 2px solid #0078D4; 
            justify-content: center;
            padding: 0;
        }}
        .tab-button {{ 
            padding: 8px 10px;
            cursor: pointer; 
            font-weight: bold; 
            color: #555; 
            border: none; 
            background: #f0f0f0; 
            border-radius: 5px 5px 0 0; 
            margin-right: 2px; 
            margin-bottom: 5px;
            font-size: 0.9em;
        }}
        .tab-button.active {{ background: #0078D4; color: white; }}
        .chart-container {{
            position: relative;
            width: 100%;
            margin: auto;
        }}
        .bar-chart-container {{
            min-height: 500px; 
            height: 50vh; 
            max-height: 600px;
        }}
        #tabCategorie .chart-container,
        #tabStoricoCat .chart-container {{
            height: 650px; 
            max-height: 90vh; 
            display: flex; 
            flex-direction: column;
            padding-top: 0px;
        }}
        .chart-container canvas {{
            max-width: 95%; 
            height: auto !important; 
            display: block;
            margin: 0 auto;
            flex-grow: 1;
        }}
    </style>
    <script>
        const currentYear = {anno_corrente_int};
        const chartInstances = {{}}; 
        window.CATEGORIE_DATA = null;
        window.CATEGORIE_STORICHE_DATA = null;
        window.DATA_SALDO_ANNUALE = JSON.parse('{dati_saldo_annuale}');
        
        const TOTALI = {{
            STORICO_EU: "{totale_eu_storico_str}",
            MENSILE_EU: "{totale_eu_mensile_str}",
            SALDO: "{saldo_finale_str}",
            SALDO_ANNUALE: "{totale_saldo_annuale_str}"
        }};

        function createChart(id, type, data, options) {{
            if (chartInstances[id] && typeof chartInstances[id].destroy === 'function') {{
                chartInstances[id].destroy(); 
            }}
            const ctx = document.getElementById(id);
            if (ctx) {{
                chartInstances[id] = new Chart(ctx, {{ type, data, options }});
                return true;
            }}
            return false;
        }}
        function drawCharts() {{
            const dataCategorie = JSON.parse('{dati_categorie}');
            if (dataCategorie && dataCategorie.labels && dataCategorie.datasets && dataCategorie.datasets.length > 0) {{
                const combinedData = dataCategorie.labels.map((label, index) => ({{
                    label: label,
                    data: dataCategorie.datasets[0].data[index],
                    backgroundColor: dataCategorie.datasets[0].backgroundColor[index]
                }}));
                combinedData.sort((a, b) => a.label.localeCompare(b.label));
                dataCategorie.labels = combinedData.map(item => item.label);
                dataCategorie.datasets[0].data = combinedData.map(item => item.data);
                dataCategorie.datasets[0].backgroundColor = combinedData.map(item => item.backgroundColor);
                dataCategorie.total = combinedData.reduce((sum, item) => sum + item.data, 0);
            }}
            window.CATEGORIE_DATA = dataCategorie; 
            const dataCategorieStoriche = JSON.parse('{dati_categorie_storiche}');
            if (dataCategorieStoriche && dataCategorieStoriche.labels && dataCategorieStoriche.datasets && dataCategorieStoriche.datasets.length > 0) {{
                const combinedData = dataCategorieStoriche.labels.map((label, index) => ({{
                    label: label,
                    data: dataCategorieStoriche.datasets[0].data[index],
                    backgroundColor: dataCategorieStoriche.datasets[0].backgroundColor[index]
                }}));
                dataCategorieStoriche.total = combinedData.reduce((sum, item) => sum + item.data, 0);
            }}
            window.CATEGORIE_STORICHE_DATA = dataCategorieStoriche;
        }}
        function toggleMenu() {{
            const menu = document.getElementById("extraMenu");
            menu.style.display = (menu.style.display === "block") ? "none" : "block";
        }}
        
        document.addEventListener("click", function(event) {{
            const menu = document.getElementById("extraMenu");
            if (!event.target.closest(".menu-button, #extraMenu")) {{
                menu.style.display = "none";
            }}
        }});
        function toggleAccordion(header) {{
            header.classList.toggle("active");
            const content = header.nextElementSibling;
            const isOpening = content.style.display === "none" || content.style.display === "";
            content.style.display = isOpening ? "block" : "none";
            if (isOpening) {{
                const activeTabButton = document.querySelector('.tab-button.active');
                if (activeTabButton) {{
                    const tabName = activeTabButton.getAttribute('onclick').match(/'([^']+)'/)[1];
                    drawSpecificChart(tabName);
                }}
            }}
        }}
        function openTab(tabName, button) {{
            document.querySelectorAll(".tab-pane").forEach(el => el.classList.remove("active"));
            document.querySelectorAll(".tab-button").forEach(el => el.classList.remove("active"));
            document.getElementById(tabName).classList.add("active");
            button.classList.add("active");
            drawSpecificChart(tabName);
        }}
        function drawSpecificChart(tabName) {{
            const dataEntrateUsciteStorici = JSON.parse('{dati_entrate_uscite_storici}');
            const dataEntrateUsciteMensili = JSON.parse('{dati_entrate_uscite_mensili}');
            const dataSaldo = JSON.parse('{dati_saldo}');
            const dataCategorie = window.CATEGORIE_DATA;
            const dataCategorieStoriche = window.CATEGORIE_STORICHE_DATA;
            const dataSaldoAnnuale = window.DATA_SALDO_ANNUALE;
            let success = false;
            const formatCurrency = (amount) => amount.toLocaleString('it-IT', {{ style: 'currency', currency: 'EUR' }});
            const barOptions = {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{ display: true }}
                }},
                barPercentage: 0.9,      
                categoryPercentage: 0.9  
            }};
            const pieOptions = {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{ display: true }}, 
                    legend: {{ 
                        display: true, 
                        position: 'bottom', 
                        align: 'start', 
                        labels: {{ usePointStyle: false, boxWidth: 20, padding: 5 }},
                        onClick: (e, legendItem, legend) => {{
                            const chart = legend.chart;
                            chart.toggleDataVisibility(legendItem.index);
                            const meta = chart.getDatasetMeta(0);
                            let newTotal = 0;
                            meta.data.forEach((element, index) => {{
                                if (chart.getDataVisibility(index)) {{ 
                                    newTotal += chart.data.datasets[0].data[index];
                                }}
                            }});
                            const newTitleText = 'Totale: ' + formatCurrency(newTotal);
                            let mainTitle = chart.options.plugins.title.text[0];
                            chart.options.plugins.title.text = [mainTitle, newTitleText];
                            chart.update(); 
                        }} 
                    }}
                }}
            }};
            switch(tabName) {{
                case 'tabStoricoEU':
                    success = createChart('entrateUsciteStoricheChart', 'bar', dataEntrateUsciteStorici, {{ 
                        ...barOptions, 
                        plugins: {{ ...barOptions.plugins, title: {{ display: true, text: ['Entrate e Uscite Storiche per Anno', 'Totali: ' + TOTALI.STORICO_EU] }} }} 
                    }});
                    break;
                case 'tabMensileEU':
                    success = createChart('entrateUsciteMensiliChart', 'bar', dataEntrateUsciteMensili, {{ 
                        ...barOptions, 
                        plugins: {{ ...barOptions.plugins, title: {{ display: true, text: ['Entrate e Uscite Mensili (' + currentYear + ')', 'Totali: ' + TOTALI.MENSILE_EU] }} }} 
                    }});
                    break;
                case 'tabCategorie':
                    const totalCat = dataCategorie.total !== undefined ? formatCurrency(dataCategorie.total) : 'N/D';
                    success = createChart('categorieChart', 'doughnut', dataCategorie, {{ 
                        ...pieOptions, 
                        plugins: {{ ...pieOptions.plugins, title: {{ display: true, text: ['Spese per Categoria (Anno Corrente)', 'Totale: ' + totalCat] }} }} 
                    }});
                    break;
                case 'tabStoricoCat':
                    const totalStoricoCat = dataCategorieStoriche.total !== undefined ? formatCurrency(dataCategorieStoriche.total) : 'N/D';
                    success = createChart('storicoCategorieChart', 'doughnut', dataCategorieStoriche, {{ 
                        ...pieOptions, 
                        plugins: {{ ...pieOptions.plugins, title: {{ display: true, text: ['Spese Storiche per Categoria (Tutti gli anni)', 'Totale: ' + totalStoricoCat] }} }} 
                    }});
                    break;
                case 'tabSaldo':
                    success = createChart('saldoChart', 'line', dataSaldo, {{ 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: {{ title: {{ display: true, text: ['Saldo Progressivo Mensile', TOTALI.SALDO] }} }} 
                    }});
                    break;
                case 'tabSaldoAnnuale':
                    success = createChart('saldoAnnualeChart', 'bar', dataSaldoAnnuale, {{ 
                        ...barOptions, 
                        scales: {{ y: {{ beginAtZero: false }} }},
                        plugins: {{ ...barOptions.plugins, title: {{ display: true, text: ['Saldo Netto Annuale per Anno', TOTALI.SALDO_ANNUALE] }} }} 
                    }});
                    break;
            }}
            if (success) {{
                chartInstances[tabName] = true; 
            }}
        }}

        document.addEventListener("DOMContentLoaded", () => {{
            drawCharts();
            const firstTabButton = document.querySelector('.tab-container .tab-button');
            if(firstTabButton) {{
                const tabName = firstTabButton.getAttribute('onclick').match(/'([^']+)'/)[1];
                openTab(tabName, firstTabButton);
            }}
            const accordionContent = document.getElementById("accordionContent");
            accordionContent.style.display = "none";
        }});
    </script>
</head>
<body>
    <header>
        <button class="menu-button" onclick="toggleMenu()">☰</button>
        <div id="extraMenu" class="dropdown">
            <a href="/">🏠 Torna alla Home</a>
            <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
            <a href="/lista">📈 Elenca/Modifica</a>
            <a href="/stats">📊 Report Mese</a>
            <a href="/report_annuo">📅 Report Annuale</a>
            <a href="/menu_esplora">🔍 Esplora</a>
            <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
            <a href="/utenze?anno={anno_corrente_format}">💧 Utenze</a>
            <a href="/logoff">🔓 Logout</a>
        </div>
        <div class="header-title">📊 Report del {oggi_formattata}</div>
    </header>
    {report_summary_html}
    <main>
        <div class="report-box">{report_content}</div>
        <div class="accordion-header" onclick="toggleAccordion(this)">
            Visualizza Grafici Dettaglio 📊
            <span class="arrow">▶</span>
        </div>
        <div id="accordionContent" class="accordion-content">
            <div class="tab-content-wrapper">
                <div class="tab-container">
                    <button class="tab-button" onclick="openTab('tabStoricoEU', this)">Storico</button>
                    <button class="tab-button" onclick="openTab('tabMensileEU', this)">Mensile</button>
                    <button class="tab-button" onclick="openTab('tabSaldo', this)">Saldo Mese</button>
                    <button class="tab-button" onclick="openTab('tabSaldoAnnuale', this)">Saldo Annuale</button> <button class="tab-button" onclick="openTab('tabCategorie', this)">Uscite</button>
                    <button class="tab-button" onclick="openTab('tabStoricoCat', this)">Uscite Storiche</button>
                </div>
                <div class="tab-content">
                    <div id="tabStoricoEU" class="tab-pane">
                        <div class="chart-container bar-chart-container">
                            <canvas id="entrateUsciteStoricheChart"></canvas>
                        </div>
                    </div>
                    <div id="tabMensileEU" class="tab-pane">
                        <div class="chart-container bar-chart-container">
                            <canvas id="entrateUsciteMensiliChart"></canvas>
                        </div>
                    </div>
                    <div id="tabCategorie" class="tab-pane">
                        <div class="chart-container">
                            <canvas id="categorieChart"></canvas>
                        </div>
                    </div>
                    <div id="tabStoricoCat" class="tab-pane">
                        <div class="chart-container">
                            <canvas id="storicoCategorieChart"></canvas>
                        </div>
                    </div>
                    <div id="tabSaldo" class="tab-pane">
                        <div class="chart-container bar-chart-container">
                            <canvas id="saldoChart"></canvas>
                        </div>
                    </div>
                    <div id="tabSaldoAnnuale" class="tab-pane"> 
                        <div class="chart-container bar-chart-container">
                            <canvas id="saldoAnnualeChart"></canvas>
                        </div>
                    </div>
                    
                </div>
            </div>
        </div>
        <a href="/" class="back">🏠 Torna alla Home</a>
    </main>
</body>
</html>
"""
        return html_template

    def get_dati_saldo_annuale_json(self):
        saldo_per_anno = {} 
        for d, voci in self.spese.items():
            anno = d.year
            if anno not in saldo_per_anno:
                saldo_per_anno[anno] = 0.0
            for voce in voci:
                importo = float(voce[2]) 
                tipo = voce[3].strip().lower()
                if tipo == "entrata":
                    saldo_per_anno[anno] += importo
                elif tipo == "uscita":
                    saldo_per_anno[anno] -= importo
        anni_ordinati = sorted(saldo_per_anno.keys())
        dati_json = {
            "labels": [str(anno) for anno in anni_ordinati],
            "datasets": [{
                "label": "Saldo Netto Annuale",
                "data": [saldo_per_anno[anno] for anno in anni_ordinati],
                "backgroundColor": ["#228B22" if saldo_per_anno[anno] >= 0 else "#c43b2e" for anno in anni_ordinati]
            }]
        }
        return json.dumps(dati_json)

    def get_dati_categorie_storiche_json(self):
        spese_per_categoria = {}
        for giorno, voci in self.spese.items():
                for voce in voci:
                        if len(voce) >= 4 and voce[3] == "Uscita":
                                categoria, _, importo, _ = voce[:4]
                                spese_per_categoria[categoria] = spese_per_categoria.get(categoria, 0.0) + importo
        if not spese_per_categoria:
                return '{"labels": ["N/D"], "datasets": [{"data": [1], "backgroundColor": ["#ccc"], "label": "Dati non disponibili"}]}'
        sorted_categorie = sorted(spese_per_categoria.keys())
        labels = sorted_categorie
        data = [spese_per_categoria[cat] for cat in sorted_categorie]
        colori_predefiniti = [
                "#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850",
                "#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff",
                "#ff9f40", "#ff6384", "#63b5ff", "#c9cbcf", "#e7e9ed"
        ]
        background_colors = [colori_predefiniti[i % len(colori_predefiniti)] for i in range(len(labels))]
        chart_data = {
                "labels": labels,
                "datasets": [{
                        "data": data,
                        "backgroundColor": background_colors,
                        "label": "Spese Storiche"
                }]
        }
        return json.dumps(chart_data)

    def calcola_statistiche_annuali_pura(self):
        from datetime import date
        oggi = date.today()
        anno_corr = oggi.year
        anno_prec = anno_corr - 1
        mese_corr = oggi.month
        tot_mese_corr = tot_mese_prec = 0.0
        tot_anno_corr = tot_anno_prec = 0.0
        stima_anno_prec = 0.0
        for giorno, voci in self.spese.items():
            for voce in voci:
                if len(voce) < 4:
                    continue
                categoria, descrizione, importo, tipo = voce[:4]
                if tipo != "Uscita":
                    continue
                if giorno.year == anno_corr and giorno.month == mese_corr:
                    tot_mese_corr += importo
                if giorno.year == anno_prec and giorno.month == mese_corr:
                    tot_mese_prec += importo
                if giorno.year == anno_corr and giorno <= oggi:
                    tot_anno_corr += importo
                if giorno.year == anno_prec and giorno <= oggi.replace(year=anno_prec):
                    tot_anno_prec += importo
                if giorno.year == anno_prec:
                    stima_anno_prec += importo
        giorni_passati = (oggi - date(anno_corr, 1, 1)).days + 1
        giorni_totali = 365
        perc_anno = giorni_passati / giorni_totali
        stima_anno_corr = tot_anno_corr / perc_anno if perc_anno else tot_anno_corr
        variazione_mese_pct = (
            (tot_mese_corr - tot_mese_prec) / tot_mese_prec * 100
            if tot_mese_prec else 0.0
        )
        differenza = stima_anno_prec - stima_anno_corr
        report = f"""📊 Bilancio dinamico Previsionale
        
 Analisi delle spese attuali e stima
 fino a fine {anno_corr}
  🔹 Mese corrente ({mese_corr:02}/{anno_corr})
  • Spese {anno_corr}:  € {tot_mese_corr:,.2f}
  • Spese {anno_prec}:  € {tot_mese_prec:,.2f}
  • Variazione mensile: {variazione_mese_pct:+.1f}%
 🔹 Da inizio anno (01/01 → oggi)
  • Totale {anno_corr}:  € {tot_anno_corr:,.2f}
  • Totale {anno_prec}:  € {tot_anno_prec:,.2f}
 🔹 Proiezione fine anno
  • Spesa stimata {anno_corr}: € {stima_anno_corr:,.2f}  
  • (⏳ {perc_anno:.1%} dell’anno trascorso)
  • Spesa effettiva {anno_prec}: € {stima_anno_prec:,.2f}
    """
        if differenza > 0:
            report += f"\n✅ Risparmio previsto: € {differenza:,.2f} \n   se mantieni questo ritmo 💰"
        else:
            report += f"\n⚠️ Possibile extra spesa: € {abs(differenza):,.2f}\n   rispetto al {anno_prec} 🪙"
        return report.strip()

    def stats_mensili_html(self):
        mesi_it = {
            "January": "gennaio", "February": "febbraio", "March": "marzo",
            "April": "aprile", "May": "aprile", "June": "giugno",
            "July": "luglio", "August": "agosto", "September": "settembre",
            "October": "ottobre", "November": "novembre", "December": "dicembre"
        }
        oggi = datetime.date.today()
        mese_en = oggi.strftime('%B')
        mese_it_corrente = mesi_it.get(mese_en, mese_en)
        titolo_mese = f"{mese_it_corrente.capitalize()} {oggi.year}"
        entrate = 0.0
        uscite = 0.0
        entrate_categorie = {}
        uscite_categorie = {}
        raw_entrate_dettaglio = {}
        raw_uscite_dettaglio = {}
        entrate_count = {}
        uscite_count = {}
        for d, voci in self.spese.items():
            if d.month == oggi.month and d.year == oggi.year:
                for voce in voci:
                    categoria, descrizione, importo, tipo = voce[:4]
                    if tipo == "Entrata":
                        entrate += importo
                        entrate_categorie[categoria] = entrate_categorie.get(categoria, 0.0) + importo
                        raw_entrate_dettaglio.setdefault(categoria, []).append((d, descrizione, importo))
                        entrate_count[categoria] = entrate_count.get(categoria, 0) + 1 
                    else:
                        uscite += importo
                        uscite_categorie[categoria] = uscite_categorie.get(categoria, 0.0) + importo
                        raw_uscite_dettaglio.setdefault(categoria, []).append((d, descrizione, importo))
                        uscite_count[categoria] = uscite_count.get(categoria, 0) + 1 
        saldo = entrate - uscite
        saldo_colore = "#3c763d" if saldo >= 0 else "#c43b2e" 

        def genera_html_categorie(categorie_totals, raw_dettaglio, prefix, counts_dict):
            html_content = ""
            if not categorie_totals:
                return f"<p class='no-data-msg'>Nessuna {prefix} per categoria da mostrare.</p>"
            html_content += "<ul class='category-list'>"
            for cat, totale in sorted(categorie_totals.items()):
                voci_dettaglio = raw_dettaglio.get(cat, [])
                
                dettagli_id = f"{prefix}_{''.join(filter(str.isalnum, cat))}"
                
                arrow_button_html = ''
                if voci_dettaglio:
                    arrow_button_html = f"""
                        <button type="button" class="category-arrow-button" onclick="toggleVisibility('{dettagli_id}', this)" aria-expanded="false" aria-controls="{dettagli_id}">
                            <span class="category-arrow">▶️</span>
                        </button>
                    """

                color_class = "detail-income" if prefix == "entrate" else "detail-expense"
                dettaglio_items_html = ''.join(
                    f'<li class="detail-item"><span class="detail-text">{data.strftime("%d-%m-%Y")}{" — " + desc if desc else ""}</span><span class="detail-amount {color_class}">€{imp:.2f}</span></li>'
                    for data, desc, imp, *_ in voci_dettaglio
                )
                if not dettaglio_items_html:
                    dettaglio_items_html = '<li>Nessun dettaglio disponibile.</li>'
                num_operations = counts_dict.get(cat, 0)
                category_name_html = f'<strong class="category-name">{cat} ({num_operations}):</strong>'
                html_content += f"""
                <li class="category-item">
                    <div class="category-summary">
                        {arrow_button_html}
                        {category_name_html}
                        <span class="category-total">€{totale:.2f}</span>
                    </div>
                    <ul id="{dettagli_id}" class="hidden category-details">
                        {dettaglio_items_html}
                    </ul>
                </li>
                """
            html_content += "</ul>"
            return html_content
        categorie_uscite_html = genera_html_categorie(uscite_categorie, raw_uscite_dettaglio, "uscite", uscite_count)
        categorie_entrate_html = genera_html_categorie(entrate_categorie, raw_entrate_dettaglio, "entrate", entrate_count)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>📊 Report Mese — {titolo_mese}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                header {{
                    background: #0078D4;
                    color: white;
                    padding: 20px 0;
                    position: relative;
                }}
                .header-title {{
                    text-align: center;
                    font-size: 1.5em;
                }}
                .menu-button {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    font-size: 1.6em;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                }}
                .dropdown {{
                    position: absolute;
                    top: 45px;
                    left: 10px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    display: none;
                    z-index: 999;
                }}
                .dropdown a {{
                    display: block;
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #0078D4;
                    font-weight: bold;
                }}
                .dropdown a:hover {{
                    background-color: #f0f0f0;
                }}
                main {{
                    padding: 15px;
                    max-width: 600px;
                    margin: auto;
                }}
                h2 {{
                    color: #333;
                    text-align: center;
                    font-size: 1.4em;
                    margin-bottom: 15px;
                    padding: 10px 0;
                    background-color: #e9e9e9;
                    border-radius: 6px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                }}
                .main-stats {{
                    list-style-type: none;
                    padding: 15px;
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(0,0,0,0.1);
                    max-width: 100%;
                    margin-bottom: 15px;
                    box-sizing: border-box;
                }}
                .main-stats li {{
                    font-size: 1.1em;
                    margin: 8px 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .main-stats li strong {{
                    flex-shrink: 0;
                }}
                .main-stats li span {{
                    text-align: right;
                    flex-grow: 1;
                }}
                .income-color {{
                    color: #3c763d;
                }}
                .expense-color {{
                    color: #c43b2e;
                }}
                .detail-income {{
                    color: #3c763d;
                }}
                .detail-expense {{
                    color: #c43b2e;
                }}

                .category-list {{
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                }}
                .category-item {{
                    font-size: 1em;
                    margin: 8px 0;
                    display: flex;
                    flex-direction: column;
                    background-color: #fcfcfc;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #eee;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }}
                .category-summary {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    width: 100%;
                }}
                .category-name {{
                    flex-grow: 1;
                }}
                .category-total {{
                    text-align: right;
                    font-weight: bold;
                    flex-shrink: 0;
                    margin-left: 10px;
                }}
                .category-arrow-button {{
                    background: none;
                    border: none;
                    font-size: 1em;
                    cursor: pointer;
                    padding: 0;
                    margin-right: 5px;
                    -webkit-appearance: none;
                    -moz-appearance: none;
                    appearance: none;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .category-arrow-button:hover {{
                    opacity: 0.8;
                }}
                .category-arrow {{
                    transition: transform 0.3s ease;
                    font-size: 0.8em;
                }}
                .category-arrow.rotated {{
                    transform: rotate(90deg);
                }}
                ul.category-details {{
                    list-style-type: none;
                    background: #f0f0f0;
                    padding: 10px 15px;
                    border-radius: 4px;
                    margin-top: 8px;
                    margin-left: 0;
                    font-size: 0.9em;
                    width: 100%;
                    box-sizing: border-box;
                }}
                ul.category-details .detail-item {{
                    display: flex;
                    justify-content: space-between;
                    align-items: baseline;
                    margin: 5px 0;
                    padding-left: 10px;
                    position: relative;
                    flex-wrap: wrap; 
                }}
                ul.category-details .detail-item::before {{
                    content: '•';
                    position: absolute;
                    left: 0;
                    color: #0078D4;
                }}
                .detail-text {{
                    flex-grow: 1;
                    flex-shrink: 1;
                    min-width: 0;
                    padding-right: 5px;
                }}
                .detail-amount {{
                    text-align: right;
                    font-weight: bold;
                    flex-shrink: 0;
                    margin-left: auto;
                }}
                .section-toggle-button {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    width: 100%;
                    padding: 12px;
                    background-color: #0078D4;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 1.05em;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    text-align: left;
                    box-sizing: border-box;
                    -webkit-appearance: none;
                    -moz-appearance: none;
                    appearance: none;
                }}
                .section-toggle-button:hover {{
                    background-color: #005ea6;
                }}
                .arrow {{
                    transition: transform 0.3s ease;
                    font-size: 0.9em;
                }}
                .arrow.rotated {{
                    transform: rotate(90deg);
                }}
                .hidden {{
                    display: none;
                }}
                .collapsible-content {{
                    display: none;
                    width: 100%;
                    box-sizing: border-box;
                    padding-bottom: 5px;
                }}
                .collapsible-content.active {{
                    display: block;
                }}
                .back {{
                    display: block;
                    text-align: center;
                    font-size: 1em;
                    text-decoration: none;
                    background: #0078D4;
                    color: white;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin: 30px auto 20px auto;
                    width: 200px;
                }}
                .back:hover {{
                    background-color: #005ea6;
                }}
                .no-data-msg {{
                    text-align: center;
                    color: #555;
                    font-style: italic;
                    margin-top: 10px;
                    padding: 10px;
                    border: 1px dashed #ccc;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                @media (max-width: 600px) {{
                    .header-title {{
                        font-size: 1.3em;
                    }}
                    main {{
                        padding: 10px;
                    }}
                    h2 {{
                        font-size: 1.2em;
                        padding: 8px 0;
                    }}
                    .main-stats li {{
                        font-size: 1em;
                    }}
                    .category-item {{
                        padding: 8px;
                    }}
                    .category-summary {{
                        flex-wrap: wrap;
                    }}
                    .category-name {{
                        white-space: normal;
                        overflow: visible;
                        text-overflow: clip;
                    }}
                    .category-total {{
                        width: auto;
                        text-align: right;
                    }}
                    .category-arrow-button {{
                        margin-right: 0;
                    }}
                    ul.category-details {{
                        padding: 8px 10px;
                        font-size: 0.85em;
                    }}
                    ul.category-details .detail-item {{
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-between;
                        align-items: baseline;
                    }}
                    .detail-text {{
                        flex-grow: 1;
                        flex-shrink: 1;
                        min-width: 0;
                        padding-right: 5px;
                    }}
                    .detail-amount {{
                        flex-shrink: 0;
                        margin-left: auto;
                        text-align: right;
                    }}

                    ul.category-details li {{
                        padding-left: 15px;
                    }}
                    .section-toggle-button {{
                        font-size: 1em;
                        padding: 10px;
                    }}
                    .back {{
                        width: 180px;
                        padding: 10px;
                    }}
                }}
            </style>
            <script>
                function toggleMenu() {{
                    const menu = document.getElementById("extraMenu");
                    menu.style.display = (menu.style.display === "block") ? "none" : "block";
                }}
                document.addEventListener("click", function(event) {{
                    const menu = document.getElementById("extraMenu");
                    const isClickInside = event.target.closest(".menu-button, #extraMenu");
                    if (!isClickInside) {{
                        menu.style.display = "none";
                    }}
                }});
                function toggleVisibility(contentId, buttonElement) {{
                    const content = document.getElementById(contentId);
                    const arrow = buttonElement.querySelector('.category-arrow') || buttonElement.querySelector('.arrow');
                    let isExpanded = false;
                    if (content.classList.contains('collapsible-content')) {{
                        isExpanded = content.classList.contains('active');
                    }} else {{
                        isExpanded = !content.classList.contains('hidden');
                    }}
                    if (isExpanded) {{
                        if (content.classList.contains('collapsible-content')) {{
                            content.classList.remove('active');
                        }} else {{
                            content.classList.add('hidden');
                        }}
                        if (arrow) arrow.classList.remove('rotated');
                        buttonElement.setAttribute('aria-expanded', 'false');
                    }} else {{
                        if (content.classList.contains('collapsible-content')) {{
                            content.classList.add('active');
                        }} else {{
                            content.classList.remove('hidden');
                        }}
                        if (arrow) arrow.classList.add('rotated');
                        buttonElement.setAttribute('aria-expanded', 'true');
                    }}
                }}
            </script>
        </head>
        <body>
            <header>
                <button class="menu-button" onclick="toggleMenu()">☰</button>
                <div id="extraMenu" class="dropdown">
                    <a href="/">🏠 Torna alla Home</a>
                    <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
                    <a href="/lista">📈 Elenca/Modifica</a>
                    <a href="/stats">📊 Report Mese</a>
                    <a href="/report_annuo">📅 Report Annuale</a>
                    <a href="/menu_esplora">🔍 Esplora</a>
                    <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
                    <a href="/utenze?anno={datetime.date.today().year}">💧 Utenze</a>
                    <a href="/logoff">🔓 Logout</a>
                </div>
                <div class="header-title">📊 Report del Mese</div>
            </header>
            <main>
                <h2>📊 Statistiche di {titolo_mese}</h2>
                <ul class="main-stats">
                    <li><strong>Entrate Totali:</strong> <span class="income-color">€{entrate:.2f}</span></li>
                    <li><strong>Uscite Totali:</strong> <span class="expense-color">€{uscite:.2f}</span></li>
                    <li><strong style="color:{saldo_colore};">Saldo:</strong> <span style="color:{saldo_colore};">€{saldo:.2f}</span></li>
                </ul>
                <button type="button" class="section-toggle-button" onclick="toggleVisibility('usciteCategorieContent', this)" aria-expanded="false" aria-controls="usciteCategorieContent">
                    <span>🧮 Uscite per Categoria</span>
                    <span class="arrow">▶️</span>
                </button>
                <div id="usciteCategorieContent" class="collapsible-content">
                    {categorie_uscite_html}
                </div>
                <button type="button" class="section-toggle-button" onclick="toggleVisibility('entrateCategorieContent', this)" aria-expanded="false" aria-controls="entrateCategorieContent">
                    <span>📥 Entrate per Categoria</span>
                    <span class="arrow">▶️</span>
                </button>
                <div id="entrateCategorieContent" class="collapsible-content">
                    {categorie_entrate_html}
                </div>
                <a href="/" class="back">🏠 Torna alla Home</a>
            </main>
        </body>
        </html>
        """

    def html_lista_spese_mensili(self):
        mesi_it = {
            "January": "gennaio", "February": "febbraio", "March": "marzo",
            "April": "aprile", "May": "maggio", "June": "giugno",
            "July": "luglio", "August": "agosto", "September": "settembre",
            "October": "ottobre", "November": "novembre", "December": "dicembre"
        }
        oggi = datetime.date.today()
        mese_en = oggi.strftime('%B')
        mese_it_corrente = mesi_it.get(mese_en, mese_en)
        titolo_mese = f"{mese_it_corrente.capitalize()} {oggi.year}"
        current_month_expenses = []
        for d, voci in self.spese.items():
            if d.month == oggi.month and d.year == oggi.year:
                for idx, voce in enumerate(voci):
                    current_month_expenses.append((d, idx, voce))
        current_month_expenses.sort(key=lambda x: x[0], reverse=True)
        if not current_month_expenses:
            schede_html = "<p class='no-data-msg'>Nessuna spesa registrata per questo mese.</p>"
        else:
            schede_html = ""
            for d, idx, voce in current_month_expenses:
                categoria, descrizione, importo, tipo = voce[:4]
                data_str = d.strftime('%d-%m-%Y')
                details_id = f"details_{d.strftime('%Y%m%d')}_{idx}"
                colore_importo = "#228B22" if tipo.strip().lower() == "entrata" else "#c43b2e"
                segno = "+" if tipo.strip().lower() == "entrata" else "-"
                schede_html += f"""
                <div class="expense-item">
                    <div class="expense-summary" onclick="toggleVisibility('{details_id}', this)">
                        <span class="arrow">▶️</span>
                        <span class="date">{data_str}</span>
                        <span class="cat">{categoria}</span>
                        <span class="amount" style="color:{colore_importo};">{segno}€{importo:.2f}</span>
                    </div>
                    <div id="{details_id}" class="collapsible-content expense-actions">
                        <div class="row-detail">
                            <span class="label">Tipo:</span>
                            <span>{tipo}</span>
                        </div>
                        <div class="row-detail">
                            <span class="label">Descrizione:</span>
                            <span>{descrizione}</span>
                        </div>
                        <div class="row-detail actions">
                            <form method="get" action="/modifica">
                                <input type="hidden" name="data" value="{data_str}">
                                <input type="hidden" name="idx" value="{idx}">
                                <button type="submit" class="details-button">✏️ Modifica</button>
                            </form>
                            <form onsubmit="
                                event.preventDefault();
                                fetch('/cancella', {{
                                    method: 'POST',
                                    headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                                    body: 'data={data_str}&idx={idx}'
                                }}).then(function() {{
                                    window.location.href='/lista';
                                }});
                            ">
                                <button type="submit" class="details-button danger">❌ Cancella</button>
                            </form>
                        </div>
                    </div>
                </div>
                """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>📈 Spese — {titolo_mese}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                header {{
                    background: #0078D4;
                    color: white;
                    padding: 20px 0;
                    position: relative;
                }}
                .header-title {{
                    text-align: center;
                    font-size: 1.5em;
                }}
                .menu-button {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    font-size: 1.6em;
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                }}
                .dropdown {{
                    position: absolute;
                    top: 45px;
                    left: 10px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                    border-radius: 4px;
                    display: none;
                    z-index: 999;
                }}
                .dropdown a {{
                    display: block;
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #0078D4;
                    font-weight: bold;
                }}
                .dropdown a:hover {{
                    background-color: #f0f0f0;
                }}
                main {{
                    padding: 15px;
                    max-width: 700px;
                    margin: auto;
                }}
                h2 {{
                    color: #333;
                    text-align: center;
                    font-size: 1.4em;
                    margin-bottom: 15px;
                    padding: 10px 0;
                    background-color: #e9e9e9;
                    border-radius: 6px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                }}
                .expense-item {{
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(0,0,0,0.1);
                    margin-bottom: 13px;
                    overflow: hidden;
                    transition: box-shadow 0.2s;
                    padding-bottom: 0;
                }}
                .expense-summary {{
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    width: 100%;
                    cursor: pointer;
                    padding: 13px 12px 8px 0px;
                    background: #f9f9f9;
                    position: relative;
                    transition: background 0.2s;
                    border-bottom: 1px solid #e5e5e5;
                    gap: 10px;
                }}
                .expense-summary:hover {{
                    background: #edf7fd;
                }}
                .arrow {{
                    flex-shrink: 0;
                    width: 22px;
                    height: 22px;
                    display: inline-block;
                    vertical-align: middle;
                    transition: transform 0.3s ease;
                    font-size: 1em;
                    margin-right: 5px;
                }}
                .date {{
                    color: #888;
                    font-size: 1.04em;
                    white-space: nowrap;
                    flex-shrink: 0;
                    margin-right: 12px;
                }}
                .cat {{
                    font-weight: bold;
                    color: #0078D4;
                    font-size: 1.09em;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    flex: 1 1 0;
                    min-width: 0;
                    margin-right: 12px;
                    max-width: 170px;
                }}
                .amount {{
                    font-weight: bold;
                    font-size: 1.09em;
                    white-space: nowrap;
                    flex-shrink: 0;
                    margin-left: auto;
                    text-align: right;
                    min-width: 100px;
                }}
                .expense-summary[aria-expanded="true"] .arrow,
                .expense-summary .arrow.rotated {{
                    transform: rotate(90deg);
                }}
                .collapsible-content {{
                    display: none;
                    width: 100%;
                    box-sizing: border-box;
                    background: #f0f0f0;
                    padding: 10px 15px;
                    border-top: 1px solid #e0e0e0;
                    animation: fadeIn 0.4s;
                }}
                .collapsible-content.active {{
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                }}
                .row-detail {{
                    display: flex;
                    gap: 7px;
                    align-items: center;
                    font-size: 1em;
                    margin-bottom: 3px;
                }}
                .row-detail .label {{
                    font-weight: 600;
                    color: #0078D4;
                    min-width: 90px;
                }}
                .actions {{
                    gap: 12px;
                    margin-top: 7px;
                }}
                .details-button {{
                    font-size: 0.96em;
                    background: none;
                    border: 1px solid #0078D4;
                    color: #0078D4;
                    cursor: pointer;
                    padding: 6px 12px;
                    border-radius: 5px;
                    margin-right: 10px;
                    margin-bottom: 0;
                    white-space: nowrap;
                    transition: background 0.2s, color 0.2s;
                }}
                .details-button:hover {{
                    background: #0078D4;
                    color: white;
                }}
                .details-button.danger {{
                    border-color: #c43b2e;
                    color: #c43b2e;
                }}
                .details-button.danger:hover {{
                    background: #c43b2e;
                    color: white;
                }}
                .no-data-msg {{
                    text-align: center;
                    color: #555;
                    font-style: italic;
                    margin-top: 10px;
                    padding: 10px;
                    border: 1px dashed #ccc;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .back {{
                    display: block;
                    text-align: center;
                    font-size: 1em;
                    text-decoration: none;
                    background: #0078D4;
                    color: white;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    margin: 30px auto 20px auto;
                    width: 200px;
                }}
                .back:hover {{
                    background-color: #005ea6;
                }}
                @media (max-width: 700px) {{
                    main {{
                        max-width: 97vw;
                    }}
                    .cat {{
                        font-size: 1em;
                        max-width: 110px;
                    }}
                    .amount {{
                        min-width: 90px;
                    }}
                }}
                @media (max-width: 600px) {{
                    .header-title {{
                        font-size: 1.2em;
                    }}
                    main {{
                        padding: 5px;
                    }}
                    h2 {{
                        font-size: 1em;
                        padding: 6px 0;
                    }}
                    .expense-summary {{
                        gap: 7px;
                        padding: 11px 8px 6px 0px;
                    }}
                    .cat {{
                        font-size: 1em;
                        max-width: 130px;
                    }}
                    .amount {{
                        font-size: 0.98em;
                        min-width: 76px;
                    }}
                    .arrow {{
                        margin-right: 3px;
                    }}
                    .collapsible-content {{
                        gap: 8px;
                        padding: 8px 7px;
                    }}
                    .back {{
                        width: 95%;
                    }}
                }}
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
            </style>
            <script>
                function toggleMenu() {{
                    const menu = document.getElementById("extraMenu");
                    menu.style.display = (menu.style.display === "block") ? "none" : "block";
                }}
                document.addEventListener("click", function(event) {{
                    const menu = document.getElementById("extraMenu");
                    const isClickInside = event.target.closest(".menu-button, #extraMenu");
                    if (!isClickInside) {{
                        menu.style.display = "none";
                    }}
                }});
                function toggleVisibility(contentId, summaryElem) {{
                    var content = document.getElementById(contentId);
                    var arrow = summaryElem.querySelector('.arrow');
                    var expanded = content.classList.contains('active');
                    if (expanded) {{
                        content.classList.remove('active');
                        arrow.classList.remove('rotated');
                        summaryElem.setAttribute('aria-expanded', 'false');
                    }} else {{
                        content.classList.add('active');
                        arrow.classList.add('rotated');
                        summaryElem.setAttribute('aria-expanded', 'true');
                    }}
                }}
            </script>
        </head>
        <body>
            <header>
                <button class="menu-button" onclick="toggleMenu()">☰</button>
                <div id="extraMenu" class="dropdown">
                    <a href="/">🏠 Torna alla Home</a>
                    <a href="/consultazione_supermercati">🛒 Gestione Supermercati</a>
                    <a href="/lista">📈 Elenca/Modifica</a>
                    <a href="/stats">📊 Report Mese</a>
                    <a href="/report_annuo">📅 Report Annuale</a>
                    <a href="/menu_esplora">🔍 Esplora</a>
                    <a href="/gestione_categorie">⚙️ Gestione Categorie</a>
                    <a href="/utenze?anno={datetime.date.today().year}">💧 Utenze</a>
                    <a href="/logoff">🔓 Logout</a>
                </div>
                <div class="header-title">📈 Spese di {titolo_mese}</div>
            </header>
            <main>
                <h2>📈 Elenco Spese di {titolo_mese}</h2>
                {schede_html}
                <a href="/" class="back">🏠 Torna alla Home</a>
            </main>
        </body>
        </html>
        """

    def modifica_voce_form(self, params):
        from datetime import datetime
        data = params.get("data", [""])[0]
        idx = int(params.get("idx", ["0"])[0])
        d_obj = datetime.strptime(data, "%d-%m-%Y").date()
        voce = self.spese[d_obj][idx]
        categoria_corrente, descrizione, importo, tipo = voce[:4]

        categorie_options = "\n".join(
            f"<option value='{c}' {'selected' if c == categoria_corrente else ''}>{c}</option>"
            for c in sorted(self.categorie)
        )
        return f"""
        <html><head><meta charset="utf-8"><title>Modifica</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Segoe UI, sans-serif;
                padding: 20px;
                background: #f4f4f4;
                margin: 0;
            }}
            .container {{
                max-width: 500px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 8px rgba(0,0,0,0.1);
            }}
            label {{
                display: block;
                margin: 12px 0 4px;
                font-weight: bold;
            }}
            input, select {{
                width: 100%;
                padding: 8px;
                font-size: 1em;
                margin-bottom: 12px;
                box-sizing: border-box;
            }}
            button {{
                background: #0078D4;
                color: white;
                border: none;
                padding: 10px;
                font-size: 1em;
                border-radius: 6px;
                width: 100%;
            }}
            a {{
                display: block;
                margin-top: 20px;
                text-align: center;
                text-decoration: none;
                color: #0078D4;
            }}
        </style>
        </head>
        <body>
            <div class="container">
                <h2 style="text-align:center;">✏️ Modifica voce del {data}</h2>
                <form method="post" action="/salva_modifica">
                    <input type="hidden" name="data" value="{data}">
                    <input type="hidden" name="idx" value="{idx}">
                    <label for="categoria">Categoria</label>
                    <select name="categoria" required>
                        {categorie_options}
                    </select>
                    <label for="descrizione">Descrizione</label>
                    <input name="descrizione" value="{descrizione}">
                    <label for="importo">Importo (€)</label>
                    <input name="importo" type="number" step="0.01" min="0.01" value="{importo}" required>
                    <label for="tipo">Tipo</label>
                    <select name="tipo">
                        <option value="Entrata" {"selected" if tipo == "Entrata" else ""}>Entrata</option>
                        <option value="Uscita" {"selected" if tipo != "Entrata" else ""}>Uscita</option>
                    </select>
                    <button type="submit">💾 Salva</button>
                </form>
                <a href="/lista" style="background:#0078D4;color:#fff;padding:10px;border-radius:6px;text-align:center;display:block;text-decoration:none;">🔙 Torna alla lista</a>
            </div>
        </body></html>
        """

    def salva_modifica_voce(self, params):
        from datetime import datetime
        data = params.get("data", [""])[0]
        idx = int(params.get("idx", ["0"])[0])
        cat = params.get("categoria", [""])[0]
        descr = params.get("descrizione", [""])[0]
        imp = float(params.get("importo", ["0"])[0])
        tipo = params.get("tipo", ["Uscita"])[0]
        d_obj = datetime.strptime(data, "%d-%m-%Y").date()

        originale = self.spese[d_obj][idx]  
        nuova_voce = [cat, descr, imp, tipo]
        if len(originale) > 4:
            nuova_voce.append(originale[4])
        self.spese[d_obj][idx] = nuova_voce
        self.save_db()
        self.carica_db_web()
        self.refresh_gui() 
        
    def cancella_voce_web(self, data_str, idx):
        try:
            d_obj = datetime.datetime.strptime(data_str, "%d-%m-%Y").date()
        except Exception as e:
            print(f"❌ Data non valida: {data_str} → {e}")
            return

        if d_obj not in self.spese or idx >= len(self.spese[d_obj]):
            print(f"❌ Voce non trovata per cancellazione")
            return
        voce_eliminata = self.spese[d_obj].pop(idx)
        print(f"🗑️ Voce eliminata:", voce_eliminata)
        self.save_db()
        self.carica_db_web()
        self.refresh_gui()

    def aggiungi_voce_web(self, voce):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                dati = json.load(f)
        except Exception:
            dati = {"spese": []}
        try:
            d_obj = datetime.datetime.strptime(voce["date"], "%Y-%m-%d").date()
            data_str = d_obj.strftime("%d-%m-%Y")
            voce["date"] = data_str  
        except Exception as e:
            print(f"❌ Data non valida: {voce['date']} → {e}")
            return
        for giorno in dati["spese"]:
            if giorno["date"] == data_str:
                giorno["entries"].append(voce)
                break
        else:
            dati["spese"].append({
                "date": data_str,
                "entries": [voce]
            })
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)
        self.carica_db_web()
        self.refresh_gui()
 
    def carica_db_web(self):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                dati = json.load(f)
        except Exception as e:
            print(f"❌ Errore lettura DB: {e}")
            return
        self.spese = {}
        for giorno in dati.get("spese", []):
            try:
                d = datetime.datetime.strptime(giorno["date"], "%d-%m-%Y").date()
                entries = []
                for e in giorno["entries"]:
                    voce = (
                        e.get("categoria", ""),
                        e.get("descrizione", ""),
                        float(e.get("importo", 0.0)),
                        e.get("tipo", "Uscita"),
                        *([e["id_ricorrenza"]] if "id_ricorrenza" in e else [])
                    )
                    entries.append(voce)
                self.spese[d] = entries
            except Exception as ex:
                print(f"⚠️ Errore parsing giorno {giorno.get('date')}: {ex}")

    def get_dati_entrate_uscite_json(self):
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        entrate_mensili = [0.0] * 12
        uscite_mensili = [0.0] * 12
        for data, entries in self.spese.items():
            if data.year == anno_corrente:
                mese_indice = data.month - 1  
                for entry in entries:
                    categoria = entry[0]
                    importo = entry[2]
                    tipo = self.categorie_tipi.get(categoria, 'Uscita') 
                    if tipo == 'Entrata':
                        entrate_mensili[mese_indice] += importo
                    else: 
                        uscite_mensili[mese_indice] += importo
        mesi = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
        
        dati = {
            'labels': mesi,
            'datasets': [
                {'label': 'Entrate (€)', 'data': entrate_mensili, 'borderColor': 'rgba(75, 192, 192, 1)', 'backgroundColor': 'rgba(75, 192, 192, 0.5)'},
                {'label': 'Uscite (€)', 'data': uscite_mensili, 'borderColor': 'rgba(255, 99, 132, 1)', 'backgroundColor': 'rgba(255, 99, 132, 0.5)'}
            ]
        }
        return json.dumps(dati)

    def get_dati_saldo_json(self):
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        saldo_mensile_netto = [0.0] * 12
        for data, entries in self.spese.items():
            if data.year == anno_corrente:
                mese_indice = data.month - 1
                for entry in entries:
                    categoria = entry[0]
                    importo = entry[2]
                    tipo = self.categorie_tipi.get(categoria, 'Uscita')
                    
                    if tipo == 'Entrata':
                        saldo_mensile_netto[mese_indice] += importo
                    else:
                        saldo_mensile_netto[mese_indice] -= importo
        saldo_progressivo = []
        saldo_accumulato = 0.0
        for saldo_netto in saldo_mensile_netto:
            saldo_accumulato += saldo_netto
            saldo_progressivo.append(round(saldo_accumulato, 2))
        mesi = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']
        dati = {
            'labels': mesi,
            'datasets': [{
                'label': 'Saldo Progressivo (€)',
                'data': saldo_progressivo,
                'fill': False,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.1
            }]
        }
        return json.dumps(dati)

    def get_dati_categorie_json(self):
        oggi = datetime.date.today()
        anno_corrente = oggi.year
        spese_per_categoria = {}
        for data, entries in self.spese.items():
            if data.year == anno_corrente:
                for entry in entries:
                    categoria = entry[0]
                    importo = entry[2]
                    tipo = self.categorie_tipi.get(categoria, 'Uscita')
                    if tipo == 'Uscita':
                        spese_per_categoria[categoria] = spese_per_categoria.get(categoria, 0.0) + importo
        labels = list(spese_per_categoria.keys())
        spese = [round(v, 2) for v in spese_per_categoria.values()]
        colori = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(labels))]
        dati = {
            'labels': labels,
            'datasets': [{
                'data': spese,
                'backgroundColor': colori,
                'hoverOffset': 4
            }]
        }
        return json.dumps(dati)

    def refresh_gui(self):
        self.update_stats()
        #self.aggiorna_combobox_categorie()
        self.update_totalizzatore_anno_corrente()
        self.update_totalizzatore_mese_corrente()
        self.update_spese_mese_corrente()
        self.colora_giorni_spese()

    def aggiorna_gui_da_db(self):
        self.spese = {}
        for giorno in self.db.get("spese", []):
            try:
                d = datetime.datetime.strptime(giorno["date"], "%d-%m-%Y").date()
                entries = []
                for e in giorno["entries"]:
                    voce = (
                        e.get("categoria", ""),
                        e.get("descrizione", ""),
                        float(e.get("importo", 0.0)),
                        e.get("tipo", "Uscita")
                    )
                    if "id_ricorrenza" in e:
                        voce += (e["id_ricorrenza"],)
                    entries.append(voce)
                self.spese[d] = entries
            except Exception as ex:
                print(f"⚠️ Errore parsing giorno: {giorno.get('date')} → {ex}")

    def save_db_web(self, db=None):
        if db is None:
            db = self.db
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
            print("💾 Database salvato correttamente.")
            self.aggiorna_gui_da_db()        
        except Exception as e:
            print("❌ Errore salvataggio DB:", e)

    def spesa_supermercato(self):
        filtro_supermercato_confronto_var = tk.StringVar(value="Tutti i supermercati")
        supermercato_destinazione_var = tk.StringVar(value="Seleziona Supermercato")
        try:
            from tkcalendar import DateEntry
        except ImportError:
            DateEntry = None
            if not hasattr(self, '_tkcalendar_warned'):
                print("AVVISO: Libreria 'tkcalendar' non trovata. La data dovrà essere inserita manualmente (gg/mm/aaaa).")
                self._tkcalendar_warned = True
        DEFAULT_SUPERMERCATI = ["Coop", "Dpiu", "Esselunga", "Eurospin", "Lidl", "Maurys"]
        SUPERMERCATI = []
        lista_spesa_data = defaultdict(lambda: {})
        campi_input_refs = {}
        dati_supermercati = {}
        ricerca_vars_crud = {}
        ricerca_var_confronto = tk.StringVar()
        supermercato_selezionato_var = tk.StringVar()
        if not hasattr(self, 'risultati_tv_ref'):
            self.risultati_tv_ref = None
        if hasattr(self, '_popup_spesa_active') and self._popup_spesa_active.winfo_exists():
            self._popup_spesa_active.lift()
            return

        def _carica_dati_interno():
            nonlocal SUPERMERCATI, dati_supermercati
            if not os.path.exists(DB_DIR):
                os.makedirs(DB_DIR, exist_ok=True)
            try:
                if not os.path.exists(SUPERMERCATI_DB) or os.stat(SUPERMERCATI_DB).st_size == 0:
                    dati = {s: [] for s in DEFAULT_SUPERMERCATI}
                    SUPERMERCATI = DEFAULT_SUPERMERCATI
                    dati_supermercati = dati
                    _salva_dati_interno(dati)
                    return
                else:
                    with open(SUPERMERCATI_DB, 'r') as f:
                        dati = json.load(f)
                        loaded_supermercati = [k for k, v in dati.items() if isinstance(v, list)]
                        loaded_supermercati.sort()
                        SUPERMERCATI = loaded_supermercati if loaded_supermercati else DEFAULT_SUPERMERCATI
                        dati_supermercati = {s: dati.get(s, []) for s in SUPERMERCATI}
            except (FileNotFoundError, json.JSONDecodeError):
                SUPERMERCATI = DEFAULT_SUPERMERCATI
                dati_supermercati = {s: [] for s in DEFAULT_SUPERMERCATI}

        def _salva_dati_interno(dati_da_salvare):
            try:
                with open(SUPERMERCATI_DB, 'w') as f:
                    dati_filtrati = {}
                    for s in SUPERMERCATI:
                        if s in dati_da_salvare and dati_da_salvare[s]:
                            lista_articoli = dati_da_salvare[s].copy()
                            lista_articoli.sort(key=lambda x: x['nome']) 
                            dati_filtrati[s] = lista_articoli
                        elif s in dati_da_salvare:
                            dati_filtrati[s] = []
                    json.dump(dati_filtrati, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Errore durante il salvataggio: {e}")

        def _svuota_campi(refs):
            refs['nome'].set(""); refs['descrizione'].set(""); refs['categoria'].set("")
            refs['prezzo'].set(""); refs['promo_attiva'].set(False); refs['prezzo_promo'].set("")
            refs['quantita'].set("");
            refs['data_scadenza'].set("")

        def _controlla_scadenza_promo():
            nonlocal dati_supermercati
            oggi = datetime.datetime.now().date()
            articoli_modificati = False

            for supermercato, articoli in dati_supermercati.items():
                for articolo in articoli:
                    if articolo.get("promo", False) and articolo.get("data_scadenza"):
                        data_scad_str = articolo["data_scadenza"].strip()
                        try:
                            data_scadenza = datetime.datetime.strptime(data_scad_str, '%d/%m/%Y').date()
                        except ValueError:
                            continue
                        if data_scadenza <= oggi:
                            articolo["promo"] = False
                            articolo["prezzo_promo"] = ""
                            articolo["data_scadenza"] = ""
                            articoli_modificati = True
            if articoli_modificati:
                _salva_dati_interno(dati_supermercati)
                if hasattr(self, 'show_custom_warning'):
                    self.show_custom_warning("Aggiornamento Automatico", "Sono state disattivate alcune promozioni scadute.")
                    
        def _sort_treeview(treeview, col, reverse):
            def convert_value(val):
                if isinstance(val, str):
                    val_clean = val.replace('€', '').replace(',', '.').strip()
                    try:
                        return float(val_clean)
                    except (ValueError, TypeError):
                        return str(val).lower()
                try:
                    return float(val)
                except:
                    return str(val).lower()
            is_hierarchical = treeview.cget('show') == 'tree headings' and col != '#0' and treeview.master.winfo_name() == 'frame_tv_lista'
            if is_hierarchical:
                for parent in treeview.get_children(''):
                    if treeview.tag_has('grand_total', parent): continue
                    children = treeview.get_children(parent)
                    data = [(treeview.set(child, col), child) for child in children if treeview.item(child, 'tags') != ('supermarket',)]
                    data.sort(key=lambda item: convert_value(item[0]), reverse=reverse)
                    for index, (val, child) in enumerate(data):
                        treeview.move(child, parent, index)
            else:
                data = [(treeview.set(child, col), child) for child in treeview.get_children('')]
                data.sort(key=lambda item: convert_value(item[0]), reverse=reverse)
                for index, (val, child) in enumerate(data):
                    treeview.move(child, '', index)
            treeview.heading(col, command=lambda _col=col, t=treeview: _sort_treeview(t, _col, not reverse))

        def _carica_treeview(treeview, supermercato, articoli_filtrati=None):
            treeview.delete(*treeview.get_children())
            articoli_iterabili = articoli_filtrati if articoli_filtrati is not None else dati_supermercati.get(supermercato, [])
            articoli_ordinati = sorted(articoli_iterabili, key=lambda x: x.get("nome", ""))
            for articolo in articoli_ordinati:
                try:
                    idx_originale = dati_supermercati[supermercato].index(articolo)
                except ValueError:
                    continue
                quantita = articolo.get("quantita", "")
                data_scadenza = articolo.get("data_scadenza", "")
                treeview.insert(
                    parent='',
                    index='end',
                    iid=f"{supermercato}_{idx_originale}", 
                    values=(
                        articolo.get("nome", ""),
                        articolo.get("descrizione", ""),
                        articolo.get("categoria", ""),
                        articolo.get("prezzo", ""),
                        "Sì" if articolo.get("promo", False) else "No",
                        articolo.get("prezzo_promo", ""),
                        quantita,
                        data_scadenza
                    )
                )

        def calcola_prezzo_minimo_globale(nome_articolo_cercato):
            minimo = float('inf')
            supermercato_migliore = None
            for nome_superm, articoli in dati_supermercati.items():
                for articolo in articoli:
                    if articolo.get('nome', '').lower() == nome_articolo_cercato.lower():
                        try:
                            prezzo_str = articolo.get('prezzo', '9999.0')
                            prezzo = float(prezzo_str.replace(',', '.'))
                        except (ValueError, TypeError):
                            continue
                        if prezzo < minimo:
                            minimo = prezzo
                            supermercato_migliore = nome_superm
            return minimo, supermercato_migliore

        def trova_dettagli_affare_migliore(nome_articolo, superm_migliore, prezzo_minimo):
            articoli_superm = dati_supermercati.get(superm_migliore, [])
            for articolo in articoli_superm:
                nome = articolo.get('nome', '').lower()
                qta_catalogo = articolo.get('qta_catalogo', '1PZ')
                prezzo_str = articolo.get('prezzo', '9999.0')
                try:
                    prezzo = float(prezzo_str.replace(',', '.'))
                except (ValueError, TypeError):
                    continue
                if nome == nome_articolo.lower() and prezzo == prezzo_minimo:
                    return {
                        'supermercato': superm_migliore,
                        'prezzo_un': prezzo,
                        'qta_catalogo': qta_catalogo 
                    }
            raise ValueError(f"Dettagli completi dell'affare non trovati per {nome_articolo}.")

        def _cerca_articoli_crud(supermercato, treeview, ricerca_var):
            testo_ricerca = ricerca_var.get().lower().strip()
            if not treeview: return
            if not testo_ricerca:
                _carica_treeview(treeview, supermercato, articoli_filtrati=None)
                return
            articoli_filtrati = []
            for articolo in dati_supermercati.get(supermercato, []):
                nome = articolo.get("nome", "").lower()
                categoria = articolo.get("categoria", "").lower()
                descrizione = articolo.get("descrizione", "").lower()
                if testo_ricerca in nome or testo_ricerca in categoria.lower() or testo_ricerca in descrizione:
                    articoli_filtrati.append(articolo)
            _carica_treeview(treeview, supermercato, articoli_filtrati=articoli_filtrati)
            
        def _funzione_crud(azione, supermercato, treeview, frame_input):
            if supermercato not in campi_input_refs: 
                self.show_custom_warning("Selezione", "Seleziona un supermercato prima di procedere."); return
            if not treeview: return
            refs = campi_input_refs.get(supermercato)
            if not refs:
                refs = campi_input_refs.get('combo_gestione_super')
            if not refs: return
            LIMITI_CARATTERI = {
                'nome': 27,
                'descrizione': 35,
                'categoria': 24,
                'quantita': 18,
                'prezzo': 7,
                'prezzo_promo': 7
            }
            
            def _valida_lunghezza_campi_locale(refs):
                errori = []
                prezzo = refs['prezzo'].get().strip()
                prezzo_promo = refs['prezzo_promo'].get().strip()
                data_scadenza = refs['data_scadenza'].get().strip()

                for key, max_len in LIMITI_CARATTERI.items():
                    if key in refs:
                        current_value = refs[key].get().strip()
                        if len(current_value) > max_len:
                            errori.append(
                                f"- Il campo '{key.upper()}' ha {len(current_value)} caratteri, "
                                f"ma il limite massimo è {max_len}. Per favore accorcia."
                            )
                campi_prezzo = {
                    'prezzo': prezzo,
                    'prezzo_promo': prezzo_promo
                }
                for key, value in campi_prezzo.items():
                    if value:
                        try:
                            float(value.replace(',', '.'))
                        except ValueError:
                            errori.append(f"- Il campo '{key.upper()}' ('{value}') deve essere un valore numerico valido (es. 10.50 o 10,50).")
                if data_scadenza:
                    formati_validi = ['%d/%m/%Y', '%d-%m-%Y']
                    data_valida = False
                    
                    for formato in formati_validi:
                        try:
                            datetime.datetime.strptime(data_scadenza, formato)
                            data_valida = True
                            break 
                        except ValueError:
                            continue
                    
                    if not data_valida:
                        errori.append(
                            f"- Il campo 'DATA SCADENZA' ('{data_scadenza}') non è nel formato richiesto (GG/MM/AAAA)."
                        )
                nome = refs['nome'].get().strip()
                descrizione = refs['descrizione'].get().strip()
                categoria = refs['categoria'].get().strip()
                quantita = refs['quantita'].get().strip()
                return errori, nome, descrizione, categoria, quantita, prezzo, prezzo_promo
            selezione = treeview.selection()
            azione_eseguita = False
            ricerca_var_locale = ricerca_vars_crud.get(supermercato, tk.StringVar())
            if azione == 'inserisci':
                errori, nome, descrizione, categoria, quantita, prezzo, prezzo_promo = _valida_lunghezza_campi_locale(refs)
                if errori:
                    errore_messaggio = "Impossibile inserire. Si sono verificati i seguenti errori:\n" + "\n".join(errori)
                    self.show_custom_warning("Errore di Validazione", errore_messaggio)
                    return
                promo_attiva = refs['promo_attiva'].get()
                data_scadenza = refs['data_scadenza'].get().strip()
                if not nome or not prezzo: self.show_custom_warning("Errore di Input", "Nome e Prezzo sono obbligatori."); return
                nuovo_articolo = {
                    "nome": nome, "descrizione": descrizione, "categoria": categoria,
                    "prezzo": prezzo,
                    "promo": promo_attiva,
                    "prezzo_promo": prezzo_promo,
                    "supermercato": supermercato,
                    "quantita": quantita,
                    "data_scadenza": data_scadenza
                }
                dati_supermercati[supermercato].append(nuovo_articolo)
                _svuota_campi(refs); _salva_dati_interno(dati_supermercati)
                _cerca_articoli_crud(supermercato, treeview, ricerca_var_locale)
                azione_eseguita = True
            elif azione == 'cancella':
                if not selezione: self.show_custom_warning("Selezione", "Selezionare un articolo da cancellare."); return
                if self.show_custom_askyesno("Conferma Cancellazione", "Sei sicuro di voler cancellare l'articolo selezionato?"):
                    iid_da_cancellare = selezione[0]
                    try: idx_cancellare = int(iid_da_cancellare.split('_')[-1])
                    except ValueError: self.show_custom_warning("Errore", "Impossibile identificare l'articolo da cancellare."); return
                    if 0 <= idx_cancellare < len(dati_supermercati[supermercato]):
                        dati_supermercati[supermercato].pop(idx_cancellare)
                        _svuota_campi(refs);
                        _salva_dati_interno(dati_supermercati)
                        _cerca_articoli_crud(supermercato, treeview, ricerca_var_locale)
                        azione_eseguita = True
            elif azione == 'modifica':
                if not selezione:
                    self.show_custom_warning("Selezione", "Selezionare **prima** un articolo per modificarlo."); return
                iid_selezionato = selezione[0]; valori_selezionati = treeview.item(iid_selezionato, 'values')
                refs['nome'].set(valori_selezionati[0]); refs['descrizione'].set(valori_selezionati[1])
                refs['categoria'].set(valori_selezionati[2]);
                refs['prezzo'].set(valori_selezionati[3])
                refs['promo_attiva'].set(True if valori_selezionati[4] == "Sì" else False)
                refs['prezzo_promo'].set(valori_selezionati[5])
                refs['quantita'].set(valori_selezionati[6] if len(valori_selezionati) > 6 else "")
                data_scadenza_str = valori_selezionati[7] if len(valori_selezionati) > 7 else ""
                refs['data_scadenza'].set(data_scadenza_str)
                popup.modifica_iid = iid_selezionato
            elif azione == 'salva':
                modifica_iid_ref = getattr(popup, 'modifica_iid', None)
                if not selezione or not modifica_iid_ref or modifica_iid_ref not in selezione:
                    self.show_custom_warning("Selezione/Stato", "Nessun articolo selezionato o lo stato di modifica non è attivo. Seleziona un articolo e premi 'Modifica', poi 'Salva'."); return
                errori, nome, descrizione, categoria, quantita, prezzo, prezzo_promo = _valida_lunghezza_campi_locale(refs)
                if errori:
                    errore_messaggio = "Impossibile salvare. Si sono verificati i seguenti errori:\n" + "\n".join(errori)
                    self.show_custom_warning("Errore di Validazione", errore_messaggio)
                    return
                promo_attiva = refs['promo_attiva'].get()
                data_scadenza = refs['data_scadenza'].get().strip()
                if not nome or not prezzo: self.show_custom_warning("Errore di Input", "Nome e Prezzo sono obbligatori per il salvataggio."); return
                if not promo_attiva:
                    data_scadenza = ""
                iid_da_salvare = selezione[0]
                try: idx_da_salvare = int(iid_da_salvare.split('_')[-1])
                except ValueError: self.show_custom_warning("Errore", "Impossibile identificare l'articolo da salvare."); return
                if 0 <= idx_da_salvare < len(dati_supermercati[supermercato]):
                    dati_supermercati[supermercato][idx_da_salvare] = {
                        "nome": nome, "descrizione": descrizione, "categoria": categoria,
                        "prezzo": prezzo,
                        "promo": promo_attiva,
                        "prezzo_promo": prezzo_promo,
                        "supermercato": supermercato,
                        "quantita": quantita,
                        "data_scadenza": data_scadenza
                    }
                    _salva_dati_interno(dati_supermercati); _svuota_campi(refs);
                    del popup.modifica_iid
                    _cerca_articoli_crud(supermercato, treeview, ricerca_var_locale)
                    azione_eseguita = True
            if azione_eseguita and self.risultati_tv_ref:
                _aggiorna_lista_spesa_intelligente(self.risultati_tv_ref)
        def _svuota_supermercato(supermercato, treeview):
            if not supermercato or supermercato == "Seleziona Supermercato":
                self.show_custom_warning("Selezione", "Seleziona un supermercato prima di svuotare."); return
            if self.show_custom_askyesno("Azzeramento Dati", f"⚠️ Sei sicuro di voler cancellare TUTTI gli articoli\n dal supermercato '{supermercato}'?"):
                dati_supermercati[supermercato] = []
                _salva_dati_interno(dati_supermercati)
                _carica_treeview(treeview, supermercato)
                if self.risultati_tv_ref:
                    _aggiorna_lista_spesa_intelligente(self.risultati_tv_ref)
                self.show_custom_warning("Successo", f"Database del supermercato '{supermercato}' azzerato.")

        def _cerca_articoli(testo_ricerca, tv_risultati):
            if not tv_risultati: return
            tv_risultati.delete(*tv_risultati.get_children())
            testo_ricerca = testo_ricerca.lower().strip()
            articoli_da_mostrare = []
            filtro_superm_selezionato = filtro_supermercato_confronto_var.get()
            if filtro_superm_selezionato == "Tutti i supermercati" or filtro_superm_selezionato == "Seleziona Supermercato":
                supermercati_da_cercare = dati_supermercati.keys()
                cerca_il_piu_conveniente = True
            else:
                supermercati_da_cercare = [filtro_superm_selezionato]
                cerca_il_piu_conveniente = False
            for supermercato in supermercati_da_cercare:
                if supermercato not in dati_supermercati: continue
                articoli = dati_supermercati[supermercato]
                for articolo in articoli:
                    nome = articolo.get("nome", "").strip()
                    categoria = articolo.get("categoria", "").strip()
                    descrizione = articolo.get("descrizione", "").strip()
                    if testo_ricerca and not (testo_ricerca in nome.lower() or testo_ricerca in categoria.lower() or testo_ricerca in descrizione.lower()):
                        continue
                    prezzo_effettivo = articolo.get("prezzo_promo") if articolo.get("promo") and articolo.get("prezzo_promo") else articolo.get("prezzo")
                    if not prezzo_effettivo: continue
                    try:
                        prezzo = float(str(prezzo_effettivo).replace(',', '.'))
                        articoli_da_mostrare.append({
                            "nome": nome,
                            "quantita": articolo.get("quantita", ""),
                            "supermercato": supermercato,
                            "descrizione": descrizione,
                            "categoria": categoria,
                            "prezzo_float": prezzo,
                            "prezzo_formattato": f"€ {prezzo:.2f}",
                            "dettagli": "Promo" if articolo.get("promo") else ""
                        })
                    except (ValueError, TypeError):
                        continue
            articoli_raggruppati_per_nome = defaultdict(list)
            for offerta in articoli_da_mostrare:
                chiave = (offerta['nome'].lower(), offerta['quantita'].lower())
                articoli_raggruppati_per_nome[chiave].append(offerta)
            tutti_gli_articoli_ordinati = sorted(articoli_da_mostrare, key=lambda x: x['nome'])
            articoli_inseriti_set = set()
            for offerta in tutti_gli_articoli_ordinati:
                chiave_comparazione = (offerta['nome'].lower(), offerta['quantita'].lower())
                iid_val = f"{offerta['nome']}|{offerta['quantita']}|{offerta['supermercato']}|{offerta['prezzo_float']}"
                if iid_val in articoli_inseriti_set: continue
                articoli_inseriti_set.add(iid_val)
                indicatore = ""
                if cerca_il_piu_conveniente:
                    prezzi_simili = [o['prezzo_float'] for o in articoli_raggruppati_per_nome.get(chiave_comparazione, [])]
                    min_price = min(prezzi_simili) if prezzi_simili else float('inf')
                    is_min_price = (offerta['prezzo_float'] == min_price)
                    count_min_price = sum(1 for p in prezzi_simili if p == min_price)
                    is_strictly_cheaper = (is_min_price and count_min_price < len(prezzi_simili))
                    
                    if is_strictly_cheaper:
                        indicatore = "⭐ Più conveniente"
                if offerta['dettagli']:
                    indicatore = f"{offerta['dettagli']} {indicatore}".strip()
                tv_risultati.insert(
                    parent='', index='end', iid=iid_val,
                    values=(
                        offerta["nome"], offerta["quantita"], offerta["supermercato"],
                        offerta["descrizione"], offerta["categoria"],
                        offerta["prezzo_formattato"], indicatore
                    )
                )

        def _ricarica_lista_spesa(tv_lista):
            tv_lista.delete(*tv_lista.get_children())
            totale_generale = 0.0
            gruppi_supermercati = defaultdict(lambda: [])
            for chiave, dati in lista_spesa_data.items():
                gruppi_supermercati[dati['supermercato']].append(dati)
            for superm in sorted(gruppi_supermercati.keys()):
                articoli = gruppi_supermercati[superm]
                articoli.sort(key=lambda x: x['nome'])
                totale_super = 0.0
                iid_super = f"group_{superm}"
                tv_lista.insert('', 'end', iid=iid_super, text=f"🛒 {superm}", tags=('supermarket',))
                for dati in articoli:
                    totale_articolo = dati['qta_int'] * dati['prezzo_un']
                    totale_super += totale_articolo
                    chiave_lista = f"{dati['nome']}|{superm}"
                    iid_articolo = f"item_{chiave_lista}"
                    tv_lista.insert(
                        iid_super, 'end', iid=iid_articolo, text=dati['nome'],
                        values=(dati['qta_catalogo'], dati['qta_int'], f"{dati['prezzo_un']:.2f}",
                                f"{totale_articolo:.2f}", dati['supermercato'])
                    )
                tv_lista.item(iid_super, values=("", "", "TOTALE PARZIALE:", f"{totale_super:.2f}", ""), tags=('supermarket',))
                totale_generale += totale_super
            tv_lista.insert('', 'end', text="TOTALE GENERALE SPESA:", values=("", "", "", f"{totale_generale:.2f}", ""), tags=('grand_total',))
            tv_lista.tag_configure('grand_total', font=('Arial', 10, 'bold'), background='#E0F7FA')
            tv_lista.tag_configure('supermarket', font=('Arial', 10, 'bold'), foreground='blue')

        def _aggiungi_a_lista_spesa(event, tv_lista, tv_risultati_ref):
            def mostra_avviso_conferma(title, message):
                TIMEOUT_MS = 10000
                risultato = {"value": 'ANNULLA'}
                dialog = tk.Toplevel(tv_risultati_ref.winfo_toplevel(), bg="orange") 
                dialog.withdraw()
                dialog.title(title)
                dialog.resizable(False, False)
                dialog.attributes("-topmost", True)
                dialog.update_idletasks()
                w, h = 480, 160
                x = dialog.winfo_screenwidth() // 2 - w // 2
                y = dialog.winfo_screenheight() // 2 - h // 2
                dialog.geometry(f"{w}x{h}+{x}+{y}")
                dialog.deiconify()
                label = tk.Label(dialog, text=message, font=("Arial", 10), justify="left", padx=16, pady=12, bg="orange")
                label.pack()
                btns = tk.Frame(dialog, bg="orange")
                btns.pack(pady=(0,10))
                def aggiungi_selezionato():
                    risultato["value"] = 'SELEZIONATO'
                    dialog.destroy()                
                def aggiungi_migliore():
                    risultato["value"] = 'MIGLIORE'
                    dialog.destroy()
                def annulla():
                    risultato["value"] = 'ANNULLA'
                    dialog.destroy()
                dialog.bind('<Escape>', lambda e: annulla())
                b1 = ttk.Button(btns, text="Aggiungi Selezionato", style="Rosso.TButton", command=aggiungi_selezionato)
                b2 = ttk.Button(btns, text="Aggiungi Affare Migliore", style="Verde.TButton", command=aggiungi_migliore)
                b3 = ttk.Button(btns, text="Annulla", style="Giallo.TButton", command=annulla) 
                b1.grid(row=0, column=0, padx=8)
                b2.grid(row=0, column=1, padx=8)
                b3.grid(row=0, column=2, padx=8)
                dialog.focus_set()
                dialog.grab_set()
                if TIMEOUT_MS > 0:
                    dialog.after(TIMEOUT_MS, annulla)
                dialog.wait_window()
                try:
                    while dialog.winfo_exists():
                        dialog.update()
                except tk.TclError:
                    pass
                return risultato["value"]
            selezione = tv_risultati_ref.selection()
            if not selezione: return
            iid_selezionato = selezione[0]
            try:
                nome, qta_catalogo_base, superm_base, prezzo_str_base = iid_selezionato.split('|')
                prezzo_float_base = float(prezzo_str_base)
                nome = nome.strip()
            except ValueError:
                return
            prezzo_minimo, superm_migliore = calcola_prezzo_minimo_globale(nome)
            azione_richiesta = 'SELEZIONATO'
            if prezzo_minimo < prezzo_float_base and superm_migliore != superm_base:
                titolo_custom = "🚨 CONVIENE ALTROVE! 🚨"
                messaggio_custom = (
                    f"L'articolo '{nome.upper()}' costa {prezzo_float_base:.2f} da {superm_base}.\n\n"
                    f"Trovato a **{prezzo_minimo:.2f} presso {superm_migliore}**."
                    f"\n\nQuale articolo vuoi aggiungere alla lista?"
                )
                azione_richiesta = mostra_avviso_conferma(titolo_custom, messaggio_custom)
            if azione_richiesta == 'ANNULLA':
                 return
            superm_finale = superm_base
            prezzo_float_finale = prezzo_float_base
            qta_catalogo_finale = qta_catalogo_base
            if azione_richiesta == 'MIGLIORE':
                 try:
                     dettagli_migliore = trova_dettagli_affare_migliore(nome, superm_migliore, prezzo_minimo)
                     superm_finale = dettagli_migliore['supermercato']
                     prezzo_float_finale = dettagli_migliore['prezzo_un']
                     qta_catalogo_finale = dettagli_migliore['qta_catalogo']
                     
                 except Exception as e:
                     errore_dialog = tk.Toplevel(tv_risultati_ref.winfo_toplevel(), bg="yellow")
                     errore_dialog.title("Errore Dati Critico")
                     tk.Label(errore_dialog, text=f"ERRORE: Impossibile recuperare i dettagli dell'affare migliore.\n{e}", fg="red", bg="yellow").pack(padx=15, pady=10)
                     ttk.Button(errore_dialog, text="OK", command=errore_dialog.destroy).pack(pady=5)
                     errore_dialog.grab_set()
                     return 
            chiave_lista = f"{nome}|{superm_finale}"
            nuova_quantita_int = lista_spesa_data[chiave_lista]['qta_int'] + 1 if chiave_lista in lista_spesa_data else 1
            lista_spesa_data[chiave_lista] = {
                'nome': nome, 
                'qta_catalogo': qta_catalogo_finale, 
                'qta_int': nuova_quantita_int,
                'prezzo_un': prezzo_float_finale, 
                'supermercato': superm_finale
            }
            _ricarica_lista_spesa(tv_lista)

        def _rimuovi_articolo_da_lista(tv_lista):
            selezione = tv_lista.selection()
            if not selezione: return
            iid_selezionato = selezione[0]
            if iid_selezionato.startswith('item_'):
                try: chiave_lista = iid_selezionato.split('item_')[1]
                except IndexError: return
                if chiave_lista in lista_spesa_data:
                    del lista_spesa_data[chiave_lista]
                    _ricarica_lista_spesa(tv_lista)
            elif iid_selezionato.startswith('group_'):
                if self.show_custom_askyesno("Conferma", "Sei sicuro di voler rimuovere tutti gli articoli\n di questo supermercato dalla lista?"):
                    superm = iid_selezionato.split('group_')[1]
                    chiavi_da_rimuovere = [k for k, v in lista_spesa_data.items() if v['supermercato'] == superm]
                    for chiave in chiavi_da_rimuovere: del lista_spesa_data[chiave]
                    _ricarica_lista_spesa(tv_lista)

        def _svuota_lista_spesa(tv_lista):
            if self.show_custom_askyesno("Conferma", "Sei sicuro di voler rimuovere TUTTI gli articoli\n dalla lista spesa?"):
                tv_lista.delete(*tv_lista.get_children())
                lista_spesa_data.clear()
                _ricarica_lista_spesa(tv_lista)

        def _on_edit_quantity(event, tv_lista):
            region = tv_lista.identify("region", event.x, event.y)
            col = tv_lista.identify_column(event.x)
            
            if region == "cell" and col == "#2":
                row_id = tv_lista.identify_row(event.y)
                if not row_id.startswith('item_'): return
                try: chiave_lista = row_id.split('item_')[1]
                except: return
                if chiave_lista not in lista_spesa_data: return
                current_value = tv_lista.item(row_id)['values'][1]
                entry_editor = ttk.Entry(tv_lista, width=10)
                entry_editor.insert(0, str(current_value))
                x, y, width, height = tv_lista.bbox(row_id, col)
                entry_editor.place(x=x, y=y, width=width, height=height)
                entry_editor.focus_set()

                def on_entry_confirm(e):
                    try:
                        new_qta = int(entry_editor.get().strip())
                        if new_qta > 0:
                            lista_spesa_data[chiave_lista]['qta_int'] = new_qta
                            _ricarica_lista_spesa(tv_lista)
                        elif new_qta == 0:
                            del lista_spesa_data[chiave_lista]
                            _ricarica_lista_spesa(tv_lista)
                    except ValueError:
                        self.show_custom_warning("Errore", "La quantità deve essere un numero intero valido.")
                    finally:
                        entry_editor.destroy()
                entry_editor.bind('<Return>', on_entry_confirm)
                entry_editor.bind('<FocusOut>', on_entry_confirm)

        def _genera_testo_esportazione():
            import datetime
            data_esportazione = datetime.datetime.now().strftime("%d/%m/%Y")
            WIDTH_NOME = 45
            WIDTH_QTA = 4
            WIDTH_PREZZO_BLOCCO = 30
            testo = f"CHECK-OUT: Spesa Ottimizzata ({data_esportazione})\n\n"
            totale_generale = 0.0
            gruppi_supermercati = defaultdict(lambda: [])
            for chiave, dati in lista_spesa_data.items(): gruppi_supermercati[dati['supermercato']].append(dati)
            for superm in sorted(gruppi_supermercati.keys()):
                articoli = gruppi_supermercati[superm]
                articoli.sort(key=lambda x: x['nome'])
                testo += f"[{superm.upper()}]\n"
                totale_super = 0.0
                for dati in articoli:
                    totale_articolo = dati['qta_int'] * dati['prezzo_un']
                    totale_super += totale_articolo
                    linea = "[ ] "
                    nome_completo = f"{dati['nome']} ({dati['qta_catalogo']})"
                    linea += f"{nome_completo:<{WIDTH_NOME}}"
                    qta_comprare = f"x {dati['qta_int']} pz"
                    linea += f"{qta_comprare:<{WIDTH_QTA + 4}}"
                    prezzo_blocco = f"(€ {dati['prezzo_un']:.2f}) - Tot: € {totale_articolo:.2f}"
                    linea += f"{prezzo_blocco:>{WIDTH_PREZZO_BLOCCO}}\n"
                    testo += linea
                testo += f"  TOTALE PARZIALE {superm}: € {totale_super:.2f}\n\n"
                totale_generale += totale_super
            testo += f"\n"
            testo += f"TOTALE GENERALE STIMATO: € {totale_generale:.2f}\n"
            return testo

        def _mostra_anteprima_esportazione():
            anteprima_text = _genera_testo_esportazione()
            preview_popup = tk.Toplevel(popup)
            preview_popup.title("Anteprima Esportazione Lista Spesa")
            preview_popup.geometry("1050x600")
            screen_width = preview_popup.winfo_screenwidth()
            screen_height = preview_popup.winfo_screenheight()
            x = (screen_width - 1050) // 2
            y = (screen_height - 600) // 2
            preview_popup.geometry(f"1050x600+{x}+{y}")
            preview_popup.after(10, lambda: preview_popup.focus_force())
            preview_popup.bind('<Escape>', lambda e: preview_popup.destroy())
            text_area = tk.Text(preview_popup, wrap='word', font=('Courier', 10), padx=10, pady=10)
            text_area.insert('1.0', anteprima_text)
            text_area.config(state='disabled')
            text_area.pack(fill='both', expand=True, padx=10, pady=10)
            frame_btn = ttk.Frame(preview_popup); frame_btn.pack(pady=(0, 10))
            ttk.Button(frame_btn, text="Chiudi", command=preview_popup.destroy, style='Giallo.TButton').pack(side='right', padx=5)
            ttk.Button(frame_btn, text="Esporta", style='Verde.TButton',
                        command=lambda: _esporta_su_file(anteprima_text, preview_popup)).pack(side='right', padx=5)

        def _esporta_su_file(content_text, preview_popup):
            preview_popup.destroy()
            now = datetime.date.today()
            default_filename = f"Lista_Spesa_{now.day:02d}_{now.month:02d}_{now.year}.txt"
            f = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("File txt", "*.txt")], title="Salva la Lista Spesa su File",
                initialdir=EXPORT_FILES, confirmoverwrite=False, initialfile=default_filename, parent=popup
            )
            if f:
                try:
                    with open(f, 'w', encoding='utf-8') as file_handle: file_handle.write(content_text)
                    self.show_custom_warning("Successo", f"✅ Lista spesa salvata con successo in:\n{f}")
                except Exception as e:
                    self.show_custom_warning("Errore", f"❌ Impossibile salvare il file:\n{e}")
            
        def _aggiorna_lista_spesa_intelligente(tv_risultati):
            if tv_risultati:
                _cerca_articoli(ricerca_var_confronto.get(), tv_risultati)
                
        def _on_supermercato_change(event, combo, treeview_crud, frame_input, ricerca_var):
            selected_superm = combo.get()
            if selected_superm == "Seleziona Supermercato":
                treeview_crud.delete(*treeview_crud.get_children())
                _svuota_campi(campi_input_refs.get('combo_gestione_super'))
                return
            if selected_superm not in campi_input_refs:
                refs = {
                    'nome': tk.StringVar(), 'descrizione': tk.StringVar(), 'categoria': tk.StringVar(),
                    'prezzo': tk.StringVar(), 'promo_attiva': tk.BooleanVar(), 'prezzo_promo': tk.StringVar(),
                    'quantita': tk.StringVar(), 'data_scadenza': tk.StringVar()
                }
                campi_input_refs[selected_superm] = refs
            refs_superm = campi_input_refs[selected_superm]
            refs_combo = campi_input_refs.get('combo_gestione_super')
            for key in refs_superm:
                refs_combo[key].set(refs_superm[key].get())
                refs_superm[key] = refs_combo[key]
            if selected_superm not in ricerca_vars_crud:
                ricerca_vars_crud[selected_superm] = tk.StringVar()
            ricerca_var.set(ricerca_vars_crud[selected_superm].get())
            _carica_treeview(treeview_crud, selected_superm)

        def _esegui_rinomina_supermercato(combo, treeview_crud, ricerca_var):
            nonlocal SUPERMERCATI, dati_supermercati, campi_input_refs
            old_superm = combo.get()
            if old_superm == "Seleziona Supermercato" or not old_superm:
                self.show_custom_warning("Modifica Supermercato", "Seleziona prima un supermercato da rinominare."); return
            input_popup = tk.Toplevel(popup)
            input_popup.title(f"Rinomina {old_superm}"); input_popup.transient(popup); input_popup.grab_set()
            ttk.Label(input_popup, text="Nuovo nome:").pack(padx=10, pady=(10, 0))
            new_name_var = tk.StringVar(value=old_superm)
            entry = ttk.Entry(input_popup, textvariable=new_name_var, width=30); entry.pack(padx=10, pady=5); entry.focus_set()
            
            def on_confirm(e=None):
                nonlocal SUPERMERCATI
                new_superm = new_name_var.get().strip(); input_popup.destroy()
                if not new_superm or new_superm == old_superm: return
                if new_superm in dati_supermercati:
                    self.show_custom_warning("Errore", f"Il supermercato '{new_superm}' esiste già."); return
                if old_superm in dati_supermercati:
                    articoli_da_aggiornare = dati_supermercati.pop(old_superm)
                    dati_supermercati[new_superm] = articoli_da_aggiornare
                    for articolo in dati_supermercati[new_superm]: articolo['supermercato'] = new_superm
                    try: 
                        index = SUPERMERCATI.index(old_superm)
                        SUPERMERCATI[index] = new_superm
                    except ValueError: 
                        pass
                    if old_superm in campi_input_refs: campi_input_refs[new_superm] = campi_input_refs.pop(old_superm)
                    if old_superm in ricerca_vars_crud: ricerca_vars_crud[new_superm] = ricerca_vars_crud.pop(old_superm)
                    combo['values'] = tuple(["Seleziona Supermercato"] + sorted(SUPERMERCATI))
                    combo.set(new_superm)
                    _carica_treeview(treeview_crud, new_superm)
                    _salva_dati_interno(dati_supermercati)
                    if self.risultati_tv_ref: _aggiorna_lista_spesa_intelligente(self.risultati_tv_ref)
                    self.show_custom_warning("Successo", f"Supermercato '{old_superm}' rinominato in '{new_superm}'.")
                    
        def info_popup():
            popup = tk.Toplevel(frame_gestione, width=550) 
            popup.title("Informazioni sull'Importazione")
            popup.withdraw() 
            popup.transient(frame_gestione)
            messaggio = (
                "Questo programma gestisce i prezzi dei supermercati. 📊\n\n"
                
                "**Non è indispensabile inserire tutti i prezzi a mano.** \nIl database "
                "viene primariamente popolato tramite l'importazione degli scontrini digitali.\n\n"

                "Su richiesta, è disponibile un Plugin separato che analizza gli scontrini, "
                "estrae i nomi degli articoli, le categorie e i prezzi, e li archivia "
                "in automatico per permettere la consultazione e il confronto."
            )
            frame_contenuto = ttk.Frame(popup, padding="20")
            frame_contenuto.pack(expand=True, fill='both')
            ttk.Label(
                frame_contenuto, 
                text=messaggio, 
                wraplength=400,
                justify='left'
            ).pack(pady=10)
            ttk.Button(frame_contenuto, text="OK", command=popup.destroy, style="Giallo.TButton").pack(pady=10)
            frame_gestione.update_idletasks()
            popup.update_idletasks() 
            width = popup.winfo_width()
            height = popup.winfo_height()
            MIN_W = 450 
            MIN_H = 300
            if width < MIN_W or height < MIN_H:
                 width = max(width, MIN_W)
                 height = max(height, MIN_H)
            parent_x = frame_gestione.winfo_rootx() 
            parent_y = frame_gestione.winfo_rooty()
            parent_width = frame_gestione.winfo_width()
            parent_height = frame_gestione.winfo_height()
            x = parent_x + (parent_width // 2) - (width // 2)
            y = parent_y + (parent_height // 2) - (height // 2)
            popup.geometry(f'{width}x{height}+{x}+{y}') 
            popup.deiconify() 
            popup.grab_set() 
            popup.bind("<Escape>", lambda e: popup.destroy())
            
        def import_supermercati_db():
            popup.lift() 
            popup.focus_force() 
            SUPERMERCATI_DB = os.path.join(DB_DIR, "supermercati.json")
            file = filedialog.askopenfilename(
                parent=popup,
                title="Importa Database Supermercati",
                defaultextension=".json",
                initialdir=EXP_DB,
                filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
            )
            if file:
                if not self.show_custom_askyesno("Conferma Ripristino", "\nSovrascrivere il database attuale dei supermercati?\n"):
                    return
                try:
                    with open(file, "r", encoding="utf-8") as fsrc:
                        dbdata = fsrc.read()
                    with open(SUPERMERCATI_DB, "w", encoding="utf-8") as fdst:
                        fdst.write(dbdata)
                    _carica_dati_interno() 
                    if popup.winfo_exists():
                        popup.destroy() 
                        self.spesa_supermercato() 
                    self.show_custom_warning("Importazione completata", f"\nDatabase Supermercati ripristinato da:\n\n {file}\n")
                except Exception as e:
                    self.show_custom_warning("Errore", f"Errore durante il ripristino: {e}")

        def export_supermercati_db():
            popup.lift() 
            popup.focus_force() 
            SUPERMERCATI_DB = os.path.join(DB_DIR, "supermercati.json")
            now = datetime.date.today()
            default_dir = EXP_DB
            default_filename = f"Export_Supermercati_{now.day:02d}-{now.month:02d}-{now.year}.json"
            file = filedialog.asksaveasfilename(
                parent=popup,
                title="Esporta Database Supermercati",
                defaultextension=".json",
                initialdir=default_dir,
                initialfile=default_filename,
                confirmoverwrite=False,
                filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")]
            )
            if file:
                try:
                    with open(SUPERMERCATI_DB, "r", encoding="utf-8") as fsrc:
                        dbdata = fsrc.read()
                    with open(file, "w", encoding="utf-8") as fdst:
                        fdst.write(dbdata)
                    self.show_custom_warning("Esportazione completata", f"Database Supermercati esportato in {file}")
                except FileNotFoundError:
                    self.show_custom_warning("Errore", "Impossibile trovare il database sorgente dei supermercati.")
                except Exception as e:
                    self.show_custom_warning("Errore", f"Errore durante l'esportazione: {e}")

            btn_frame = ttk.Frame(input_popup); btn_frame.pack(pady=(0, 10))
            ttk.Button(btn_frame, text="Annulla", command=input_popup.destroy, style='Giallo.TButton').pack(side='left', padx=5)
            ttk.Button(btn_frame, text="Rinomina", command=on_confirm, style='Blu.TButton').pack(side='left', padx=5)
            entry.bind("<Return>", on_confirm)
            input_popup.update_idletasks()
            w = input_popup.winfo_reqwidth(); h = input_popup.winfo_reqheight()
            x = popup.winfo_rootx() + (popup.winfo_width() // 2) - (w // 2)
            y = popup.winfo_rooty() + (popup.winfo_height() // 2) - (h // 2)
            input_popup.geometry(f'+{x}+{y}')
            input_popup.protocol("WM_DELETE_WINDOW", input_popup.destroy)

        _carica_dati_interno()
        _controlla_scadenza_promo()
        popup = tk.Toplevel(self.master)
        barra_menu_popup = tk.Menu(popup)
        barra_menu_popup.config(bg="black", fg="white")
        popup.config(menu=barra_menu_popup) 
        menu_db = tk.Menu(barra_menu_popup, tearoff=0)
        barra_menu_popup.add_cascade(label="💾 Database", menu=menu_db)
        menu_db.add_command(label="📥 Importa Supermercati", command=import_supermercati_db)
        menu_db.add_command(label="📤 Esporta Supermercati", command=export_supermercati_db)
        self._popup_spesa_active = popup
        popup.title("Gestione e Confronto Spesa")
        popup.geometry("1200x630")
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 630) // 2
        popup.geometry(f"1200x630+{x}+{y}")
        popup.after(10, lambda: popup.focus_force())
        popup.bind('<Escape>', lambda event: popup.destroy())
        
        def on_popup_close():
            _salva_dati_interno(dati_supermercati)
            popup.destroy()
        popup.protocol("WM_DELETE_WINDOW", on_popup_close)

        notebook = ttk.Notebook(popup)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        frame_lista = ttk.Frame(notebook, padding="10", name='frame_lista')
        notebook.add(frame_lista, text="Lista Spesa Intelligente")
        frame_lista.grid_rowconfigure(1, weight=1)
        frame_lista.grid_rowconfigure(3, weight=2)
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_ricerca_input = ttk.Frame(frame_lista)
        frame_ricerca_input.grid(row=0, column=0, sticky='ew', pady=5)
        frame_ricerca_input.grid_columnconfigure(3, weight=1) 
        ttk.Label(frame_ricerca_input, text="Filtra Supermercato:").grid(row=0, column=0, padx=(5,0), sticky='w')
        combo_filtro_confronto = ttk.Combobox(
            frame_ricerca_input,
            textvariable=filtro_supermercato_confronto_var,
            values=tuple(["Tutti i supermercati"] + sorted(SUPERMERCATI)),
            state='readonly', width=30
        )
        combo_filtro_confronto.grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(frame_ricerca_input, text="Cerca Articolo (Testo):").grid(row=0, column=2, padx=(15, 0), sticky='w')
        entry_ricerca = ttk.Entry(frame_ricerca_input, textvariable=ricerca_var_confronto)
        entry_ricerca.grid(row=0, column=3, padx=5, sticky='ew') 
        ttk.Button(frame_ricerca_input, text="Cerca/Aggiorna Confronto", style='Verde.TButton',
                   command=lambda: _aggiorna_lista_spesa_intelligente(risultati_tv)).grid(row=0, column=4, padx=(10, 5), sticky='e')
        combo_filtro_confronto.bind('<<ComboboxSelected>>', lambda e: _aggiorna_lista_spesa_intelligente(risultati_tv))
        cols_risultati = ("Nome Articolo", "Qtà Catalogo", "Supermercato", "Descrizione", "Categoria", "Prezzo", "Confronto")
        frame_tv_risultati = ttk.Frame(frame_lista)
        frame_tv_risultati.grid(row=1, column=0, sticky='nsew', pady=5)
        risultati_tv = ttk.Treeview(frame_tv_risultati, columns=cols_risultati, show='headings')
        self.risultati_tv_ref = risultati_tv
        vbar_res = ttk.Scrollbar(frame_tv_risultati, orient="vertical", command=risultati_tv.yview)
        hbar_res = ttk.Scrollbar(frame_tv_risultati, orient="horizontal", command=risultati_tv.xview)
        risultati_tv.configure(yscrollcommand=vbar_res.set, xscrollcommand=hbar_res.set)
        vbar_res.pack(side="right", fill="y")
        hbar_res.pack(side="bottom", fill="x")
        risultati_tv.pack(side="left", fill='both', expand=True)
        risultati_tv.heading("Nome Articolo", text="Articolo"); 
        risultati_tv.heading("Qtà Catalogo", text="Qtà Cat."); 
        risultati_tv.heading("Supermercato", text="Supermercato"); 
        risultati_tv.heading("Prezzo", text="Prezzo")
        risultati_tv.heading("Confronto", text="Confronto")
        risultati_tv.heading("Descrizione", text="Descrizione")
        risultati_tv.heading("Categoria", text="Categoria")
        risultati_tv.column("Descrizione", width=180, stretch=True)
        risultati_tv.column("Categoria", width=130, stretch=False)
        risultati_tv.column("Qtà Catalogo", width=80, anchor='center', stretch=True)
        risultati_tv.column("Prezzo", width=80, anchor='e', stretch=False)
        risultati_tv.column("Confronto", width=130, anchor='center')
        risultati_tv.column("Nome Articolo", width=100, anchor='w', stretch=True)
        risultati_tv.column("Supermercato", width=130, anchor='w', stretch=False)
        for col in cols_risultati:
            text_to_show = {
                "Nome Articolo": "Articolo", 
                "Qtà Catalogo": "Qtà Cat.", 
                "Supermercato": "Supermercato",
                "Descrizione": "Descrizione",
                "Categoria": "Categoria",
                "Prezzo": "Prezzo",
                "Confronto": "Confronto"
            }.get(col, col)
            risultati_tv.heading(col, text=text_to_show, command=lambda _col=col, t=risultati_tv: _sort_treeview(t, _col, False))
        ttk.Label(frame_lista, text="La Tua Lista Spesa Ottimizzata (Doppio Click su Qtà per Modificare)", font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, sticky='ew', pady=(10, 5))
        cols_lista_spesa = ("Qtà Catalogo", "Qtà da Comprare", "Pezzo Un. (€)", "Totale (€)", "Supermercato")
        frame_tv_lista = ttk.Frame(frame_lista, name='frame_tv_lista')
        frame_tv_lista.grid(row=3, column=0, sticky='nsew')
        tv_lista_spesa = ttk.Treeview(frame_tv_lista, columns=cols_lista_spesa, show='tree headings')
        vbar_list = ttk.Scrollbar(frame_tv_lista, orient="vertical", command=tv_lista_spesa.yview)
        hbar_list = ttk.Scrollbar(frame_tv_lista, orient="horizontal", command=tv_lista_spesa.xview)
        tv_lista_spesa.configure(yscrollcommand=vbar_list.set, xscrollcommand=hbar_list.set)
        vbar_list.pack(side="right", fill="y")
        hbar_list.pack(side="bottom", fill="x")
        tv_lista_spesa.pack(side="left", fill='both', expand=True)
        tv_lista_spesa.heading("#0", text="Articolo/Gruppo")
        heading_map = {
            "Qtà Catalogo": "Qtà Cat.",
            "Qtà da Comprare": "Qtà Ordine",
            "Pezzo Un. (€)": "Pezzo Un. (€)",
            "Totale (€)": "Totale (€)",      
            "Supermercato": "Supermercato"
        }
        for col in cols_lista_spesa: 
            tv_lista_spesa.heading(col, text=heading_map.get(col, col))
        tv_lista_spesa.column("#0", width=180, anchor='w', stretch=True)
        tv_lista_spesa.column("Qtà Catalogo", width=80, anchor='center', stretch=False)
        tv_lista_spesa.column("Qtà da Comprare", width=120, anchor='center', stretch=False)
        tv_lista_spesa.column("Pezzo Un. (€)", width=140, anchor='e', stretch=False)
        tv_lista_spesa.column("Totale (€)", width=100, anchor='e', stretch=False)
        tv_lista_spesa.column("Supermercato", width=120, anchor='center')

        for col in cols_lista_spesa:
            tv_lista_spesa.heading(col, command=lambda _col=col, t=tv_lista_spesa: _sort_treeview(t, _col, False))
        risultati_tv.bind('<Double-1>', lambda e, tv_list=tv_lista_spesa, tv_res=risultati_tv: _aggiungi_a_lista_spesa(e, tv_list, tv_res))
        entry_ricerca.bind('<KeyRelease>', lambda e, tv=risultati_tv: _cerca_articoli(ricerca_var_confronto.get(), tv))
        tv_lista_spesa.bind('<Button-1>', lambda e, tv=tv_lista_spesa: _on_edit_quantity(e, tv))
        frame_pulsanti_lista = ttk.Frame(frame_lista)
        frame_pulsanti_lista.grid(row=4, column=0, sticky='ew', pady=5)
        ttk.Button(frame_pulsanti_lista, text="❌ Rimuovi Selezionato", style='Rosso.TButton',
                   command=lambda tv=tv_lista_spesa: _rimuovi_articolo_da_lista(tv)).pack(side='left', padx=5)
        ttk.Button(frame_pulsanti_lista, text="🗑️ Svuota Lista", style='Rosso.TButton',
                   command=lambda tv=tv_lista_spesa: _svuota_lista_spesa(tv)).pack(side='left', padx=5)
        ttk.Button(frame_pulsanti_lista, text="🚪 Chiudi", style='Giallo.TButton',
                   command=lambda: on_popup_close()).pack(side='right', padx=5)
        ttk.Button(frame_pulsanti_lista, text="🖨️ Esporta Lista", style='Verde.TButton',
                   command=_mostra_anteprima_esportazione).pack(side='right', padx=5)

        frame_gestione = ttk.Frame(notebook, padding="10")
        notebook.add(frame_gestione, text="Gestione Supermercati")
        frame_gestione.grid_columnconfigure(0, weight=1)
        frame_gestione.grid_rowconfigure(3, weight=1)
 
        self.label_conteggio_db = ttk.Label(
            frame_gestione, 
            text="🛒", 
            font=('Arial', 12, 'bold'), 
            foreground='#3f51b5'
        )
        self.label_conteggio_db.bind("<Button-1>", lambda event: info_popup())
        self.label_conteggio_db.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        
        frame_selezione = ttk.Frame(frame_gestione)
        frame_selezione.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        ttk.Label(frame_selezione, text="Seleziona Supermercato da Gestire:").pack(side='left', padx=5)
        combo_supermercato = ttk.Combobox(frame_selezione, textvariable=supermercato_selezionato_var,
                                         values=tuple(["Seleziona Supermercato"] + sorted(SUPERMERCATI)),
                                         state='readonly', width=30, name='combo_gestione_super')
        combo_supermercato.pack(side='left', padx=5)
        supermercato_selezionato_var.set("Seleziona Supermercato")
        ttk.Button(frame_selezione, text="✏️ Rinomina Selezionato", style='Giallo.TButton',
                   command=lambda c=combo_supermercato, t=None, r=None: _esegui_rinomina_supermercato(c, tree_super_crud, ricerca_vars_crud.get(supermercato_selezionato_var.get(), tk.StringVar()))).pack(side='left', padx=15)
        canvas_input = tk.Canvas(frame_gestione, height=140)
        canvas_input.grid(row=1, column=0, sticky='ew', pady=5)
        
        if 'combo_gestione_super' not in campi_input_refs:
            campi_input_refs['combo_gestione_super'] = {
                'nome': tk.StringVar(), 'descrizione': tk.StringVar(), 'categoria': tk.StringVar(),
                'prezzo': tk.StringVar(), 'promo_attiva': tk.BooleanVar(), 'prezzo_promo': tk.StringVar(),
                'quantita': tk.StringVar(), 'data_scadenza': tk.StringVar()
            }
        refs_crud = campi_input_refs['combo_gestione_super']
        
        frame_input = ttk.Frame(canvas_input)
        frame_input.grid_columnconfigure(1, weight=1); frame_input.grid_columnconfigure(3, weight=1)
        canvas_input.create_window((0, 0), window=frame_input, anchor="nw")
        frame_input.bind("<Configure>", lambda e: canvas_input.configure(scrollregion=canvas_input.bbox("all")))
        ttk.Label(frame_input, text="Nome Articolo:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(frame_input, textvariable=refs_crud['nome']).grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        ttk.Label(frame_input, text="Categoria:").grid(row=0, column=2, padx=5, pady=2, sticky='w')
        combo_categoria = ttk.Combobox(
            frame_input, 
            textvariable=refs_crud['categoria'],
            values=CATEGORIE_PREDEFINITE,
            state='readonly'
        )
        combo_categoria.grid(row=0, column=3, padx=5, pady=2, sticky='ew')
        if CATEGORIE_PREDEFINITE:
            combo_categoria.set(CATEGORIE_PREDEFINITE[0])

        ttk.Label(frame_input, text="Descrizione:").grid(row=1, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(frame_input, textvariable=refs_crud['descrizione']).grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        ttk.Label(frame_input, text="Quantità (es: 500g):").grid(row=1, column=2, padx=5, pady=2, sticky='w')
        ttk.Entry(frame_input, textvariable=refs_crud['quantita']).grid(row=1, column=3, padx=5, pady=2, sticky='ew')
        ttk.Label(frame_input, text="Prezzo Normale (€):").grid(row=2, column=0, padx=5, pady=2, sticky='w')
        ttk.Entry(frame_input, textvariable=refs_crud['prezzo']).grid(row=2, column=1, padx=5, pady=2, sticky='ew')
        ttk.Label(frame_input, text="Prezzo Promo (€):").grid(row=2, column=2, padx=5, pady=2, sticky='w')
        ttk.Entry(frame_input, textvariable=refs_crud['prezzo_promo']).grid(row=2, column=3, padx=5, pady=2, sticky='ew')
        ttk.Checkbutton(frame_input, text="Articolo in Promozione", variable=refs_crud['promo_attiva']).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(frame_input, text="Data Scadenza:").grid(row=3, column=2, padx=5, pady=2, sticky='w')
        frame_data_input = ttk.Frame(frame_input)
        frame_data_input.grid(row=3, column=3, padx=5, pady=2, sticky='ew')
        frame_data_input.grid_columnconfigure(0, weight=1)
        entry_data_scadenza = ttk.Entry(frame_data_input, textvariable=refs_crud['data_scadenza'])
        entry_data_scadenza.grid(row=0, column=0, sticky='ew')
        ttk.Button(
            frame_data_input, 
            text="🗓️", 
            style='Giallo.TButton',
            width=3, 
            command=lambda e=entry_data_scadenza: self.mostra_calendario_popup(e, refs_crud['data_scadenza'])
        ).grid(row=0, column=1, sticky='e', padx=(5, 0))
        frame_ricerca_crud = ttk.Frame(frame_gestione)
        frame_ricerca_crud.grid(row=2, column=0, sticky='ew', pady=(0, 5))
        ttk.Label(frame_ricerca_crud, text="Cerca Articolo (Filtro):").pack(side='left', padx=5)
        ricerca_var_crud_attuale = tk.StringVar()
        entry_ricerca_crud = ttk.Entry(frame_ricerca_crud, textvariable=ricerca_var_crud_attuale, width=40)
        entry_ricerca_crud.pack(side='left', padx=5, fill='x', expand=True)
        
        def update_crud_search_var(e=None):
            current_superm = supermercato_selezionato_var.get()
            if current_superm != "Seleziona Supermercato":
                _cerca_articoli_crud(current_superm, tree_super_crud, ricerca_var_crud_attuale)
        
        ttk.Button(frame_ricerca_crud, text="Cerca", style='Blu.TButton', command=update_crud_search_var).pack(side='left', padx=10)
        entry_ricerca_crud.bind('<KeyRelease>', update_crud_search_var)
        
        cols_super = ("Nome", "Descrizione", "Categoria", "Prezzo", "Promo", "Prezzo Promo", "Quantità", "Scadenza")
        frame_tv_crud = ttk.Frame(frame_gestione)
        frame_tv_crud.grid(row=3, column=0, sticky='nsew', pady=(5, 0))
        
        tree_super_crud = ttk.Treeview(frame_tv_crud, columns=cols_super, show='headings')
        vbar_tv = ttk.Scrollbar(frame_tv_crud, orient="vertical", command=tree_super_crud.yview)
        hbar_tv = ttk.Scrollbar(frame_tv_crud, orient="horizontal", command=tree_super_crud.xview)
        tree_super_crud.configure(yscrollcommand=vbar_tv.set, xscrollcommand=hbar_tv.set)
        vbar_tv.pack(side="right", fill="y")
        hbar_tv.pack(side="bottom", fill="x")
        tree_super_crud.pack(side="left", fill='both', expand=True)

        for col in cols_super:
            tree_super_crud.heading(col, text=col, command=lambda _col=col, t=tree_super_crud: _sort_treeview(t, _col, False))
            
        tree_super_crud.column("Promo", width=50, anchor='center', stretch=False)
        tree_super_crud.column("Prezzo Promo", width=90, anchor='e', stretch=False)
        tree_super_crud.column("Quantità", width=80, anchor='center', stretch=False)
        tree_super_crud.column("Prezzo", width=65, anchor='e', stretch=False)
        tree_super_crud.column("Scadenza", width=90, anchor='center', stretch=False)
        tree_super_crud.column("Nome", width=120, anchor='w')
        tree_super_crud.column("Descrizione", width=120, anchor='w')
        tree_super_crud.column("Categoria", width=90, anchor='w')

        frame_pulsanti_crud = ttk.Frame(frame_gestione)
        frame_pulsanti_crud.grid(row=4, column=0, sticky='ew', pady=5) # Ad esempio, row 4
        ttk.Label(frame_pulsanti_crud, text="Sposta Articolo").pack(side='left', padx=(20, 5))
        
        combo_super_sposta = ttk.Combobox(
            frame_pulsanti_crud,
            textvariable=supermercato_destinazione_var,
            values=tuple(["Destinazione"] + sorted(SUPERMERCATI)),
            state='readonly', width=20
        )
        combo_super_sposta.pack(side='left', padx=5)
        
        ttk.Button(frame_pulsanti_crud, text="➡️ Sposta", style='Giallo.TButton',
                   command=lambda tv=tree_super_crud, combo=combo_super_sposta: _sposta_articolo_tra_super(tv, combo)).pack(side='left', padx=10)

        def _sposta_articolo_tra_super(treeview_crud, combo_superm_dest):
            selected_item_iid = treeview_crud.focus()
            if not selected_item_iid:
                self.show_custom_warning("Destinazione Mancante", "Seleziona un supermercato di destinazione valido.")
                return
            super_destinazione = combo_superm_dest.get()
            super_corrente = supermercato_selezionato_var.get()
            
            if super_destinazione in ["Destinazione", "Sposta Articolo in:"]:
                self.show_custom_warning("Destinazione Mancante", "Seleziona un supermercato di destinazione valido.")
                return
            if super_destinazione == super_corrente:
                self.show_custom_warning("Spostamento Inutile", "L'articolo è già nel supermercato selezionato come destinazione.")
                return
            if not dati_supermercati.get(super_corrente):
                self.show_custom_warning("Errore Dati", "Supermercato di origine non trovato.")
                return
            try:
                iid_parts = selected_item_iid.split('_')
                if len(iid_parts) == 3 and iid_parts[0] == 'item':
                    idx_da_rimuovere = int(iid_parts[2])
                else:
                    item_values = treeview_crud.item(selected_item_iid, 'values')
                    if not item_values:
                        self._show_custom_warning("Errore Dati", "Articolo non trovato nei dati del supermercato corrente.")
                        return
                    nome_articolo = item_values[0]
                    articoli_correnti = dati_supermercati[super_corrente]
                    try:
                        idx_da_rimuovere = next(i for i, a in enumerate(articoli_correnti) if a.get('nome') == nome_articolo)
                    except StopIteration:
                        self.show_custom_warning("Errore Dati", f"Errore durante l'estrazione o rimozione dell'articolo: {e}")
                        return
                articolo_spostato = dati_supermercati[super_corrente].pop(idx_da_rimuovere)
            except Exception as e:
                self.show_custom_warning("Errore Dati", f"Errore durante l'estrazione o rimozione dell'articolo: {e}")
                return
                
            dati_supermercati[super_destinazione].append(articolo_spostato)
            self.show_custom_warning("Spostamento Riuscito", f"L'articolo è stato spostato con successo da '{super_corrente}' a '{super_destinazione}'.")
            ricerca_var_attuale = ricerca_vars_crud.get(super_corrente, tk.StringVar())
            _cerca_articoli_crud(super_corrente, treeview_crud, ricerca_var_attuale)
            combo_supermercato.set("Seleziona Supermercato")

        def _genera_testo_esportazione_supermercato(supermercato):
            import datetime 
            data_esportazione = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            testo = f"=== CATALOGO SUPERMERCATO: {supermercato.upper()} ({data_esportazione}) ===\n"
            articoli = dati_supermercati.get(supermercato, [])
            if not articoli:
                testo += "\nNessun articolo registrato per questo supermercato."
                return testo
            articoli.sort(key=lambda x: x.get('nome', ''))
            WIDTH_NOME = 30
            WIDTH_DESC = 30
            WIDTH_CAT = 20
            WIDTH_QTA = 10
            WIDTH_PREZZO = 10
            WIDTH_PROMO = 10
            WIDTH_SCAD = 10
            intestazione = (
                f"{'Nome':<{WIDTH_NOME}} {'Descrizione':<{WIDTH_DESC}} {'Categoria':<{WIDTH_CAT}} "
                f"{'Qtà':<{WIDTH_QTA}} {'P. Normale':>{WIDTH_PREZZO}} {'P. Promo':>{WIDTH_PROMO}} "
                f"{'In Promo':<{8}} {'Scadenza':<{WIDTH_SCAD}}"
            )
            separatore = "-" * len(intestazione)
            testo += "\n" + separatore + "\n"
            testo += intestazione + "\n"
            testo += separatore + "\n"
            for articolo in articoli:
                nome = articolo.get("nome", "")
                descrizione = articolo.get("descrizione", "")
                categoria = articolo.get("categoria", "")
                quantita = articolo.get("quantita", "")
                prezzo = str(articolo.get("prezzo", ""))
                promo = "SI" if articolo.get("promo") else "NO"
                prezzo_promo = str(articolo.get("prezzo_promo", ""))
                data_scadenza = articolo.get("data_scadenza", "")
                prezzo_fmt = f"€ {float(prezzo):.2f}" if prezzo and prezzo.replace('.', '', 1).isdigit() else ""
                promo_fmt = f"€ {float(prezzo_promo):.2f}" if prezzo_promo and prezzo_promo.replace('.', '', 1).isdigit() else ""
                linea = (
                    f"{nome[:WIDTH_NOME-1]:<{WIDTH_NOME}} "
                    f"{descrizione[:WIDTH_DESC-1]:<{WIDTH_DESC}} "
                    f"{categoria[:WIDTH_CAT-1]:<{WIDTH_CAT}} "
                    f"{quantita[:WIDTH_QTA-1]:<{WIDTH_QTA}} "
                    f"{prezzo_fmt:>{WIDTH_PREZZO}} "
                    f"{promo_fmt:>{WIDTH_PROMO}} "
                    f"{promo:<{8}} "
                    f"{data_scadenza:<{WIDTH_SCAD}}\n"
                )
                testo += linea
            testo += separatore + "\n"
            return testo

        def _mostra_anteprima_esportazione_supermercato(supermercato):
            if supermercato == "Seleziona Supermercato" or not supermercato:
                self.show_custom_warning("Selezione", "Seleziona un supermercato da esportare."); return
            anteprima_text = _genera_testo_esportazione_supermercato(supermercato)
            def _esporta_su_file_super(content_text, default_name, preview_popup):
                preview_popup.destroy()
                f = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("File txt", "*.txt")],
                    title=f"Salva Catalogo {supermercato} su File",
                    initialdir=EXPORT_FILES,
                    confirmoverwrite=False,
                    initialfile=default_name,
                    parent=popup
                )
                if f:
                    try:
                        with open(f, 'w', encoding='utf-8') as file_handle: file_handle.write(content_text)
                        self.show_custom_warning("Successo", f"✅ Catalogo salvato con successo in:\n{f}")
                    except Exception as e:
                        self.show_custom_warning("Errore", f"❌ Impossibile salvare il file:\n{e}")
            preview_popup = tk.Toplevel(popup)
            preview_popup.title(f"Anteprima Esportazione Catalogo: {supermercato}")
            WIDTH = 1150
            HEIGHT = 600
            screen_width = preview_popup.winfo_screenwidth()
            screen_height = preview_popup.winfo_screenheight()
            x = (screen_width - WIDTH) // 2
            y = (screen_height - HEIGHT) // 2
            preview_popup.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
            preview_popup.after(10, lambda: preview_popup.focus_force())
            preview_popup.bind('<Escape>', lambda e: preview_popup.destroy())
            text_area = tk.Text(preview_popup, wrap='word', font=('Courier', 10), padx=10, pady=10)
            text_area.insert('1.0', anteprima_text)
            text_area.config(state='disabled')
            text_area.pack(fill='both', expand=True, padx=10, pady=10)
            frame_btn = ttk.Frame(preview_popup); frame_btn.pack(pady=(0, 10))
            ttk.Button(frame_btn, text="Chiudi", command=preview_popup.destroy, style='Giallo.TButton').pack(side='right', padx=5)
            now = datetime.date.today()
            default_filename = f"Catalogo_{supermercato}_{now.day:02d}_{now.month:02d}_{now.year}.txt"
            ttk.Button(frame_btn, text="Esporta", style='Verde.TButton',
                         command=lambda: _esporta_su_file_super(anteprima_text, default_filename, preview_popup)
            ).pack(side='right', padx=5)

        def crud_wrapper(azione, tree, frame_input):
            superm = supermercato_selezionato_var.get()
            if superm == "Seleziona Supermercato":
                self.show_custom_warning("Selezione", "Seleziona un supermercato prima di eseguire l'azione."); return
            _funzione_crud(azione, superm, tree, frame_input)
        ttk.Button(frame_pulsanti_crud, text="➕ Inserisci", style='Blu.TButton',
                   command=lambda a='inserisci', t=tree_super_crud, f=frame_input: crud_wrapper(a, t, f)).pack(side='left', padx=5)
        ttk.Button(frame_pulsanti_crud, text="✏️ Modifica", style='Blu.TButton',
                   command=lambda a='modifica', t=tree_super_crud, f=frame_input: crud_wrapper(a, t, f)).pack(side='left', padx=5)
        ttk.Button(frame_pulsanti_crud, text="💾 Salva Modifiche", style='Blu.TButton',
                   command=lambda a='salva', t=tree_super_crud, f=frame_input: crud_wrapper(a, t, f)).pack(side='left', padx=5)
        ttk.Button(frame_pulsanti_crud, text="❌ Cancella", style='Rosso.TButton',
                   command=lambda a='cancella', t=tree_super_crud, f=frame_input: crud_wrapper(a, t, f)).pack(side='left', padx=5)
        ttk.Button(frame_pulsanti_crud, text="💣 AZZERA Database Supermercato", style='Rosso.TButton',
                   command=lambda s=supermercato_selezionato_var, t=tree_super_crud: _svuota_supermercato(s.get(), t)).pack(side='right', padx=15)
        ttk.Button(frame_pulsanti_crud, text="🖨️ Esporta Catalogo", style='Verde.TButton',
                   command=lambda s=supermercato_selezionato_var: _mostra_anteprima_esportazione_supermercato(s.get())).pack(side='right', padx=5)
        combo_supermercato.bind('<<ComboboxSelected>>', 
                                lambda e, c=combo_supermercato, t=tree_super_crud, f=frame_input, r=ricerca_var_crud_attuale: _on_supermercato_change(e, c, t, f, r))
        _cerca_articoli("", risultati_tv)
        _ricarica_lista_spesa(tv_lista_spesa)
        popup.wait_visibility()

    def _attiva_timer_inattivita(self):
        if self._timer_inattivita:
            self.after_cancel(self._timer_inattivita)
        self._timer_inattivita = self.after(self._timeout_inattivita, self._iconizza_finestra)
        self.bind_all("<Motion>", lambda e: self._reset_inattivita())
        self.bind_all("<Key>", lambda e: self._reset_inattivita())
        self.bind_all("<Button>", lambda e: self._reset_inattivita())
    def _reset_inattivita(self):
        if self.state() == "iconic":
            self.deiconify()  
        self._attiva_timer_inattivita()  
    def _iconizza_finestra(self):
        #print("💤 Inattività: finestra iconificata.")
        self.iconify()
        self.mostra_avviso_iconizzata()
        self._attiva_timer_inattivita()  
    def mostra_avviso_iconizzata(self):
        splash = tk.Toplevel()
        splash.overrideredirect(True)
        splash.attributes("-topmost", True)
        width, height = 400, 130
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = screen_width - width - 1  # ↪ angolo in alto a destra
        y = 30
        splash.geometry(f"{width}x{height}+{x}+{y}")
        splash.configure(bg="#7fc2c7")
        label = tk.Label(
            splash,
            text = f"💤 {NAME} v.{VERSION}\n\nFinestra minimizzata per inattività.\n\nPassa il mouse qui o clicca l’icona sulla barra per riaprirla.",
            font=("Arial", 9, "bold"),
            bg="#7fc2c7"
        )
        label.pack(expand=True, pady=30)
        splash.update()
        splash.after(3000, splash.destroy)  

    def _iconizza_finestra_startup(self):
        self.iconify()
        splash = self.mostra_avviso_iconizzata_startup()
        if splash:
            splash.bind("<Motion>", lambda e: self._deiconify_from_splash(splash))
            splash.bind("<Button>", lambda e: self._deiconify_from_splash(splash))
            
    def _deiconify_from_splash(self, splash_window):
        self.deiconify()
        splash_window.destroy()
        self._reset_inattivita() 

    def mostra_avviso_iconizzata_startup(self):
        splash = tk.Toplevel()
        splash.overrideredirect(True)
        splash.attributes("-topmost", True)
        width, height = 400, 130
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = screen_width - width - 1
        y = 30
        splash.geometry(f"{width}x{height}+{x}+{y}")
        splash.configure(bg="#7fc2c7")
        label = tk.Label(
            splash,
            text=f"💤 {NAME} v.{VERSION}\n\nFinestra minimizzata.\n\nPassa il mouse qui o clicca l’icona sulla barra per riaprirla.",
            font=("Arial", 9, "bold"),
            bg="#7fc2c7"
        )
        label.pack(expand=True, pady=30)
        splash.update()
        splash.after(3000, splash.destroy)
        return splash 

    def set_app_icon(window):
        ICON_PATH = os.path.join(DB_DIR, ICON_NAME)
        if os.path.exists(ICON_PATH):
            try:
                icon = tk.PhotoImage(file=ICON_PATH)
                window.iconphoto(False, icon)
            except tk.TclError as e:
                print(f"Errore: Impossibile impostare l'icona dal file {ICON_PATH}.")
        else:
            print("Icona non trovata in locale. Tentativo di download...")
            try:
                response = requests.get(ICON_URL, timeout=10)
                response.raise_for_status()
                os.makedirs(DB_DIR, exist_ok=True)
                with open(ICON_PATH, 'wb') as f:
                    f.write(response.content)
                icon = tk.PhotoImage(file=ICON_PATH)
                window.iconphoto(False, icon)
                print("Icona scaricata e impostata con successo!")
            except requests.exceptions.RequestException as e:
                print("Errore durante il download dell'icona.")
            except tk.TclError as e:
                print("Errore: L'immagine scaricata non è valida.")

    def check_aggiornamento_con_api(self):
        from datetime import datetime, timedelta
        try:
            if os.path.exists(RIMANDA_FILE):
                with open(RIMANDA_FILE, "r") as f:
                    data = json.load(f)
                    rimanda = datetime.strptime(data.get("rimanda_fino", ""), "%Y-%m-%d")
                    if datetime.today() < rimanda:
                        print(f"⏳ Rimandato fino al {rimanda.date()}")
                        return

            api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
 
            params = {"path": NOME_FILE, "per_page": 1}
            response = requests.get(api_url, params=params, timeout=5)
            response.raise_for_status()
            commits = response.json()
            if not commits:
                return 
            commit_date = commits[0]["commit"]["committer"]["date"]
            remote_time = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ").replace(microsecond=0)
            changelog_text = ""
            for commit in commits:
                date_str = commit["commit"]["committer"]["date"]
                commit_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                message = commit["commit"]["message"].strip()
                message = message.replace('\r', '') 
                lines = message.split('\n')
                subject = lines[0] 
                
                body_lines = lines[1:] 
                start_index = 0
                while start_index < len(body_lines):
                    current_line = body_lines[start_index].strip()
                    if not current_line or current_line == subject.strip():
                        start_index += 1
                    else:
                        break
                body_lines = body_lines[start_index:]
                changelog_entry = f"📝 [{commit_dt.strftime('%d/%m/%y %H:%M')}] {subject}\n"
                if body_lines:
                    for line in body_lines:
                        if line.strip(): 
                            changelog_entry += f" ➡️ {line}\n"
                        else:
                             changelog_entry += "\n"
                changelog_entry += "\n" 
                changelog_text += changelog_entry
                
            if not os.path.exists(NOME_FILE):
                self.show_custom_warning("File mancante", "⚠️ Il file locale non esiste. Aggiornamento consigliato.")
                return

            local_time = datetime.utcfromtimestamp(os.path.getmtime(NOME_FILE)).replace(microsecond=0)

            if remote_time.date() > local_time.date():
                style = ttk.Style()
                win = tk.Toplevel(self)
                win.title("🔄 Aggiornamento disponibile")

                label_timer = ttk.Label(win, text="⏱️ Chiusura automatica tra 60 secondi", style="Timer.TLabel")
                label_timer.pack(pady=(10, 0))

                msg = (
                    "🆕 È stato rilevato un possibile aggiornamento.\n\n"
                    f"📡 Ultima versione online: {remote_time.strftime('%d/%m/%Y %H:%M')}\n"
                    f"🖥️ Versione attuale locale: {local_time.strftime('%d/%m/%Y %H:%M')}"
                )
                ttk.Label(win, text=msg, wraplength=460, justify=tk.LEFT).pack(padx=20, pady=(10, 0))
                
                ttk.Label(win, text="Storico Modifiche (Changelog):", style="Timer.TLabel").pack(pady=(10, 0))
                
                frame_changelog = ttk.Frame(win)
                frame_changelog.pack(padx=20, pady=(5, 10), fill='both', expand=True)

                scrollbar = ttk.Scrollbar(frame_changelog)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                text_area = tk.Text(frame_changelog, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=6, width=60, font=("Arial", 9))
                text_area.insert(tk.END, changelog_text.strip())
                text_area.config(state=tk.DISABLED, background="#F0F0F0") 
                text_area.pack(side=tk.LEFT, fill='both', expand=True)
                
                scrollbar.config(command=text_area.yview)
                
                ttk.Label(win, text="👉 Vuoi procedere con l'aggiornamento adesso?").pack(pady=(5, 10))

                frame_bottoni = ttk.Frame(win)
                frame_bottoni.pack(pady=10)

                def aggiorna_timer(secondi_rimasti):
                    if secondi_rimasti > 0:
                        colore = "red" if secondi_rimasti <= 10 else "gray"
                        style.configure("Timer.TLabel", foreground=colore)
                        label_timer.config(text=f"⏱️ Chiusura automatica tra {secondi_rimasti} secondi")
                        win.after(1000, aggiorna_timer, secondi_rimasti - 1)
                    else:
                        label_timer.config(text="⏱️ Chiusura automatica...")
                        win.destroy()

                timeout_id = win.after(60000, win.destroy)
                aggiorna_timer(60)

                def annulla_timeout():
                    win.after_cancel(timeout_id)

                def aggiorna():
                    annulla_timeout()
                    win.destroy()
                    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{NOME_FILE.replace(' ', '%20')}"
                    self.aggiorna(url, NOME_FILE)
                    if os.path.exists(RIMANDA_FILE):
                        try:
                            os.remove(RIMANDA_FILE)
                            print("🧹 File rimando eliminato dopo aggiornamento.")
                        except Exception as err:
                            print(f"⚠️ Errore durante l'eliminazione del file rimando: {err}")

                def chiudi():
                    annulla_timeout()
                    win.destroy()

                def rimanda():
                    annulla_timeout()
                    win.destroy()
                    nuova_data = datetime.today() + timedelta(days=15)
                    with open(RIMANDA_FILE, "w") as f:
                        json.dump({"rimanda_fino": nuova_data.strftime("%Y-%m-%d")}, f)
                    print(f"⏳ Rimandato fino al {nuova_data.date()}")
                    data_formattata = nuova_data.date().strftime("%d/%m/%Y")
                    self.show_custom_warning("Aggiornamento Rimandato", f"⏳ Aggiornamento Rimandato fino al {data_formattata}")
                    
                ttk.Button(frame_bottoni, text="🔄 AGGIORNA", command=aggiorna, style="Verde.TButton").pack(side="left", padx=5)
                ttk.Button(frame_bottoni, text="❌ CHIUDI", command=chiudi, style="Giallo.TButton").pack(side="left", padx=5)
                ttk.Button(frame_bottoni, text="⏳ RIMANDA", command=rimanda, style="Arancio.TButton").pack(side="left", padx=5)

                win.withdraw()
                win.update_idletasks()
                min_w, min_h = 460, 410
                w = max(win.winfo_width(), min_w)
                h = max(win.winfo_height(), min_h)
                x = self.winfo_rootx() + (self.winfo_width() // 2) - (w // 2)
                y = self.winfo_rooty() + (self.winfo_height() // 2) - (h // 2)
                win.geometry(f"{w}x{h}+{x}+{y}")

                win.deiconify()
                win.grab_set()
                win.transient(self)
                win.focus_set()
                win.wait_window()

        except ConnectionError:
            print("🌐 Connessione assente o GitHub non raggiungibile.")
        except RequestException as e:
            print(f"⚠️ Errore HTTP o API: {e}")
        except Exception as e:
            print(f"⚠️ Errore generico durante il controllo aggiornamento: {e}")

    def esegui_backup_zip(self):
        from datetime import datetime
        percorso_archivio = ""
        cartella_temp_path = None
        print(f"Tentativo di backup di '{self.current_folder}'...")
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"{self.current_folder}_backup_{timestamp}"
            percorso_completo_output = filedialog.asksaveasfilename(
                title="Scegli dove salvare il file di backup",
                initialdir=os.path.expanduser('~'),
                initialfile=default_name,
                confirmoverwrite=False,
                defaultextension=f".{self.backup_formato}",
                filetypes=[(f"Archivi {self.backup_formato.upper()}", f"*.{self.backup_formato}")]
            )
            if not percorso_completo_output:
                print("❌ Backup annullato dall'utente.")
                return ""
            self.update_idletasks()
            self.update() 
            percorso_output_senza_ext, _ = os.path.splitext(percorso_completo_output)
            cartella_destinazione = os.path.dirname(percorso_output_senza_ext)
            root_dir_compress = os.path.dirname(os.getcwd())
            cartella_sorgente = os.path.join(root_dir_compress, self.current_folder)
            cartella_temp_path = tempfile.mkdtemp()
            cartella_dati_nel_temp_nome = self.current_folder
            cartella_dati_nel_temp_path = os.path.join(cartella_temp_path, cartella_dati_nel_temp_nome)
            PATTERNS_DA_IGNORARE = ('*.lock', '*-journal', '*.db-wal', '*.tmp')
            shutil.copytree(
                cartella_sorgente,
                cartella_dati_nel_temp_path,
                ignore=shutil.ignore_patterns(*PATTERNS_DA_IGNORARE)
            )
            print("✅ Copia temporanea creata (nel percorso TEMP di sistema).")
            os.makedirs(cartella_destinazione, exist_ok=True)
            percorso_archivio = shutil.make_archive(
                base_name=percorso_output_senza_ext,
                format=self.backup_formato,
                root_dir=cartella_temp_path,
                base_dir=cartella_dati_nel_temp_nome
            )
            print(f"✅ Backup di '{self.current_folder}' completato.")
            self.show_custom_warning ("Salvataggio", f"Backup di {self.current_folder} completato. !")
            print(f"File salvato in: {percorso_archivio}")
        except Exception as e:
            print(f"❌ ERRORE FATALE durante il backup: {e}")
        finally:
            if cartella_temp_path and os.path.exists(cartella_temp_path):
                shutil.rmtree(cartella_temp_path, ignore_errors=True)
                print("✅ Pulizia cartella TEMP completata.")
        return percorso_archivio
        
def backup_incrementale(file_path, cartella_backup="backup", max_backup=10):
    if not os.path.exists(file_path):
        return
    os.makedirs(cartella_backup, exist_ok=True)
    nome = os.path.basename(file_path)
    data = datetime.datetime.today().strftime("%d-%m-%Y")
    backup_file = os.path.join(cartella_backup, f"{data}-{nome}")
    shutil.copy2(file_path, backup_file)

    files = sorted(
        [f for f in os.listdir(cartella_backup) if f.startswith(nome)],
        key=lambda x: os.path.getmtime(os.path.join(cartella_backup, x)),
        reverse=True
    )
    for f in files[max_backup:]:
        os.remove(os.path.join(cartella_backup, f))

def install_tkcalendar():
    package_name = "tkcalendar"
    try:
        from tkcalendar import Calendar, DateEntry
    except ImportError:
        print(f"{package_name} non è installato. Installazione in corso...")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        print(f"{package_name} installato con successo!")
        from tkcalendar import Calendar, DateEntry
    return Calendar, DateEntry

def install_requests():
    try:
        import requests
    except ImportError:
        print("requests non trovato. Installazione in corso...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        import requests
    return requests
requests = install_requests()
from requests.exceptions import ConnectionError, RequestException

def install_win32_libraries():
    if platform.system() != "Windows":
        print("Sistema operativo non Windows: installazione non necessaria.")
        return None, None, None

    try:
        import win32print
        import win32api
        import win32con
    except ImportError:
        print("Moduli win32 non trovati. Installazione di pywin32 in corso...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"], check=True)
        print("pywin32 installato con successo.")
        #import win32print
        #import win32api
        #import win32con

    #return win32print, win32api, win32con #carica all'occorrenza

def check_single_instance():
    global _lock_file_handle
    global _mutex_handle
    _lock_file_handle = None 
    _mutex_handle = None
    if sys.platform.startswith("win"):
        import ctypes
        LAST_ERROR_ALREADY_EXISTS = 183
        mutex_name = "Global\\CasaFacileWeb_Mutex_34A5B6C7"
        mutex = ctypes.windll.kernel32.CreateMutexW(None, True, mutex_name)
        if ctypes.windll.kernel32.GetLastError() == LAST_ERROR_ALREADY_EXISTS:
            print("Un'altra istanza è già in esecuzione! (Windows)")
            show_warning_popup()
            sys.exit(1)
        _mutex_handle = mutex
        print("Avvio riuscito. Acquisito il Mutex (Windows).")
        return
    else:
        import fcntl
        lock_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        lock_file_path = os.path.join(lock_dir, 'casa_facile.lock')
        try:
            lock_file = open(lock_file_path, 'a')
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            _lock_file_handle = lock_file
            lock_file.write(f"{os.getpid()}\n") 
            lock_file.flush()
            print("Avvio riuscito. Acquisito il lock (Linux/Unix).")
            return
        except BlockingIOError:
            print("Un'altra istanza è già in esecuzione! (Linux/Unix)")
            show_warning_popup()
            sys.exit(1)
        except Exception as e:
            print(f"Errore critico durante la creazione del lock: {e}")
            sys.exit(1)

def show_warning_popup():
    splash = tk.Tk()
    splash.overrideredirect(True)
    width, height = 360, 110
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")
    splash.configure(bg="white")
    label = tk.Label(
        splash,
        text= f"{NAME}\nApp già in esecuzione!",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#b22222",
        justify="center"
    )
    label.pack(expand=True, fill="both")  
    splash.after(5000, splash.destroy)
    splash.mainloop()
    return splash

def show_backup_popup():
    splash = tk.Tk()
    splash.overrideredirect(True)
    width, height = 360, 110
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")
    splash.configure(bg="white")
    label = tk.Label(
        splash,
        text= f"{NAME}\nBackup Effettuato !",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#b22222",
        justify="center"
    )
    label.pack(expand=True, fill="both")  
    splash.after(5000, splash.destroy)
    splash.mainloop()
    return splash
if __name__ == "__main__":
    try:
        sys.stderr = open(os.devnull, 'w')
    except Exception:
        pass
        
    print(f"""
    📘 {NAME} — Guida agli argomenti da riga di comando
    
    ▶ auto       Avvio automatico con impostazione password:

      • auto <password>   → usa la password specificata
      • auto ""           → imposta una password vuota
      • auto              → usa la password predefinita (es. "return")

    ▶ noweb      Avvia senza interfaccia web (disabilita server locale)

    Esempi:
    {NAME}.pyw auto 1234     # imposta password “1234”
    {NAME}.pyw auto ""       # password vuota
    {NAME}.pyw auto          # password automatica (definita da utente)
    {NAME}.pyw noweb         # GUI senza web server
    {NAME}.pyw auto "" noweb # password vuota + niente web

    """)
 
    Calendar, DateEntry = install_tkcalendar()
    install_requests()
    install_win32_libraries()
    check_single_instance()
    print("Programma avviato.")

    if not os.path.exists(EXPORT_FILES):
        os.makedirs(EXPORT_FILES)
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    if not os.path.exists(EXP_DB):
        os.makedirs(EXP_DB)
    if not os.path.exists(UTENZE_DB):
        with open(UTENZE_DB, "w") as file:
            file.write("")  
            
    if not os.path.exists(PORTA_DB):
        with open(PORTA_DB, "w") as file:
            file.write("8081")
        PORTA = 8081
    else:
        with open(PORTA_DB, "r") as file:
            PORTA = int(file.read().strip())
         
    app = GestioneSpese()
    app.mainloop()

