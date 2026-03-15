-	How big is the dataset?
wc -l clean_dialog.csv
du -h clean_dialog.cs
10000 lines
-	What’s the structure of the data? (i.e., what are the field and what are values in them)
head -n 5 clean_dialog.csv
head -n 1 clean_dialog.csv | tr ',' '\n' | nl
dialogs
-	How many episodes does it cover?
csvtool -t ',' col 1 clean_dialog.csv | tail -n +2 | sort | uniq | wc -l
500
-	During the exploration phase, find at least one aspect of the dataset that is unexpected – meaning that it seems like it could create issues for later analysis.
grep -n ",," clean_dialog.csv | wc -l
csvtool -t ',' col 2 clean_dialog.csv | tail -n +2 | sort | uniq -c | sort -nr | head -20
dialogs 

