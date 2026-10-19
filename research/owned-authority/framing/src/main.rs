use continuum_journal_framing::{create, decode};
use std::{env, fs, path::Path};

fn main() {
    let args: Vec<String> = env::args().collect();
    let result: Result<(), String> = (|| {
        match args.get(1).map(String::as_str) {
            Some("journal-init") if args.len() == 3 => {
                continuum_journal_framing::journal::Journal::init(Path::new(&args[2]))
                    .map_err(|e| e.to_string())?;
            }
            Some("journal-read") if args.len() == 3 => {
                let journal =
                    continuum_journal_framing::journal::Journal::open(Path::new(&args[2]))
                        .map_err(|e| e.to_string())?;
                println!(
                    "{} committed frames",
                    journal.records().map_err(|e| e.to_string())?.len()
                );
            }
            Some("journal-append") if args.len() == 5 => {
                let mut journal =
                    continuum_journal_framing::journal::Journal::open(Path::new(&args[2]))
                        .map_err(|e| e.to_string())?;
                let result = journal.append(args[4].as_bytes().to_vec(), &args[3]);
                if args[3] == "sync-error" {
                    if result.is_ok()
                        || journal.records().is_ok()
                        || journal.append(b"retry".to_vec(), "none").is_ok()
                    {
                        return Err("poison guard failed".into());
                    }
                    println!("injected uncertainty: reads and writes refused on same handle");
                } else {
                    result.map_err(|e| e.to_string())?;
                    println!("committed");
                }
            }
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
