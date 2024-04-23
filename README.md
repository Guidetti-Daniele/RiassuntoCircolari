Riassunto Circolari
===
***
Scheduled Job
-
### Parameters
 - ***-folder_path***    
Path to the folder containing all the files
 - ***-base_url***   
Base URL for the DB API
- ***-db_api_key***   
Key for the DB API
 - ***-prefix_file_name***   
Name of the file located in the files folder that contains the LLM prefix
 - ***-api_key***   
OpenAI API key
 - ***-openai_model***   
OpenAI model, for example "gpt-4-turbo-preview"
 - ***-model_pricing_input*** (Optional)  
OpenAI Input pricing per million tokens, this is used to calculate the cost per document when debugging
- ***-model_pricing_output*** (Optional)  
The same but for the output tokens

### Prefix file
This file is located in the folder where all the PDF files are stored (***-folder_path***).   
Three prefixes are needed for this script, and you can separate them using these keywords:
- ***#PREFIX***   
This is the LLM prefix, always used
- ***#JSON_PREFIX***   
This text is sent to the LLM before parsing the data from a text and saving it in a JSON string
- ***#TEXT_PREFIX***   
This text is sent to the LLM before summarizing the text

Example:

```
#PREFIX
Se la domanda inizia per JSON:{
Rispondi solamente con il formato json dei dati richiesti dall'utente.
}

Se la domanda inizia per TEXT:{
Aiuti le persone a guardare gli argomenti delle circolari del registro classeviva.
Le tue risposte devono essere complete ma brevi e devono contenere tutte le informazioni importanti contenute nelle circolari, scrivendo in elenco puntato un riassunto completo per ogni circolare.
Devi specificare il contenuto di ogni circolare, il suo numero indicato in (Circolare n.) e il suo nome, le tue risposte devono essere lunghe.
}
#JSON_PREFIX
JSON
Dati richiesti:
{
"Numero": (Numero della circolare, se non specificato è -1),
"Nome": (Nome della circolare),
"Destinatari": (rispondi usando alcune tra queste parole come lista: "Studenti", "Docenti", "Genitori", "Personale"),
"Classi": (Le classi che riguardano la circolare come lista, se tutte rispondi con ["##"], scrivi il numero della classe a cifre e non parole (Esempio: Quinta CT -> 5CT , IIRF -> 2RF), se la sezione non viene specificata rispondi con (ESEMPIO: classi quarte -> 4#) , NON rispondere in altri formati)
}

Se questi dati si ripetono uniscili tutti in un unico blocco dati
#TEXT_PREFIX
TEXT
```

***
Server
-
### Execution parameters
- ***-db_connection_string***    
  Path to the SQLite DB used to store the parsed documents
- ***-parameters_file***   
  Path to the JSON file that contains the parameters

### Parameters file
Example:

```json
{
  "circolari_name": "circolari",
  "circolari_rows": {
    "hash": "TEXT PRIMARY KEY",
    "numero": "INTEGER",
    "nome": "TEXT",
    "data": "DATE",
    "destinatari": "TEXT",
    "classi": "TEXT",
    "riassunto": "TEXT"
  },
  "comunicazioni_name": "comunicazioni",
  "comunicazioni_rows": {
    "hash": "TEXT PRIMARY KEY",
    "nome": "TEXT",
    "data": "DATE",
    "destinatari": "TEXT",
    "classi": "TEXT",
    "riassunto": "TEXT"
  },
  "not_to_add": [
    "1#",
    "2#",
    "3#",
    "4#",
    "5#",
    "##"
  ],
  "all_class": "Tutte le classi",
  "all_classes_db": "##",
  "all_dest": "Tutti",
  "circ_type": {
    "circolari": "Circolari",
    "comunicazioni": "Comunicazioni"
  },
  "db_api_key_hash": "ddf5c7a9aa3b43aadb06c7683d43fe215aa739ef75b9d6f58c3879be263f4e72"
}
```

- ***circolari_name***    
Name for the table used to store the circulars in the database
- ***circolari_rows***    
All the rows used to store the circulars in the database
- ***comunicazioni_name***    
Name for the table used to store the notices in the database
- ***comunicazioni_rows***    
All the rows used to store the notices in the database, this one does not require the row for the document's number
- ***not_to_add***   
This array contains every class symbol that should not be displayed on the server page, but is needed to select the documents.  
For example if in the server page someone selects 2CT, then all the documents that contain 2# as a class will be selected
- ***all_class***  
This is the text showed in the *select all the classes* section
- ***all_dest***  
This is the text showed in the *select all the recipients* section
- ***all_classes_db***  
This is the symbol used in the database when a document refers to all the classes
- ***circ_type***  
This is used to tell the server the names of the two types of documents to show in the *select document* list, and the table they refer to.
- ***db_api_key_hash***  
This is the SHA256 hash of the key used in the DB API, the key used in the example is "example_key"