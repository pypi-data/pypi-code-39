"""A starter tutorial to learn about ASP.

"""


TUTORIAL_NAME = 'ASP basics'
ORDERED_TUTO = (
"""
$focus Graph
% Hello !
% This interactive tutorial is written in ASP.
% As you can see, everything after a '%' is a comment.

% The Run button below will run the code in this box.
%  Currently, it will give you an empty model and therefore an empty graph
%  (see in the tabs, upper center of your screen).

% To start the tutorial, touch the Next button below.
$end
""", """
$focus ASP
$run
% Let's talk about atoms
% Atoms are the most basic objects in ASP. Here is one:

a.

% This is the atom 'a'.
% The dot is the statement terminator (like semicolons in C).

% For ASP, this signifies that the atom 'a' is true.
% Everything that is not true is false:
%  therefore all ASP program is really
%  about finding which atoms should be true.

% Any name matching [a-z_][A-Za-z0-9_]+ is a valid literal name,
%  and a valid atom name:

hello_world09.

% Atoms can have any number of arguments:

father(luke,vader).  % Arity of 2

% ('Arity' is a fancy name for 'number of arguments')

myatom(with,3,"arguments").  % May be any type

myatom(with(1,internal_atom(also_having_an("internal atom !")))).  % And can be nested !


$run
% I just hit the Run button for you, telling biseau to read the code here and execute it.
$pause

% Lookup the tabs on the left:
% ASP and Models tabs have changed.

$focus ASP
$wait 1
% ASP hold our program, which will come in handy much later.

$focus Models
$wait 1
% Models on the other hand is already useful:
%  it shows us the ASP atoms that where derived from our program.
% Very useful for debugging !

% The two other tabs are basically empty. We will soon see their interest.
% But first, let's finish to dive into atoms.
$end
""", """
% Before diving into the real thing, let's review some basic data encoding.
% Numbers:
order(10).  % tells us order(10) is true.
$run
% Strings:
name(1,"Yolande").  % the first name is Yolande
name(2,"Gaspard").  % the second one is Gaspard
$run

% We're ready ; let's go !
$end
""", ("""
% First exercise.

% Create an atom of predicate 'hello', having 3 arguments:
%  one integer, one string and one literal.

% Let's go: write something in that area,
%  and hit the Validate button below
%  your answer to check.
""",
    # validation function:
    lambda model: any(any(type(arg) is int for arg in args) and
                      any(type(arg) is str and not arg.startswith('"') for arg in args) and
                      any(type(arg) is str and arg.startswith('"') for arg in args)
                      for args in model.get('hello/3', ())),  # expected output
), """
% We saw that we could write atoms such as:
father(luke,"Darth Vader").
$run

% But then, nothing really interesting happen.

% Let's try this atom now:

node(a).  % an atom of predicate 'node', with one argument being the literal 'a'.

% If you hit Run now, and visit the 'Graph' tab, you will see a node named 'a'.
% Let me do that.
$run
$focus Graph

% This is not strictly speaking ASP, but rather biseau: biseau looks for
%  particular atoms in the 'Models' tab, node/1 being one of them.

$end
""")
# """, """
