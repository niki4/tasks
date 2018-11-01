# tasks
delayed tasks launch

Currently, under construction. 

## Command-line interface (CLI):
Built using only standard Python 3 library, only hardcore :-)

```shell
(venv)> python example_tasks.py mult --params "{'operands':[3,2,8]}"
48
```

```shell
(venv)> python example_tasks.py multiprint --params "{'msg':'foo','count':5}"
foo
foo
foo
foo
foo
```

## HTTP Rest API

Built using Django and django-rest-framework.

To set solution up, run following commands (Linux):

```shell
export DJANGO_SECRET_KEY='blah'
```

```shell
python3 manage.py migrate
```

```shell
chmod +x example_tasks.py
```

```shell
python3 manage.py runserver
```

Now open a browser at http://127.0.0.1:8000/ and play with DRF UI.

Send request to http://127.0.0.1:8000/tasks/ endpoint with following body
```json
{
  "task_name": "multiprint",
  "params": {"msg": "hello", "count": 2}
}
```
And you get a response with the task result:
```json
{
  "result": "hello\nhello"
}
```

Alternatively, use curl to send requests.

Tasks requests and results are saved in DB, so you could always review them.

Stay tuned!
