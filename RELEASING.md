# Releasing the AMSD clld app

```shell
git clone https://github.com/clld/amsd
git clone --branch v2026.07.1 --depth 1 https://github.com/clld/amsd-data
cd amsd
pip install -e .[test]
```


```shell
clld initdb development.ini --cldf ../amsd-data/cldf/Generic-metadata.json
```

```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 amsd > amsd.sql.gz
```

