(*******************************************************************
   This file ("translator.ml") provides stub functions for the extra
   code you need to write for this assignment.

   There are two major stub functions in "translator.ml":
   "ast_ize_P" (which transforms a parse tree for a program into
                an abstract syntax tree[AST]); and
   "translate" (which translates an AST into an equivalent C program).

   You are also being provided with a file called "parser.ml" which
   contains working code to produce a parse tree for a program.
   Everything in the file "parser.ml" is complete and usable as-is.

   The major entry point for the parser provided in "parser.ml" is
   a function called "parse" invoked with two parameters: A parse table,
   and a string containing a calculator language program.

   The file "parser.ml" constructs two example parse tables:
   "cg_parse_table" (for the original calculator language grammar), and
   "ecg_parse_table" (for the extended calculator language grammar).

   Here are two parser examples which will work as-is:

      parse cg_parse_table sum_ave_prog;;
      parse ecg_parse_table primes_prog;;
   		
   "sum_ave_prog" and "primes_prog" are provided at the end of this
   file (as strings). "sum_ave_prog" uses the original calculator
   language grammar, while "primes_prog" uses the extended calculator
   language grammar.

   When complete, your translator code should work when invoked as
   follows:

      print_string
        (snd
          (translate
            (ast_ize_P
              (parse ecg_parse_table primes_prog)
            )
          )
        );;
   	
   The result of this invocation should be a C program on standard
   output, which can be compiled and run to produce the first N primes
   (where N is a number typed by the user).
 *******************************************************************)

#use "parser.ml";;


(*******************************************************************
   Declarations and functions to transform a parse tree into an
   abstract syntax tree (AST)
 *******************************************************************)

type ast_sl = ast_s list
and ast_s =
    | AST_error
    | AST_assign of (string * ast_e)
    | AST_read of string
    | AST_write of ast_e
    | AST_if of (ast_e * ast_sl)
    | AST_do of ast_sl
    | AST_check of ast_e
and ast_e =
    | AST_binop of (string * ast_e * ast_e)
    | AST_id of string
    | AST_num of string;;

	
let rec ast_ize_P (p:parse_tree) : ast_sl =
  (* your code should replace the following line *)
  match p with
  | PT_nt ("P", [statement_list; PT_term "$$"])
        -> (ast_ize_SL statement_list)
  | _ -> raise (Failure "malformed parse tree in ast_ize_P") 

and ast_ize_SL (sl:parse_tree) : ast_sl =
  match sl with
    | PT_nt ("SL", []) -> []
(*
your code here ...
*)
  | PT_nt("SL", [statement; statement_list])
        -> (ast_ize_S statement)::(ast_ize_SL statement_list)
  | _ -> raise (Failure "malformed parse tree in ast_ize_SL")

and ast_ize_S (s:parse_tree) : ast_s =
  match s with
    | PT_nt ("S", [PT_id lhs; PT_term ":="; expr])
      -> AST_assign (lhs, (ast_ize_expr expr))
(*
your code here ...
*)
  | PT_nt ("S", [PT_term "read"; PT_id rhs])
      -> AST_read(rhs)
  | PT_nt ("S", [PT_term "write"; expr])
      -> AST_write(ast_ize_expr expr)
  | PT_nt ("S", [PT_term "if"; relation ; statement_list; PT_term "fi"])
        -> AST_if (ast_ize_expr relation, ast_ize_SL statement_list)
  | PT_nt ("S", [PT_term "do"; statement_list ; PT_term "od"])
        -> AST_do (ast_ize_SL statement_list)
  | PT_nt ("S", [PT_term "check"; relation])
        -> AST_check (ast_ize_expr relation)
  | _ -> raise (Failure "malformed parse tree in ast_ize_S")

and ast_ize_expr (e:parse_tree) : ast_e =
  (* e is an R, E, T, or F parse tree node *)
  match e with
