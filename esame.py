# Compito d'esame Laboratorio: Emanuele Lasorte
# Matricola: EC2100877
# Programma per estrarre dati da un file CSV e calcolare la differenza giornaliera di temperatura 

class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    
    def __init__(self, name=None):
        self.name=name
    
    def get_data(self):
        
        lista_dati = []

        # Verifica se il file è stato inserito
        if self.name is None:
            raise ExamException('il file csv non è stato inserito!')

        # Verifica se il nome del file è una stringa
        if not isinstance(self.name, str):
            raise ExamException('il nome del file csv deve essere stringa!')

        # Apre il file
        try:
            my_file = open(self.name, 'r')
            
        except:
            raise ExamException('il file csv non esiste')

        # Itera ogni riga del file
        for line in my_file:

            # Divide la riga in due elementi separati dalla virgola e limita la lunghezza della 
            # lista a due elementi
            elements = line.strip().split(',')[:2]

            # Verifica se ci sono solo due elementi
            if len(elements) == 2:

                # Estrae i due elementi (epoch e temperature)
                epoch = elements[0]
                temperature = elements[1]
                
                try:
                    
                    # Verifica se epoch è un numero intero
                    epoch = int(float(epoch))

                    # Verifica se temperature è un numero
                    temperature = float(temperature)
                    
                except:

                    # Salta 
                    continue

                # Verifica se temperature è un numero diverso da 0
                if (isinstance(temperature,int) or isinstance(temperature,float) ) and temperature!=0:
                    # Crea una nuova lista
                    lista_nuova=[]
                    lista_nuova.append(epoch)
                    lista_nuova.append(temperature)

                    # Verifica se la lista è vuota
                    if not lista_dati: 
                        lista_dati.append(lista_nuova)
                    
                    else:

                        # Verifica che gli epoch siano in ordine crescente
                        lista_precedente=lista_dati[-1]
                    
                        if not epoch>lista_precedente[0]:
                            raise ExamException('il timestamp è fuori ordine o duplicato.')
                            
                        else:
                            lista_dati.append(lista_nuova)
            else:

                # Salta l'iterazione
                continue
                
        # Chiude il file
        my_file.close()

        # Verifica se la lista è vuota/non contiene valori validi
        if not lista_dati:
            raise ExamException('nessun dato è stato importato: file vuoto o nessun valore accettabile')
        
        return lista_dati

