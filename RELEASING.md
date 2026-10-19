# Releasing the AMSD clld app

```shell
git clone https://github.com/clld/amsd
cd amsd
pip install -e .[test]
```


```shell
clld initdb development.ini --cldf ../../amsd/amsd-data/cldf/Generic-metadata.json
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
pg_dump -xO amsd > amsd.sql
zip amsd.sql.zip amsd.sql
rm amsd.sql
```

