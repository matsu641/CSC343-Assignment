University of Toronto
csc343, Winter 2026

# Assignment 3

Due: Wednesday, April 1st, at 3:00 pm.
You must declare your partnership (or that you are working solo) on MarkUs before the above due date, even if you
have an extension.

FAQ: A summary of key clarifications for this assignment will be provided in an FAQ on Piazza if needed. Check it
regularly for updates. Both the FAQ and any Quercus announcements are required reading.

## Learning Goals

By the end of this assignment you should be able to:

- identify tradeoffs that must be made when designing a schema in the relational model, and make reasonable
    choices,
- express a schema in SQL’s Data Definition Language,
- identify limitations to the constraints that can be expressed using the DDL,
- identify and document constraints that would require assertions or triggers to implement (but you will NOT
    write any assertions or triggers in this assignment),
- appreciate scenarios where the rigidity of the relational model may force an awkward design,
- generate example data to populate the schema you design,
- formally reason about functional dependencies, and
- apply functional dependency theory to database design.

This assignment is more open-ended that the other two assignments in the course. This is on purpose. We will
be looking for you to follow the guiding principles below, but there is no one “right” answer we are looking for.

## Part 1: Informal Relational Design

In class, we are in the middle of learning about functional dependencies and how they are used to design relational
schemas in a principled fashion. After that, we will learn how to use Entity-Relationship diagrams to model a domain
and come up with a draft schema which can be normalized according to those principles. By the end of term you
will be ready to put all of this together, but in the meanwhile, it is instructive to go through the process of designing
a schema informally. We expect that what you are learning in class helps inform your decisions in this assignment,
but we do not expect that your schema is normalized in the ways we discuss in lecture. Instead, you should aim to
make good design decisions, informed by what we are learning in class, and you should document the choices you
are making and why.

### The domain

Suppose a new company is trying to break into the concert ticket business and you are designing the database
back-end for their app. Below is the information that they want to be able to store for their first proof-of-concept
version of the database. There is much more to be added later, such as credit card information, but this is not your
responsibility.


- Concerts are booked into venues. A venue has a name (not unique), city, and street address.
- Every venue also has an owner, which could be a person or an organization or company. For now we are just
    storing the owner name as a string, and a single phone number associated with the owner. No two owners have
    the same phone number.
- Some people/organizations own multiple venues but all venues have a single owner (as defined above).
- Every venue has at least 10 seats and there is no upper limit. Each seat has an identifier, such as “B37” (but
    it could be any string).
- Seats in a venue are organized into sections. The same organization is used for every concert in that venue.
    Every seat belongs to exactly one section. Each section has a name, such as “floor level 1” that is unique within
    that venue, but another venue might use the same section name.
- Seat names do not repeat within the same section in a venue. But two different sections may have seats with
    the same name.
- Every concert has a name, such as “Mariah Carey - Merry Christmas to all”, a date and time, and is in exactly
    one venue. We won’t worry about concert durations or end times.
- All seats in the venue are available for every concert, i.e., we won’t account for venues that have different
    configurations where some seats are closed off for some concerts.
- Concert names are not unique. For instance, a concert with the same name may be given for several nights in
    a row in the same venue, or may tour to venues across many cities.
- A venue can only have one concert at a given date and time.
- In each venue, some seats — anywhere from none to all seats — are accessible to people with mobility issues.
- The price of a ticket depends the concert and the section in which the seat is located within the venue.
- Users of the app have a unique username, and that’s all we’ll store about them for now. A user can purchase
    one or more tickets to any concert. When we record this, we also record the date and time of purchase.

Several features above are not realistic, for instance that every seat in a venue is available for every concert, but they
simplify your assignment. If we have not constrained something, assume it is unconstrained. For example, if we said
houses have windows but didn’t constrain it further, you should be prepared that a house may have no windows, 1
window, or many windows.

### Task 1: Define a schema

Your first task is to construct a relational schema for our domain, expressed in DDL. Write your schema in a file
calledschema.ddl.

As you know, there are many possible schemas that satisfy the description above. There is no single right answer
we are looking for. Instead, we are looking to see how the schema you choose deals with the principles below.

We aren’t following a formal design process for Part 1, so instead follow as many of these general principles as
you can when choosing among options:

1. Avoid redundancy.
2. Avoid designing your schema in such a way that there are attributes that can be NULL.
3. If a constraint given above in the domain description can be expressed without using assertions or triggers,
    then it should be enforced by your schema, unless you can articulate a good reason not to do so.
4. There may be additional constraints that make sense but were not specified in the domain description. You
    get to decide on whether to enforce any of these in your DDL.


You may find there is tension between some of these principles. Where that occurs, prioritize in the order shown
above. Use your judgment to make any other decisions. Additional requirements:

