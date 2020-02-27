Constructing a Rule-Based Algorithm to Classify Radiology Text Reports
================

In order to ensure the best possible comparability of the
rule-based algorithm developed here, the entire algorithm is developed
only on the annotated data sets.

### Preliminary considerations

Theoretically, it should be possible to create a very accurate (even
more accurate than BERT-based algorithms) rule-based algorithm for the
classification of text reports. However, this is challenging.
Accurate knowledge of the text structure as well as the findings
structure is necessary to recognize pitfalls.

#### Unclear statements

Radiological text reports are not always clearly formulated and sometimes 
leave room for interpretation. 

**Example**:

> “Maskierte Infiltrate in den basalen, minderbelüfteten Arealen
> möglich”

Roughly translating into:

> “Masked infiltrates possible in basal, poorly ventilated areas.”

This wording, which is often found in reports of intensive care chest X-rays,
expresses either the radiologist's uncertainty about 
infiltrates as a cause for the patient's elevated infection levels due do insufficient 
ventilation of the lungs OR, that she/he does not wish to make a clear decision in ruling out pneumonia, even though the X-ray does not actually show any clear indications for its presence.
Clinical practice shows that the above-referenced formulation rather indicates that no clear signs of pneumonia can be seen in the chest X-ray. 

#### Insufficient and therefore unevaluable reports

Findings are considered to be unevaluable if they do not contain
sufficient information, e.g. if no explicit statement is made about the
location of the foreign materials, but these are instead described as “no
change of foreign materials” (German: “Fremdmaterial idem”). However,
the word “idem” should not always mark a report as unevaluable, as it
can also be used if no change occured. This is particularly tricky and no
simple rule can be established, as even perfectly sufficient report texts
might contain this expression. 

**Examples**:

> Kein Pneumothorax nach Drainagenanlage. Darüber hinaus kein
> Befundwandel

> No pneumothorax after inserting a chest tube. No further change.

Not evaluable.

> Herz nicht verbreitert. Keine Stauung. Kein Erguss. Kein Infiltrat.
> Fremdmaterial idem.

> Heart not enlarged. No congestion. No effusion. No infiltrate. Foreign
> material idem.

Not evaluable. No statement regarding pneumothorax, still it can be
assumed that there is none, since such an important but rare finding is
probably always reported if present , but often not reported if not. However, one cannot draw a conclusion regarding the therapy aids such as catheters, drains etc.

> Herz nicht verbreitert. Keine Stauung. Kein Erguss. Kein Infiltrat.
> Fremdmaterial idem (ZVK, TK).

> Heart not enlarged. No congestion. No effusion. No infiltrate. Foreign
> material idem (zentral venous catheter, tracheal cannula).

Evaluable. The foreign materials are named explicitly, but this is not always the case. 

> Herz nicht verbreitert. Keine Stauung. Kein Erguss. Kein Infiltrat.
> Neuer ZVK von rechts, kein Pneumothorax. Sonst Fremdmaterial idem.

> Heart not enlarged. No congestion. No effusion. No infiltrate. Foreign
> material idem (zentral venous catheter, tracheal cannula).

Not evaluable, as there is no information about the other unchanged
materials. 

#### Unlikely differential diagnoses

If a differential diagnosis is mentioned, it is difficult to exclude this
string:

**Example**:

> Rechts zentral betonte flächige Verschattung, vereinbar mit
> pneumonischer Infiltration DD bei vermehrter Gefäßzeichnung
> stauungsbedingt

> Right central shading, compatible with pneumatic infiltration DD with
> increased vascular drawing due to congestion

In this case, there is probably no congestion (congestion should be symmetrical) and
it should thus be annotated accordingly. 
   

``` r
library(tidyverse)
```

    ## ── Attaching packages ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── tidyverse 1.2.1 ──

    ## ✔ ggplot2 3.2.1     ✔ purrr   0.3.2
    ## ✔ tibble  2.1.3     ✔ dplyr   0.8.3
    ## ✔ tidyr   1.0.0     ✔ stringr 1.4.0
    ## ✔ readr   1.3.1     ✔ forcats 0.4.0

    ## ── Conflicts ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── tidyverse_conflicts() ──
    ## ✖ dplyr::filter() masks stats::filter()
    ## ✖ dplyr::lag()    masks stats::lag()

``` r
library(magrittr)
```

    ## 
    ## Attaching package: 'magrittr'

    ## The following object is masked from 'package:purrr':
    ## 
    ##     set_names

    ## The following object is masked from 'package:tidyr':
    ## 
    ##     extract

### Loading the text files stored as single R file:

