Organization of Programming Languages Assignment 3
Name: Cameron Knopp (project completed solo)

In order to run this program, do the following:

- Start the ocaml interpreter by typing "ocaml" in your terminal
- Enter: #use "translator.ml";;
- Enter: print_string (snd
		(translate (ast_ize_P
		(parse ecg_parse_table primes_prog))));;