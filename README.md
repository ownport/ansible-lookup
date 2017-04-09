# ansible-lookup

Research project of Ansible Lookups 

Changes:
- for several components removed dependencies to Ansible templates and loaders


## How to use from command line

```shell
$ ./ansible-lookups --help 
usage: ansible-lookups [-h]
                         {redis_kv,sequence,nested,ini,file,dnstxt,shelvefile,cartesian,first_found,dict,etcd,subelements,env,indexed_items,csvfile,flattened,password,random_choice,url,items,credstash,dig,lines,together,pipe,consul_kv,hashi_vault,fileglob}
                         ...
  
  optional arguments:
    -h, --help            show this help message and exit
  
  actions:
    {redis_kv,sequence,nested,ini,file,dnstxt,shelvefile,cartesian,first_found,dict,etcd,subelements,env,indexed_items,csvfile,flattened,password,random_choice,url,items,credstash,dig,lines,together,pipe,consul_kv,hashi_vault,fileglob}
                          Loolup actions handler
      redis_kv            Action: redis_kv
      sequence            Action: sequence
      nested              Action: nested
      ini                 Action: ini
      file                Action: file
      dnstxt              Action: dnstxt
      shelvefile          Action: shelvefile
      cartesian           Action: cartesian
      first_found         Action: first_found
      dict                Action: dict
      etcd                Action: etcd
      subelements         Action: subelements
      env                 Action: env
      indexed_items       Action: indexed_items
      csvfile             Action: csvfile
      flattened           Action: flattened
      password            Action: password
      random_choice       Action: random_choice
      url                 Action: url
      items               Action: items
      credstash           Action: credstash
      dig                 Action: dig
      lines               Action: lines
      together            Action: together
      pipe                Action: pipe
      consul_kv           Action: consul_kv
      hashi_vault         Action: hashi_vault
      fileglob            Action: fileglob
```
to get help for specific lookup action
```shell
$ ./ansible-lookups <action> --help
```
for example:
```shell
$ ./ansible-lookups env --help
usage: ansible-lookups env [-h] [--terms TERMS]

optional arguments:
  -h, --help     show this help message and exit
  --terms TERMS  lookup terms as JSON string
```

To run lookup action you need to pass `terms` parameter as JSON string 
```shell
$ ./target/ansible-lookups env --terms='["LANG","LC_NAME"]'
["en_US.UTF-8", "en_US.UTF-8"]
$
$ ./ansible-lookups dig --terms '["google.com"]'
["216.58.214.206"]
```

## Lookups status

Name                |   Status                     
------------------- | ---------------------------- 
cartesian           |   tested
consul_kv           |   reviewed but not tested
creadstash          |   reviewed but not tested 
csvfile             |   reviewed but not tested
dict                |   reviewed but not tested
dig                 |   reviewed but not tested
dnstxt              |   reviewed but not tested
env                 |   tested
etcd                |   reviewed but not tested
file                |   reviewed but not tested
fileglob            |   reviewed but not tested
first_found         |   tested
flattened           |   tested
hashi_vault         |   reviewed but not tested
indexed_item        |   tested
ini                 |   reviewed but not tested
inventory_hostname  |   removed
items               |   tested, can be merged with `flattened`
lines               |   reviewed but not tested
list                |   removed
nested              |   tested
password            |   reviewed but not tested
pipe                |   reviewed but not tested
random_choice       |   reviewed but not tested
redis_kv            |   reviewed but not tested
sequence            |   reviewed but not tested
shelvefile          |   reviewed but not tested
subelements         |   reviewed but not tested
template            |   removed
together            |   reviewed but not tested
url                 |   reviewed but not tested

