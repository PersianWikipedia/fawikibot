source ~/venv/bin/activate
python3 ~/core/pwb.py ANBcounter 
python3 ~/core/pwb.py GANtable
python3 ~/core/pwb.py FACtable
python3 ~/core/pwb.py categorize -newpages:500 -always
python3 ~/core/pwb.py categorize -random:500 -always