``` r
textreports <- read_csv("/media/bressekk/0B36170D0B36170D/Textdaten_csv/all_data.csv")
```

    ## Parsed with column specification:
    ## cols(
    ##   Filename = col_character(),
    ##   Stauung = col_double(),
    ##   Verschattung = col_double(),
    ##   Erguss = col_double(),
    ##   Pneumothorax = col_double(),
    ##   Thoraxdrainage = col_double(),
    ##   ZVK = col_double(),
    ##   Magensonde = col_double(),
    ##   Tubus = col_double(),
    ##   Materialfehllage = col_double(),
    ##   Annotator = col_character(),
    ##   Confidence = col_character(),
    ##   text = col_character(),
    ##   DICOM_path = col_character()
    ## )

### Removal of unevaluable reports

Since the annotations already contain if a finding was useful or
not, this was done in advance. In the final model, however, this will be
built in.

Removal by fixed
strings:

``` r
unevaluable = "Fremdmaterial idem|kurzfristigen Verlauf kein Befundwandel"
textreports %<>% filter(!str_detect(text, unevaluable))
```

### Set up dataframe for annotations

``` r
set.seed(081219)
train <- sample(1:nrow(textreports), round(0.8*nrow(textreports)), F)


annotations <- tibble(stauung = rep(NA, nrow(textreports)),
                      erguss = NA,
                      verschattung = NA,
                      pneumothorax = NA, 
                      zvk = NA, 
                      thoraxdrainage = NA, 
                      magensonde = NA, 
                      tubus = NA, 
                      fehllage = NA)
```

### Congestion (German: Stauung)

In case the finding is not mentioned, it is assumed that it is not
present (reasonable as unevaluable reports have previously been
excluded. 

``` r
congestion_names <- "stauung|dekompensat|volumen|flüssigkeitseinlag|gestaut|ödem"

annotations$stauung <-  ifelse(
                          str_detect(
                            str_to_lower(textreports$text), 
                            congestion_names), 
                          annotations$stauung, 
                          0) 
```

The findings are all printed out in the terminal, the text is
manually evaluated and the strings are then copied to the vectors for
`negations` or `positive_finding`.

``` r
negations <- read_csv("negative_congestion.csv", col_names = F) %>% 
  select("X1") %>% 
    unlist() %>% 
      str_to_lower()

positive_finding <- read_csv("positive_congestion.csv", col_names = F) %>% 
  select("X1") %>% 
    unlist() %>% 
      str_to_lower()
```

Positive findings should be evaluated first. “congestion” and
“no congestion” will be rated as positive initially, but the second
finding will then be labeled as negative in the next loop.

``` r
for (str in positive_finding) {
  annotations[train,]$stauung <- ifelse(
                                    str_detect(
                                      str_to_lower(textreports[train,]$text), 
                                      str), 
                                    1, 
                                    annotations[train,]$stauung) 
}

for (str in negations) {
  annotations[train,]$stauung <- ifelse(
                                    str_detect(
                                      str_to_lower(textreports[train,]$text), 
                                      str), 
                                    0, 
                                    annotations[train,]$stauung) 
}
```

Evaluate accuracy of rule-based algorithm on training
data

``` r
mean(annotations[train,]$stauung == textreports[train, ]$Stauung, na.rm = T)
```

    ## [1] 0.9010582

Missed annotations on training data

``` r
mean(is.na(annotations[train,]$stauung))
```

    ## [1] 0.012023

Accuray with missed set to
0/FALSE

``` r
annotations[train,]$stauung <- ifelse(is.na(annotations[train,]$stauung), 
                                      0, 
                                      annotations[train,]$stauung)

mean(annotations[train,]$stauung == textreports[train, ]$Stauung, na.rm = T)
```

    ## [1] 0.9012023

Evaluate accuracy of rule based algorithm on test data

``` r
for (str in positive_finding) {
  annotations[-train,]$stauung <- ifelse(
                                    str_detect(
                                    str_to_lower(
                                      textreports[-train,]$text), str), 
                                    1, 
                                    annotations[-train,]$stauung) }

for (str in negations) {
  annotations[-train,]$stauung <- ifelse(
                                    str_detect(
                                      str_to_lower(
                                        textreports[-train,]$text), str), 
                                    0, 
                                    annotations[-train,]$stauung) }

mean(annotations[-train,]$stauung == textreports[-train, ]$Stauung, na.rm = T)
```

    ## [1] 0.9304933

Missed annotations on test data

``` r
mean(is.na(annotations[-train,]$stauung))
```

    ## [1] 0.06694561

Accuracy with missed annotations set to
0/FALSE

``` r
annotations[-train,]$stauung <- ifelse(is.na(annotations[-train,]$stauung), 
                                       1, 
                                       annotations[-train,]$stauung)

mean(annotations[-train,]$stauung == textreports[-train, ]$Stauung, na.rm = T)
```

    ## [1] 0.916318
