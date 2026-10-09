---
title: "Luciano Code style"
author: Luciano
original: Luciano Code style.odt
original_sha256: dde507fc49a0763cb0c5645746a31169d10c785e4cb5c058756133c04768cfa3
created: 2022-06-28T22:25:12
modified: 2022-07-07T11:59:58
words: 891
converted_by: import_notes v1; pandoc 3.10.2; gfm
note: the original is next to this file; this conversion is derived and may be redone
---
Luciano Code Manifest

I code to understand.

Si quiero entender, entonces debo poder manipular el codigo y ver que es mejor. Debo entender como los cambios en mi codigo repercuten en observables de mi codigo.

Cuales serian estos observables?

1\) Expresividad: el codigo debe expresar la intención del mismo tanto para el que leer el codigo como para el compilador.

Un codigo es mas expresivo cuando

1\. refiere a estructuras o algoritmos conocidos y esta referencia es real. Por ejemplo, no puedo llamar array a una lista.

2\. Expresa conceptos extra-computacionales (por ejemplo probabilidad) de forma intuitiva y veraz. La idea es abstraer las propiedades compulacionales de estos conceptos y proveer los mecanismos para verificar su cumplimiento. Por ejemplo, la probabilidad es un numero entre 0 y 1: deberia no aceptar probabilides fuera de ese rango y deberia reportar calculos que generen valores invalidos.

3\. Cuando se trata de implementar nuevos conceptos, se define la operacion de forma expresiva, no se dejan flotando operaciones que no se sabe que hacen. Por otro lado, es posible que una algoritmo que es expresado de una forma clara pero computacionalmente no eficiente pueda ser optimizado con un algoritmo mas criptico. Esto se expresa claramente como un algoritmo equivalente al algoritmo lento y claro. La ventaja del algoritmo lento y claro es que es mas facil convencerse de que es correcto y luego sirve de gold standard para el algoritmo rapido y obtuso.

Mientras caminaba pense en que lo que debiera hacer es una libreria que permita lo siguiente.

1\) Expresar variables y tipos, y tipos funcionales, de clases etc y con sus semantica.

Esta semantica "vive" en su propio universo que no es el de C++, aunque use las estructuras de C++ para expresarlos.

2\) La idea es poder crear nuevos "objetos" (sean valores o variables, de tipos, funciones o "clases"). Al mismo tiempo perder la distincion entre codigo y dato.

3\) Es importante establecer las relaciones de equivalencia en quimulun. Esto permite optimizar los tiempos de calculo.

Entonces, los dos objetivos son

1\) abstraer y formalizar los mecanismos de determnacion sematinca de forma que haya una relacion uno a uno entre el razonamiento y el flujo del codigo. De esta forma verificar la validez de los razonamientos. Es una vieja idea.

2\) una vez que se establece la validez semantica y la equivalencia semantica se puede optar por el camino mas eficiente.

Si queremos aplicar estas ideas a macror, como hago?

Puedo empezar tratando de implementar la probabilidad de encontar a un canal en un estado.

El tema pasa por como construyo los estados.

En particular como construyo la multiplicidad de estados.

Esto es basicamente multiplicar la preposicion "el canal esta en un estado" por un numero de posibilidades, es decir "el canal esta en uno de n estados".

Entonces, cual es el conocimiento que quiero expresar?

1\) "mi canal a está en el estado i. Esto seria una funcion de a --\> i

si quiero decir el estado i entre N estados "similares", el tipo del estado i seria estado x N, siendo N el tipo 1+1+1..+1 N veces. Es decir el set de N componentes.

O sea que aqui debo definir los siguientes valores y tipos.

1\) un tipo channel state que es isomorfico con el tipo ONE

2\) un tipo a physical channel que tambien es isomorfico con ONE

3\) un constructor de tipos que toma un numero natural y te devuelve un conjunto que contiene ese numero natural.

aqui tengo que pensar hasta que punto sigo con type theory y hasta que punto uso category theory.

tengo que ver el capitulo de category theory del libro de hott

No encuentro nada particular

Bueno, no me queda otra que empezar a trabajar.

voy a tratar de implementar un environment donde testear mis distintos algoritmos de aproximacion de la log-likelihood.

1\) tengo que definir un modelo cienetico

2\) tengo ejecutar samples de este modelo

3\) tengo que mostrar si este metodo cumple los requerimientos.

Para definir un modelo cinetico tengo que definir

1\) estado

2\) multiplicidad de estado (como suma, es decir esta en un estado)

3\) conductancia del estado

4\) canal

5\) multiplicidad de canales (pero como producto, no suma, exponencial a un numero)

6\) estar en un estado

7\) probabilidad de estar en un estado, de un canal y de multiples canales.

8\) probabilidad de transicion.

9\) muestra y probabilidad --\> dualidad y tests que demuestran que se cumple.

Relacion de equivalencia entre (state\*k)^N y Sum\_{\|a\|=k} C(n,a) \*state^a , a-\>multiindice

state^a=Prod_i state_i^a_i

No me queda otra que empezar a armarlo de cero.

Voy a clonar macrodr en un branch separado y empezar de cero.

el primer punto es importar los datos experimentales.

ahi se me plantea el problema de como los defino.

Como creo valores (values) y sus tipos (types), variables (variables), y tipos de variables (¿?), funciones y tipos de funciones.

En principio tenemos tipos de valores primitivos: boolean, integer, real, string, nothing (or zero), one (or something), memory (¿?), size (¿?)

y tenemos funciones primitivas: suma, resta, multiplicacion, division, division entera, modulo, concatenacion de strings...., and, or, not, greater than, equal..

ahora necesito funciones para crear cosas nuevas

dependent-types: son tipos que dependen de un valor, lo cual hace que su cardinalidad sea la del typo del valor que toma

Un dependent tipe es .
