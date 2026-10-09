---
title: "tapp wish list"
author: Luciano
original: tapp wish list.odt
original_sha256: d895d8f26edc3acdbbbd3a1b0f9da6bcfec78aac5e81959670377d9cc90af172
created: 2023-02-22T16:12:49
modified: 2023-02-23T18:49:12
words: 260
converted_by: import_notes v1; pandoc 3.10.2; gfm
note: the original is next to this file; this conversion is derived and may be redone
---
tapp wish list

1 Dos tipos de tipos:

1\. Constructivos (suma, producto, exponencial, composicion de funciones)

2\. Declarativos: cumplen una proposicion. (subobject classifier de una suma producto o exponencial)

Las funciones se definen con precondiciones (los subtipos de los argumentos) y postcondiciones (proposiciones que involucran a argumentos y valores retornados). Las poscondiciones definen el subtipo de la funcion, lo cual hace que este subtipo sea usado como precondicion de otra funcion.

Esto hace que muchas funciones se deban definir en grupo ya que las postcondiciones involucran a varias funciones a la vez (como leer y escribir o las operaciones en un objeto matematico como un grupo o field.

Tengo que poder definir este tipo de objetos matematicos.

2 deseo

Code as data. Debo poder operar sobre las definiciones de funciones. O sea que debo distinguir entre el codigo y la aplicacion del codigo.

3 deseo.

convertir unsafe code en safe code (usando los tipos como codificadores de precondiciones).

4

convertir untested code en tested code: haciendo que las implementaciones de las funciones solo pertenezcan a un tipo si han sido debidamente testeadas y que las condicones de testeo aseguran la validez del codigo.

5\.

Permitir la optimizacion automatica del codigo a medida que se mide el consumo de recursos de implementaciones alternativas de distintas funciones.

6\. La idea es que de cada corrida del codigo algo se aprende, ya sea se sabe que una implementacion es correcta ya que se mide su velocidad.

7\. Partes

A. tapp grammar definition, semantics rules etc

B. tapp front compiler from tapp to c++
