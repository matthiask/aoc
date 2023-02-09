use regex::Regex;
use std::env;
use std::fs;
use std::io::{self, BufRead};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Point {
    initial: (i32, i32),
    velocity: (i32, i32),
}

impl Point {
    fn position(&self, time: i32) -> (i32, i32) {
        (
            self.initial.0 + time * self.velocity.0,
            self.initial.1 + time * self.velocity.1,
        )
    }
}

fn parse_point(line: &str) -> Point {
    let numbers_re = Regex::new(r"([-\d]+)").unwrap();
    let tokens: Vec<i32> = numbers_re
        .captures_iter(&line)
        .map(|c| c.get(1).unwrap().as_str().parse::<i32>().unwrap())
        .collect();

    Point {
        initial: (tokens[0], tokens[1]),
        velocity: (tokens[2], tokens[3]),
    }
}

fn process(filename: &str) {
    let file = fs::File::open(filename).unwrap();
    let reader = io::BufReader::new(file);

    let points: Vec<Point> = reader.lines().map(|c| parse_point(&c.unwrap())).collect();

    println!("{points:?}");

    // println!("part 1: {}", metadata.iter().sum::<i32>());
    // println!("part 2: {}", node_value(&mut numbers.iter()));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
