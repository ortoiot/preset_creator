# 🚀 OrtoIoT Preset Creator - Istruzioni Windows

## 📋 File Necessari

Assicurati di avere questi file nella stessa cartella:

```
📁 ortoiot-preset-creator/
├── 📄 preset_creator.py          (programma principale)
├── 🔧 SETUP_AND_RUN.bat         (installazione + avvio automatico)
├── 📦 INSTALL_ONLY.bat          (solo installazione)
├── 🚀 RUN_PROGRAM.bat           (solo avvio programma)
├── 📋 requirements.txt          (lista dipendenze)
└── 📖 ISTRUZIONI_WINDOWS.md     (questo file)
```

## 🎯 Metodo 1: Tutto Automatico (CONSIGLIATO)

### ✅ Un Click e Funziona
1. **Doppio click** su `SETUP_AND_RUN.bat`
2. **Aspetta** che installi tutto automaticamente
3. **Il programma si avvia** da solo!

```cmd
🔥 SETUP_AND_RUN.bat
├─ Controlla Python
├─ Installa dipendenze  
├─ Avvia programma
└─ 🎉 Pronto!
```

## 🎯 Metodo 2: Passo Passo

### Passo 1: Installazione
1. **Doppio click** su `INSTALL_ONLY.bat`
2. **Aspetta** che installi tutto
3. **Chiude** quando finito

### Passo 2: Avvio
1. **Doppio click** su `RUN_PROGRAM.bat`  
2. **Il programma si apre**

## 🛠️ Se Python Non è Installato

Il batch ti dirà e aprirà automaticamente:
- https://www.python.org/downloads/

**IMPORTANTE**: Durante installazione Python:
- ✅ **Spunta** "Add Python to PATH"
- ✅ **Spunta** "Install for all users" (opzionale)

## 🎮 Come Usare il Programma

### 1. **Nuovo Preset**
- Clicca `🆕 New Preset`
- Compila nome, descrizione, categoria
- Vai su tab "Automation Settings"
- Attiva e configura le automazioni desiderate

### 2. **Salvare Preset**
- Clicca `💾 Save` per salvare nella libreria

### 3. **Esportare per OrtoIoT**
- Clicca `📤 Export` 
- Scegli dove salvare il file .json
- Importa questo file in OrtoIoT

### 4. **Categorie Disponibili**
- **Cannabis**: Indica, Sativa, Hybrid, Ruderalis
- **Vegetables**: Leafy Greens, Fruiting Plants, Herbs
- **Flowers**: Annuals, Perennials
- **Specialty**: Mushrooms, Microgreens

## 🔧 Automazioni Configurabili

| Automazione | Parametri | Descrizione |
|-------------|-----------|-------------|
| 🌡️ Temperature | Target °C | Controllo temperatura |
| 💧 Humidity | Target % | Controllo umidità |
| 💨 CO2 | Target ppm | Livelli CO2 |
| ⚡ EC | Target mS/cm | Fertilizzante |
| 🚿 Irrigation | Durata, Intervallo | Irrigazione |
| 💡 Lighting | Orario, Durata | Illuminazione |
| 🔆 Lamp | Distanza cm | Altezza lampada |
| 🌪️ Ventilation | Durata, Intervallo | Ventilazione |
| 🌿 Foliar | Frequenza, Durata | Nutrizione fogliare |

## ❌ Risoluzione Problemi

### ❌ "Python non trovato"
**Soluzione:**
1. Installa Python da https://www.python.org/downloads/
2. **IMPORTANTE**: Spunta "Add Python to PATH"
3. Riavvia il computer
4. Riprova con il batch

### ❌ "Errore installazione dipendenze"
**Soluzione:**
1. Apri Prompt Comandi come Amministratore
2. Esegui: `python -m pip install --upgrade pip`
3. Esegui: `python -m pip install customtkinter pillow`
4. Riprova

### ❌ "File preset_creator.py non trovato"
**Soluzione:**
- Assicurati che tutti i file siano nella stessa cartella
- Non spostare i file .bat senza il programma principale

### ❌ "Il programma si chiude subito"
**Soluzione:**
1. Apri Prompt Comandi
2. Vai nella cartella: `cd C:\path\to\preset-creator`
3. Esegui: `python preset_creator.py`
4. Leggi l'errore specifico

## 🚀 Metodo Manuale (Avanzato)

Se preferisci fare tutto a mano:

```cmd
# 1. Controlla Python
python --version

# 2. Installa dipendenze
pip install customtkinter pillow

# 3. Avvia programma
python preset_creator.py
```

## 📱 Contatti

- **Problemi**: Crea issue su GitHub
- **Supporto**: Discord OrtoIoT
- **Email**: support@ortoiot.com

## 🎉 Primo Utilizzo Consigliato

1. **Avvia** con `SETUP_AND_RUN.bat`
2. **Crea preset** "Test Cannabis Indica"  
3. **Configura** temperatura 24°C, umidità 60%
4. **Salva** nella libreria
5. **Esporta** per OrtoIoT
6. **Importa** in OrtoIoT per testare

Buon lavoro! 🌱