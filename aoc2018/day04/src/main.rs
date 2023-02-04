use std::fs;
use std::io::{self, BufRead};

type Guard = Vec<i32>;

fn main() -> io::Result<()> {
    // let file = fs::File::open("04-test.txt")?;
    let file = fs::File::open("04.txt")?;
    let reader = io::BufReader::new(file);
    let result: Result<Vec<_>, _> = reader.lines().collect();
    let mut lines = result.unwrap();
    lines.sort();

    println!("{}", lines.len());

    let mut guards: Vec<Guard> = Vec::new();
    let iter = lines.iter();

    loop {
        let mut guard: Guard = vec![0; 60];
    }


    for line in &lines {
        // println!("{}", line);
        let mut guard: Guard = vec![0; 60];

        let parts: Vec<&str> = line.split(&[' ', '#']).collect();

    }

    Ok(())
}