(*
your code here ...
*)
  | PT_nt ("R", [expr; expr_tail])
      -> ast_ize_reln_tail (ast_ize_expr(expr)) (expr_tail)
  | PT_nt ("E", [term; term_tail])
      -> ast_ize_expr_tail (ast_ize_expr(term)) (term_tail)
  | PT_nt ("T", [factor; factor_tail])
        -> ast_ize_expr_tail (ast_ize_expr(factor)) (factor_tail)
  | PT_nt ("F", [PT_id id])
        -> AST_id (id)
  | PT_nt ("F", [PT_num num])
        -> AST_num (num)
  | PT_nt ("F", [PT_term "("; expr ; PT_term ")"])
        -> ast_ize_expr (expr)
  | _ -> raise (Failure "malformed parse tree in ast_ize_expr")

and ast_ize_reln_tail (lhs:ast_e) (tail:parse_tree) : ast_e =
  (* lhs is an inherited attribute.
     tail is an ET parse tree node *)
  match tail with
(*
your code here ...
*)
  | PT_nt ("ET", []) -> lhs
  | PT_nt ("ET", [PT_nt(ro, [PT_term operator]); expr]) -> AST_binop (operator, lhs, ast_ize_expr(expr))
  | _ -> raise (Failure "malformed parse tree in ast_ize_reln_tail")

and ast_ize_expr_tail (lhs:ast_e) (tail:parse_tree) : ast_e =
  (* lhs is an inherited attribute.
     tail is a TT or FT parse tree node *)
  match tail with
(*
your code here ...
*)
  | PT_nt ("TT", []) -> lhs
  | PT_nt ("FT", []) -> lhs
  | PT_nt ("TT", [PT_nt (ao, [PT_term operator]); term; term_tail])
      -> AST_binop (operator, lhs, (ast_ize_expr_tail(ast_ize_expr(term)) term_tail))
  | PT_nt ("FT", [PT_nt (mo, [PT_term operator]); factor; factor_tail])
      -> AST_binop (operator, lhs, (ast_ize_expr_tail(ast_ize_expr(factor)) factor_tail))
  | _ -> raise (Failure "malformed parse tree in ast_ize_expr_tail")
;;


(*******************************************************************
   Functions to translate an AST into C
 *******************************************************************)

(* The code below is (obviously) a bare stub. The intent is that when
   you run translate on a full, correct AST, you'll get back code for an
   equivalent C program. If there are any variables that are written in
   the program but never read, you'll also get a warning message`
   indicating their names and the lines on which the writes occur. Your
   C program should contain code to check for dynamic semantic errors. *)

let rec translate (ast:ast_sl) 
:  string *  string = 
  let t1, t2, t3 = translate_sl ast [] [] in
  ("WARNING - The following variables were declared but never used: "^(warning t1 t2) ^ "\n", out^t3^"}\n")

and translate_sl (ast:ast_sl) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with 
  | head :: tail -> 
  let t1, t2,t3 = translate_s head terms used in
  let t4, t5, t6 = translate_sl tail t1 t2 in
  (t4, t5, t3 ^ t6)
  | _ -> (terms,used, "")

