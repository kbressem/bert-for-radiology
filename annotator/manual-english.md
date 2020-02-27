# Operating Instructions for Text Annotator

The annotator is a Python script and cannot be executed without Python. Therefore, some preparatory steps are necessary.  

## 1. Installing von Pyhton3
### Linux (Ubuntu)
On Linux, Python3 should be installed from the start. If this is not the case, open a terminal with [Ctrl] + [Alt] + [T] and install Python3 with the following command.

```bash
sudo apt-get install python3
```

### Linux (Ubuntu) subsystem for Windows

Python3 is not preinstalled in the Linux subsystem for Windows. The command is the same as in normal Ubuntu.

### Mac
On Mac, it is recommended to install Python3 with __homebrew__:  

#### Installing Homebrew
Open with Command (Mac key) and Space Spotlight and enter 'Terminal'. [Homebrew](https://brew.sh/) can be installed with the following command, which is copied to the terminal:

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew
/install/master/install)"
```
If necessary, brew must be added to the system path (PATH):

```bash
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```
#### Installing Python with Homebrew
Again via terminal:

```bash
brew install python
```

## 2. Setting up a virtual environment

If you ever plan to run other scripts again, it is advisable to work with virtual Python environments. Here pip-venv or Anaconda are suitable. Anaconda has the advantage that it is both package manager and manager for the virtual environments, while with pip-venv you would need pip as package manager additionally.

### Installing Anaconda on Linux
Several steps are necessary here, so we would like to refer to the following __[blog post (click)](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart). __

### Installing Anaconda on Mac
There are also very good external __[instructions (click)](https://www.datacamp.com/community/tutorials/installing-anaconda-mac-os-x)__

### Setting up a virtual environment
Enter the following code into the terminal:

```bash
conda create --name=simple-annotator numpy pandas
conda activate simple annotator
```
These commands create a new virtual environment called `simple-annotator` and simultaneously install the pandas and numpy packages with the latest version. These are required by the annotator.

Alternatively, if you don't want to use virtual environments (e.g. on the Linux subsystem) you can use pip only:


``` bash
pip install --user numpy pandas
```
The `--user` flag is useful to prevent system programs from being updated, because e.g. in Ubuntu important system packages depend on Python. The rule is: __Never use pip with sudo!__.


## 3. Starting the Annotator
Unpack the package in any directory, e.g. in the _Documents_ folder.
Now open the terminal, if it is not already open, and activate the previously created environment. Then navigate to the folder. Assuming the folder has been unpacked to _simple-annoator_: _/path/to/simple-annoator_

```bash
conda activate simple-annotator
cd /path/to/simple-annoator
python3 simple-annotator.py
```
Please maximize the terminal immediately.

## 4. Cache
Every keystroke should trigger an automatic cache, but unfortunately it may happen in rare cases that the program crashes and data may be lost. Therefore, it is advisable to make regular backup copys of the file `file_dir.csv` in the folder `/data`.

## 5. Operating the Annotator
The user interface is written in English.
Annotations are made via the keys [1], [2], [3], to [9]. Additionally, there is the possibility to mark findings as unevaluable ([x]), to select [a] or deselect [d] all annotations. In addition, a rating should be given for each annotation indicating your level of certainty (low, medium, high), which may be selected with the up/down arrow keys. [d] deletes the entire selection.
There is also the possibility to jump only between annotated reports or non-annotated reports ([A]).

## 6. Guide to the Annotation of Thoraxic Images
Some reports for chest X-rays might contain unclear wordings. To still achieve a high interrater agreement we would suggest the following procedure:

### Unevaluable
- If foreign material is described as idem (not changed).
- If less than three findings are mentioned (e.g. only "No pneumothorax after central venous catheter"). If the report would instead read: "No congestion, no infiltrates, no effusion" we would suggest to annotate it as absent pneumothorax.
- Severe dictation errors which blur the meaning of the text report.

### Congestion:
Congestion would be indicated by:
- (Low)central congestion signs
- Pulmonary edema/pulmonary fluid retention

Congestion should __ NOT__ be considered, when there are:
- No signs of higher degrees of congestion
- No congestion when lying down.
- Centrally accentuated fluid retentions without higher degree of congestion.

### Attenuation
After annotation of the first 500 texts, we found that it was often not possible to distinguish between infiltrates or dystelectasis.

Attenuation is present in case of:
- Infiltrates/ dystelectases/ atelectases/ reduced ventilation etc., even if these are described as discrete.

There is __NO__ attenuation in case of:
- "Masked infiltrates possible in the basal parts of the lung", an exception can be made if this appears to be reasonable in the context: "Question wording: High CRP, RGs, productive cough. Findings/assessment: No confluent infiltrates when lying down. Reduced ventilation in the basal parts of the lung, here masked infiltrates may be present. "
- Lung nodule/tumor
- Foreign material (e.g. metal splinters)
- Pleural shadow

### Pleural effusion
Pleural effusion can be:
- Blunting of the costophrenic/cardiophrenic angle, fluid within the horizontal or oblique fissures, seropneumothorax.

There is __NO__ effusion in case of:
- Homogeneous reduction of transparency (unless evaluated as effusion)

### Pneumothorax
Pneumothorax may be indicated by:
- pneu, pneumothorax, seropneumothorax etc.

There is __NO__ presence of pneumothorax in case of:
- 'No evidence of pneumothorax in a lying position' or 'as far as assessable in a lying position no pneumothorax or similar'
- Deep costophrenic angle, if this is mentioned without evaluation.  

### Malposition
#### Central venous catheter (CVC)
- CVC, Shaldon, Dialysis catheter, PICC etc. In short, everything that goes into a vein and about which medication could be given.

#### Tube
- Tube, tracheal cannula, tracheostoma etc.

#### Thoracic drain
- Thoracic drain, chest tube etc.

#### Stomach tube
- Stomach tube, tiger tube, feeding tube etc. But not: PEG

#### Malposition
- CVC: buckling, turned over or other explicit malposition
- Tube: ending < 2 cm above the carina
- Chest tube: kinking or other explicit malposition. Atypical projections do not correspond to malposition.
- Gastric tube: loops outside the stomach, end with projection on the oesophagus etc.
