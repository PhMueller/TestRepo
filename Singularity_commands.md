## Container Tips und Befehle

### 1) Erzeugen von Images:

```sudo singularity build <Name>.sif <Pfad zu Image-Rezept> ```

oder als Sandbox:

```sudo singularity build --sandbox <Name>/ <Pfad zu Image-Rezept> ```

### 2) Starten eines Images: 

```sudo singularity instance start <Name>.sif <Instance-Name>```

Falls Sandbox:
in übergeordneten Ordner navigieren und 

```sudo singularity shell --writable <Name>/```

allgemeine Tips unter: \
https://sylabs.io/guides/3.4/user-guide/build_a_container.html

### 3) Management von aktiven Instanzen 

Auflisten:\
```sudo singularity instance list```

Stoppen:\
```sudo singularity instance stop <Instance Name>```

### 4) Misc:

- Einmal sudo, immer sudo!
- Alles Pickleable! Wenn configspace verwendet-> cast to json!
- copy: \
  ```sudo cp -r ~/Dokumente/Code/HPOlib2_container/hpolib/ /home/philipp/Dokumente/Images/xgboost/home/miniconda/lib/python3.7/site-packages/```
- link in instance: \
```/home/philipp/Dokumente/Images/xgboost/home/miniconda/lib/python3.7/site-packages/hpolib```

Ablauf:
-------
- Container erstellen. Daten müssen vorhanden sein!
- Container müssen auf Singularity hochgeladen sein, sonst einstellung use_instance! --> umständlich und nicht erläutert
- Checken ob Container schon verfügbar. 
- Fehler weitergabe etwas erschwerlich
- Aktuell: Instanz starten mit fixem Namen. Die ist auch so genannet in Client/Abstract_benchmark. \
--> Console: \
```singularity instance start /home/philipp/Dokumenete/images/xgboost/ Test``` 
- Dann server aufruf.
(```singularity run instance://Test XGBoostOnMnist Test``` <-- startet Server)
- Dann xgb_example: Das ruft aufch client/abstract_benchmark auf.  
- CLient/abstract_bench ruft momentan noch nicht server/abstract_benchmark auf. 
- nächster Versuch: alles wieder auf normal + funktion schöner machen für einstellungen! (Verbesserung)