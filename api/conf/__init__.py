import yaml
from schemas import Secrets, Config


with open("conf/secrets.yaml") as f:
    secrets = Secrets(**yaml.safe_load(f))

with open("conf/base.yaml") as f:
    config = Config(**yaml.safe_load(f))
