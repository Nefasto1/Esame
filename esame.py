class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    #name

    # Inizializzo l'oggetto con il nome del file
    def __init__(self, name):
        self.name = name;

    # Funzione che riceve un array contenente [epoch, temperature] e restituisce un array contenente una lista contenente [temp_max, temp_min, temp_med]
    def get_data(self):

        # Provo ad aprire il file 
        try:
            file = open(self.name, 'r')
        except FileNotFoundError:
            raise ExamException('Errore nome file, File non Trovato')
        except Exception as e:
            raise ExamException('Errore apertura del file, {}' .format(e))         

        time_series = []   # Inizializzo l'array che conterrà l'output
        prev = 0     # Inizializzo la variabile che conterrà l'epoch precedente

        # Ciclo per ogni riga del file
        for line in file:

            # Provo ad eseguire lo split, in caso di errore restituisce una lista vuota
            try:
                element = line.split(",")
            except Exception as e:
                print('\nErrore nello split: {}' .format(e))
                element = []
            
            # Controllo che il numero di elementi della lista sia del numero corretto, in caso contrario salto la riga
            # (2 elementi -> [epoch | temperature])
            if(len(element) == 2):
                valida = True # Variabile Booleana

                # Controllo che l'epoch sia di tipo numerico e lo converto in intero
                try:
                    element[0] = int(float(element[0]))
                except Exception as e:
                    valida = False
                    
                # Controllo che la temperatura sia di tipo numerico e lo converto in float
                try:
                    element[1] = float(element[1])
                except Exception as e:
                    valida = False


                # Se una variabile non è di tipo corretto salto la riga 
                if valida:
                    # Se l'epoch corrente è maggiore di quello precedente i dati sono validi e li aggiungo alla lista in uscita 
                    if prev < element[0]:
                        prev = element[0]
                        time_series.append(element)
                    
                    # Se l'epoch è uguale a quello precedente la riga è duplicata, quindi restituisce errore
                    elif prev == element[0]:
                        raise ExamException('Errore, Riga Duplicata')

                    # Se l'epoch è minore di quello precedente la lista non è ordinata quindi restituisco errore 
                    # (Si potevano considerare come unico else ma ho preferito distinguere i casi per comprendere meglio l'errore)
                    else:
                        raise ExamException('Errore, Lista non ordinata')
                else:
                    print('\nRiga non valida, Tipo elementi non valido')
            else:
                print('\nRiga non valida, Numero elementi non valido')
            time_series.append(element)

        return time_series

def daily_stats(time_series):

    value = []   # Inizializzo l'array che conterrà l'output
    day = 0      # Inizializzo il giorno che sto controllando al momento
    c = 0        # Inizializzo il contatore che conterrà il numero di rilevazioni della temperatura in un giorno
    
    for element in time_series:
        # Mi calcolo il giorno a cui mi riferisco
        epoch = element[0] - (element[0] % 86400)

        # Controllo se il valore si riferisce ad un nuovo giorno o è il primo valore che ricevo
        if day < epoch:
            # Se il contatore è diverso da zero vuol dire che ho terminato il controllo di un giorno e ne sto controllando uno nuovo quindi salvo i risultati nella lista di output
            if not c == 0:
                # Divido la somma delle temperature registrata nella giornata per il numero di rilevazioni effettuate
                med /= c
                # Aggiungo il valore alla lista di output
                value.append([min, max, med])

            # Inizializzo i valori delle variabili al primo valore del nuovo giorno
            day = epoch
            max = element[1]
            min = element[1]
            med = element[1]
            c = 1

        # Controllo se il valore si riferisce allo stesso giorno dei precedenti
        # (Sono sicuro che sia uguale perché ho controllato prima se la lista è ordinata o contiene duplicati)
        else:
            # Incremento il contatore
            c += 1

            # Controllo se la temperatura è la massima raggiunta in quella giornata
            if max < element[1]:
                max = element[1]

            # Controllo se la temperatura è la minima raggiunta in quella giornata
            if min > element[1]:
                min = element[1] 
            
            # Sommo la temperatura alla variabile che conterrà la media
            med += element[1]
    
    value.append([min, max, med/c])
    return value