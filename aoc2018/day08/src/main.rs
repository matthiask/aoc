use std::env;
use std::fs;

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Before {
    required: char,
    step: char,
    seconds: u32,
}

fn parse_node(numbers: &mut dyn Iterator<Item = i32>, metadata: &mut Vec<i32>) {
    let child_nodes = numbers.next().unwrap();
    let metadata_nodes = numbers.next().unwrap();

    for _i in 0..child_nodes {
        parse_node(numbers, metadata);
    }

    for _i in 0..metadata_nodes {
        metadata.push(numbers.next().unwrap());
    }
}

fn process(filename: &str) {
    let content = String::from(fs::read_to_string(filename).unwrap().trim());
    let mut numbers = content
        .split_whitespace()
        .map(|token| token.parse::<i32>().unwrap());

    let mut metadata: Vec<i32> = vec![];

    parse_node(&mut numbers, &mut metadata);

    println!("part 1: {}", metadata.iter().sum::<i32>());

    // println!("{numbers:?}");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
