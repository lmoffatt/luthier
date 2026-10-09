---
title: "tapp before"
author: Luciano
original: tapp before.odt
original_sha256: ee9fb8365db5d54ab85794b3cf7ca963d50bdd6a1a426abe12bd9c40446da53c
created: 2022-08-03T11:56:32
modified: 2022-08-03T11:56:42
words: 252
converted_by: import_notes v1; pandoc 3.10.2; gfm
note: the original is next to this file; this conversion is derived and may be redone
---
tapp, jeje

Despues de unos dias "estudiando" Haskell, Elixir y ADA (y "mirando APL"), encontre una idea que me puede servir de generadora para tapp/quimulun: la idea de que el signo "=" representa aserciones, es decir que un lado es igual al otro.

Esto se usa para pattern matching cuando algun simbolo es desconocido.

No se si se usa para aserciones con predicados, esa es mi idea: usar el igual para definir tipos subobjetos. (lo puedo indicar con guardas "\|").

La composicion la indico con puntos . (esto explica los metodos de clases)

El otro criterio es usar la "autodeteccion" de tipos.

El concepto mas importante es el de subObjeto: un subconjunto del objeto algebraico que cumple con un cierto predicado, un test.

Ahora un test o es exitoso o hay una explicacion de porque falla.

Entonces, la idea es que un tipo

maybe a = Nothing \| Just a

either a b = Left a \| Right b

sum a b = fist a \| second b

write a : a-\>string

como expreso el tipo de write a?

Identity id \| for_all x:a {id x = x}

maybe a {}

io a s: string write_fun: (a-\>s) read_fun: (s-\> (Maybe a, s)) =

io{ write = write_fun read= read_fun}

when (for_all x: a {x\| write \| read = (Just x,"")}) & (forall y: s {y\| read \| write = y})

io (write w) (read r) (type T) = forall T t:

functions are of two types

1\. predefined types

2\. user defined
