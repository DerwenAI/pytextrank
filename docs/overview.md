# Overview

## Open Source Integration

The **kglab** package is mostly about integration.
On the one hand, there are useful graph libraries, most of which don't
share much common ground and can often be difficult to use together.
One the other hand, there are the popular tools used for data science
and data engineering, with expectation about how to repeat process,
how to scale and leverage multi-cloud resources, etc.

Much of the role of **kglab** is to provide abstractions that make
these integrations simpler, while fitting into the tools and processes
that are expected by contemporary data teams in industry.
The following figure shows a *landscape diagram* for how **kglab**
fits into multiple technology stacks and related workflows:

<a href="../assets/landscape.png" target="_blank"><img src="../assets/landscape.png" width="500" /></a>

Items shown in *black* have been implemented, while the items shown in
*blue* are on our roadmap.
We include use cases for most of what's
implemented within the [tutorial](../tutorial/).


## Just Enough Math, Edition 2

To be candid, **kglab** is partly a follow-up edition of 
[*Just Enough Math*](../biblio/#nathan2014jem)
– which originally had the elevator pitch: 

> practical uses of advanced math for business execs (who probably didn't take +3 years of calculus) to understand big data use cases through hands-on coding experience plus case studies, histories of the key innovations and their innovators, and links to primary sources

[*JEM*](../biblio/#nathan2014jem) started as a book which –
thanks to quick thinking by editor Ann Spencer – 
turned into a popular video+notebook series,
followed by tutorials, and then a community focused on open source.
Seven years later the field of 
[data science](../glossary/#data-science)
has changed dramatically
This time around, **kglab** starts as an open source Python library,
with a notebook-based tutorial at its core,
focused on a community and their business use cases.

The scope now is about
[*graph-based data science*](../glossary/#graph-based-data-science),
and perhaps someday this may spin-out a book or other learning materials.


## How to use these materials

Following the *JEM* approach, throughout the tutorial you'll find a
mix of topics:
data science, business context, AI applications, data management, 
design, distributed systems – plus explorations of how to leverage
relatively advanced math, where appropriate.

To addresses these topics, this documentation uses a particular
structure, shown in the following figure:

<a href="../assets/learning.png" target="_blank"><img src="../assets/learning.png" width="500" /></a>

To make these materials useful to a wide audience, we've provided
multiple entry points, depending on what you need:

  * Introduce [concepts](../concepts), exploring the math behind the concepts
  * Point toward histories, [primary sources](../biblio), and other materials for context
  * Show [use cases](../use_case) and linking to related case studies for grounding
  * Practice through [hands-on coding](../tutorial/), based on a progressive example
  * Clarify terminology with a [glossary](../glossary) for shared definitions

Ideally, there should also be two other parts – stay tuned for both:

  * *self-assessments* for personal feedback
  * the coding examples show lead into a *capstone project*

In any case, the objective for these materials is to help people learn
how leverage **kglab** effectively, gain confidence working with
graph-based data science, plus have examples to repurpose for your own
use cases.

Start at any point, whatever is most immediately useful for you.
The material is hyper-linked together; it may be helpful to run
JupyterLab for the coding examples in one browser tab, while reading
this documentation in another browser tab.

Again, we're focused on a [community](../#community-resources)
and pay special attention to their business use cases.
We're also eager to hear your feedback and suggestions for this 
open source project.
