# Towards higher-dimensional syntax — Astra Kolomatskaia

- **Oradora:** Astra Kolomatskaia (trabajo conjunto con Kevin Carlson)
- **Evento:** Topos Institute Colloquium
- **Fecha:** 2026-06-15 · **Duración:** ~61 min
- **Fuente:** https://www.youtube.com/live/XwGtQq-1gBI

> Transcripción automática (faster-whisper, modelo medium.en, CPU). El video no tenía subtítulos de YouTube. Se corrigieron a mano nombres/jerga de alta confianza: Kolomatskaia, Narya, HoTT, M. Shulman, Thorsten Altenkirch, Ambrus Kaposi. Pueden quedar errores menores en otros términos técnicos.

---

## Transcripto (con marcas de tiempo)

[00:00:00 -> 00:00:02] Welcome back to the Topos Institute Colloquium.
[00:00:02 -> 00:00:05] Today we're very happy to have Astra Kolomatskaia
[00:00:05 -> 00:00:08] telling us about higher dimensional syntax.
[00:00:08 -> 00:00:11] So please Astra whenever you're ready.
[00:00:11 -> 00:00:14] Thank you, David, for the invitation.
[00:00:14 -> 00:00:16] I'll be happy to talk about work
[00:00:16 -> 00:00:19] that was done jointly with Kevin Carlson,
[00:00:19 -> 00:00:20] who is here at Topos.
[00:00:21 -> 00:00:25] But that was during one week in May, 2024,
[00:00:25 -> 00:00:28] we took the proof assistant Narya out for a spin
[00:00:28 -> 00:00:34] and current things are in the wake of that.
[00:00:34 -> 00:00:36] You'll notice that I don't have slides.
[00:00:36 -> 00:00:39] I'm in a kind of surreal situation.
[00:00:39 -> 00:00:42] Imagine that, for example, in 2010,
[00:00:43 -> 00:00:46] everyone who is interested in type theory,
[00:00:46 -> 00:00:50] a situation happened, a left behind situation
[00:00:50 -> 00:00:52] where half the population got teleported
[00:00:52 -> 00:00:53] to a different earth.
[00:00:53 -> 00:00:56] The theory developed on each earth for 30 years
[00:00:56 -> 00:00:58] and then at some point they reunify.
[00:01:00 -> 00:01:04] I read very few papers in the fields in grad school
[00:01:04 -> 00:01:07] because I entered type theory somewhat later.
[00:01:07 -> 00:01:12] And recently I made first contact with the literature
[00:01:12 -> 00:01:15] around March at the round time of my HoTT talk.
[00:01:15 -> 00:01:19] And so my understanding has been shifting very rapidly
[00:01:20 -> 00:01:23] after that.
[00:01:23 -> 00:01:28] And often like, as I'm going towards a talk now,
[00:01:31 -> 00:01:33] a lot has moved in the previous couple of days.
[00:01:33 -> 00:01:35] And this has happened today as well.
[00:01:38 -> 00:01:41] So display type theory is joint work with Michael Shulman.
[00:01:44 -> 00:01:49] Mike has with Thorsten Altenkirch and Ambrus Kaposi
[00:01:51 -> 00:01:56] long standing project on higher observational type theory.
[00:01:56 -> 00:01:58] Display type theory and higher observational type theory
[00:01:58 -> 00:02:03] originally were not seen as related projects
[00:02:03 -> 00:02:06] and it was almost a surprise to Mike and I
[00:02:06 -> 00:02:09] how much what we had been doing in one setting
[00:02:09 -> 00:02:11] turned out to be related to what Mike was doing
[00:02:11 -> 00:02:12] at the other setting.
[00:02:14 -> 00:02:19] And more surprising translations to existing work
[00:02:19 -> 00:02:22] kind of make this a bit of an attributional nightmare.
[00:02:22 -> 00:02:24] So I'd like to begin with some acknowledgements.
[00:02:26 -> 00:02:30] First off towards Mike, Reed and Kevin,
[00:02:30 -> 00:02:35] Reed Mullenix and Kevin worked with me in Bonn
[00:02:35 -> 00:02:38] on a formalization that I'll be describing.
[00:02:38 -> 00:02:40] Reed and I have since then continued working
[00:02:40 -> 00:02:45] on higher dimensional syntax in a certain direction.
[00:02:47 -> 00:02:48] The formalization was in Narya,
[00:02:48 -> 00:02:50] a proof assistant that Mike developed
[00:02:50 -> 00:02:54] based on a unification of these higher dimensional theories.
[00:02:56 -> 00:02:59] I really learned type theory kind of by arguing with Mike
[00:02:59 -> 00:03:01] and by listening to Emily.
[00:03:03 -> 00:03:04] There's a couple of other people
[00:03:04 -> 00:03:07] that I'd like to have knowledge.
[00:03:07 -> 00:03:08] While I was in Stockholm last week,
[00:03:08 -> 00:03:12] there were incredible six days of conversation
[00:03:12 -> 00:03:14] with Andreas Knuths that were very useful
[00:03:14 -> 00:03:16] in shaping this talk.
[00:03:16 -> 00:03:20] John Sterling gave a talk at Miri in 2021
[00:03:20 -> 00:03:24] that was a bit of an inspiration to me.
[00:03:24 -> 00:03:28] At Stockholm, I also had productive conversation
[00:03:28 -> 00:03:31] with Simone Henry, Christian Sattler
[00:03:32 -> 00:03:36] and Andre Bauer, also Mario Parioli.
[00:03:36 -> 00:03:39] And I would also like to thank Dan Lakota,
[00:03:39 -> 00:03:40] my postdoc advisor.
[00:03:42 -> 00:03:45] The kind of unsung heroes of the talk
[00:03:45 -> 00:03:51] that I'm going to be giving today are Andreas
[00:03:51 -> 00:03:54] for teaching me much of this.
[00:03:54 -> 00:03:58] And then having finally made first contact
[00:03:59 -> 00:04:04] with Guillem Moulins internalizing parametricity thesis.
[00:04:10 -> 00:04:11] So let's begin.
[00:04:16 -> 00:04:19] The big twists that made this talk
[00:04:19 -> 00:04:24] rapidly shifted and evolve was my learning
[00:04:26 -> 00:04:29] that within the internalizing parametricity thesis,
[00:04:29 -> 00:04:34] there's several different theories that are developed.
[00:04:34 -> 00:04:37] The first is a higher dimensional theory.
[00:04:37 -> 00:04:39] It has higher dimensional cubes.
[00:04:39 -> 00:04:43] This was the contents of a Bradley-Moulon 12,
[00:04:45 -> 00:04:48] a computational interpretation for higher parametricity.
[00:04:50 -> 00:04:54] Moulins considered that work to be superseded
[00:04:54 -> 00:04:59] by the later developments of parametric type theory
[00:04:59 -> 00:05:06] in BCM with theoretical cons.
[00:05:06 -> 00:05:10] It was critically recently discovered
[00:05:10 -> 00:05:14] that there is an error in BCM,
[00:05:14 -> 00:05:18] an error in the semantics of their pre-shoot models.
[00:05:18 -> 00:05:24] There is a graduate thesis on this in 2025
[00:05:24 -> 00:05:32] by Sarah Reboulet.
[00:05:32 -> 00:05:35] And I'll be talking and moving towards that.
[00:05:35 -> 00:05:41] And also in the context of the Mike's work
[00:05:42 -> 00:05:44] a higher observational type theory team work.
[00:05:45 -> 00:05:48] With that being said, there'll be some context
[00:05:48 -> 00:05:54] to getting to see what the error is in BCM
[00:05:54 -> 00:05:58] and how the theory that Moulins originally conceived of
[00:05:58 -> 00:06:01] of higher dimensional cubes was moved away from.
[00:06:01 -> 00:06:06] And kind of returning possibly to Moulins
[00:06:06 -> 00:06:08] original formulation of higher dimensional syntax
[00:06:08 -> 00:06:11] might be the theme of this talk.
[00:06:11 -> 00:06:13] I'm going to start presenting material more formally now.
[00:06:13 -> 00:06:16] I would like to mention that if anyone has questions
[00:06:16 -> 00:06:19] please just interrupt me and ask.
[00:06:22 -> 00:06:25] I think I'll move towards some slides
[00:06:25 -> 00:06:36] that I had from previous presentations.
[00:06:36 -> 00:06:39] So first off, let's talk about cubicle type theory.
[00:06:40 -> 00:06:45] Most generally I'm going to consider a cube category
[00:06:45 -> 00:06:48] to be a monoidal category that has a single generator.
[00:06:48 -> 00:06:50] I'll write that as cube one.
[00:06:52 -> 00:06:53] Products of cube categories
[00:06:53 -> 00:06:56] can also be seen of as cube categories.
[00:06:56 -> 00:07:00] Notably Evans thesis does a dual univalence
[00:07:03 -> 00:07:06] identity type and unary parametricity
[00:07:06 -> 00:07:09] CCHM cross BCH cube category model.
[00:07:11 -> 00:07:14] When it comes to viewing it as a monoidal category
[00:07:14 -> 00:07:15] there's several settings.
[00:07:15 -> 00:07:17] There's the Cartesian setting
[00:07:17 -> 00:07:20] which I'll say happens when the cube category
[00:07:20 -> 00:07:22] is a monoidal Cartesian category.
[00:07:24 -> 00:07:28] Failing that as happens in the BCM cube category
[00:07:28 -> 00:07:32] you can still ask for the monoidal unit
[00:07:32 -> 00:07:34] to be a terminal object.
[00:07:34 -> 00:07:38] When that happens, I call such settings semi-Cartesian.
[00:07:38 -> 00:07:42] And when that fails as well, all bets are off
[00:07:42 -> 00:07:45] and the setting is non-Cartesian.
[00:07:45 -> 00:07:50] An example of a non-Cartesian cube category is Omega,
[00:07:50 -> 00:07:54] the natural numbers with just a single inclusion
[00:07:54 -> 00:07:56] going up dimensions.
[00:07:56 -> 00:08:00] The pre-sheaves on that are known as the toposic trees
[00:08:00 -> 00:08:02] and that's related to garden type theory.
[00:08:06 -> 00:08:10] So because we have a monoidal category
[00:08:13 -> 00:08:17] we can consider tensoring with one.
[00:08:17 -> 00:08:20] The one will be my monoidal generator.
[00:08:20 -> 00:08:22] I'll start my cube indexing at zero.
[00:08:22 -> 00:08:25] The objects are the natural numbers.
[00:08:25 -> 00:08:29] This is an endo-functor on the cube category.
[00:08:29 -> 00:08:34] Precomposition gives a endo-functor on pre-sheaves.
[00:08:37 -> 00:08:42] Now this object in every single cubicle type theory
[00:08:42 -> 00:09:06] is the main thing that we want to study.
[00:09:06 -> 00:09:07] Why?
[00:09:07 -> 00:09:10] Well, in a Cartesian setting, well, I mean,
[00:09:10 -> 00:09:16] or more generally, since the cube category is monoidal,
[00:09:16 -> 00:09:20] pre-sheaves inherits day convolution
[00:09:20 -> 00:09:21] and day exponentiation.
[00:09:23 -> 00:09:28] If we take the representable one cube
[00:09:28 -> 00:09:33] and we write day exponentiation like this suggestively,
[00:09:33 -> 00:09:38] that's going to be our realization of this operation.
[00:09:39 -> 00:09:42] In Cartesian settings, this would be just plain
[00:09:42 -> 00:09:46] exponentiation with an interval objects.
[00:09:46 -> 00:09:50] And so in general, pre-composition with monoidal shift
[00:09:50 -> 00:09:53] is what we consider as the path space object
[00:09:53 -> 00:09:54] in a cubicle theory.
[00:09:56 -> 00:10:05] It has a left adjoint given by day convolution.
[00:10:24 -> 00:10:29] In semi-Cartesian settings, if gamma is some pre-sheave,
[00:10:29 -> 00:10:34] one kind of considers this day convolution
[00:10:35 -> 00:10:44] to be extension with an interval variable.
[00:10:44 -> 00:10:49] And then the path space is literal exponentiation.
[00:10:49 -> 00:10:51] And so in Cartesian settings,
[00:10:51 -> 00:10:55] there's a very nice internalization
[00:10:55 -> 00:11:00] of this global operation locally to the fibers
[00:11:00 -> 00:11:04] by saying, well, if we have some family over the interval,
[00:11:04 -> 00:11:18] we can construct some path.
[00:11:18 -> 00:11:40] Let's call this in the universe.
[00:11:40 -> 00:11:43] My setting is a non-Cartesian setting
[00:11:43 -> 00:11:45] in the context of display type theory.
[00:11:46 -> 00:11:51] The category that I'll consider
[00:11:51 -> 00:11:59] will be called the unary semi-cube category.
[00:11:59 -> 00:12:03] Its objects are the natural numbers
[00:12:03 -> 00:12:08] and a map, let's say B from M to N
[00:12:08 -> 00:12:22] is to be thought of as a order preserving injection
[00:12:22 -> 00:12:28] from M to the, from the ordinal M to the ordinal N.
[00:12:30 -> 00:12:38] This category is the augmented semi-simplex category,
[00:12:38 -> 00:12:40] although one usually starts indexing
[00:12:40 -> 00:12:50] from dimension negative one there.
[00:12:50 -> 00:12:56] From the, if we, for example, take Yanada of box three,
[00:12:57 -> 00:13:04] there's two different ways to visualize this.
[00:13:05 -> 00:13:09] From the perspective of thinking simplicially,
[00:13:09 -> 00:13:14] we could imagine that its elements are three points, X, Y, Z,
[00:13:14 -> 00:13:25] three lines, alpha, beta, gamma, a triangle F,
[00:13:25 -> 00:13:29] but this entire thing, it's taking place somewhere.
[00:13:29 -> 00:13:30] Where is it taking place?
[00:13:30 -> 00:13:34] It's taking place on a page Z.
[00:13:34 -> 00:13:36] And that's the simplicial picture.
[00:13:39 -> 00:13:41] From the unary semi-cube picture,
[00:13:41 -> 00:13:45] we could consider intervals with only one end point.
[00:13:46 -> 00:13:50] So kind of box zero would,
[00:13:51 -> 00:13:55] visualizing its representables would just be a point.
[00:13:55 -> 00:13:58] Box one would be a half open interval.
[00:13:58 -> 00:14:05] Box two would be a product like this.
[00:14:08 -> 00:14:14] And box three extends that one dimension up.
[00:14:17 -> 00:14:20] The correspondence is that I think,
[00:14:20 -> 00:14:25] so the one key thing is that this cube category
[00:14:25 -> 00:14:36] has an initial objects, box zero,
[00:14:36 -> 00:14:39] and that corresponds to every single simplex
[00:14:39 -> 00:14:41] living on a unique page.
[00:14:41 -> 00:14:44] If there's points on two different pages,
[00:14:44 -> 00:14:46] then there's no hope of ever connecting them.
[00:14:47 -> 00:14:49] On the other hand, we don't have degeneracies.
[00:14:49 -> 00:15:02] So it does not have a terminal object.
[00:15:02 -> 00:15:04] So what do the pages represent?
[00:15:04 -> 00:15:08] I didn't understand.
[00:15:08 -> 00:15:13] So from the perspective of products of intervals,
[00:15:17 -> 00:15:21] this diagram here would kind of correspond
[00:15:21 -> 00:15:22] to this diagram here.
[00:15:22 -> 00:15:25] What we can imagine is if we take this representable,
[00:15:25 -> 00:15:30] taking a plane that's perpendicular to that one point
[00:15:30 -> 00:15:35] and intersecting these axis, this, the shape,
[00:15:36 -> 00:15:41] you would recover a, so there'd be three points,
[00:15:41 -> 00:15:44] three lines in the interior of the triangle.
[00:15:44 -> 00:15:47] And you can think of kind of the unique point
[00:15:47 -> 00:15:50] in enfold products of half open intervals
[00:15:50 -> 00:15:54] as a point at infinity at this plane.
[00:15:54 -> 00:15:57] And thinking simplishly, that's the augmentation,
[00:15:58 -> 00:16:00] that's the page.
[00:16:00 -> 00:16:06] Interesting, thanks.
[00:16:06 -> 00:16:12] So we built a theory with this as its index category.
[00:16:15 -> 00:16:17] What is interesting is that we're operating
[00:16:17 -> 00:16:19] in the non-Cartesian setting.
[00:16:19 -> 00:16:21] We don't have a terminal objects.
[00:16:21 -> 00:16:25] Roughly the history has been such that
[00:16:26 -> 00:16:30] orton and pits and lofts
[00:16:30 -> 00:16:33] were slightly too powerful of papers.
[00:16:34 -> 00:16:37] There's a framework that lets one work
[00:16:37 -> 00:16:40] with interval based theories that is very powerful.
[00:16:40 -> 00:16:43] And a lot of current work sits in that framework.
[00:16:43 -> 00:16:47] It doesn't handle the case
[00:16:47 -> 00:16:51] of non-Cartesian index categories very nicely
[00:16:51 -> 00:16:54] for reasons that I'll explain in this talk.
[00:16:54 -> 00:16:58] And in particular, I am going to claim
[00:16:58 -> 00:17:01] that we give a computationally adequate accounts
[00:17:01 -> 00:17:05] of the path types of our theory
[00:17:05 -> 00:17:06] without using an interval
[00:17:06 -> 00:17:08] with the like computational behavior
[00:17:08 -> 00:17:11] that you'd expect in modern cubicle type theories.
[00:17:11 -> 00:17:18] But we do so where an interval theory
[00:17:19 -> 00:17:20] would not be possible.
[00:17:22 -> 00:17:27] And Mike with Thorsten and Ambrash
[00:17:28 -> 00:17:30] have also been moving towards
[00:17:31 -> 00:17:34] a account of a cubicle theory
[00:17:34 -> 00:17:36] that is not based on an interval,
[00:17:36 -> 00:17:38] but that is based observationally.
[00:17:38 -> 00:17:40] The core idea of internal parametricity
[00:17:40 -> 00:17:44] is common to both theories.
[00:17:44 -> 00:17:46] I think that display type theory
[00:17:46 -> 00:17:49] has a strong case to make
[00:17:49 -> 00:17:54] that the move to treating the pop types observationally
[00:17:55 -> 00:17:57] was forced because it's a generous
[00:17:57 -> 00:17:58] as an interval based theory
[00:17:58 -> 00:18:02] simply would not work in this setting.
[00:18:02 -> 00:18:04] And I'll get around to that.
[00:18:04 -> 00:18:12] So towards that end, what's the theory?
[00:18:12 -> 00:18:17] So display type theory is a multimodal type theory.
[00:18:17 -> 00:18:19] The main idea and display type theory
[00:18:19 -> 00:18:22] was made so that we could construct
[00:18:22 -> 00:18:25] semi-simplicial types and semantic generality.
[00:18:25 -> 00:18:29] Give me any category with families
[00:18:29 -> 00:18:31] with pi types and universes.
[00:18:32 -> 00:18:36] I would like to locate semi-simplicial types
[00:18:36 -> 00:18:41] in that given category of families strictly.
[00:18:41 -> 00:18:42] We're going to need to assume
[00:18:42 -> 00:18:43] some existence of co-inductive types,
[00:18:43 -> 00:18:46] but we'll get to that in a second.
[00:18:46 -> 00:18:49] The idea is that like,
[00:18:49 -> 00:18:51] if we want to construct semi-simplicial types,
[00:18:51 -> 00:18:54] one can phrase it as the question, what is a triangle?
[00:18:54 -> 00:18:58] And then one builds a universe
[00:18:58 -> 00:19:01] in which everything is a triangle.
[00:19:01 -> 00:19:04] So starting from the model of your original type theory,
[00:19:04 -> 00:19:06] there's a model of diagrams.
[00:19:06 -> 00:19:09] This is, I kind of use a coherent solving worlds.
[00:19:10 -> 00:19:13] In that stronger model,
[00:19:13 -> 00:19:14] there's more syntax that applies to it
[00:19:14 -> 00:19:18] because we've given ourselves some power.
[00:19:18 -> 00:19:20] Using that extra syntax,
[00:19:20 -> 00:19:23] we can construct semi-simplicial types there.
[00:19:23 -> 00:19:24] The diagram world is like a world
[00:19:24 -> 00:19:25] in which everything is a triangle.
[00:19:25 -> 00:19:27] And then there is a triangle of triangles
[00:19:27 -> 00:19:29] that semi-simplicial types,
[00:19:29 -> 00:19:32] and there's modalities reflecting these different models.
[00:19:32 -> 00:19:34] Diamond is a modality
[00:19:34 -> 00:19:36] that takes the discrete part of a diagram.
[00:19:36 -> 00:19:38] So when we construct semi-simplicial types
[00:19:38 -> 00:19:39] in the coherent solving world,
[00:19:39 -> 00:19:41] we'll take its discrete part
[00:19:41 -> 00:19:44] and get semi-simplicial types in our own model.
[00:19:44 -> 00:19:47] And this is kind of an instance
[00:19:47 -> 00:19:49] of a microcosm principle
[00:19:49 -> 00:19:52] where if we want to define something,
[00:19:52 -> 00:19:57] we need to strengthen the hypothesis of the construction
[00:19:58 -> 00:20:01] in a way that requires language
[00:20:01 -> 00:20:07] that is very much of the elk of that construction.
[00:20:07 -> 00:20:08] We're kind of doing the opposite
[00:20:08 -> 00:20:10] of two-level type theory
[00:20:10 -> 00:20:13] where we're addressing coherences
[00:20:13 -> 00:20:15] not by throwing away the homotopical content
[00:20:15 -> 00:20:18] but by adding more homotopical contents.
[00:20:22 -> 00:20:23] These modalities here,
[00:20:23 -> 00:20:25] they're the traditional modalities,
[00:20:25 -> 00:20:29] and they are not the driving fuel of the theory.
[00:20:29 -> 00:20:32] So what I said before was we're going to start
[00:20:32 -> 00:20:37] with a CWF for our base universe.
[00:20:38 -> 00:20:40] This is kind of an intended model construction.
[00:20:40 -> 00:20:42] And what we're going to construct
[00:20:42 -> 00:20:44] is really vibrant presheaves.
[00:20:45 -> 00:20:47] In the semantics of cubicle type theory,
[00:20:47 -> 00:20:51] one usually considers presheaves
[00:20:51 -> 00:20:54] in the sense of valued in sets.
[00:20:54 -> 00:20:58] We kind of replace set with an arbitrary category
[00:20:58 -> 00:20:59] with family Cs,
[00:20:59 -> 00:21:03] and we can consider a inverse diagram model.
[00:21:04 -> 00:21:09] The unary semi-cubes are a direct category
[00:21:10 -> 00:21:12] and then thinking with the attitude
[00:21:12 -> 00:21:15] of presheave contra-variantly,
[00:21:15 -> 00:21:18] this would be a inverse diagram model.
[00:21:18 -> 00:21:20] Notably inverse diagram models,
[00:21:21 -> 00:21:23] we do not understand
[00:21:23 -> 00:21:25] or rather for 3D diagram models,
[00:21:25 -> 00:21:28] we do not know how to construct them
[00:21:28 -> 00:21:33] in settings that are not either inverse or inverse EI,
[00:21:34 -> 00:21:36] so permitting symmetries.
[00:21:36 -> 00:21:39] In particular, in the presence of degeneracies,
[00:21:39 -> 00:21:42] one loses access to 3D vibrancy.
[00:21:42 -> 00:21:48] And that's going to be the story of the error in BCM.
[00:21:48 -> 00:21:51] So at the very least we have upgraded
[00:21:52 -> 00:21:55] the setting of working in presheaves
[00:21:55 -> 00:21:58] to presheaves valued in an arbitrary state of value FC.
[00:21:59 -> 00:22:03] The modalities, it's good to give their action globally.
[00:22:03 -> 00:22:07] Diamond is evaluation at box zero at the initial object.
[00:22:07 -> 00:22:09] It takes the discrete part of the diagram.
[00:22:09 -> 00:22:11] This is not global sections.
[00:22:11 -> 00:22:14] If in a semi-Cartesian setting
[00:22:14 -> 00:22:16] where box zero is the terminal object,
[00:22:16 -> 00:22:17] this would be global sections,
[00:22:17 -> 00:22:20] but diamond is not global sections.
[00:22:20 -> 00:22:23] Evaluating a zero does not give global sections.
[00:22:23 -> 00:22:26] Triangle builds a constant diagram
[00:22:26 -> 00:22:29] by expanding co-skeletally
[00:22:29 -> 00:22:31] and box is the limit of the diagram,
[00:22:31 -> 00:22:35] which would usually be evaluation of the terminal object,
[00:22:35 -> 00:22:36] but which we do not have.
[00:22:37 -> 00:22:39] The interest though,
[00:22:39 -> 00:22:41] isn't any of these traditional modalities,
[00:22:41 -> 00:22:44] it's how do we treat the path space operation
[00:22:44 -> 00:22:46] pre-composition of the monoidal shift.
[00:22:47 -> 00:22:51] This operation it's interpreted
[00:22:51 -> 00:22:53] thinking simplicially as decolauge.
[00:22:55 -> 00:22:56] To give a picture of decolauge,
[00:22:56 -> 00:23:01] imagine that we kind of take a diagram
[00:23:01 -> 00:23:07] that's like the representable two simplex
[00:23:07 -> 00:23:09] or representable box three,
[00:23:10 -> 00:23:13] and we draw it the way that I drew it before,
[00:23:13 -> 00:23:14] simplicially.
[00:23:14 -> 00:23:16] Decolauge is this kind of construction
[00:23:16 -> 00:23:18] that's going to shift everything down a dimension.
[00:23:19 -> 00:23:21] So this triangle had points X, Y, Z.
[00:23:21 -> 00:23:26] In the decolauge, the pages become X, Y, Z,
[00:23:26 -> 00:23:29] and kind of on the page for X,
[00:23:29 -> 00:23:32] you are co-slicing by that,
[00:23:32 -> 00:23:33] although we call it slicing
[00:23:33 -> 00:23:36] and you have what goes out of X.
[00:23:36 -> 00:23:37] So beta goes out of X,
[00:23:37 -> 00:23:39] alpha goes out of X
[00:23:39 -> 00:23:42] and F is a line that joins alpha to beta.
[00:23:42 -> 00:23:45] Decolauge forgets one of the face maps.
[00:23:45 -> 00:23:49] So F no longer remembers that it lives over gamma.
[00:23:53 -> 00:23:58] This forgotten face map gives us a natural transformation
[00:24:00 -> 00:24:02] from decolauge to the identity.
[00:24:02 -> 00:24:06] So we have substitutions and I call them here row gamma
[00:24:06 -> 00:24:08] from gamma decolauge to gamma.
[00:24:09 -> 00:24:20] This is important, I'll write it down here.
[00:24:20 -> 00:24:31] What we do not have is a kind of degeneracy map.
[00:24:45 -> 00:24:49] For example, if we consider a representable,
[00:24:50 -> 00:24:55] then it's actually going to have a B.
[00:24:55 -> 00:24:58] Well, thinking with CS sets,
[00:24:58 -> 00:24:59] if we take a representable,
[00:24:59 -> 00:25:02] it's zeros above a certain dimension
[00:25:02 -> 00:25:04] because we don't have degeneracies.
[00:25:04 -> 00:25:08] If you shift down and you have top element.
[00:25:18 -> 00:25:19] Okay, that argument does not work,
[00:25:19 -> 00:25:22] but this operation doesn't exist.
[00:25:22 -> 00:25:24] I was going to say that there's nothing
[00:25:24 -> 00:25:26] to send the higher points to,
[00:25:26 -> 00:25:29] but yeah, no, there's nothing to send
[00:25:29 -> 00:25:31] the higher points to, that's right.
[00:25:31 -> 00:25:33] For simplicity, it was the identity, right?
[00:25:33 -> 00:25:37] The map row gamma, was it?
[00:25:37 -> 00:25:38] For simplicity.
[00:25:38 -> 00:25:40] So here, let's take a look at the picture.
[00:25:42 -> 00:25:45] So we've shifted everything down a dimension now.
[00:25:48 -> 00:25:51] One second.
[00:25:51 -> 00:25:56] So now if we look below these two diagrams,
[00:25:57 -> 00:26:00] kind of with their dependencies are lined up.
[00:26:00 -> 00:26:05] So in dimension two, where we previously had lines,
[00:26:05 -> 00:26:07] alpha and beta and gamma, we now have F.
[00:26:07 -> 00:26:11] Now F has forgotten that it lives over gamma.
[00:26:11 -> 00:26:16] So if we give a natural transformation in this direction,
[00:26:19 -> 00:26:22] then F will get sent to gamma.
[00:26:23 -> 00:26:26] Row remembers what Dakalage forgot.
[00:26:29 -> 00:26:30] In the picture above,
[00:26:30 -> 00:26:33] it looked like F was the one simplex and so was gamma.
[00:26:36 -> 00:26:41] So what the picture course-
[00:26:41 -> 00:26:45] I might be misunderstanding at a more basic level.
[00:26:45 -> 00:26:47] Yeah, when I'm considering this example,
[00:26:49 -> 00:26:53] my pre-sheaf would be something like gamma naught
[00:26:53 -> 00:26:56] contains just a single point z,
[00:26:56 -> 00:27:03] gamma one contains three points x, y, z.
[00:27:03 -> 00:27:10] Gamma two contains alpha beta gamma
[00:27:10 -> 00:27:17] and gamma three has F and it's empty above.
[00:27:23 -> 00:27:30] Then Dakalage is a downward shift operation.
[00:27:31 -> 00:27:36] So the n-dimensional elements of the Dakalage
[00:27:36 -> 00:27:44] are the n plus one dimensional elements of gamma.
[00:27:44 -> 00:27:46] So everything moves down.
[00:27:46 -> 00:27:51] And by moving down, we forget one of the face maps
[00:27:51 -> 00:27:55] and row exactly remembers that forgotten face map.
[00:27:55 -> 00:27:56] Row is that missing face map.
[00:28:02 -> 00:28:04] This also shows that we don't have a map
[00:28:04 -> 00:28:07] in the other direction in the case where,
[00:28:08 -> 00:28:10] well, we cut it off at a certain dimension
[00:28:10 -> 00:28:14] because you have zeros above it.
[00:28:14 -> 00:28:18] The Dakalage doesn't have anything
[00:28:18 -> 00:28:22] in the last non-empty dimension of gamma.
[00:28:22 -> 00:28:25] And so there's nothing to send points
[00:28:25 -> 00:28:30] in that dimension to.
[00:28:30 -> 00:28:33] So to tie this concretely,
[00:28:36 -> 00:28:41] in interval-based theories,
[00:28:42 -> 00:28:56] how one really works is supposing an interval variable,
[00:28:57 -> 00:29:17] one can then form this kind of construction
[00:29:22 -> 00:29:28] where this is going to be some rather odd total space
[00:29:29 -> 00:29:32] that kind of has information mixed across dimensions.
[00:29:34 -> 00:29:37] If we think about stats,
[00:29:37 -> 00:29:47] then gamma having a map from this to delta
[00:29:48 -> 00:29:54] because this is day convolution
[00:29:54 -> 00:29:58] is the same as giving a map gamma to delta Dakalage.
[00:30:01 -> 00:30:05] And one of the things that interval-based theories
[00:30:05 -> 00:30:08] rely on is, for example, the ability to say,
[00:30:08 -> 00:30:15] oh, well, if we have a over the interval,
[00:30:15 -> 00:30:17] we can specialize away from that.
[00:30:17 -> 00:30:22] We can form a i naught and type.
[00:30:24 -> 00:30:29] But this would require a substitution gamma i and i to gamma,
[00:30:36 -> 00:30:38] which by the adjunction would be a map
[00:30:38 -> 00:30:39] from gamma to gamma Dakalage,
[00:30:39 -> 00:31:00] which is precisely what we don't have.
[00:31:00 -> 00:31:04] So the game of modal type theory,
[00:31:04 -> 00:31:09] and this goes back all the way to LOBS
[00:31:09 -> 00:31:12] with an internal construction of vibrant universes
[00:31:12 -> 00:31:14] and kind of some internal language
[00:31:15 -> 00:31:18] of a pre-chief model for some notion of internal language.
[00:31:20 -> 00:31:25] The approach to the issue with vibrancy
[00:31:25 -> 00:31:29] was that it was very finicky under substitution.
[00:31:30 -> 00:31:33] If one naively tried to construct a universe
[00:31:33 -> 00:31:38] of vibrant types, one would have that if a vibration,
[00:31:38 -> 00:31:42] if any of it's pulled back to a global elements
[00:31:42 -> 00:31:47] were vibrations, then the A would be a vibration over gamma,
[00:31:48 -> 00:31:51] but that isn't usually what happens.
[00:31:51 -> 00:31:54] And so modal aspects started to enter the type theory.
[00:31:55 -> 00:31:59] Modal type theory is all about having a global operation
[00:31:59 -> 00:32:01] that you want to localize,
[00:32:03 -> 00:32:06] but complexities come up in the context
[00:32:06 -> 00:32:08] of that localization.
[00:32:08 -> 00:32:13] And so where LOBS achieves the solution
[00:32:13 -> 00:32:18] of using a crisp modal pi types
[00:32:18 -> 00:32:22] and the existence of an amazing right adjoint,
[00:32:22 -> 00:32:24] that will kind of be an amazing right adjoint
[00:32:24 -> 00:32:31] to exponentiation of the interval.
[00:32:31 -> 00:32:33] I'll have more to say on that,
[00:32:33 -> 00:32:37] but the entire framework of intervals based theories
[00:32:37 -> 00:32:40] all the way up to transpension kind of works
[00:32:40 -> 00:32:43] towards the direction of the vibrancy constructions
[00:32:43 -> 00:32:45] using the amazing right adjoints.
[00:32:45 -> 00:32:46] And as we're gonna see,
[00:32:46 -> 00:32:49] we're going to go in a rather different direction.
[00:32:49 -> 00:32:51] How are we going to use our,
[00:32:51 -> 00:32:54] give a constructive treatment of our path space object,
[00:32:54 -> 00:32:57] our decal large, that's our global construction.
[00:32:57 -> 00:33:00] How do we localize it to a fiber?
[00:33:00 -> 00:33:02] Well, in the words of the first ends,
[00:33:02 -> 00:33:05] I'm going to give you the global action
[00:33:05 -> 00:33:09] of the pre-composition for the monoidal shifts
[00:33:09 -> 00:33:11] on types in a context.
[00:33:11 -> 00:33:13] So the conclusions of this rule
[00:33:13 -> 00:33:16] are not stated in a general context,
[00:33:16 -> 00:33:18] and we'll add more modal guards later,
[00:33:18 -> 00:33:20] but this is our first approximation.
[00:33:21 -> 00:33:24] If we have a type A over gamma,
[00:33:24 -> 00:33:29] then the vibrant localization of the global operation
[00:33:30 -> 00:33:33] of decal large is known as display.
[00:33:33 -> 00:33:35] If you take A and you display it,
[00:33:35 -> 00:33:38] you decal large the entire context.
[00:33:38 -> 00:33:43] But what's worse is that not only does your context
[00:33:43 -> 00:33:48] become bigger in by virtue of decal large,
[00:33:48 -> 00:33:53] but A, the AD also acquires a self indexing.
[00:33:56 -> 00:34:06] So I'll write this formula down.
[00:34:06 -> 00:34:15] We have, if in the simplicial mode of our theory,
[00:34:15 -> 00:34:20] that A gamma is a type,
[00:34:20 -> 00:34:28] then in the decal large context,
[00:34:28 -> 00:34:31] well, A doesn't live over the decal large context,
[00:34:31 -> 00:34:34] but we can pull it back by our row gamma,
[00:34:36 -> 00:34:48] row gamma, gamma decal large to gamma.
[00:34:48 -> 00:34:52] And then we kind of have that A is a predicates,
[00:34:53 -> 00:35:09] AD is a predicates on A.
[00:35:09 -> 00:35:11] And similarly on terms,
[00:35:11 -> 00:35:14] the key relationship between decal large and display
[00:35:14 -> 00:35:19] is how decal large acts on an extended context.
[00:35:20 -> 00:35:23] When you decal large an extended context,
[00:35:23 -> 00:35:27] it is equivalent to extending the decal large context
[00:35:27 -> 00:35:29] twice.
[00:35:29 -> 00:35:32] So if gamma consists entirely of variables,
[00:35:32 -> 00:35:33] you can think of this as doubling the length
[00:35:33 -> 00:35:34] of the context.
[00:35:36 -> 00:35:40] Every variable is replaced with itself
[00:35:40 -> 00:35:42] and its parametricity witness.
[00:35:43 -> 00:35:46] This unary predicate over it.
[00:35:46 -> 00:35:51] And similarly for relations.
[00:35:51 -> 00:35:54] The computation rules for display
[00:35:54 -> 00:35:57] and display has computation rules
[00:35:57 -> 00:36:00] are those of unary parametricity
[00:36:00 -> 00:36:04] then with the original translation by John Philippe Bernardi
[00:36:06 -> 00:36:08] in 2012.
[00:36:10 -> 00:36:12] In display type theory,
[00:36:12 -> 00:36:16] all of these computation rules are definitional.
[00:36:16 -> 00:36:17] I'm writing them Russell style.
[00:36:17 -> 00:36:21] One would in Tarski style have a couple of Ls
[00:36:21 -> 00:36:23] in some places.
[00:36:23 -> 00:36:27] And the fact that we actually have these computation rules
[00:36:27 -> 00:36:30] strictly on the nose is a really important point
[00:36:30 -> 00:36:33] that we'll come back to.
[00:36:34 -> 00:36:37] So, and if you iterate parametricity,
[00:36:37 -> 00:36:40] starting with some closed type,
[00:36:40 -> 00:36:44] you get to probe the diagram level wise.
[00:36:45 -> 00:36:48] You see the entire diagram structure.
[00:36:48 -> 00:36:51] So the fact that we've passed from some model
[00:36:51 -> 00:36:53] of type theory to its diagram model,
[00:36:53 -> 00:36:56] this kind of index modality treatments
[00:36:56 -> 00:37:01] fully probes the diagram structure in a way
[00:37:01 -> 00:37:04] that's Orton Pitt style axiomatization
[00:37:04 -> 00:37:06] of if you only have this structure,
[00:37:06 -> 00:37:08] then you can construct vibrant universes.
[00:37:08 -> 00:37:09] And that's so powerful.
[00:37:10 -> 00:37:14] So there isn't incentive to push the methods.
[00:37:14 -> 00:37:20] We like get a full grasp on the diagram model structure.
[00:37:20 -> 00:37:23] So how do we get semi-simplicial types?
[00:37:25 -> 00:37:27] There's a secret unpublished note
[00:37:27 -> 00:37:29] that Mike had in October, 2012,
[00:37:29 -> 00:37:31] which gave it a universal characterization
[00:37:31 -> 00:37:34] of semi-simplicial sets.
[00:37:34 -> 00:37:37] The idea behind this characterization was that
[00:37:37 -> 00:37:40] if you have a semi-simplicial set, not a type,
[00:37:41 -> 00:37:42] what do you get from it?
[00:37:43 -> 00:37:44] Well, you get a set of zero simplices.
[00:37:44 -> 00:37:47] And for every zero simplex, you can form the slice,
[00:37:47 -> 00:37:49] which is another semi-simplicial set.
[00:37:51 -> 00:37:56] The slice it's end simplices when you've sliced over X,
[00:37:56 -> 00:37:58] they're the N plus one simplices
[00:37:58 -> 00:38:00] of A whose last vertex is X.
[00:38:00 -> 00:38:03] We delete the first vertex repeatedly.
[00:38:03 -> 00:38:08] The first couple of face maps of AM plus one
[00:38:08 -> 00:38:10] go to the slice, but then one is forgotten.
[00:38:10 -> 00:38:15] And that forgotten face map assembles into a projection
[00:38:15 -> 00:38:17] from the slice to A.
[00:38:17 -> 00:38:19] And this data can kind of be assembled
[00:38:19 -> 00:38:22] into saying that on the category S,
[00:38:22 -> 00:38:26] we have some gadget that assigns to every object of S,
[00:38:26 -> 00:38:31] a set, a family of objects in S indexed by that set.
[00:38:33 -> 00:38:34] These are the slices.
[00:38:34 -> 00:38:39] And also morphisms from the slices
[00:38:39 -> 00:38:42] to kind of the constant family over the points.
[00:38:42 -> 00:38:45] This is a dependent functor
[00:38:45 -> 00:38:48] only by virtue of this last A here.
[00:38:49 -> 00:38:51] Kind of the A naught and the A over X,
[00:38:51 -> 00:38:53] the slices, those are formal variables,
[00:38:53 -> 00:38:55] but here we have a dependency.
[00:38:55 -> 00:38:57] So this is starting to look like
[00:38:57 -> 00:39:00] some kind of co-pointed endofunctor.
[00:39:00 -> 00:39:05] And one can make this precise by saying,
[00:39:05 -> 00:39:07] well, what is a family co-algebra structure in general
[00:39:07 -> 00:39:09] on some category C?
[00:39:10 -> 00:39:15] This is a co-algebra of a co-pointed endofunctor.
[00:39:16 -> 00:39:20] One can say that such data would be
[00:39:20 -> 00:39:24] for every object of C, a sets C zero,
[00:39:24 -> 00:39:28] a family of slices,
[00:39:28 -> 00:39:31] objects in C indexed by that sets,
[00:39:31 -> 00:39:34] and then a kind of projection maps
[00:39:34 -> 00:39:37] from the slices back down to the object itself.
[00:39:37 -> 00:39:41] And Mike's observation was that
[00:39:41 -> 00:39:45] this universally characterizes semi-simplicial sets
[00:39:45 -> 00:39:47] with the structure presented before
[00:39:47 -> 00:39:51] as a terminal co-algebra of this co-pointed endofunctor.
[00:39:51 -> 00:39:53] The proof is the nerve.
[00:39:54 -> 00:39:59] If you have a family co-algebra structure
[00:39:59 -> 00:40:00] on some category C,
[00:40:00 -> 00:40:02] then you have everything necessary
[00:40:02 -> 00:40:05] to build a semi-simplicial set, which is its nerve.
[00:40:06 -> 00:40:09] But this does not directly lead to semi-simplicial types.
[00:40:09 -> 00:40:15] We have this set level, families indexed by sets,
[00:40:15 -> 00:40:17] and we have this projection data there.
[00:40:17 -> 00:40:19] And the perennial question is,
[00:40:19 -> 00:40:21] how do we replace set with type?
[00:40:21 -> 00:40:24] And in display type theory,
[00:40:24 -> 00:40:29] what we do instead is we build the diagram model
[00:40:30 -> 00:40:35] for this displayed mode directly via parametricity.
[00:40:35 -> 00:40:38] Everything is constructed in terms of parametricity.
[00:40:38 -> 00:40:40] So I am short on time.
[00:40:40 -> 00:40:43] I was going to go into more detail in the construction,
[00:40:43 -> 00:40:49] but just skipping ahead,
[00:40:49 -> 00:40:53] the magical property is matching objects.
[00:40:53 -> 00:40:56] We're going to build a Reedy CWF,
[00:40:56 -> 00:40:59] and we kind of need these matching objects.
[00:41:05 -> 00:41:08] And the construction is going to be level-wise
[00:41:08 -> 00:41:10] for truncated models.
[00:41:10 -> 00:41:22] And we'll mutually with this construction,
[00:41:22 -> 00:41:26] suppose that we have like this is in semantics land,
[00:41:26 -> 00:41:28] some display operation.
[00:41:30 -> 00:41:33] We will prove in the course of this construction
[00:41:33 -> 00:41:35] that the expected formula for declarative
[00:41:35 -> 00:41:37] and extended context holds,
[00:41:37 -> 00:41:39] and we'll construct the rest of the structure
[00:41:39 -> 00:41:45] such as functorial actions on these matching objects.
[00:41:45 -> 00:41:50] And the crux of this is that there's a decomposition.
[00:41:53 -> 00:41:58] Of matching objects in terms of display.
[00:41:58 -> 00:42:02] A N plus two matching object is a N matching objects,
[00:42:02 -> 00:42:05] an N plus one matching object,
[00:42:05 -> 00:42:07] a N plus one simplex,
[00:42:07 -> 00:42:10] and an N plus one matching object of the displayed objects.
[00:42:13 -> 00:42:15] And when we finally get around to building
[00:42:15 -> 00:42:18] something like pie types,
[00:42:18 -> 00:42:21] because we're doing this construction level-wise,
[00:42:21 -> 00:42:26] one assumes they have pie types up to level N,
[00:42:26 -> 00:42:28] and then what should it be at level N?
[00:42:28 -> 00:42:31] Well, everything's defined nicely in terms of display.
[00:42:31 -> 00:42:32] So there's this on salts,
[00:42:32 -> 00:42:35] and the on salts is the parametricity formula.
[00:42:35 -> 00:42:38] Why not define it so that at the top level,
[00:42:40 -> 00:42:44] pie types are just the N plus two simplices
[00:42:46 -> 00:42:48] in a pie type are N plus one simplices
[00:42:48 -> 00:42:51] in the expected parametricity formula.
[00:42:51 -> 00:42:53] So like this one stage translation.
[00:42:54 -> 00:42:57] Similarly, the parametricity formulas would say,
[00:42:57 -> 00:43:00] if you display a lambda, you get a double lambda.
[00:43:00 -> 00:43:03] If you display an application, you get a double application
[00:43:03 -> 00:43:07] and then one just checks that the beta and eta laws holds
[00:43:07 -> 00:43:08] and they hold on the nose.
[00:43:08 -> 00:43:10] There's no strictification involved.
[00:43:10 -> 00:43:12] And the matching objects are all
[00:43:12 -> 00:43:15] completely definitionally functorial.
[00:43:17 -> 00:43:21] So display is corely built into the theory
[00:43:21 -> 00:43:25] and the idea should be that these slices,
[00:43:25 -> 00:43:28] for example, a slice category shouldn't be thought
[00:43:28 -> 00:43:30] of as a category, rather it should be thought
[00:43:30 -> 00:43:33] of as a category displayed over the thing
[00:43:33 -> 00:43:34] that you sliced.
[00:43:34 -> 00:43:36] And similarly, a semi-simplicial type,
[00:43:36 -> 00:43:38] it really shouldn't be,
[00:43:38 -> 00:43:40] the slice of a semi-simplicial type
[00:43:40 -> 00:43:42] shouldn't be another semi-simplicial type.
[00:43:42 -> 00:43:47] It should be a semi-simplicial type displayed over A,
[00:43:47 -> 00:43:49] the semi-simplicial type that you slice.
[00:43:49 -> 00:43:54] So if we allow for co-inductive definitions
[00:43:54 -> 00:43:56] that can refer to their own type
[00:43:56 -> 00:43:57] of parametricity witnesses,
[00:43:57 -> 00:44:00] one could write this co-inductive definition
[00:44:00 -> 00:44:02] saying I'm thinking of a type,
[00:44:02 -> 00:44:04] I'll call it semi-simplicial types.
[00:44:04 -> 00:44:07] What will I tell you about semi-simplicial types?
[00:44:07 -> 00:44:09] Well, every semi-simplicial type
[00:44:09 -> 00:44:11] has a type of zero simplices
[00:44:11 -> 00:44:13] and also for every semi-simplicial type
[00:44:13 -> 00:44:16] and zero simplex of it, you've conformed the slice,
[00:44:16 -> 00:44:18] which is a semi-simplicial type displayed
[00:44:18 -> 00:44:20] over A, that semi-simplicial type.
[00:44:22 -> 00:44:24] So that's how we built the theory.
[00:44:24 -> 00:44:26] This is implemented in ARIA
[00:44:26 -> 00:44:29] and you do get simplex extractions.
[00:44:29 -> 00:44:32] Morally, the idea is that's kind of
[00:44:32 -> 00:44:34] in a semi-simplicial type,
[00:44:34 -> 00:44:36] how do we think of the slice?
[00:44:36 -> 00:44:40] Well, if you've sliced by X is zero simplex in the slice,
[00:44:40 -> 00:44:41] well, what are zero simplices
[00:44:41 -> 00:44:43] in a displayed semi-simplicial type?
[00:44:43 -> 00:44:45] They live over simplices downstairs.
[00:44:45 -> 00:44:49] So a zero simplex in the slice over X
[00:44:49 -> 00:44:53] lives over another zero simplex Y downstairs.
[00:44:53 -> 00:44:56] And then we can see that as this line Z.
[00:44:56 -> 00:44:59] And then what is a line in the slice
[00:44:59 -> 00:45:01] over this blue line here?
[00:45:01 -> 00:45:03] Well, it's the data in green.
[00:45:03 -> 00:45:06] And from this, you can extract simplices.
[00:45:06 -> 00:45:10] I'm now going to get onto the work that we did in Bonn.
[00:45:12 -> 00:45:13] I'm aware of the time.
[00:45:13 -> 00:45:16] So we constructed concomplexes.
[00:45:16 -> 00:45:18] Shortly after I defended my thesis, Mike,
[00:45:19 -> 00:45:24] and this is mainly just solo code that he's written.
[00:45:24 -> 00:45:25] I have not contributed codes in ARIA,
[00:45:25 -> 00:45:28] but I got a proof of assistance for my thesis,
[00:45:28 -> 00:45:30] which was very delightful.
[00:45:30 -> 00:45:34] And so we were in Bonn and we take it out for a spin
[00:45:34 -> 00:45:37] and the impression that,
[00:45:37 -> 00:45:38] well, the impression that I had,
[00:45:38 -> 00:45:41] but also Rita and Kevin had this impression as well,
[00:45:41 -> 00:45:43] but wouldn't phrase it in this language,
[00:45:43 -> 00:45:46] but oh my God, what did I create?
[00:45:46 -> 00:45:51] This is the most difficult system to work in ever.
[00:45:54 -> 00:45:58] It is in a very meaningful sense, higher dimensional,
[00:45:58 -> 00:46:02] but not in the way that I'm pitching towards in this
[00:46:02 -> 00:46:05] talk.
[00:46:05 -> 00:46:05] At some point,
[00:46:05 -> 00:46:08] symmetries come into play and it's possible for code to
[00:46:08 -> 00:46:11] meaningfully be an end dimensional object,
[00:46:11 -> 00:46:16] which you can shape rotate by permuting its things
[00:46:16 -> 00:46:19] in dimension one, you shape rotate code
[00:46:19 -> 00:46:21] in higher dimensional space.
[00:46:21 -> 00:46:26] And your kind of thread is solving coherence problems
[00:46:26 -> 00:46:29] by threading a needle to make everything line up
[00:46:29 -> 00:46:30] entirely right.
[00:46:31 -> 00:46:35] But after a week of working, we developed idioms.
[00:46:35 -> 00:46:37] We like worked out what the patterns were,
[00:46:37 -> 00:46:39] and then it became a lot easier to work in the system.
[00:46:39 -> 00:46:41] And so I'll talk about our formalization
[00:46:42 -> 00:46:44] of con complexes.
[00:46:44 -> 00:46:46] First, if we give a semi-simplicial type,
[00:46:46 -> 00:46:51] we're going to define it's two different types.
[00:46:52 -> 00:46:54] They're going to be the type of end simplex boundaries
[00:46:54 -> 00:46:55] and end simplex fillers.
[00:46:55 -> 00:46:57] So if you give me a semi-simplicial type
[00:46:57 -> 00:47:00] and I ask for an end simplex boundary,
[00:47:00 -> 00:47:04] that's like, this is kind of just a representation
[00:47:04 -> 00:47:08] of a functor from the representable boundary,
[00:47:08 -> 00:47:09] except we don't do it that way.
[00:47:09 -> 00:47:11] We define it directly by just probing the type.
[00:47:11 -> 00:47:16] And then boundary fillers are indexed by a boundary.
[00:47:16 -> 00:47:18] And the idea for the inductive construction is,
[00:47:18 -> 00:47:22] well, let's look at kind of this three simplex boundary.
[00:47:22 -> 00:47:25] If we have a two simplex boundary partial A,
[00:47:25 -> 00:47:26] and we have a point,
[00:47:27 -> 00:47:30] then we can form the slice over that point,
[00:47:30 -> 00:47:34] and we can take a displayed boundary over partial A.
[00:47:34 -> 00:47:36] Let's call that partial A prime.
[00:47:36 -> 00:47:41] This is a boundary in the slice displayed,
[00:47:43 -> 00:47:45] the slice over point displayed
[00:47:45 -> 00:47:48] over the boundary partial A.
[00:47:48 -> 00:47:49] And then one also fills partially,
[00:47:49 -> 00:47:50] and that should assemble
[00:47:50 -> 00:47:54] into a higher dimensional boundary.
[00:47:54 -> 00:47:58] And so one just writes that up in ARIA.
[00:47:59 -> 00:48:04] It's an induction on N and in dimension zero.
[00:48:05 -> 00:48:06] So these are defined mutually,
[00:48:07 -> 00:48:09] the fillers are on this slide.
[00:48:09 -> 00:48:12] There's no data in a zero simplex boundary,
[00:48:12 -> 00:48:13] so it's the unit type.
[00:48:13 -> 00:48:15] Then in a successor dimension,
[00:48:15 -> 00:48:17] well, it's a zero simplex in A,
[00:48:17 -> 00:48:20] an N boundary in at A,
[00:48:20 -> 00:48:23] a filler of that N boundary and a displayed boundary
[00:48:23 -> 00:48:26] in the slice over the point over that boundary.
[00:48:26 -> 00:48:29] The line below is just a helpful typing annotation.
[00:48:29 -> 00:48:33] For simplex fillers, well, what does one say?
[00:48:33 -> 00:48:37] So with the trick that we're using here
[00:48:38 -> 00:48:40] is displayed induction.
[00:48:40 -> 00:48:42] The theorem calls its own displayed version
[00:48:42 -> 00:48:43] in the course of induction.
[00:48:43 -> 00:48:48] And so here the definition of a simplex filler
[00:48:48 -> 00:48:50] is going to call its own displayed version.
[00:48:50 -> 00:48:53] And the record type from before just deassembles
[00:48:53 -> 00:48:56] and it slots into all the perfect positions
[00:48:56 -> 00:48:59] and we get the construction.
[00:48:59 -> 00:49:01] Then there's a demo of this
[00:49:01 -> 00:49:03] and I'll show you in ARIA,
[00:49:03 -> 00:49:06] but here one can postulate like an SST,
[00:49:06 -> 00:49:09] then three points X, Y, Z,
[00:49:09 -> 00:49:11] lines alpha, beta, gamma, triangle F.
[00:49:11 -> 00:49:13] And then one can populate, for example,
[00:49:13 -> 00:49:16] give it two simplex boundary in some decomposition
[00:49:16 -> 00:49:19] and give a filler up that boundary as F.
[00:49:19 -> 00:49:21] That F is able to type check here
[00:49:21 -> 00:49:23] is a witness that the theory
[00:49:23 -> 00:49:25] is sufficiently computational.
[00:49:34 -> 00:49:37] To show you this running in ARIA.
[00:49:37 -> 00:49:39] So this was, we developed this code
[00:49:39 -> 00:49:41] over the course of a week.
[00:49:41 -> 00:49:46] One starts with the definitions of the empty type,
[00:49:48 -> 00:49:50] inductive with no constructors,
[00:49:51 -> 00:49:53] the units record with no fields,
[00:49:53 -> 00:49:56] natural numbers, semi-simplicial types, three lines.
[00:49:56 -> 00:49:59] Here are simplex boundaries and fillers.
[00:49:59 -> 00:50:01] At this stage already,
[00:50:01 -> 00:50:03] we can kind of look here
[00:50:03 -> 00:50:04] and type check this construction.
[00:50:04 -> 00:50:08] If I give this boundary and I put a hole there,
[00:50:12 -> 00:50:15] I can see that the hole expects
[00:50:15 -> 00:50:17] a triangle alpha, beta, gamma.
[00:50:17 -> 00:50:20] So that's my F.
[00:50:20 -> 00:50:23] I see you're in your question time now.
[00:50:23 -> 00:50:35] I see.
[00:50:35 -> 00:50:35] Okay.
[00:50:39 -> 00:50:42] So I would like to say this,
[00:50:42 -> 00:50:45] and then one constructs called complexes.
[00:50:45 -> 00:50:49] There's a nice decomposition of horns.
[00:50:49 -> 00:50:58] That's similarly combinatorial.
[00:50:58 -> 00:51:00] Here are some pictures for that.
[00:51:00 -> 00:51:02] And one gives the definitions
[00:51:02 -> 00:51:04] and then following this,
[00:51:04 -> 00:51:06] the definition of a con complex,
[00:51:07 -> 00:51:09] horns aren't defined directly.
[00:51:09 -> 00:51:12] We define a kind of a horn index by a simplex boundary.
[00:51:12 -> 00:51:14] We call that a horn boundary.
[00:51:14 -> 00:51:16] So a horn is really a simplex boundary
[00:51:16 -> 00:51:17] and the horn boundary index by it.
[00:51:17 -> 00:51:20] And then a horn filler is a simplex filler
[00:51:20 -> 00:51:21] and a horn filler.
[00:51:21 -> 00:51:23] And the con structure on a semi-simplicial type
[00:51:23 -> 00:51:25] says that for every N and K,
[00:51:25 -> 00:51:27] give me an N K horn I can fill it.
[00:51:29 -> 00:51:31] The motivation for higher dimensional syntax
[00:51:31 -> 00:51:35] was that, well, when one gets this,
[00:51:35 -> 00:51:37] one can make a definition.
[00:51:40 -> 00:51:42] Any notion of path types will do.
[00:51:43 -> 00:51:47] There are every space has points, lines and triangles
[00:51:47 -> 00:51:49] kind of given by the path types.
[00:51:49 -> 00:51:52] This is the singular semi-simplicial type of a type X.
[00:51:55 -> 00:51:58] So this is less than a hundred lines of code.
[00:51:58 -> 00:52:00] There is a lot of examples,
[00:52:00 -> 00:52:04] but I mean, this concretely is line 132,
[00:52:04 -> 00:52:07] but all of this can be done in less than a hundred lines.
[00:52:10 -> 00:52:12] Sync-con-x, for all X in type,
[00:52:12 -> 00:52:13] there is a con structure
[00:52:13 -> 00:52:15] on the singular semi-simplicial types.
[00:52:15 -> 00:52:16] This is an internal statement
[00:52:16 -> 00:52:21] that types are infinity group points.
[00:52:21 -> 00:52:23] I will try and move on to questions now.
[00:52:23 -> 00:52:28] And one tries to improve this, but there's a difficulty.
[00:52:28 -> 00:52:30] The difficulty is that there's a difference
[00:52:30 -> 00:52:31] if we make a displayed call
[00:52:31 -> 00:52:34] between a displayed con structure
[00:52:34 -> 00:52:36] and a relative con structure.
[00:52:36 -> 00:52:38] If you make this naive recursive call,
[00:52:38 -> 00:52:40] you're in the inductive case,
[00:52:40 -> 00:52:43] you get a kind of in a semi-simplicial type
[00:52:43 -> 00:52:46] in upstairs and downstairs.
[00:52:46 -> 00:52:51] For horns upstairs and with a con structure downstairs,
[00:52:51 -> 00:52:53] you get fillers upstairs
[00:52:53 -> 00:52:57] over the prescribed filler by that con structure.
[00:52:57 -> 00:52:59] But we want it over arbitrary fillers.
[00:52:59 -> 00:53:01] Postulating the Siegel hypothesis
[00:53:01 -> 00:53:03] and asking for a contractible space of fillers
[00:53:03 -> 00:53:04] kind of doesn't work
[00:53:04 -> 00:53:06] because then you have to transport
[00:53:06 -> 00:53:08] and display is the theory about indexing.
[00:53:08 -> 00:53:10] And then you're immediately just land and transport help.
[00:53:10 -> 00:53:12] So we're in a situation
[00:53:12 -> 00:53:15] where we can make a lot of constructions,
[00:53:15 -> 00:53:17] but we can't prove things about them.
[00:53:17 -> 00:53:19] And thinking about this,
[00:53:19 -> 00:53:22] we, Reed and I had the idea to do a shape theory.
[00:53:24 -> 00:53:26] It's kind of a modal theory
[00:53:26 -> 00:53:28] where the modes are indexed by shapes.
[00:53:28 -> 00:53:30] And one can talk about type theory
[00:53:30 -> 00:53:33] and extra axis of higher dimensionality.
[00:53:34 -> 00:53:37] Defined in a shape DSL families of shapes
[00:53:37 -> 00:53:40] over the dimension variables.
[00:53:40 -> 00:53:45] And then shapes act on types in a proof relevant way.
[00:53:45 -> 00:53:47] If shapes are co-fibrations theory,
[00:53:47 -> 00:53:49] they're proof relevant co-fibrations.
[00:53:49 -> 00:53:51] There's no extensional face lattice.
[00:53:51 -> 00:53:53] Shapes store their computational behavior,
[00:53:53 -> 00:53:54] which is critical
[00:53:54 -> 00:53:57] because one then defines a relative con structure
[00:53:59 -> 00:54:01] and the strengthens.
[00:54:01 -> 00:54:05] So this says that you can fill upstairs
[00:54:05 -> 00:54:07] over any choice of fillers downstairs.
[00:54:08 -> 00:54:13] One proves the theorem, same con relatively.
[00:54:13 -> 00:54:15] And the key is that one raises the degree of the diagram
[00:54:15 -> 00:54:17] instead of using a displayed call,
[00:54:17 -> 00:54:19] one builds a higher dimensional cube.
[00:54:19 -> 00:54:21] And this means parameterizing the theorem
[00:54:21 -> 00:54:23] over all degrees of relativity.
[00:54:23 -> 00:54:26] There's a categorical explanation for this.
[00:54:26 -> 00:54:29] And that was kind of the lead in before
[00:54:29 -> 00:54:32] I read any of the things that I learned this week.
[00:54:32 -> 00:54:35] So the exciting things that I spent most of the last
[00:54:35 -> 00:54:39] couple of days working on up, I did not talk about,
[00:54:39 -> 00:54:45] but I looked at a lot of the work
[00:54:45 -> 00:54:51] and Mike's pushback against a lot of this proposal
[00:54:51 -> 00:54:53] to move towards a higher dimensional theory
[00:54:53 -> 00:54:59] was to avoid primitives in every single dimension.
[00:54:59 -> 00:55:03] After reading, oh, okay.
[00:55:03 -> 00:55:08] Well, so the mistake found in BCM,
[00:55:08 -> 00:55:10] like the actual math error
[00:55:10 -> 00:55:12] is that in their previous chief construction,
[00:55:12 -> 00:55:15] they're doing these I set kind of things,
[00:55:15 -> 00:55:17] which is kind of like a really construction,
[00:55:17 -> 00:55:19] but it's not exactly that
[00:55:19 -> 00:55:22] because they can only work with the strict projections.
[00:55:24 -> 00:55:29] And the crux is that you would like to justify
[00:55:29 -> 00:55:32] the rule type DA is A to type,
[00:55:32 -> 00:55:34] a display type is a dependent type.
[00:55:35 -> 00:55:37] In theories where this isn't definitionally,
[00:55:37 -> 00:55:39] you have a gel construction.
[00:55:39 -> 00:55:44] Gel takes a type family to a display type.
[00:55:44 -> 00:55:46] And there's two different round trips.
[00:55:46 -> 00:55:49] One of them can be proven to be an isomorphism,
[00:55:49 -> 00:55:52] but the other one has difficulty.
[00:55:52 -> 00:55:56] And in BCM, they claim that it is,
[00:55:56 -> 00:55:58] can you can have a search type rule,
[00:56:00 -> 00:56:03] but this is not verified by the model
[00:56:03 -> 00:56:06] in nominal sets.
[00:56:09 -> 00:56:12] And reading that and reading a couple of other things,
[00:56:12 -> 00:56:14] I kind of realized that you don't actually need
[00:56:14 -> 00:56:20] to index over dimension variables.
[00:56:20 -> 00:56:22] It's enough to just do a move in one dimension.
[00:56:22 -> 00:56:25] And what's really going on is
[00:56:25 -> 00:56:28] it's kind of like a Baba is you forcing style thing
[00:56:28 -> 00:56:32] where you have syntax in every mode.
[00:56:32 -> 00:56:33] Everything is modal.
[00:56:33 -> 00:56:35] Display is no longer in deck large.
[00:56:35 -> 00:56:37] They're not endo-modalities.
[00:56:37 -> 00:56:38] They do with this rotation.
[00:56:40 -> 00:56:43] It's kind of, I can justify why it's bad
[00:56:43 -> 00:56:44] to think of them as endo-modalities.
[00:56:44 -> 00:56:49] And you can imagine like building this,
[00:56:49 -> 00:56:52] doing a display, having access to this extra shape structure
[00:56:52 -> 00:56:54] being on the outside meta you,
[00:56:54 -> 00:56:56] and then you can imagine doing kind of like
[00:56:56 -> 00:57:00] a absoluteness style thing where you become the you
[00:57:00 -> 00:57:05] that is oblivious to that extra access of dimensionality.
[00:57:05 -> 00:57:07] And so it's possible to think of it entirely
[00:57:07 -> 00:57:09] as just these local moves
[00:57:09 -> 00:57:11] where all the emergent higher structure is where,
[00:57:11 -> 00:57:13] for example, if you are Narya,
[00:57:13 -> 00:57:15] then you're in a fixed dimension
[00:57:15 -> 00:57:17] and how it stores it on the computer.
[00:57:17 -> 00:57:21] And then you can't do these perspective equivocation things
[00:57:21 -> 00:57:23] of just doing these movements.
[00:57:23 -> 00:57:26] And so that's where the higher dimensional stuff
[00:57:26 -> 00:57:28] emerges from.
[00:57:28 -> 00:57:31] But locally you can do all of these constructions
[00:57:31 -> 00:57:33] by kind of changing the definition of you across.
[00:57:33 -> 00:57:35] So do you want any time for questions?
[00:57:35 -> 00:57:36] I do.
[00:57:36 -> 00:57:38] Okay, that's the talk.
[00:57:38 -> 00:57:40] Okay, thank you.
[00:57:40 -> 00:57:42] I think we have time for one question.
[00:57:42 -> 00:57:45] Maybe we'll see at the length.
[00:57:45 -> 00:57:54] Does anyone have questions?
[00:57:54 -> 00:57:57] Let's see, none arriving yet.
[00:57:57 -> 00:57:58] Yeah, I can ask.
[00:57:58 -> 00:58:00] Hey, Astrid, good to see you.
[00:58:00 -> 00:58:02] So what are you gonna do now
[00:58:02 -> 00:58:06] since everything sounds like changed in Sweden?
[00:58:06 -> 00:58:08] Oh, who's-
[00:58:08 -> 00:58:09] Yes, Kevin.
[00:58:09 -> 00:58:10] That's Kevin.
[00:58:10 -> 00:58:14] Yeah, yes.
[00:58:14 -> 00:58:15] Hey, Kevin.
[00:58:15 -> 00:58:17] Let's see.
[00:58:17 -> 00:58:21] So the big thing that happened in Sweden was
[00:58:21 -> 00:58:24] I hadn't read Moolan's thesis before.
[00:58:24 -> 00:58:29] I literally know Moolan's original paper
[00:58:29 -> 00:58:31] has these cubes of variables,
[00:58:33 -> 00:58:36] but it didn't have a pre-sheep semantics.
[00:58:36 -> 00:58:38] It only had an operational semantics.
[00:58:38 -> 00:58:41] And then I think there was like pressure on Moolan
[00:58:41 -> 00:58:43] to make a simpler theory.
[00:58:43 -> 00:58:45] And then theory pecan came in with the idea
[00:58:45 -> 00:58:48] of the nominal set model and connecting that
[00:58:48 -> 00:58:50] to kind of the interval variable appearance
[00:58:50 -> 00:58:52] and type theory and color.
[00:58:53 -> 00:58:55] An interval based theory treatment was given.
[00:58:58 -> 00:59:02] This doesn't work for non-Cartesian.
[00:59:02 -> 00:59:04] Like extending by an interval variable
[00:59:04 -> 00:59:06] this day convolution operation,
[00:59:06 -> 00:59:08] it doesn't reify nicely in syntax
[00:59:08 -> 00:59:10] in our Cartesian settings.
[00:59:10 -> 00:59:11] And I think I know why.
[00:59:11 -> 00:59:17] Like I actually understand where the failure,
[00:59:19 -> 00:59:20] they call it relativity.
[00:59:20 -> 00:59:25] Type DA is A to type can be justified in some way.
[00:59:25 -> 00:59:26] In Evan's thesis, by the way,
[00:59:26 -> 00:59:31] this is justified by univalence, but not computationally.
[00:59:31 -> 00:59:34] Mike's team is having difficulty with this
[00:59:34 -> 00:59:39] because after ACKS, which does span based,
[00:59:40 -> 00:59:42] not relational parametricity.
[00:59:43 -> 00:59:43] So it's like a total space.
[00:59:43 -> 00:59:45] It's not, you don't have the indexing graph
[00:59:45 -> 00:59:47] to recover it by taking path types.
[00:59:48 -> 00:59:52] They do not justify the round trip equations.
[00:59:52 -> 00:59:54] And they say that we just get a section.
[00:59:55 -> 00:59:57] And they've kind of been blocked
[00:59:57 -> 00:59:59] on constructing vibrant universes
[00:59:59 -> 01:00:00] with the difficulty of proving
[01:00:00 -> 01:00:03] that the universe of vibrant types is itself vibrant.
[01:00:03 -> 01:00:06] Which when speaking to Ambrosian Dubianna
[01:00:06 -> 01:00:11] before Stockholm, he had not read the DTT work
[01:00:11 -> 01:00:13] and he was really surprised to hear
[01:00:13 -> 01:00:15] that DTT literally has type DA as A to type.
[01:00:20 -> 01:00:22] And I think that happens that we,
[01:00:22 -> 01:00:26] I couldn't justify in the display type theory paper
[01:00:26 -> 01:00:28] is that we don't give a co-recursion principle
[01:00:28 -> 01:00:30] for displayed semi-simplicial types.
[01:00:32 -> 01:00:34] What happens is if you try and do it,
[01:00:34 -> 01:00:36] you see that two indices get swapped,
[01:00:36 -> 01:00:41] which is the classical move on problem.
[01:00:41 -> 01:00:43] But looking around how.
[01:00:43 -> 01:00:45] We're basically out of time for the main thing.
[01:00:46 -> 01:00:47] You wanna wrap up anything or?
[01:00:47 -> 01:00:52] Right, so there's by making display
[01:00:53 -> 01:00:56] and decolauge not be endo-modalities.
[01:00:56 -> 01:00:59] By making them change the mode of the theory
[01:00:59 -> 01:01:02] to expose an extra Sierpinski axis
[01:01:02 -> 01:01:05] in the shape of the diagram in which you're working,
[01:01:06 -> 01:01:07] we get a co-recursion principle
[01:01:07 -> 01:01:10] for displayed semi-simplicial types.
[01:01:10 -> 01:01:12] Like all of these twisting problems,
[01:01:12 -> 01:01:15] we can just do the theory without symmetries,
[01:01:15 -> 01:01:17] I'll then back later if we won't,
[01:01:17 -> 01:01:20] but everything works out from this picture
[01:01:20 -> 01:01:23] of higher dimensional stuff that I didn't present.
[01:01:23 -> 01:01:24] Thanks.
[01:01:24 -> 01:01:25] Okay, thank you.
[01:01:25 -> 01:01:26] And thanks Kevin for the question.
[01:01:26 -> 01:01:28] So we'll stop the presentation here.
[01:01:28 -> 01:01:29] Thanks again, Astra.
