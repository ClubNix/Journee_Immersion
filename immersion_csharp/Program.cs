// See https://aka.ms/new-console-template for more information
using System;
using System.Text;
using System.Diagnostics;

public class Program {
	private static string x0rD3c0de(int[] arr, int[] keys) {
		byte[] ret = new byte[arr.Length];
		for(int i = 0; i < ret.Length; i++) {
			ret[i] ^= (byte)((arr[i] ^ keys[i % keys.Length]) % 256);
		}
		return Encoding.UTF8.GetString(ret, 0, ret.Length);
	}
	public static void Main(string[] args) {
		string PASSWORD = x0rD3c0de(
			new int[] { 121, 107, 109, 55 },
			new int[] { 1, 2, 3, 4 }
		);
		if(args.Length == 0) {
			Console.WriteLine("Usage: ./immersion <password>");
			return;
		}
		if(args[0] == PASSWORD) {
			Console.WriteLine("Félicitations, vous avez trouvé le mot de passe !");
		} else {
			Console.WriteLine("HAHAHAHAHAHAHAHAHAHA vous ne trouverez jamais le mot de passe !");
		}
		return;
	}
}


/*
code original en rust:


use std::env;
    fn main(){
	    const PASSWORD:&str = "GUESS";
	    let input = match env::args().nth(1) {
	            Some(input) => input,
	            None => {
                    println!("Usage: ./immersion <password>");
                    return;
                }
        };
	    let input = input.trim();
	    match input.eq(PASSWORD) {
		true => {
		    println!("Félicitations, vous avez trouvé le mot de passe !");
		},
		false => println!("HAHAHAHAHAHAHAHAHAHA vous ne trouverez jamais le mot de passe !")
	    }
*/

