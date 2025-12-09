use rand::Rng;
use std::env;
use std::process::Command;

/*fn check_ssh() -> bool {
    println!("Checking SSH service");
    let output = Command::new("systemctl")
        .arg("status")
        .arg("ssh")
        .output()
        .expect("Failed to execute command");
    let output = String::from_utf8_lossy(&output.stdout);
    if output.contains("active (running)") {
        println!("SSH service is running");
        return true;
    } else {
        println!("SSH service is not running");
        return false;
    }
}

fn open_ssh() {
    println!("Opening SSH service");
    let output = Command::new("systemctl")
        .arg("start")
        .arg("ssh")
        .output()
        .expect("Failed to execute command");
    let output = String::from_utf8_lossy(&output.stdout);
    println!("{}", output);
}*/

fn changing_hostname(hostname: &str) {
    println!("Changing hostname to {}", hostname);
    let mut output = Command::new("sudo")
        .arg("hostname")
        .arg(hostname)
        .spawn()
        .expect("Failed to execute command");

    let _result = output.wait().unwrap();
}

fn update_machine() {
    println!("Updating machine");
    let mut output = Command::new("sudo")
    	.arg("apt")
        .arg("update")
        .spawn()
        .expect("Failed to execute command");
    let _result = output.wait().unwrap();

}

fn install_app_with_sudo(app: &str) {
    println!("Installing {}", app);
    let mut output = Command::new("sudo")
        .arg("apt")
        .arg("install")
        .arg(app)
        .arg("-y")
        .spawn()
        .expect("Failed to execute command");
    let _result = output.wait().unwrap();
}

fn code_to_compile() -> String {
    return r#"use std::env;
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
    }"#.replace("GUESS", format!("{}{}", "xin",rand::thread_rng().gen_range(0..9)).as_str());
}

fn python_code() -> String {
    return r#"import subprocess

def generatePasswords():
    """write your password generator and call testPass to check if the password is good"""

def testPass(password: str) -> bool:
    test = subprocess.check_output("./Immersion " + password, shell=True).decode().strip()
    return test != "Haha vous n'aurez pas le mot de passe!!!"

if __name__ == "__main__":
    generatePasswords()"#.to_string();
}


fn install_rust() {
    // Check if Rust is installed
    if Command::new("rustc").output().is_ok() {
        println!("Rust is already installed.");
    } else {
        // Install Rust using rustup
        println!("Rust is not installed. Installing Rust...");

        let status = Command::new("curl")
            .args(&["--proto", "=https", "--tlsv1.2", "-sSf", "https://sh.rustup.rs" , "-o", "rustup-init.sh"])
            .status()
            .expect("Failed to run curl");

        if status.success() {
            let status = Command::new("sh")
                .args(&["rustup-init.sh", "-y"]) // Pass the -y flag for automatic installation
                .status()
                .expect("Failed to run rustup-init.sh");

            if status.success() {
                println!("Rust has been successfully installed.");
                
            } else {
                eprintln!("Error: Rust installation failed.");
                std::process::exit(1);
            }
        } else {
            eprintln!("Error: Failed to download Rust installer.");
            std::process::exit(1);
        }
    }
}

fn main() {
    let hostname = env::args().nth(1).expect("No hostname provided");

    /*if !check_ssh() {
        open_ssh();
    }*/

    install_rust();

    let code = code_to_compile();
    let code_file = "./immersion.rs";
    std::fs::write(code_file, code).expect("Unable to write file");

    let output = Command::new("/home/kali/.cargo/bin/rustc")
        .arg(code_file)
        .output()
        .expect("Failed to execute command");

    println!("Compilation stdout: {}", String::from_utf8_lossy(&output.stdout));
    println!("Compilation stderr: {}", String::from_utf8_lossy(&output.stderr));

    if output.status.success() {
        println!("Compilation successful");
    } else {
        eprintln!("Compilation failed");
        return;
    }

    let python_code = python_code();
    let python_code_file = "./bruteforce_incomplet.py";
    std::fs::write(python_code_file, python_code).expect("Unable to write file");

    update_machine();

    install_app_with_sudo("x11vnc");

    println!("Starting x11vnc");

    Command::new("x11vnc")
        .arg("-forever")
        .arg("-nopw")
        .arg("-quiet")
        .arg("-shared")
        .spawn()
        .expect("Failed to execute command");

    changing_hostname(&hostname);

    println!("X11VNC started");

    println!("script finished bye bye");

}
