---
title: "estoy perdido"
author: Luciano
original: estoy perdido.odt
original_sha256: 49c6fcf3809317544938a2c73b881760289c449cfe68231528a45de29677e264
created: 2023-03-02T11:27:43
modified: 2023-03-08T19:31:03
words: 271
converted_by: import_notes v1; pandoc 3.10.2; gfm
note: the original is next to this file; this conversion is derived and may be redone
---
Estoy perdido

estoy perdido!

Me puse a ver el tema de las presheaves (base los topoi) y como se codifica un grafo o un sistema dinamico en cateogry theory

conceptos claros

1\) Functores : implementaciones

2\) Natural transformations: traducir una implementacion en otra

Pero la pregunta importante es:

como expreso las definiciones matematicas como categoria, functor, grupo etc

empiezo con HoTT o con ZMT?

despues de leer hott me quedan dos ideas

1\) declaration: decis que algo tiene un tipo

2\) definition: decis como obtener el valor.

Ahora, tenemos dos tipos de definiciones las constructivas y las declarativas

----

Como defino cosas en un environment?

1\. Defino variables de un tipo dado sin decir cual es el valor, es decir parametros.

2\. Defino variables que son funcion de otras variables o parametros. Se verifica si los argumentos de las funciones cumplen con las precondiciones (es decir que pertenecen al tipo predicho. En caso que

El tipo se deduce por el calculo de tipos. Si el tipo derivado es mayor que el tipo del parametro, se indica.

3\. Defino funciones que son de un tipo dado (es decir que cumplen con ciertas postconditions) sin decir cual es la implmentacion.

4\. Defino funciones y doy su implementacion que depende de funciones cuya implementacion no se.

5\. Defino tipos de variables, diciendo cuales son sus postcondiciones

6\. Defino tipos de funciones, diciendo cuales son las postcondiciones.

7\. Defino una tupla de tipos de variables y de funciones con postcondiciones que involucran a toda la tupla. (crosscondiciones).

===\> solo hay una forma de definir y es en tuplas, que pueden tener uno o mas identificadores.
