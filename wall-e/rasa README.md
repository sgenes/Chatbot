Create nlu.md defining all intents
```
## intent:greet
- hey 
- hello 
...
```

create config.yml
```
langugage: "en_core_web_md"
...
```


<b> Training model</b>
```
python3 -m rasa_nlu.train -c .yml --data data/nlu.md -o models --fixed_model_name nlu --project current --verbose
```
