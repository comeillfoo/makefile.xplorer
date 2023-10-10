#lang br

makefile : statement*

statement : comment | assignment | conditional

conditional : conditional-directive statement+ ( "else" conditional-directive statement+ )* [ "else" statement+ ] "endif"

conditional-directive : "ifdef" variable | "ifndef" variable

variable-name : TARGET
get-variable : "$(" variable-name ")"
variable-substituion : "$(" get-variable ")" | "$(" variable-substituion ")"

assignment-op : "+=" | "="
assignment : pattern assignment-op path+

path : DIR* FILE

pattern : [ TARGET ] [ get-variable ] TARGET