and translate_s (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_assign id_e-> translate_assign ast terms used
  | AST_read id -> translate_read ast terms used
  | AST_write e -> translate_write ast terms used
  | AST_if e_sl-> translate_if ast terms used
  | AST_do sl -> translate_do ast terms used
  | AST_check e -> translate_check ast terms used
  | _ -> raise (Failure "translate_s ")

and translate_assign (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_assign (id, e) -> 
    let t1, t2, t3 = translate_expr e terms used in
    let db2 = if mem id terms then terms else id::terms in
    (db2, t2, "setvar(" ^ "\"" ^id ^ "\", " ^ t3 ^ ");\n")
  | _ -> raise (Failure "translate_assign ")

and translate_read (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_read id-> let db2 = if mem id terms then terms else id::terms in
  (db2, used, "setvar(" ^ "\"" ^id ^ "\", getint()); \n")
  | _ -> raise (Failure "translate_read ")

and translate_write (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_write e -> 
    let t1, t2, t3 = translate_expr e terms used in
    (t1, t2, "putint(" ^ t3 ^ ");\n")
  | _ -> raise (Failure "translate_write ")

and translate_if (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_if (e, sl) -> 
    let t1, t2, t3 = translate_expr e terms used in
    let t4, t5, t6 = translate_sl sl t1 t2 in
    ( t4, t5, "if (" ^ t3 ^ ")\n {\n" ^ t6 ^ "}\n")
  | _ -> raise (Failure "translate_if ")

and translate_do (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_do sl -> 
    let t1, t2, t3 = translate_sl sl terms used in
    (t1, t2, "while (1) {" ^ t3 ^ "}\n")
  | _ -> raise (Failure "translate_do ")

and translate_check (ast:ast_s) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_check e -> 
    let t1, t2, t3 = translate_expr e terms used in
    (t1, t2, "if(!(" ^ t3 ^ ")) break;\n")
  | _ -> raise (Failure "translate_check")

and translate_expr (ast:ast_e) (terms:string list) (used: string list):  string list * string list *  string = 
  match ast with
  | AST_binop ("/", e1, e2) -> 
    let t1, t2, t3 = translate_expr e1 terms used in
    let t4, t5, t6 = translate_expr e2 t1 t2 in
    (t4, t5, "divide(" ^ t3 ^ ", " ^ t6 ^ ") ")
  | AST_binop (op, e1, e2 )-> 
    let t1, t2, t3 = translate_expr e1 terms used in
    let t4, t5, t6 = translate_expr e2 t1 t2 in
    (t4, t5, t3 ^ op ^ t6)
  | AST_id id -> 
    let used = if mem id terms then id::used else used in
    (terms, used, "getvar( \"" ^ id ^ "\"" ^ ")")
  | AST_num num -> (terms, used, num);;
 
let rec warning (terms:string list) (used: string list) : string =
  match terms with
  | head :: tail-> if mem head used then warning tail used else head^ " " ^ (warning tail used)
  | _ -> "";;
  

let out = "

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int array[100];
char* string[100];

int getint() 
  {
  char str[100];
  int n = scanf(\"%s\", str);
  if(n != 1)
      {
    printf(\"Unexpected end of input!\\n\");
    exit(1);
      }
  else{
    for(int k = 0; str[k]!='\\0' ; k++)
      {
      if(str[k] >'9' || str[k] <'0')
        {
        printf(\"non numeric input!\\n\");
        exit(1);
        }
      }
    return atoi(str);
      }
  }
void putint(int n) 
{
  printf(\"%d\\n\", n);
}

int divide (int a, int b)
{
  if(b == 0)
  {
    printf(\"A division by zero error!\\n\");
    exit(1);
  }
  return a/b ;
}

int getvar(char* a)
  {
  for(int i = 0; string [i] != 0;i++)
    {
    if(!strcmp(string[i],a)){
      return array[i];
    }
  }
  printf(\"Use of uninitialized variable %s\\n\", a);
  exit (1);
}
int setvar(char* a, int n)
  {
  int i;
  for(i = 0; string [i] != 0;i++)
    {
    if(!strcmp(string[i],a)){
      array[i] = n;
      return 1;
    }
  }
  string[i] = a;
  array[i] = n; 
  return 0;
}

int main(int argc, char* argv[]) 
{
  int a; a = getint();
  int b; b = getint();
  int sum; sum = a + b;
  putint (sum);
  putint (sum/2);
  return 0;
}
";;



(*******************************************************************
   Sample programs in the calculator language
 *******************************************************************)



let sum_ave_prog = "
  read a
  read b
  sum := a + b
  write sum
  write sum / 2";;
	 
let primes_prog = "
  read n
  cp := 2
  do check n > 0
    found := 0
    cf1 := 2
    cf1s := cf1 * cf1
    do check cf1s <= cp
      cf2 := 2
      pr := cf1 * cf2
      do check pr <= cp
        if pr == cp
          found := 1
        fi
        cf2 := cf2 + 1
        pr := cf1 * cf2
      od
      cf1 := cf1 + 1
      cf1s := cf1 * cf1
    od
    if found == 0
      write cp
      n := n - 1
    fi
    cp := cp + 1
  od";;
