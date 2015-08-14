# FEC data processor

## Setup

```
mkvirtualenv fec-ie-2012
pip install -r requirements.txt
```

## Usage

```
cd fec-ie-2012
workon fec-ie-2012
```

Remove amendments and filter to president only:

```
./fec.py --office P input.csv output.csv
```

Keep amendments and filter to Senate only:

```
./fec.py --office S --keep-amendments input.csv output.csv
```
