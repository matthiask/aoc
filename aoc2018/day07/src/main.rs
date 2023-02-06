use std::env;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Before {
    before: char,
    after: char,
}

fn parse_before(s: &str) -> Before {
    let tokens: Vec<&str> = s.split_whitespace().collect();
    Before {
        before: tokens[1].chars().next().unwrap(),
        after: tokens[7].chars().next().unwrap(),
    }
}

fn process(filename: &str) {
    let file = fs::File::open(filename).unwrap();
    let reader = io::BufReader::new(file);

    let coords: Vec<Before> = reader
        .lines()
        .map(|line| parse_before(&line.unwrap()))
        .collect();

    println!("pairs: {}", coords.len());
    println!("{:?}", &coords);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
