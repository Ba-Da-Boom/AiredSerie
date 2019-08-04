#!/bin/bash
read -p "name of the serie you are looking for : " NAME
python3 rserie.py $NAME >> fiche_serie.txt && echo "Finished task with rserie.py" .


