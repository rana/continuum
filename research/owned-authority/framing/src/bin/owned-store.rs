//! Trusted disposable JSON CLI. No provider calls or command execution.
use continuum_journal_framing::{
    Object,
    journal::Journal,
    store::{Request, Store},
};
use serde_json::json;
use std::{env, fs, path::Path};
fn main() {
    let args: Vec<String> = env::args().collect();
    let result = (|| -> Result<serde_json::Value, Box<dyn std::error::Error>> {
        if args.len() < 3 {
            return Err("usage: owned-store COMMAND DIRECTORY [ARG ...]".into());
        }
        let path = Path::new(&args[2]);
        if args[1] == "init" {
            Journal::init(path)?;
            return Ok(json!({"initialized":true}));
        }
        if args[1] == "restore" && (args.len() == 4 || args.len() == 5) {
            Store::restore(
                Path::new(&args[3]),
                path,
                args.get(4).map_or("none", String::as_str),
            )?;
            return Ok(json!({"restored":true}));
        }
        let mut store = Store::open(path)?;
        Ok(match args[1].as_str() {
            "export" if args.len() == 4 || args.len() == 5 => {
                store.export(
                    Path::new(&args[3]),
                    args.get(4).map_or("none", String::as_str),
                )?;
                json!({"exported":true})
            }
            "put" if args.len() == 4 => {
                let object: Object = serde_json::from_slice(&fs::read(&args[3])?)?;
                json!({"id":store.put(object)?})
            }
            "get" if args.len() == 4 => json!(store.get(args[3].parse()?)?),
            "head" if args.len() == 5 => json!(store.head(&args[3], &args[4])?),
            "receipt" if args.len() == 5 => json!(store.receipt(&args[3], &args[4])?),
            "accept" if args.len() == 4 || args.len() == 5 => {
                let request: Request = serde_json::from_slice(&fs::read(&args[3])?)?;
                json!(store.accept(request, args.get(4).map_or("none", String::as_str))?)
            }
            _ => return Err("invalid command/arguments".into()),
        })
    })();
    match result {
        Ok(value) => println!("{value}"),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    }
}
