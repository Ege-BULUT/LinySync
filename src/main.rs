mod bus;
mod catalog;
mod cli;
mod look;
mod me;
mod os;
mod seal;
mod session;
mod ui;
mod wire;

const HELP: &str = "LinySync: move your setup from one Linux machine to another

  linysync                               open the window
  linysync --scan                        what this device could send
  linysync --give <id> [--only a,b]      ask device <id> to receive, then send
  linysync --accept [--only a,b]         approve the request waiting here, then do this side
  linysync --id                          this device's id, name and look
  linysync --snap out.png [--scene s]    render the window on made-up devices, headless (--list-scenes)";

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let only: Vec<String> = args.iter().position(|a| a == "--only").and_then(|i| args.get(i + 1))
        .map(|s| s.split(',').map(|x| x.trim().to_string()).filter(|x| !x.is_empty()).collect()).unwrap_or_default();
    let first = args.first().map(String::as_str).unwrap_or("");
    let r = match first {
        "" => {
            ui::run(false);
            Ok(())
        }
        a if ui::is_tooling_arg(a) => {
            ui::run(true);
            Ok(())
        }
        "--scan" => {
            let o = session::offer(&os::Env::here());
            println!("{} ({})", o.os, o.home);
            for i in &o.items {
                println!("  {:<40} {}{}", i.id, i.name, if i.secret { " [secret]" } else { "" });
            }
            Ok(())
        }
        "--give" => match args.get(1) {
            Some(peer) => cli::give(peer.trim_start_matches('#'), only),
            None => Err("--give needs a device id".into()),
        },
        "--accept" => cli::accept(only),
        "--id" => {
            let c = me::Config::load();
            println!("{} #{} {:?}", c.name, c.id, c.look);
            Ok(())
        }
        "--help" | "-h" => {
            println!("{HELP}");
            Ok(())
        }
        _ => Err(format!("unknown option {first}\n\n{HELP}")),
    };
    if let Err(e) = r {
        eprintln!("linysync: {e}");
        std::process::exit(1);
    }
}
