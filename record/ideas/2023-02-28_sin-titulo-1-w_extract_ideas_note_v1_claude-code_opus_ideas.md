---
note: 2023-02-28 Sin título 1 w.md
note_dir: HoTTification
note_sha256: 78c527cdd46f5e056f9c52bcf2fbbcd63b59035b0f1ca078aea5b91b524662c4
title: "Sin título 1 w"
author: Luciano
created: 2023-02-28T18:06:52
ideas: 6
quotes_found: 6/6
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### categoria-declaracion-estilos
- **What**: Opens the question of how to declare a category in the language, and notes there could be different styles for doing so.
- **Quote**: "como hago para declarar una categoria" (line 1)
- **Also at**: line 3
- **Open**: which style to use is left open ("diferentes estilos"), only the C++ style is sketched.

### estilo-cpp-clases-funciones
- **What**: One style for declaring a category modeled on C++, where there are classes or structs and functions.
- **Quote**: "Estilo c++" (line 5)
- **Also at**: line 7
- **Open**: presented as one option among several ("diferentes estilos"), the others not written.

### categoria-como-clase-con-componentes
- **What**: A category declared as a class constructed from its components: objects, homs, composition and identity.
- **Quote**: "Category(Obj,Hom,Compose,Id)" (line 13)

### object-y-hom-como-tipos-dependientes
- **What**: Object is a type indexed by a category, and Hom is a type indexed by two objects.
- **Quote**: "type Hom(Object X, Object Y)" (line 17)
- **Also at**: line 15

### compose-con-ley-de-asociatividad
- **What**: Composition is a function on homs whose type carries the law that it is associative.
- **Quote**: "function Compose (Hom(X,Y), Hom(Y,Z))-\>Hom(X,Z)=\>Associative (Compose)" (line 19)

### id-con-leyes-de-identidad
- **What**: Id is a function giving an endo-hom whose type carries the left and right identity laws.
- **Quote**: "function Id(X)-\>Hom(X,X) =\> Identity_right(Id(X),Hom(X,Y)) & Identity_left(Hom(Y,X),Id(X))" (line 21)