- Define appropriate constraints, i.e.,
    - Define a primary key for every table. Make it a single attribute that is an integer (you can use type
       SERIAL if you like). We are about to learn that single-attribute integer keys are ideal. One reason is that
       it makes search by the primary key, which we expect to do a lot or we wouldn’t have defined something as
       the primary key, faster. Every time a comparison is needed during the search, it is just a comparison of
       two ints. Computers are really fast at comparing ints! Having a single integer as primary key also makes
       joining on the primary key much faster, and this is something that will happena lot.
    - UseUNIQUEif appropriate to further constrain the data.
    - Define foreign keys as appropriate.
    - For each column, add aNOT NULLconstraint unless there is a good reason not to.
- All constraints associated with a table must be defined either in the table definition itself, or immediately after
    it.
- To facilitate repeated importing of the schema as you correct and revise it, begin your DDL file with our
    standard three lines:

```
drop schema if exists TicketSchema cascade;
create schema TicketSchema;
set search_path to TicketSchema;
```
You may invent IDs, or define additional columns if you feel this is appropriate. Use your best judgment.

There may be things we didn’t specify that you would like to know. In a real design scenario, you would ask your
client or domain experts. For this assignment, make reasonable assumptions. Keep track of these in writing, as we
will ask you to articulate them at the top of your DDL file.

### Is it really okay to invent IDs?

Don’t be reluctant to invent IDs—it can sometimes really simplify things. Think back to the old, familiar university
database. In the Offering table, we made up the oID column so that we wouldn’t have to use the combination of
{dept, cnum, term, instructor}to identify an offering when we needed to refer to a single offering, for instance, in
the Took table. This simplified the Took table, and also made joins between Offering and Took much easier!

Sometimes, introducing an invented ID will take away the opportunity to enforce a constraint. For example,
suppose we wanted to enforce that no student can take the same course (dept-cnum combination) twice. With
relational algebra, we can write arbitrarily complex constraints. But in SQL, we have more limited things we can
express in a table definition. If the Took table only has oID, we can’t enforce the constraint. So we might consider
including dept and cnum into Took. We’d still need oID so we could do a join to find out the term and instructor.
What are the pros and cons of this design?

- It allows us to enforce the new constraint: we could say that sid, dept, cnum is unique in Took.
- But it makes the design much more complicated, and it introduces redundancy. If Offering already says that
    offering 14239 is csc108, we don’t need to repeat that in the Took table every time there is a row about
    someone’s grade in offering 14239! This also opens up the opportunity for update and deletion anomalies,
    which is very bad.

On balance, we would not recommend choosing this design with dept and cnum included in the Took table. We’d
suggest sacrificing constraint enforcement in order to avoid the negative consequences described above. And in a
real situation, we wouldn’t need to rely on the DDL to do all constraint enforcement; we could write the Python
methods that update the Took table so that they enforce the constraint!


### Task 2: Document your choices and assumptions

At the top of your DDL file, include a comment that answers these questions:

- Could not:What constraints from the domain specification could not be enforced without using assertions
    or triggers, if any? (Again, you are not writing any assertions or triggers on this assignment.)
- Did not:What constraints from the domain specification could have been enforced without using assertions
    or triggers, but were not enforced, if any? Why not?
- Extra constraints:What additional constraints that we didn’t mention did you enforce, if any?
- Assumptions:What assumptions did you make?
    There may be things we didn’t specify that you would like to know. In a real design scenario, you would ask
    your client or domain experts. For this assignment, make reasonable assumptions and document them here.

Use the headings given above, and where there are no items to list under a heading, write “None”.

### Task 3: Make an instance and write queries

Once you have defined your schema, create a file calleddata.sqlthat inserts data into your database with the
schema you designed above. This file should insert the data necessary to have the queries described below produce
results as described. You may find it instructive to consider this data as you are working on the design.

Note: If you have not already developed some automated processes for generating data, we encourage you to do
that now. Remember that the only generative AI tool you should be sharing course materials with is UofT’s Copilot
instance. It is OK to use Copilot to help you generate the data here; you will still need to verify it.

```
Then, write queries to do the following:
```
1. For each concert, report the total number of tickets sold, total value of all tickets sold, and the percentage of
    the venue that was sold. The result should include at least three concerts, with one having at least 50 tickets
    sold, one with 0 tickets sold, and one with somewhere between 0 and 50 (exclusive). It is OK to have more
    concerts in your result.
2. For each owner, report how many venues they own. There must be at least 5 rows in the result, and at least
    one owner must own 3 or more venues.
3. For each venue, report the number of seats and the percentage of seats that are accessible. There must be at
    least 10 rows in the result, and each venue must have at least 10 seats. At least one venue must be at least
    25% accessible.
4. Report the username of the person who has purchased the most tickets and the number of tickets they have
    purchased. If there is a tie, report them all. The top number of tickets must be at least 25.

We will not be autotesting your queries, so you have latitude regarding details like attribute types and output format.
Make good choices to ensure that your output is easy to read and understand. You do not need to worry about how
your queries handle corner cases.

