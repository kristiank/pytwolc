==============================
Morphophonemic representations
==============================

In linguistics, we say that word forms consist of :term:`morphs <morph>`, which are sequences of :term:`phonemes <phoneme>` and which have a meaning, e.g.: a Finnish word form ``kaloja`` could be broken into three morphs::

  kalo - 'a fish' - KALA
  j    - plural
  a    - partitive

Another word form ``kalassa`` could be segmented as::

  kala - 'a fish' - KALA
  ssa  - inessive

Our goal is to find a common representation for morphs of the same :term:`morpheme`.  E.g. for ``kala`` and ``kalo`` we could establish a single form ``k a l {ao}`` which could serve as the lexical entry for the morpheme KALA, 'a fish'.

The :term:`morphophonemic representation` can be built from a table of segmented word forms by a set of scripts.  The process is mostly automatic but human intervention is needed in:

- collecting model words and arranging as a table with columns for different relevant forms and rows for different lexemes

- segmenting the word forms so that their morphs are separated e.g. with a period

- renaming the automatically produced raw morphophonemes

The process consists of four scripts:

The input for the first step is a CSV table, e.g.::

   ID,STM,STM INE,STM ESS,STM PL INE
   MÄKI,mäki,mäe.ssä,mäke.nä,mä.i.ssä
   KÄSI,käsi,käde.ssä,käte.nä,käs.i.ssä
   LASI,lasi,lasi.ssa,lasi.na,lase.i.ssa
   LAKI,laki,lai.ssa,laki.na,lae.i.ssa

1. ``paratab2segcsv.py`` which reads in a paradigm table of word forms and writes the data in a format where each word form is on line of its own.  Both the input table and the output file are in the CSV format.  Output contains two fields, e.g.::

     MORPHEMES,MORPHS
     MÄKI,mäki
     MÄKI INE,mäe.ssä
     MÄKI ESS,mäke.nä
     MÄKI PL INE,mä.i.ssä
     KÄSI,käsi
     KÄSI INE,käde.ssä
     KÄSI ESS,käte.nä
     KÄSI PL INE,käs.i.ssä
     LASI,lasi
     LASI INE,lasi.ssa
     LASI ESS,lasi.na
     LASI PL INE,lase.i.ssa
     LAKI,laki
     LAKI INE,lai.ssa
     LAKI ESS,laki.na
     LAKI PL INE,lae.i.ssa

2. ``segm2zerofilled.py`` which reads the data in one word form per line CSV format and aligns each morpheme and writes a CSV file augmented with the aligned i.e. zero-filled example word forms.  The :doc:`alignment` is accomplished by the ``multialign.py`` module, see :py:mod:`multialign`. The output contains the two fields in the input and the zero-filled word forms as the third field, e.g.::

     MORPHEMES,MORPHS,ZEROFILLED
     MÄKI,mäki,mäki
     MÄKI INE,mäe.ssä,mäØe.ssä
     MÄKI ESS,mäke.nä,mäke.nä
     MÄKI PL INE,mä.i.ssä,mäØØ.i.ssä
     KÄSI,käsi,käsi
     KÄSI INE,käde.ssä,käde.ssä
     KÄSI ESS,käte.nä,käte.nä
     KÄSI PL INE,käs.i.ssä,käsØ.i.ssä
     LASI,lasi,lasi
     LASI INE,lasi.ssa,lasi.ssa
     LASI ESS,lasi.na,lasi.na
     LASI PL INE,lase.i.ssa,lase.i.ssa
     LAKI,laki,laki
     LAKI INE,lai.ssa,laØi.ssa
     LAKI ESS,laki.na,laki.na
     LAKI PL INE,lae.i.ssa,laØe.i.ssa

3. ``zerofilled2rawmphon.py`` which reads in the aligned example words and constructs a raw morphophonemic representation for each example word.  The construction is made according to a user given set of *principal forms* i.e. a subset of inflected forms.  If one knows the principal forms, one can mechanically produce all other inflected forms.  Output contains the three fields in the input and two new ones, the raw morphophonemic representation of the word form and the symbol pair (two-level) representation of the word form, e.g.::

     MORPHEMES,MORPHS,ZEROFILLED,RAW,PAIRSYMS
     MÄKI,mäki,mäki,m ä {kØkØ} {ieeØ} ,m ä {kØkØ}:k {ieeØ}:i
     MÄKI INE,mäe.ssä,mäØe.ssä,m ä {kØkØ} {ieeØ} s s {aä},m ä {kØkØ}:Ø {ieeØ}:e s s {aä}:ä
     MÄKI ESS,mäke.nä,mäke.nä,m ä {kØkØ} {ieeØ} n {aä},m ä {kØkØ}:k {ieeØ}:e n {aä}:ä
     MÄKI PL INE,mä.i.ssä,mäØØ.i.ssä,m ä {kØkØ} {ieeØ} i s s {aä},m ä {kØkØ}:Ø {ieeØ}:Ø i s s {aä}:ä
     KÄSI,käsi,käsi,k ä {sdts} {ieeØ} ,k ä {sdts}:s {ieeØ}:i
     KÄSI INE,käde.ssä,käde.ssä,k ä {sdts} {ieeØ} s s {aä},k ä {sdts}:d {ieeØ}:e s s {aä}:ä
     KÄSI ESS,käte.nä,käte.nä,k ä {sdts} {ieeØ} n {aä},k ä {sdts}:t {ieeØ}:e n {aä}:ä
     KÄSI PL INE,käs.i.ssä,käsØ.i.ssä,k ä {sdts} {ieeØ} i s s {aä},k ä {sdts}:s {ieeØ}:Ø i s s {aä}:ä
     LASI,lasi,lasi,l a s {iiie} ,l a s {iiie}:i
     LASI INE,lasi.ssa,lasi.ssa,l a s {iiie} s s {aä},l a s {iiie}:i s s {aä}:a
     LASI ESS,lasi.na,lasi.na,l a s {iiie} n {aä},l a s {iiie}:i n {aä}:a
     LASI PL INE,lase.i.ssa,lase.i.ssa,l a s {iiie} i s s {aä},l a s {iiie}:e i s s {aä}:a
     LAKI,laki,laki,l a {kØkØ} {iiie} ,l a {kØkØ}:k {iiie}:i
     LAKI INE,lai.ssa,laØi.ssa,l a {kØkØ} {iiie} s s {aä},l a {kØkØ}:Ø {iiie}:i s s {aä}:a
     LAKI ESS,laki.na,laki.na,l a {kØkØ} {iiie} n {aä},l a {kØkØ}:k {iiie}:i n {aä}:a
     LAKI PL INE,lae.i.ssa,laØe.i.ssa,l a {kØkØ} {iiie} i s s {aä},l a {kØkØ}:Ø {iiie}:e i s s {aä}:a

4. ``raw2named.py`` which renames some raw morphophonemes of the example word forms and writes a file of examples where each example is a line of blank separated string of :term:`pair symbols <pair-symbol>`.  Pair symbols are the newly renamed ones or if the raw symbol is not yet renamed, the pair symbol is the original raw one.

Assigning names to raw morphophonemes is usually done incrementally with the aid of ``twdiscov.py``, see :doc:`/twdiscov`.  The rule discovery module helps to identify similar raw morphophonemes and to give a common name to them.  One may also write a two-level rule for such tentatively final morphophoneme and test the validity of the rule using ``twol`` rule compiler.  See separate documents for them.