#### Prerequisites

In order to package your dependencies locally, you need to have `Python3.13` installed locally. You can create and activate a dedicated virtual environment with the following command:

```
python3.13 -m venv ./venv
source ./venv/bin/activate
```

You will need to first install `werkzeug`, `boto3` dependencies, as well as all other dependencies listed in `requirements.txt`. It is recommended to use a dedicated virtual environment for that purpose. You can install all needed dependencies with the following commands:

```
pip install werkzeug boto3
pip install -r requirements.txt
```

You can then run the application with the following command:

```
docker compose up -d
python app/app.py
```