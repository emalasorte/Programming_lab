#Compito di laboratorio
#Lasorte Emanuele EC2100877
#Programma per estrarre dati da un file csv e  capire se dati due anni consecutivi c’è stata una variazione nel numero di passeggeri tra coppie di mesi quasi uguale (+-2), da un anno all’altro

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

            # Divide la riga in due elementi separati dalla virgola e limita la lunghezza della lista a due elementi
            elements = line.strip().split(',')[:2]

            # Verifica se ci sono solo due elementi
            if len(elements) == 2:

                # Estrae i due elementi (date e passeggeri)
                dates = elements[0]
                passengers = elements[1]
                
                try:
                    
                    # Verifica se passeggeri è un numero intero
                    passengers = int(float(passengers))
                    
                except:

                    # Salta 
                    continue

                # Verifica se passeggeri è intero
                if (isinstance(passengers,int) and passengers>=0):
                    # Serie di if per verificare la validità degli ANNI-MESI
                    if '-' in elements[0]:
                        test_mesi=elements[0].split('-')
                        for i,item in enumerate(test_mesi):
                            if (test_mesi[i].isnumeric()):
                                if int(test_mesi[1]) in range(1,13):
                                    
                    # Crea una nuova lista
                                    lista_nuova=[]
                                    lista_nuova.append(dates)
                                    lista_nuova.append(passengers)
                                    

                    # Verifica se la lista è vuota
                        if not lista_dati: 
                            lista_dati.append(lista_nuova)
                            
                        else:

                        # Verifica che le date siano in ordine crescente
                            lista_precedente=lista_dati[-1]
                    
                            if not dates>lista_precedente[0]:
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


#Funzione

