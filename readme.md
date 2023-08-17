# WIP relational algebra tree generator

## Usage

Write somewhat of a query intermixed with latex in the `input` file such as:

```
// This is a comment. 

// SELECT NomeConvenzione, SUM(NumeroPersone) AS TotalePersone
// FROM ClientiConvenzionati
// JOIN CorseConvenzionate ON IDCliente = IDConvenzionato
// JOIN Corse c ON CorseConvenzionate.CodPrenotazione = c.CodPrenotazione
// WHERE c.DataInizio > '2021-01-01'
// GROUP BY NomeConvenzione
// HAVING SUM(NumeroPersone) > 20

project (

    filter(
        group_by (

                join (
                    join (
                    ClientiConvenzionati, CorseConvenzionate
                    , IDCliente = IDConvenzionato
                    ) ,
                    filter(Corse c
                    , c.DataInizio > '2021-01-01'
                    )
                    , CorseConvenzionate.CodPrenotazione = c.CodPrenotazione
                )

            , {NomeConvenzione}, {SUM(NumeroPersone)}
        )
        , SUM \lpar NumeroPersone\rpar > 20
)
, {NomeConvenzione, SUM(NumeroPersone) \,\,AS\,\, TotalePersone})
```

Get a nice result by running the following command, where `2` is the tree width:

```
python3 parser.py input 2
```

![pic](https://github.com/mell-o-tron/RelationalAlgebraGenerator/blob/main/preview.png)