# Ora la funzione vera e proprio che calcola la massima differenza giornaliera
def compute_daily_max_difference(time_series=None):

    # Verifica che il parametro sia stato inserito
    if time_series is None: 
        raise ExamException ("il parametro compute_daily_max_difference non è stato inserito!")

    # Verifica che il parametro sia una lista
    if not isinstance(time_series,list):
        raise ExamException("il parametro compute_daily_max_difference è inserito, ma non e' una lista!")

    # Verifica che la lista non sia vuota
    if not time_series:
        raise ExamException ("è stata inserita una lista vuota in compute_daily_max_difference!")

    # Verifica che ogni elemento della lista sia una lista
    for item in time_series:
        if not isinstance(item,list):
            raise ExamException('compute_daily_max_difference deve ricevere in input una lista di liste')

    # Verifica che ogni sottolista abbia esattamente 2 elementi
    for item in time_series:
        if isinstance(item,list) and len(item) !=2:
            raise ExamException('le sottoliste non sono di 2 elementi come richiesto')
               
    for i in range(len(time_series)):

        # Verifica che la prima posizione della sottolista sia un intero o un float convertibile ad un intero
        if isinstance(time_series[i][0],float):
            time_series[i][0] = int(time_series[i][0])
        
        if not isinstance(time_series[i][0],int):
            raise ExamException('ho trovato un epoch che non è numerico!')

        # Verifica che gli epoch siano ordinati e non duplicati
        if i>0:
            if not time_series[i][0] > time_series[i-1][0]:
                raise ExamException('gli epoch non sono ordinati o duplicati!')

        # Verifica che la seconda posizione della sottolista sia un numero
        if not (isinstance(time_series[i][1],int) or isinstance(time_series[i][1],float)):
            raise ExamException('la temperatura non è numerica: non accettabile!')

        # Verifica che la temperatura non sia nulla
        if time_series[i][1] == 0:
            raise ExamException('la temperatura è nulla: non accettabile!')

    # Inizializzazione della lista per contenere le statistiche totali
    lista_differenze_totale = []

    # Creazione di una lista per contenere i giorni
    lista_giorni = []

    # Iterazione sui dati delle serie temporali per estrarre i giorni 
    for item in time_series:
        lista_giorni.append(item[0]-(item[0]%86400))
        
    # Inizializzazione del contatore 'i'
    i=0

    # Loop che continua finché 'i' è inferiore alla lunghezza della lista dei giorni
    while i<len(lista_giorni):

        # Creazione della lista delle temperature per ogni giorno
        lista_temperature=[time_series[i][1]]

        # Inizializzazione della lista per le differenze giornaliere
        differenze_giornaliere=[]

        # Inizializzazione del contatore 'j' come 'i'+1
        j=i+1

        # Flag per indicare se siamo passati al giorno successivo
        giorno_successivo=False

        # Loop che continua finché 'j' è inferiore alla lunghezza della lista dei giorni
        # e il giorno successivo non è ancora stato raggiunto
        while j<len(lista_giorni) and giorno_successivo is False:

        # Se il giorno corrente è uguale al giorno successivo, 
        # aggiungi la temperatura del giorno successivo alla lista
        # e incrementa 'j'
            if lista_giorni[j] == lista_giorni[i]:
                lista_temperature.append(time_series[j][1])
                j+=1
                
            else:

                # Altrimenti, imposta 'i' come 'j' e imposta il flag a vero
                i=j
                giorno_successivo = True

                # Come da istruzioni, se un giorno ha soltanto una misurazione il risultato deve essere None.
                if len(lista_temperature) == 1:
                    differenza_min_max = None

                # Calcola il minimo, il massimo e la differenza tra il massimo e il minimo
                # per la lista delle temperature del giorno
                else:
                
                    minimo = min(lista_temperature)
                    massimo = max(lista_temperature)
                    differenza_min_max = massimo-minimo

                # Aggiungi la differenza al giorno come differenza giornaliera
                differenze_giornaliere = [differenza_min_max]

                # Aggiungi le differenze giornaliere alla lista delle differenze totali
                lista_differenze_totale.append(differenze_giornaliere)

        # se l'indice "j" raggiunge la fine della lista "lista_giorni
        if j == len(lista_giorni):

            # Come da istruzioni, se un giorno ha soltanto una misurazione il risultato deve essere None.
            if len(lista_temperature) == 1:
                    differenza_min_max = None

            else: 
            # Calcola il minimo e il massimo delle temperature per il giorno corrente.
                minimo = min(lista_temperature)
                massimo = max(lista_temperature)
                differenza_min_max = massimo-minimo

            # Calcola la differenza tra il massimo e il minimo e la memorizza come differenza giornaliera.
            differenze_giornaliere=[differenza_min_max]

            # Aggiunge la differenza giornaliera alla lista totale delle differenze.
            lista_differenze_totale.append(differenze_giornaliere)

            # Aggiorna l'indice "i" per evitare di esaminare nuovamente il giorno corrente.
            i=j

    return lista_differenze_totale


# Test

"""
try:

    print('\n...apertura del file csv in corso...\n')
    time_series_file = CSVTimeSeriesFile(name="data.csv")
    time_series=time_series_file.get_data()
    
    print('>> Operazione avvenuta con successo!')
    print('>> Rilevazioni importate: {}'.format(len(time_series)))


    differenze=compute_daily_max_difference(time_series)
    
    print('>>Stampa delle differenze massime giornaliere:')
    
    for item in differenze:
        print('',(item[0]))

except ExamException as e:
    print("C'è stato un problema: {}".format(e))
"""