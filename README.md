# 📚 Biblioteca WebApp

Applicazione web moderna per la gestione completa di una biblioteca, con interfaccia responsive e sistema CRUD per libri, lettori e prestiti.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.3-purple.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0+-orange.svg)

## 🎯 Funzionalità

- ✅ **Gestione Libri**: CRUD completo per il catalogo della biblioteca
- ✅ **Gestione Lettori**: Registrazione e gestione anagrafiche utenti
- ✅ **Gestione Prestiti**: Tracciamento prestiti con evidenziazione ritardi
- ✅ **Dashboard**: Statistiche in tempo reale su libri, lettori e prestiti attivi
- ✅ **Paginazione**: Visualizzazione tabelle con controllo righe (5, 10, 25, 50, Tutti)
- ✅ **Design Responsive**: Interfaccia ottimizzata per desktop, tablet e mobile
- ✅ **Tema Biblioteca**: Palette colori caldi (beige, marrone, verde) con stile cartaceo

## 🛠️ Tecnologie Utilizzate

### Backend
- **Flask**: Framework Python per API REST
- **MySQL**: Database relazionale
- **mysql-connector-python**: Driver per connessione MySQL
- **Flask-CORS**: Gestione Cross-Origin Resource Sharing

### Frontend
- **HTML5/CSS3**: Struttura e stile
- **Bootstrap 5**: Framework CSS responsive
- **JavaScript (Vanilla)**: Logica client-side e chiamate API
- **Bootstrap Icons**: Icone UI

## 📁 Struttura del Progetto

```
biblioteca-webapp/
├── app.py                 # Backend Flask con API REST
├── index.html             # Frontend con interfaccia completa
├── requirements.txt       # Dipendenze Python
└── README.md             # Questo file
```

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.8+
- MySQL 8.0+ (o Aiven MySQL)
- pip

### 1. Clona la repository
```bash
git clone https://github.com/tuo-username/biblioteca-webapp.git
cd biblioteca-webapp
```

### 2. Installa le dipendenze Python
```bash
pip install -r requirements.txt
```

### 3. Configura il database
Modifica la configurazione in `app.py`:
```python
DB_CONFIG = {
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "your_db_host.aivencloud.com",
    "port": 27368,
    "database": "biblioteca",
    "ssl_disabled": False
}
```

### 4. Crea le tabelle del database
```bash
python create_tables.py
```

### 5. Avvia il server Flask
```bash
python app.py
```

Il server sarà disponibile su `http://127.0.0.1:5000`

### 6. Apri l'applicazione
Apri `index.html` nel browser o servilo tramite un web server locale.

## 📊 Schema Database

### Tabella: `Libri`
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id_libro | INT (PK, AUTO_INCREMENT) | Identificativo univoco |
| titolo | VARCHAR(200) | Titolo del libro |
| autore | VARCHAR(150) | Nome autore |
| anno_pubblicazione | INT | Anno di pubblicazione |
| genere | VARCHAR(50) | Genere letterario |

### Tabella: `Lettori`
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id_lettore | INT (PK, AUTO_INCREMENT) | Identificativo univoco |
| nome | VARCHAR(100) | Nome del lettore |
| cognome | VARCHAR(100) | Cognome del lettore |
| email | VARCHAR(150) UNIQUE | Email (univoca) |
| citta | VARCHAR(100) | Città di residenza |

### Tabella: `Prestiti`
| Campo | Tipo | Descrizione |
|-------|------|-------------|
| id_prestito | INT (PK, AUTO_INCREMENT) | Identificativo univoco |
| id_libro | INT (FK) | Riferimento a Libri |
| id_lettore | INT (FK) | Riferimento a Lettori |
| data_prestito | DATE | Data inizio prestito |
| data_restituzione | DATE (nullable) | Data restituzione (NULL se attivo) |

## 🔌 API Endpoints

