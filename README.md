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
env                 |   reviewed but not tested
etcd                |   reviewed but not tested
file                |   reviewed but not tested
fileglob            |   reviewed but not tested
first_found         |   tested
flattened           |   
hashi_vault         |
indexed_item        |
ini                 |
inventory_hostname  |
items               |
lines               |
list                |
nested              |
password            |
pipe                |
random_choice       |
redis_kv            |
sequence            |
shelvefile          |
subelements         |
template            |
together            |
url                 |   reviewed but not tested