Write your queries in files calledq1.sqlthroughq4.sql. Download filerunner.txt, which has commands to
import each query one at a time. Once all your queries are working, start postgreSQL, importrunner.txt, and cut
and paste your entire interaction with the postgreSQL shell into a plain text file calleddemo.txt. We will assess
the correctness of your queries based only on reading demo.txt, so it must show both the queries being run and the
results of the queries. There is no need to insert into tables (since we are not autotesting). We will also be looking
at your queries to make sure they access the appropriate tables you defined in your schema.

There will be lots of notices, like: Eg. INSERT 0 1, psql:q2.sql:16: NOTICE: view ”blah” This is normal, and
we are expecting to see it.


### What to hand in for Part 1

Hand in plain text filesschema.ddl,data.sql, andq1.sqlthroughq4.sql, anddemo.txt. These must be plain
text files.

IMPORTANT:You must include the demo file, and it must show the output of your queries, or you will get
zero for this part of the assignment.

### How Part 1 will be marked

Your design for Part 1 will be graded for how well you document your design choices, and for design quality, including:
whether it can represent the data described above, appropriate enforcement of the constraints described, avoiding
redundancy, avoiding unnecessary NULLs, following the priorities given above above for any tradeoffs that had to
be made, and good use of DDL (choice of types, NOT NULL specified wherever appropriate, etc.) Your queries will
be assessed for correctness, as described above.

```
Your code will also be assessed for these qualities:
```
- Names: Is every name well chosen so that it will assist the reader in understanding the code quickly? This
    includes table, view, and column names.
- Comments:
    Does every table or view have a comment above it specifying clearly exactly what a row means? Together, the
    comments and the names should tell the reader everything they need to know in order to use a table or view.
    For views in particular, comments should describe the data (e.g., “The student number of every student who
    has passed at least 4 courses.”) not how to find it (e.g., “Find the student numbers by self-joining.. .”).
- Formatting according to these rules:
    - An 80-character line limit is used.This is important so your submission is readable in MarkUs
       for the graders
    - Keywords are capitalized consistently, either always in uppercase or always in lowercase.
    - Table names begin with a capital letter and if multi-word names, use CamelCase.
    - attribute names are not capitalized.
    - Line breaks and indentation are used to assist the reader in parsing the code.

Your queries will be graded based on whether they give the correct answer for your dataset and meet the required
conditions.


## Part 2: Functional Dependencies, Decompositions, and Normal Forms

In your answers for this part, please list all attributes in final relations and FDs for each part in alphabetical order.
This will make it easier for the graders to read your answers. Within each individual FD, this means stating an FD
asXY→ABC, not asY X→BCA. Also, list the FDs in alphabetical order ascending according to the left-hand
side, then by the right-hand side. This means,W X→Acomes beforeW XZ→Awhich comes beforeW XZ→B.
You could also combine FDs with the same LHS in your final answer.

1. Consider a relationR 1 with attributesLMNOP QRSwith functional dependenciesS 1 :

```
S 1 ={L→NQ, MNR→O, O→M, NQ→LS, S→OP R}
```
```
(a) State which of the given FDs violate BCNF.
(b) Employ the BCNF decomposition algorithm to obtain a lossless and redundancy-preventing decomposition
of relationR 1 into a collection of relations that are in BCNF. Make sure it is clear to the reader which
relations are in the final decomposition, and don’t forget to project the dependencies onto each relation
in that final decomposition. Because there are choice points in the algorithm, there may be more than
one correct answer. List the final relations in alphabetical order.
(c) Does your schema preserve dependencies? Explain how you know that it does or does not.
(d) Use the Chase Test to show that your schema is a lossless-join decomposition. (This is guaranteed by the
BCNF algorithm, but it’s a good exercise.)
```
2. Consider a relationR 2 with attributesABCDEF GHand functional dependenciesS 2.

```
S 2 ={AB→C, C→ABD, CF D→E, E→B, BF→EC, B→DA}
```
```
(a) Compute a minimal basis forS 2. In your final answer, put the FDs into alphabetical order.
(b) Using your minimal basis from the last subquestion, compute all keys forR 2.
(c) Employ the 3NF synthesis algorithm to obtain a lossless and dependency-preserving decomposition of
relationR 2 into a collection of relations that are in 3NF. Do not “over normalize”. This means that you
should combine all FDs with the same left-hand side to create a single relation. If your schema includes
one relation that is a subset of another, remove the smaller one.
(d) Does your schema allow redundancy? Explain how you know that it does or does not.
```
Show all of your steps so that we can give part marks where appropriate. There are no marks for simply a correct
answer. You must justify every shortcut that you take.

### What to hand in for Part 2

Type your answers up using a tool like LaTeX or Word. Hand in your typed answers, in a single pdf file called
a3.pdf. Handwritten submissions will not be accepted and will receive a grade of 0.

## Final Thoughts

Submission:Check that you have submitted the correct version of your files by downloading it from MarkUs; new
files will not be accepted after the due date.

Marking:The marking scheme will be approximately this: Part 1 70%, and Part 2 30%.

Some parting advice:It will be tempting to divide the assignment up with your partner. Remember that both of
you probably want to answer all the questions on the final exam.