def detect_similar_monthly_variations(time_series, years):
    
    # Controlla che l'input years sia una lista
    if not isinstance(years, list):
            raise ExamException('Errore, i valori non sono inseriti in una lista, ma si tratta di: {}'.format(type(years)))

    # Controlla che la lista years abbia esattamente due elementi
    if (len(years)!=2):
        raise ExamException('Errore, la lista inserita non può essere considerata perchè non ha due due valori ma ne ha: {}'.format(len(years)))

    # Controlla che entrambi gli elementi della lista years siano numeri interi
    if (isinstance(years[0], int)==False or isinstance(years[1], int)==False):
        raise ExamException('Errore, gli elementi della lista devono essere due numeri interi')

    # Controlla che per entrambi gli anni esista almeno un dato nella time_series
    for year in years:
        if not any(x[0].startswith(str(year)) for x in time_series):
            raise ExamException(f"Nessun dato disponibile per l'anno: {year}")

    # Controlla che il primo anno sia inferiore al secondo
    if(years[0]>=years[1]):
        raise ExamException('Errore, range di anni non valido')

    # Controlla che i due anni siano consecutivi
    if(years[1]-years[0]!=1):
        raise ExamException('Errore, range di anni non valido perchè i due anni inseriti devono essere consecutivi')


    # Inizializza una lista vuota per contenere i dati
    lista_dati = []

    # Per ogni lista nella lista time_series
    for item in time_series:

    # Inizializza una nuova lista vuota per contenere i dati della riga
        riga_dati = []

        # Per ogni elemento nella lista della riga
        for i, element in enumerate(item):

            # Se l'elemento è il primo, estrai l'anno e il mese e aggiungi alla riga dei dati
            if i == 0:
                anno_mese = element.split('-')
                riga_dati.append(int(anno_mese[0]))
                riga_dati.append(int(anno_mese[1]))

            # Se l'elemento non è il primo, aggiungi il valore alla riga dei dati
            else:
                riga_dati.append(element)

        # Aggiungi la riga dei dati alla lista dei dati
        lista_dati.append(riga_dati)


    # Inizializza le liste vuote anno_0 e anno_1
    anno_0 = []
    anno_1 = []

    # Scorri ogni lista nella lista di liste lista_dati
    for item in lista_dati:
        # Se l'anno nella lista corrente è uguale all'anno iniziale specificato
        if item[0] == years[0]:
            # Aggiungi alla lista anno_0 il mese e il valore della lista corrente
            anno_0.append([item[1], item[2]])

        # Se l'anno nella lista corrente è uguale all'anno finale specificato
        if item[0] == years[1]:
            # Aggiungi alla lista anno_1 il mese e il valore della lista corrente
            anno_1.append([item[1], item[2]])


        # Crea una lista di 12 elementi, tutti uguali a None, e assegnala alla variabile anno_0_passeggeri
    anno_0_passeggeri = [None for i in range(12)]

    # Crea una lista di 12 elementi, tutti uguali a None, e assegnala alla variabile anno_1_passeggeri
    anno_1_passeggeri = [None for i in range(12)]


        # Scorri tutti gli elementi della lista anno_0
    for item in anno_0:
        
        # Estrai il valore del mese 
        mese = int(item[0])
        
        # Assegna il valore del numero di passeggeri alla posizione corretta nella lista anno_0_passeggeri
        anno_0_passeggeri[mese - 1] = item[1]

    # Scorri tutti gli elementi della lista anno_1
    for item in anno_1:
        
        # Estrai il valore del mese e sottrai 1 per ottenere l'indice corretto nella lista anno_1_passeggeri
        mese = int(item[0])
        
        # Assegna il valore del numero di passeggeri alla posizione corretta nella lista anno_1_passeggeri
        anno_1_passeggeri[mese - 1] = item[1]

        
    # Inizializzo due liste vuote che conterranno le differenze tra i passeggeri mensili dell'anno 0 e dell'anno 1
    diff_anno_0=[]
    diff_anno_1=[]

    # Calcolo la differenza tra i passeggeri di ogni mese dell'anno 0
    for i in range(11):
    
        # Se uno dei due mesi da confrontare non è disponibile, viene inserito None in diff_anno_0
        if(anno_0_passeggeri[i]==None or anno_0_passeggeri[i+1]==None):
            diff_anno_0.append(None)
        # Altrimenti viene calcolata la differenza tra i due mesi e viene inserita in diff_anno_0
        else:
            diff_anno_0.append(anno_0_passeggeri[i+1]-anno_0_passeggeri[i])

    # Stampo la lista contenente le differenze tra i passeggeri mensili dell'anno 0
    print(diff_anno_0)

    # Calcolo la differenza tra i passeggeri di ogni mese dell'anno 1
    for i in range(11):
    
        # Se uno dei due mesi da confrontare non è disponibile, viene inserito None in diff_anno_1
        if(anno_1_passeggeri[i]==None or anno_1_passeggeri[i+1]==None):
            diff_anno_1.append(None)
        # Altrimenti viene calcolata la differenza tra i due mesi e viene inserita in diff_anno_1
        else:
            diff_anno_1.append(anno_1_passeggeri[i+1]-anno_1_passeggeri[i])

    # Stampo la lista contenente le differenze tra i passeggeri mensili dell'anno 1
    # print(diff_anno_1)

    # Inizializzazione di una lista vuota "risultato".
    risultato = []

    # Ciclo "for" che itera 11 volte.
    # "range(11)" produce una sequenza di numeri da 0 a 10.
    for i in range(11):
    
        # Verifica se uno dei valori nella lista "diff_anno_0" o "diff_anno_1" è None.
        # Se uno dei valori è None, allora la condizione dell'"if" sarà vera, e l'elemento "False" sarà aggiunto alla lista "risultato".
        if(diff_anno_0[i] == None or diff_anno_1[i] == None):
            risultato.append(False)
    
        # Verifica se la differenza tra i valori nella lista "diff_anno_0" e "diff_anno_1" è compresa tra -2 e 2.
        # Se la differenza rientra in questo intervallo, allora la condizione dell'"elif" sarà vera, e l'elemento "True" sarà aggiunto alla lista "risultato".
        elif(diff_anno_0[i] - diff_anno_1[i] in range(-2, 3)):
            risultato.append(True)
    
        # Se nessuna delle condizioni precedenti è vera, allora l'elemento "False" sarà aggiunto alla lista "risultato".
        else:
            risultato.append(False)

    # La funzione restituisce la lista "risultato".
    return risultato


    
    
# Utilizzo
"""
csv_file=CSVTimeSeriesFile('data.csv') 
time_series=csv_file.get_data()
lista=[1949,1954]
result=detect_similar_monthly_variations(time_series,lista)
print(result)
"""