use std::env;
use std::fs;

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Before {
    required: char,
    step: char,
    seconds: u32,
}

fn parse_node(numbers: &mut dyn Iterator<Item = &i32>, metadata: &mut Vec<i32>) {
    let child_nodes = *numbers.next().unwrap();
    let metadata_nodes = *numbers.next().unwrap();

    for _i in 0..child_nodes {
        parse_node(numbers, metadata);
    }

    for _i in 0..metadata_nodes {
        metadata.push(*numbers.next().unwrap());
    }
}

fn node_value(numbers: &mut dyn Iterator<Item = &i32>) -> i32 {
    let child_nodes = *numbers.next().unwrap();
    let metadata_nodes = *numbers.next().unwrap();

    if child_nodes > 0 {
        let values: Vec<i32> = (0..child_nodes).map(|_c| node_value(numbers)).collect();
        let mut v: i32 = 0;
        for _i in 0..metadata_nodes {
            let idx = *numbers.next().unwrap() as usize;
            v += values.get(idx - 1).unwrap_or(&0);
        }
        v
    } else {
        let mut v: i32 = 0;
        for _i in 0..metadata_nodes {
            v += *numbers.next().unwrap();
        }
        v
    }
}

fn process(filename: &str) {
    let content = String::from(fs::read_to_string(filename).unwrap().trim());
    let numbers: Vec<i32> = content
        .split_whitespace()
        .map(|token| token.parse::<i32>().unwrap())
        .collect();

    let mut metadata: Vec<i32> = vec![];
    parse_node(&mut numbers.iter(), &mut metadata);
    println!("part 1: {}", metadata.iter().sum::<i32>());

    println!("part 2: {}", node_value(&mut numbers.iter()));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    process(args.get(1).unwrap_or(&String::from("input.txt")));
}
