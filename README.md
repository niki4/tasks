# tasks
delayed tasks launch

Only standard Python 3 library, only hardcore :-)

Currently, under construction. 

CLI prototype is ready so you can play around with running functions and methods from your terminal, like this
```shell
(venv)> python example_tasks.py mult --params "{'operands':[3,2,8]}"
all_functions [('multi_print', <function task.<locals>.decorator.<locals>.wrapper at 0x024E6A98>)]
{}
all_classes [('Multiply', <class '__main__.Multiply'>)]
Multiply cls_obj.name: mult <class 'str'>
args.command mult <class 'str'>
args Namespace(command='mult', params="{'operands':[3,2,8]}")
args.params {'operands':[3,2,8]}
Result: 48
```

```shell
(venv)>python example_tasks.py multi_print --params "{'msg':'foo','count':5}"
all_functions [('multi_print', <function task.<locals>.decorator.<locals>.wrapper at 0x02386A98>)]
{}
all_classes [('Multiply', <class '__main__.Multiply'>)]
Multiply cls_obj.name: mult <class 'str'>
args.command multi_print <class 'str'>
args Namespace(command='multi_print', params="{'msg':'foo','count':5}")
args.params {'msg':'foo','count':5}
multiprint -----
Result: foo
foo
foo
foo
foo
```

Stay tuned!
