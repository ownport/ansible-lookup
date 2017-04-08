# ansible-lookup

Research project of Ansible Lookups 

Changes:
- for several components removed dependencies to Ansible templates and loaders


## How to use from command line

```shell
$ lookups <lookup> <terms> <params> <kwargs> 
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
inventory_hostname  |   review is required
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

