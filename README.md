# Gonad
This is a simple project to profile and do Data Quality test of your Enterprice Data Warehouse

It's using the following librarys
- pytest
- pytest BDD
- jinja2
- and probably some more

Everything should be included eighter in the docker image or in the requirements.txt

## How to use
Open the project in devcontainer in VSCode, all dependencies should be installed automatically

### Configure
#### Update your profile in the profiles.yaml file

```yaml
project:
    target: your_target
    outputs:
        your_target:
            type: sqlserver
            server: your_server
            port: your_port
            user: your_user
            password: your_password
            database: your_database

```

#### Update the identifier section in the config.yaml file
```yaml

```

### Run the tests


3. Run the following command
```bash
pytest -m "data_mart" -s -v --alluredir=reports
```


## TODO:
Get Allure to work to serve nice looking test reports in a website