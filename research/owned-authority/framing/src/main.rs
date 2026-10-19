use continuum_journal_framing::{create, decode};
use std::{env, fs, path::Path};

fn main() {
    let args: Vec<String> = env::args().collect();
    let result: Result<(), String> = (|| {
        match args.get(1).map(String::as_str) {
            Some("create") | Some("create-exit-before-reply") if args.len() >= 4 => {
                let records: Vec<_> = args[3..].iter().map(|s| s.as_bytes().to_vec()).collect();
                create(Path::new(&args[2]), &records).map_err(|e| e.to_string())?;
                if args[1] == "create-exit-before-reply" {
                    std::process::exit(73);
                }
                println!(
                    "file sync returned; {} frames; parent directory durability unqualified",
                    records.len()
                );
            }
            Some("read") if args.len() == 3 => {
                let image = fs::read(&args[2]).map_err(|e| e.to_string())?;
                let records = decode(&image).map_err(|e| format!("integrity refusal: {e:?}"))?;
                println!("{} frames (syntactic integrity only)", records.len());
            }
            _ => {
                return Err(
                    "usage: framing create|create-exit-before-reply PATH PAYLOAD... | read PATH"
                        .into(),
                );
            }
        }
        Ok(())
    })();
    if let Err(error) = result {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
