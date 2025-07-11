# Weather forecast API + Client
Weather forecast è un'API RESTful realizzata in python con Flask. Fornisce previsioni meteo.
## Link del deploy
API: [backendprojectppm-production.up.railway.app](https://backendprojectppm-production.up.railway.app)

Client: [backendprojectppm-production-36ab.up.railway.app](https://backendprojectppm-production-36ab.up.railway.app)

# Struttura del progetto
`/app`: progetto dell'API

  - `/models`: contiene i modelli del database
  - `/auth`: contiene il blueprint flask per le rotte di registrazione e autenticazione
  - `/forecast_api`: contiene le rotte per richiedere/inserire previsioni meteo e per visualizzare le query passate degli utenti registrati
  - `app.py`: file principale di avvio dell'API. Contiene l'inizializzazione dell'app e dei sui componenti
  - `db.py`: file di dichiarazione del database. Contiene anche il metodo to_dict, che permette di serializzare gli oggetti del database in formato dizionario, rendendoli facili da convertire in JSON
  - `client.py`: file che importa il modulo request. Modificandolo, si possono testare le risposte in JSON che l'API manda a seguito di specifiche richieste

`/docs`: client minimale per esplorare l'API. Consente di registrarsi e fare il login, richiedere previsioni e vedere le richieste fatte in precedenza. Gli utenti admin sono in grado solo di aggiungere luoghi e previsioni al database

# Setup locale dell'API
Clonare il repository e installare le dipendenze. Le dipendenze sono elencate nel file `requirements.txt`.

Impostare in un file `.env` le seguenti variabili:

  - `SECRET_KEY`: chiave usata per fare l'hash dei cookie
  - `JWT_SECRET_KEY`: chiave usata per fare l'hash dei token di autenticazione
  - `DATABASE_URL`: url del database. È presente un piccolo database pre-popolato nel progetto: per usarlo impostare la variabile `= sqlite:///istance/database.db`
  - `PORT`: porta sulla quale il server Flask deve mettersi in ascolto. Di default è `5000`

Avviare l'app da terminale con `python app.py` oppure `flask run`. Adesso il server sarà in esecuzione su localhost.

# Setup locale del Client
Nel file `config.js`, impostare la variabile `API_BASE_URL` all'URL dell'API. Con il database del repo usare: `http://localhost:<port>`
Avviare il file `index.html`

# Modello del database

### User
Rappresenta un utente registrato nell'API

Colonna  |   Tipo    |  Descrizione  |
---------|-----------|---------------|
id       |  Integer  | Id dell'utente (chiave primaria) |
username |  String   | Username dell'utente  |
password_hash  |  String  | Password dell'utente hashata  |
is_admin |  Bool  | Parametro per indicare se l'utente è admin o no  |

### Location
Rappresenta un luogo geografico

Colonna  | Tipo  | Descrizione |
---------|-------|-------------|
id  | Integer  |  Id del luogo (chiave primaria)  |
name  |  String  | Nome del luogo  |
lat  |  Float  |  Latitudine del luogo  |
lon  |  Float  |  Longitudine del luogo  |

### Forecast
Rappresenta una previsone meteo

Colonna  |  Tipo  |  Descrizione  |
---------|--------|---------------|
id  |  Integer  |  Id della previsione (chiave primaria)  |
location_id  |  Integer  |  Id del luogo della previsione (chiave esterna)  |
date  |  Date  |  Data dalla previsione  |
time  |  Time  |  Orario della previsione  |
temperature  |  Float  |  Temperatura  della previsione  |
condition  |  String  |  Condizione metereologica  |
rain  |  Float  |  Quantità di pioggia  |

### QueryLog
Rappresenta le previsioni salvate degli utenti registrati

Colonna  |  Tipo  |  Descrizione  |
---------|--------|---------------|
id  |  Integer  |  Id della query salvata (chiave primaria)  |
user_id  |  Integer  |  Id dell'utente che ha fatto la query (chiave esterna)  |
forecast_id  |  Integer  |  Id della previsione fatta nella query (chiave esterna)  |
timestamp  |  DateTime  |  Data e orario di quando è stata effettuata la query  |

### DailyIpRequest
Rappresenta il numero di richeste giornaliere fatte da Anonimo (pubblico).
Utilizza l'ip per riconoscere l'anonimo.

Colonna  |  Tipo  |  Descrizione  |
---------|--------|---------------|
id  |  Integer  |  Id delle richieste giornaliere dell'ip (chiave primaria)  |
ip  |  Integer  |  Ip dell'Anonimo  |
date  |  Date  |  Data in cui sono effettuate le richieste  |
count  |  Integer  |  Numero di richieste effettuate in quel giorno  |

# Documentazione dell'API

`NOTA`: Visto che questa è una "demo", non è permesso registrare altri utenti con campo `is_admin = True`. Un utente admin viene creato ogni volta che viene istanziato un nuovo database. 
L'utente admin serve solo per facilitare l'aggiunta di nuove Location e Forecast, non può fare query di previsioni e non le può salvare. Se si vuole aggiungere Location e/o Forecast, fare il login con l'account admin, che ha credenziali
`username: admin` e `password: admin`.

`NOTA`: Tutti i metodi `POST` richiedono il body in formato JSON (in headers: `"Content-Type": "application/json"`)

`NOTA`: Tutti i metodi `GET` ricevono i dati tramite query sring nell'URL (es: `/api/route?param1=val1&param2=val2`)

`NOTA`: L'API risponde sempre in formato JSON

`NOTA`: Il JSON Web Token (JWT) viene assegnato nel momento del login. Se si ottiene un errore che riguarda il JWT (es: `status code 422`) bisogna effettuare nuovamente il login.
Queste sono escluse dall'elenco delle risposte sottostante.

### `auth/register`
Permette di registrarsi come utente.

#### POST

**Parametri**:

  - `username`: Nome utente da registrare
  - `password`: Password dell'utente da registrare (verrà salvata dopo aver fatto l'hash)

**Risposte**:

  - `201 CREATED`: Utente creato correttamente
  - `400 BAD REQUEST`: Parametri mancanti o non validi
  - `409 CONFLICT`: Esiste già un utente con quello username

### `auth/login`
Permette di fare il login con username e password.

#### POST

**Parametri:**

  - `username`: Nome dell'utente che vuole fare il login
  - `password`: Password dell'utente che vuole fare il login

**Risposte**

- `400 BAD REQUEST`: Parametri mancanti o non validi
- `401 UNAUTHORIZED`: Username o password sbagliati
- `200 OK`: Login effettuato. L'API risponde mandando un JSON con l'access token nel campo `"access_token"`

### `api/forecast`

#### GET
Permette di vedere le previsioni. L'Anonimo (pubblico) ha un massimo di 10 richieste giornaliere. Le richieste degli User vengono salvate.

**Parametri**

  - `location`: Nome del luogo
  - `date`: Data della previsione
  - `time`: Orario della previsione

**Risposte**

  - `404 NOT FOUND`: Luogo/previsione non trovata
  - `400 BAD REQUEST`: Parametri mancanti o non validi
  - `403 FORBIDDEN`: Un admin sta provando ad vedere una previsione
  - `429 TOO MANY REQUESTS`: Un Anonimo (pubblico) ha raggiunto il limite massimo di richieste giornaliere
  - `200 OK`: Previsione trovata. L'API risponde mandando in formato JSON tutti i campi della previsione

#### POST
Permette all'admin di inserire nuove previsioni nel database. Richiede il JWT.

**Parametri**

  - `location`: Nome del luogo
  - `date`: Data della previsione
  - `time`: Orario della previsione
  - `condition`, `temperature`, `rain`: Parametri meteo

  - `JWT`: Da passare in `headers` con formato `"Authorization": "Bearer <token>"`

**Risposte**

  - `403 FORBIDDEN`: Un utente non admin sta cercando di inserire una previsione
  - `404 NOT FOUND`: Luogo non trovato
  - `400 BAD REQUEST`: Parametri mancanti
  - `201 CREATED`: Previsione aggiunta correttamente

### `api/savedQueries`

#### GET
Restituisce tutte le query salvate dell'utente. Richiede il JWT.

**Parametri**

  - `JWT`: Da passare in `headers` con formato `"Authorization": "Bearer <token>"`

**Risposte**

  - `200 OK`: Restituisce tutte le previsioni visualizzate dall'utente in formato JSON

### `api/location`

#### POST
Permette all'admin di inserire luoghi nel database. Richiede il JWT.

**Parametri**

  - `name`: Nome del luogo
  - `lat`: Latitudine del luogo
  - `lon`: Longitudine del luogo

  - `JWT`: Da passare in `headers` con formato `"Authorization": "Bearer <token>"`

**Risposte**

  - `403 FORBIDDEN`: Un utente non admin sta cercando di inserire un luogo
  - `400 BAD REQUEST`: Parametri mancanti
  - `201 CREATED`: Luogo aggiunto correttamente

### `api/userinfo`

#### GET
Permette di avere le info sull'user attualmente loggato. Richiede il JWT.

**Parametri**

  - `JWT`: Da passare in `headers` con formato `"Authorization": "Bearer <token>"`

**Risposte**

  - `200 OK`: L'API restituisce in formato JSON tutti i campi dell'utente loggato
