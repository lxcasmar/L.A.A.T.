# EdgeTrading_beta

## Setup instructions:

1. Install Python

2. Setup a virtual environment:

```
python -m venv env
```

3. Activate the environment:
   Windows:

```
env\scripts\activate
```

Mac/Unix:

```
source env/bin/activate
```

4. Install the dependencies from the directories you need, which are located within each folder.

```
pip install -r requirements.txt
```

If you install anymore dependencies, make sure to do so and update requirements.txt:

 &nbsp; i. Get all the packages that are recognized in your environment:

```
pip freeze
```

&nbsp; ii. Copy from the terminal and paste into requirements.txt.

5. Add config.py file to directory with bot.py (not here yet):

```
API_KEY_ID = '...'
API_SECRET_KEY = '...'
```
Get the keys from google doc
