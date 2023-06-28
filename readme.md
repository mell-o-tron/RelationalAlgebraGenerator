# WIP relational algebra tree generator

## Usage

Write somewhat of a query intermixed with latex in the `input` file such as:

```
project(
    group_by (
        join( Studenti, Esami, \small\texttt{S.matricola}=\texttt{E.matricola as nEsami})
        , {nome, cognome} ,{count(*)}
    )
, {S.nome, S.cognome, count(*)})
```

Get a nice result by running the following command, where `2` is the tree width:

```
python3 parser.py input 2
```

![image](https://github.com/mell-o-tron/RelationalAlgebraGenerator/blob/main/preview.png)