### Libri
- `GET /api/libri` - Ottieni tutti i libri
- `GET /api/libri/<id>` - Ottieni libro specifico
- `POST /api/libri` - Crea nuovo libro
- `PUT /api/libri/<id>` - Aggiorna libro esistente
- `DELETE /api/libri/<id>` - Elimina libro

### Lettori
- `GET /api/lettori` - Ottieni tutti i lettori
- `GET /api/lettori/<id>` - Ottieni lettore specifico
- `POST /api/lettori` - Crea nuovo lettore
- `PUT /api/lettori/<id>` - Aggiorna lettore esistente
- `DELETE /api/lettori/<id>` - Elimina lettore

### Prestiti
- `GET /api/prestiti` - Ottieni tutti i prestiti (con JOIN su libri e lettori)
- `GET /api/prestiti/<id>` - Ottieni prestito specifico
- `POST /api/prestiti` - Crea nuovo prestito
- `PUT /api/prestiti/<id>` - Aggiorna prestito esistente (es. restituzione)
- `DELETE /api/prestiti/<id>` - Elimina prestito

### Esempio Request POST
```json
POST /api/libri
Content-Type: application/json

{
  "titolo": "Il Nome della Rosa",
  "autore": "Umberto Eco",
  "anno_pubblicazione": 1980,
  "genere": "Giallo"
}
```

## 🎨 Caratteristiche UI

- **Palette Colori**: Toni caldi (beige #f5e6d3, marrone #8b4513, verde #2d5016)
- **Icone**: Bootstrap Icons per azioni e navigazione
- **Responsive**: Layout adattivo per tutti i dispositivi
- **Paginazione**: Controllo visualizzazione con dropdown righe
- **Alert Ritardi**: Badge rosso lampeggiante per prestiti scaduti (>30 giorni)
- **Modal Form**: Form inserimento/modifica in modal Bootstrap
- **Scroll Ottimizzato**: Tabelle con altezza fissa per evitare scroll anomali

## 🧪 Testing

### Test Connessione Database
```bash
python test_db.py
```

### Test Manuale API
Apri il browser e visita:
```
http://127.0.0.1:5000/api/libri
```

Dovresti vedere un array JSON con i libri del database.

## 🐛 Risoluzione Problemi

### Errore: "Errore nel caricamento dei libri"
- ✅ Verifica che Flask sia avviato (`python app.py`)
- ✅ Controlla la configurazione database in `app.py`
- ✅ Verifica che le tabelle esistano (`python create_tables.py`)
- ✅ Controlla la console browser (F12) per dettagli errore

### Errore CORS
- ✅ Verifica che `flask-cors` sia installato
- ✅ Controlla che `CORS(app)` sia presente in `app.py`

### Database vuoto
- ✅ Esegui `python create_tables.py` per creare tabelle e dati demo

## 📝 TODO / Miglioramenti Futuri

- [ ] Autenticazione utenti (login/logout)
- [ ] Filtri di ricerca avanzati per tabelle
- [ ] Esportazione dati in CSV/PDF
- [ ] Sistema di notifiche email per scadenze
- [ ] Statistiche avanzate con grafici
- [ ] API rate limiting e caching
- [ ] Containerizzazione con Docker
- [ ] Test unitari con pytest

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## 👤 Autore

**Gabriele**
- GitHub: [@tuo-username](https://github.com/tuo-username)

## 🤝 Contributi

I contributi sono benvenuti! Per favore:
1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/NuovaFeature`)
3. Committa le modifiche (`git commit -m 'Aggiunta NuovaFeature'`)
4. Pusha sul branch (`git push origin feature/NuovaFeature`)
5. Apri una Pull Request

## 📞 Supporto

Per problemi o domande, apri una [Issue](https://github.com/tuo-username/biblioteca-webapp/issues) su GitHub.

---

⭐ Se questo progetto ti è stato utile, lascia una stella su GitHub!
