"""Tutorial to show how to produce FCA visualization with biseau.

"""


TUTORIAL_NAME = 'Implements FCA with biseau: a primer'
ORDERED_TUTO = (
"""
% Lets represent the following formal context:

%          |1|2|3|4|5|
%         a|×| |×| |×|
%         b| |×|×| | |
%         c| |×| |×|×|
%         d|×|×| |×| |
%         e|×| |×|×|×|

% To do this, we will use rel/2 atoms:
rel(a,1).  % object a holds attribute 1.

% Lets define all of them:
rel(a,(3;5)).  % Equivalent to write both "rel(a,3)." and "rel(a,5)."

% The full context:

$speed quick
% Formal context:    %   |1|2|3|4|5|
rel(a,(1  ;3  ;5)).  %  a|×| |×| |×|
rel(b,(  2;3    )).  %  b| |×|×| | |
rel(c,(  2  ;4;5)).  %  c| |×| |×|×|
rel(d,(1;2  ;4  )).  %  d|×|×| |×| |
rel(e,(1  ;3;4;5)).  %  e|×| |×|×|×|

$end
""", """$title Mine the formal concepts

% Let's mine the formal concepts.

$speed instant
% Formal context:    %   |1|2|3|4|5|
rel(a,(1  ;3  ;5)).  %  a|×| |×| |×|
rel(b,(  2;3    )).  %  b| |×|×| | |
rel(c,(  2  ;4;5)).  %  c| |×| |×|×|
rel(d,(1;2  ;4  )).  %  d|×|×| |×| |
rel(e,(1  ;3;4;5)).  %  e|×| |×|×|×|
$speed normal

ext(X) :-              % (0)
    rel(X,_) ;         % (1)
    rel(X,Y): int(Y).  % (2)
$pause

% (0) X belong to the extent if…
$pause
% (1) X is an object, and
$pause
% (2) for all Y in intent, there is a link between X and Y.
$pause

% The intent has the exact same definition:
int(Y) :-
    rel(_,Y) ;
    rel(X,Y): ext(X).
$pause

% (0) Y belong to the intent if…
% (1) Y is an attribute, and
$pause
% (2) for all X in extent, there is a link between X and Y.
$pause

% this is enought to get all concepts,
%  and also supremum and infimum.

% Once run, we got one model for each formal concept.
$run
$focus Models

% For the moment however, we got nothing to show as a graph.

$end
""", """$title Aggregate the formal concepts

$speed instant
% Formal context:    %   |1|2|3|4|5|
rel(a,(1  ;3  ;5)).  %  a|×| |×| |×|
rel(b,(  2;3    )).  %  b| |×|×| | |
rel(c,(  2  ;4;5)).  %  c| |×| |×|×|
rel(d,(1;2  ;4  )).  %  d|×|×| |×| |
rel(e,(1  ;3;4;5)).  %  e|×| |×|×|×|

$speed quick
% Mining the formal concepts.
ext(X) :- rel(X,_) ; rel(X,Y): int(Y).
int(Y) :- rel(_,Y) ; rel(X,Y): ext(X).
$speed normal

% The previous stage provided us one model for each concept,
%  but in order to compare them for the concept lattice building,
%  we need to aggregate them.

% In biseau, a checkbox is available under scripts.

$aggregate true
$run
$focus Models
% I just emulate that. Look at the Models.
$end
""", """$title Build the concept lattice

% In the previous stage, we obtained the following atoms:
$speed instant
ext(0,c).  int(0,2).  int(0,4).  int(0,5).
ext(1,c).  ext(1,e).  int(1,4).  int(1,5).
ext(2,c).  ext(2,d).  ext(2,e).  int(2,4).
ext(3,c).  ext(3,d).  int(3,2).  int(3,4).
ext(4,a).  ext(4,c).  ext(4,e).  int(4,5).
ext(5,b).  ext(5,c).  ext(5,d).  int(5,2).
ext(6,a).  ext(6,b).  ext(6,c).  ext(6,d).  ext(6,e).
ext(7,d).  ext(7,e).  int(7,1).  int(7,4).
ext(8,d).  int(8,1).  int(8,2).  int(8,4).
ext(9,a).  ext(9,d).  ext(9,e).  int(9,1).
ext(10,e).  int(10,1).  int(10,3).  int(10,4).  int(10,5).
ext(12,a).
int(11,1).  int(11,2).  int(11,3).  int(11,4).  int(11,5).
ext(12,e). int(12,1).  int(12,3).  int(12,5).
ext(13,b).  int(13,2).  int(13,3).
ext(14,a).  ext(14,b).  ext(14,e).  int(14,3).
$speed normal

$end
"""
)
# """, """
