Riassunto Circolari
===
***
Scheduled Job
-
### Parameters
 - ***-folder_path***    
Path to the folder containing all the files
 - ***-db_connection_string***   
Path to the SQLite DB
 - ***-prefix_file_name***   
Name of the file located in the files folder that contains the LLM prefix
 - ***-api_key***   
OpenAI API key
 - ***-openai_model***   
OpenAI model, for example "gpt-4-turbo-preview"

### Prefix file
This file is located in the folder where all the PDF files are stored (***-folder_path***).   
Three prefixes are needed for this script, and you can separate them using these keywords:
- ***#PREFIX***   
This is the LLM prefix, always used.
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
Numero (Numero della circolare, se non specificato è -1),
Nome (Nome della circolare),
Destinatari (rispondi usando alcune tra queste parole come lista: "Studenti", "Docenti", "Genitori", "Personale"),
Classi (Le classi che riguardano la circolare come lista, se tutte rispondi con ["Tutte le classi"], se la sezione non viene specificata rispondi con "n#" , dove n è il numero della classe)
#TEXT_PREFIX
TEXT

```