use std::fs;
use std::io::{self, BufRead};

fn main() -> io::Result<()> {
    // let file = fs::File::open("04-test.txt")?;
    let file = fs::File::open("04.txt")?;
    let reader = io::BufReader::new(file);
    let result: Result<Vec<_>, _> = reader.lines().collect();
    let mut lines = result.unwrap();
    lines.sort();

    println!("{}", lines.len());

    for line in &lines {
        println!("{}", line);
    }

    Ok(())
}
