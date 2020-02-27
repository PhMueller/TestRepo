## Install
- Navigate into folder HPOlib3
- for normal xgboost local: ```pip install .[xgboost]```
- for xgboost and container: ```pip install .[xgboost,singularity] ```
- Use singularity on Cluster:
  Only Kisbat3 and \
  ```export PATH=/usr/local/kislurm/singularity-3.5/bin/:$PATH```

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


Erstellen von Container + Hochladen
-----------------------------------
### Before Starting
- Go to : https://cloud.sylabs.io/
- Click “Sign in to Sylabs” and follow the sign in steps.
- Click on your login id (same and updated button as the Sign in one).
- Select “Access Tokens” from the drop down menu.
- Click the “Manage my API tokens” button from the “Account Management” page.
- Click “Create”.
- Click “Copy token to Clipboard” from the “New API Token” page.
Paste the token string into your ~/.singularity/sylabs-token file.


###  1) Using the Remote Building Tool:
- Go to: https://cloud.sylabs.io/builder . In field 'Build recipe file is', change 'default' to 'automl'. 
  Append name of the benchmark. \
  Example: phmueller/automl/xgboost_benchmark.
- Paste Recipe in the form above
- Click on Build
- Verify Container
    - https://sylabs.io/guides/3.0/user-guide/signNverify.html#signing-your-own-containers \
    ``` singularity keys newpair ```
    (email is email from login to singularity)
- ```singularity pull --name <name after downloading> library://<username>/automl/<benchmark_name>``` \
  Example: \
  ```singularity pull --name xgboost_benchmark library://phmueller/automl/xgboost_benchmark ```
- ```singularity sign <name after download>``` \
  Example: \
  ```singularity sign xgboost_benchmark```
- ```singularity push <name after download> library://<username>/automl/xgboost_benchmark``` \
  Example: \
  ```singularity push xgboost_benchmark library://phmueller/automl/xgboost_benchmark```
  
###  1) Using the Command Line Building Tool:
- Create Image: ```sudo singularity build <container_name> <Pfad zu Image-Rezept>```
  Example:\
  ```sudo singularity build xgboost_benchmark hpolib/container/recipes/ml/Singularity.XGBoostOnMnist```
- Verify Container
    - https://sylabs.io/guides/3.0/user-guide/signNverify.html#signing-your-own-containers \
    ``` singularity keys newpair ```
    (email is email from login to singularity)
- ```singularity sign <container_name>```
- ```singularity push <container_name> library://<username>/automl/<container_name>```
