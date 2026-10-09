---
title: "hacia Luthier"
author: Luciano
original: hacia Luthier.odt
original_sha256: fd10d79348640d9db7cdbe4d5005f839361ed9a9382e12f23a44963a4f24d8fa
created: 2023-03-13T14:48:27
modified: 2023-03-29T18:28:11
words: 287
converted_by: import_notes v1; pandoc 3.10.2; gfm
note: the original is next to this file; this conversion is derived and may be redone
---
tema la vaca

como es Luthier el lenguaje para escribir programas autoverificados?

Luthier es una cadena de asignaciones.

cada asignacion tiene un identificador para recuperar el objeto creado, un signo igual y una operacion para crear el objeto.

Las creaciones de objetos verifican que se cumplans las pre y pos conditions del objeto creado.

En el caso que las postcondiciones de los objetos sean interdependientes, los objetos se asignan simultaneamente.

Ahora, esto plantea un problema: en realidad el resultado de cualquier condicion deberia ser uno si se cumplen las condiciones y un mensaje indicando porque no se cumplieron.

la estructura mas importante de la programacion es el diccionario que une el humano con la maquina, es la base del literalismo

-----

Como hacen otros lenguajes?

vamos de mas simple a mas complejo

1\. C

tenemos declaraciones de variables, struct y funciones y sus punteros

tenemos implementacion de funciones y assigment de variables y estructuras

tenemos estructuras de control de flujo: if else , for loop y while

2\. C++

agregamos

1\. classes: tienen methods y virtual methods y inheritance

1\. function overloading

2\. template function y template class

3\. podes imitar functional programming

3\. Haskell

las funciones son puras

usas pattern matching en lugar de if else

usas recursive functions en lugar for loops

usas map y reduce.

List es un tipo fundamental

data para declarar nuevos tipos

type signature y kind signature

class where // instance where para nuevos typeclasess (

y

guards, where y let (como reemplazo de los blocks para variables que desaparecen)

4\. Elixir

mucho mucho pattern matching. mucho

atoms como tipo

signo igual como <span id="anchor"></span>match operator (pattern matching)

List, tuples y maps

metaprogramming:

quote y unquote, escape

5\. Lisp

Code as data.
