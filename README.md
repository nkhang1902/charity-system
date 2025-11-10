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

Build layer command (for deploying only):
```
PYTHON_VERSION="3.12"; LAYER_DIR="layer"; LAYER_PATH="$LAYER_DIR/python/lib/python${PYTHON_VERSION}/site-packages"; ZIP_NAME="layer.zip"; mkdir -p $LAYER_PATH && pip install --platform manylinux2014_x86_64 -t --implementation cp --only-binary=:all: --upgrade --target=$LAYER_PATH -r requirements.txt && cd $LAYER_DIR && zip -r ../$ZIP_NAME python > /dev/null && cd .. && echo "Layer zip created: $ZIP_NAME"
```

You can run Flask application with the following command:

```
docker compose up -d
python -m app.app
```